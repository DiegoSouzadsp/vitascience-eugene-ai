"""
Eugene Schwartz RAG System
Implementação do sistema de Retrieval-Augmented Generation
para análise de copywriting baseada na metodologia dos 5 níveis de consciência
"""

import os
import json
import logging
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass
from pathlib import Path
import asyncio
import time

import fitz  # PyMuPDF for PDF processing
import numpy as np
from openai import OpenAI
from sqlalchemy import create_engine, text, Column, Integer, String, Text, Float, Index
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.dialects.postgresql import JSONB
from pgvector.sqlalchemy import Vector
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import uvicorn

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Database configuration
Base = declarative_base()

class EugeneKnowledge(Base):
    """Tabela para armazenar conhecimento do Eugene Schwartz"""
    __tablename__ = 'eugene_knowledge'

    id = Column(Integer, primary_key=True)
    content = Column(Text, nullable=False)
    embedding = Column(Vector(3072))  # text-embedding-3-large dimensions
    category = Column(String(50), index=True)
    chapter = Column(String(100), index=True)
    confidence_score = Column(Float)
    metadata = Column(JSONB)
    created_at = Column(Text)  # ISO timestamp

    # Add vector similarity index for performance
    __table_args__ = (
        Index('ix_eugene_knowledge_embedding_cosine', 'embedding', postgresql_using='ivfflat', postgresql_ops={'embedding': 'vector_cosine_ops'}),
        Index('ix_eugene_knowledge_category_embedding', 'category', 'embedding'),
    )

@dataclass
class DocumentChunk:
    """Representa um chunk de documento processado"""
    content: str
    category: str
    chapter: str
    metadata: Dict[str, Any]
    confidence_score: float = 0.0

@dataclass
class RetrievalResult:
    """Resultado de uma busca no sistema RAG"""
    content: str
    similarity_score: float
    category: str
    chapter: str
    metadata: Dict[str, Any]

class EugeneRAGSystem:
    """
    Sistema RAG especializado para metodologia Eugene Schwartz
    Focado nos 5 níveis de consciência do mercado
    """

    def __init__(self, database_url: str = None, openai_api_key: str = None):
        self.database_url = database_url or os.getenv('DATABASE_URL')
        self.openai_api_key = openai_api_key or os.getenv('OPENAI_API_KEY')

        # Configure OpenAI client
        self.openai_client = OpenAI(api_key=self.openai_api_key) if self.openai_api_key else None

        # Database setup
        self.engine = None
        self.Session = None

        # RAG configuration
        self.chunk_size = int(os.getenv('RAG_CHUNK_SIZE', 1000))
        self.chunk_overlap = int(os.getenv('RAG_CHUNK_OVERLAP', 200))
        self.embedding_model = os.getenv('EMBEDDING_MODEL', 'text-embedding-3-large')

        # Eugene Schwartz specific categories
        self.categories = {
            'consciousness_theory': 'Teoria dos 5 níveis de consciência',
            'frameworks': 'Estruturas de copywriting (PAS, AIDA, etc.)',
            'techniques': 'Técnicas específicas de Eugene',
            'examples': 'Casos práticos e exemplos',
            'evaluation': 'Critérios de análise'
        }

        logger.info("Eugene RAG System initialized")

    async def setup_database(self) -> bool:
        """Configura o banco de dados PostgreSQL com pgvector"""
        try:
            self.engine = create_engine(self.database_url)
            self.Session = sessionmaker(bind=self.engine)

            # Enable pgvector extension
            with self.engine.connect() as conn:
                conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
                conn.commit()

            # Create tables
            Base.metadata.create_all(self.engine)

            logger.info("Database setup completed successfully")
            return True

        except Exception as e:
            logger.error(f"Database setup failed: {e}")
            return False

    def extract_text_from_pdf(self, pdf_path: str) -> Dict[str, str]:
        """
        Extrai texto do PDF preservando estrutura de capítulos
        """
        try:
            doc = fitz.open(pdf_path)
            chapters = {}
            current_chapter = "Introduction"

            for page_num in range(len(doc)):
                page = doc[page_num]
                text = page.get_text()

                # Identify chapter markers (simple heuristic)
                lines = text.split('\n')
                for line in lines:
                    line = line.strip()
                    if (line.isupper() and len(line) > 10 and len(line) < 100) or \
                       ('Chapter' in line and len(line) < 100):
                        current_chapter = line
                        chapters[current_chapter] = ""
                        break

                # Add text to current chapter
                if current_chapter not in chapters:
                    chapters[current_chapter] = ""
                chapters[current_chapter] += text + "\n"

            doc.close()
            logger.info(f"Extracted text from {len(chapters)} chapters")
            return chapters

        except Exception as e:
            logger.error(f"PDF extraction failed: {e}")
            return {}

    def categorize_content(self, text: str, chapter: str) -> str:
        """
        Categoriza o conteúdo baseado em palavras-chave da metodologia Eugene
        """
        text_lower = text.lower()
        chapter_lower = chapter.lower()

        # Consciousness theory keywords
        consciousness_keywords = [
            'conscious', 'awareness', 'sophisticated', 'level', 'stage',
            'unconscious', 'problem aware', 'solution aware'
        ]

        # Framework keywords
        framework_keywords = [
            'pas', 'aida', 'formula', 'structure', 'framework',
            'attention', 'interest', 'desire', 'action'
        ]

        # Technique keywords
        technique_keywords = [
            'technique', 'method', 'approach', 'strategy',
            'headline', 'hook', 'story', 'proof'
        ]

        # Example keywords
        example_keywords = [
            'example', 'case', 'study', 'campaign', 'ad',
            'copy', 'sales letter', 'advertisement'
        ]

        # Count keyword occurrences
        consciousness_score = sum(1 for kw in consciousness_keywords if kw in text_lower)
        framework_score = sum(1 for kw in framework_keywords if kw in text_lower)
        technique_score = sum(1 for kw in technique_keywords if kw in text_lower)
        example_score = sum(1 for kw in example_keywords if kw in text_lower)

        # Determine category based on highest score
        scores = {
            'consciousness_theory': consciousness_score,
            'frameworks': framework_score,
            'techniques': technique_score,
            'examples': example_score
        }

        max_category = max(scores, key=scores.get)

        # Default to evaluation if no clear category
        if scores[max_category] == 0:
            return 'evaluation'

        return max_category

    def semantic_chunking(self, text: str, chapter: str) -> List[DocumentChunk]:
        """
        Implementa chunking semântico preservando integridade conceitual
        """
        # Split by paragraphs first
        paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]

        chunks = []
        current_chunk = ""

        for paragraph in paragraphs:
            # Check if adding this paragraph would exceed chunk size
            if len(current_chunk) + len(paragraph) + 1 > self.chunk_size:
                if current_chunk:
                    # Create chunk from current content
                    category = self.categorize_content(current_chunk, chapter)
                    chunk = DocumentChunk(
                        content=current_chunk.strip(),
                        category=category,
                        chapter=chapter,
                        metadata={
                            'length': len(current_chunk),
                            'paragraph_count': current_chunk.count('\n\n') + 1,
                            'processing_timestamp': time.time()
                        }
                    )
                    chunks.append(chunk)

                    # Start new chunk with overlap
                    if len(current_chunk) > self.chunk_overlap:
                        current_chunk = current_chunk[-self.chunk_overlap:] + "\n\n" + paragraph
                    else:
                        current_chunk = paragraph
                else:
                    current_chunk = paragraph
            else:
                if current_chunk:
                    current_chunk += "\n\n" + paragraph
                else:
                    current_chunk = paragraph

        # Add final chunk if exists
        if current_chunk:
            category = self.categorize_content(current_chunk, chapter)
            chunk = DocumentChunk(
                content=current_chunk.strip(),
                category=category,
                chapter=chapter,
                metadata={
                    'length': len(current_chunk),
                    'paragraph_count': current_chunk.count('\n\n') + 1,
                    'processing_timestamp': time.time()
                }
            )
            chunks.append(chunk)

        logger.info(f"Created {len(chunks)} semantic chunks for chapter: {chapter}")
        return chunks

    def generate_embedding(self, text: str) -> Optional[List[float]]:
        """
        Gera embedding usando OpenAI text-embedding-3-large
        """
        try:
            if not self.openai_client:
                logger.error("OpenAI client not configured")
                return None

            response = self.openai_client.embeddings.create(
                model=self.embedding_model,
                input=text
            )
            return response.data[0].embedding

        except Exception as e:
            logger.error(f"Embedding generation failed: {e}")
            return None

    def store_chunks(self, chunks: List[DocumentChunk]) -> bool:
        """
        Armazena chunks no banco de dados com embeddings
        """
        try:
            session = self.Session()
            import datetime
            timestamp = datetime.datetime.now().isoformat()

            for chunk in chunks:
                # Generate embedding
                embedding = self.generate_embedding(chunk.content)
                if not embedding:
                    continue

                # Create database record
                knowledge = EugeneKnowledge(
                    content=chunk.content,
                    embedding=embedding,
                    category=chunk.category,
                    chapter=chunk.chapter,
                    confidence_score=chunk.confidence_score,
                    metadata=chunk.metadata,
                    created_at=timestamp
                )

                session.add(knowledge)

            session.commit()
            session.close()

            logger.info(f"Stored {len(chunks)} chunks in database")
            return True

        except Exception as e:
            logger.error(f"Failed to store chunks: {e}")
            return False

    async def process_eugene_book(self, pdf_path: str) -> bool:
        """
        Processo completo: extração → chunking → embedding → armazenamento
        """
        logger.info("Starting Eugene Schwartz book processing...")

        # Extract text from PDF
        chapters = self.extract_text_from_pdf(pdf_path)
        if not chapters:
            logger.error("Failed to extract text from PDF")
            return False

        # Process each chapter
        all_chunks = []
        for chapter_title, chapter_text in chapters.items():
            if len(chapter_text.strip()) < 100:  # Skip very short chapters
                continue

            chunks = self.semantic_chunking(chapter_text, chapter_title)
            all_chunks.extend(chunks)

        logger.info(f"Total chunks created: {len(all_chunks)}")

        # Store chunks with embeddings
        success = await self.store_chunks(all_chunks)

        if success:
            logger.info("Eugene Schwartz book processing completed successfully")
        else:
            logger.error("Failed to complete book processing")

        return success

    async def get_consciousness_level_context(self, query: str, level: Optional[int] = None) -> List[RetrievalResult]:
        """
        Busca contexto específico para níveis de consciência
        """
        try:
            # Generate query embedding
            query_embedding = await self.generate_embedding(query)
            if not query_embedding:
                return []

            session = self.Session()

            # Build query with filters
            sql_query = text("""
                SELECT content, chapter, category, metadata,
                       embedding <-> :query_embedding as similarity_score
                FROM eugene_knowledge
                WHERE category = 'consciousness_theory'
                ORDER BY embedding <-> :query_embedding
                LIMIT 5
            """)

            result = session.execute(sql_query, {
                'query_embedding': str(query_embedding)
            })

            results = []
            for row in result:
                results.append(RetrievalResult(
                    content=row.content,
                    similarity_score=float(row.similarity_score),
                    category=row.category,
                    chapter=row.chapter,
                    metadata=row.metadata or {}
                ))

            session.close()
            return results

        except Exception as e:
            logger.error(f"Consciousness context retrieval failed: {e}")
            return []

    async def get_framework_guidance(self, copy_type: str) -> List[RetrievalResult]:
        """
        Busca guidance sobre frameworks de copywriting
        """
        try:
            query_embedding = await self.generate_embedding(f"copywriting framework {copy_type}")
            if not query_embedding:
                return []

            session = self.Session()

            sql_query = text("""
                SELECT content, chapter, category, metadata,
                       embedding <-> :query_embedding as similarity_score
                FROM eugene_knowledge
                WHERE category = 'frameworks'
                ORDER BY embedding <-> :query_embedding
                LIMIT 3
            """)

            result = session.execute(sql_query, {
                'query_embedding': str(query_embedding)
            })

            results = []
            for row in result:
                results.append(RetrievalResult(
                    content=row.content,
                    similarity_score=float(row.similarity_score),
                    category=row.category,
                    chapter=row.chapter,
                    metadata=row.metadata or {}
                ))

            session.close()
            return results

        except Exception as e:
            logger.error(f"Framework guidance retrieval failed: {e}")
            return []

    async def get_improvement_techniques(self, problem_area: str) -> List[RetrievalResult]:
        """
        Busca técnicas específicas para problemas identificados
        """
        try:
            query_embedding = await self.generate_embedding(f"copywriting technique improve {problem_area}")
            if not query_embedding:
                return []

            session = self.Session()

            sql_query = text("""
                SELECT content, chapter, category, metadata,
                       embedding <-> :query_embedding as similarity_score
                FROM eugene_knowledge
                WHERE category IN ('techniques', 'examples')
                ORDER BY embedding <-> :query_embedding
                LIMIT 4
            """)

            result = session.execute(sql_query, {
                'query_embedding': str(query_embedding)
            })

            results = []
            for row in result:
                results.append(RetrievalResult(
                    content=row.content,
                    similarity_score=float(row.similarity_score),
                    category=row.category,
                    chapter=row.chapter,
                    metadata=row.metadata or {}
                ))

            session.close()
            return results

        except Exception as e:
            logger.error(f"Improvement techniques retrieval failed: {e}")
            return []

    async def health_check(self) -> Dict[str, Any]:
        """
        Verifica saúde do sistema RAG
        """
        try:
            session = self.Session()

            # Count total chunks
            total_chunks = session.execute(text("SELECT COUNT(*) FROM eugene_knowledge")).scalar()

            # Count by category
            category_counts = {}
            for category in self.categories.keys():
                count = session.execute(text(f"""
                    SELECT COUNT(*) FROM eugene_knowledge
                    WHERE category = '{category}'
                """)).scalar()
                category_counts[category] = count

            session.close()

            return {
                'status': 'healthy',
                'total_chunks': total_chunks,
                'category_distribution': category_counts,
                'database_connection': True,
                'embedding_model': self.embedding_model,
                'chunk_size': self.chunk_size,
                'chunk_overlap': self.chunk_overlap
            }

        except Exception as e:
            logger.error(f"Health check failed: {e}")
            return {
                'status': 'unhealthy',
                'error': str(e)
            }

# Utility functions for testing and validation

async def test_rag_system():
    """
    Testa o sistema RAG com queries de exemplo
    """
    rag = EugeneRAGSystem()

    # Setup database
    await rag.setup_database()

    # Test queries
    test_queries = [
        "What are the 5 levels of market consciousness?",
        "How to write headlines for problem-aware audience?",
        "PAS formula application in copywriting",
        "Examples of successful sales letters"
    ]

    results = {}
    for query in test_queries:
        start_time = time.time()
        consciousness_context = await rag.get_consciousness_level_context(query)
        response_time = time.time() - start_time

        results[query] = {
            'response_time_ms': response_time * 1000,
            'results_count': len(consciousness_context),
            'avg_similarity': np.mean([r.similarity_score for r in consciousness_context]) if consciousness_context else 0
        }

    return results

if __name__ == "__main__":
    # Initialize and test RAG system
    async def main():
        rag = EugeneRAGSystem()

        # Setup
        setup_success = await rag.setup_database()
        if not setup_success:
            print("Database setup failed")
            return

        # Process book
        pdf_path = "docs/Breakthrough_Advertising_-_Eugene_Schwartz.pdf"
        if os.path.exists(pdf_path):
            processing_success = await rag.process_eugene_book(pdf_path)
            if processing_success:
                print("Book processing completed")
            else:
                print("Book processing failed")
        else:
            print(f"PDF not found at: {pdf_path}")

        # Health check
        health = await rag.health_check()
        print(f"System health: {health}")

        # Run tests
        test_results = await test_rag_system()
        print(f"Test results: {test_results}")

    asyncio.run(main())
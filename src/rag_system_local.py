"""
Eugene Schwartz RAG System - Local Version
Versão econômica usando embeddings locais para preservar API credits
"""

import os
import json
import logging
import time
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass
from pathlib import Path
import asyncio

import fitz  # PyMuPDF for PDF processing
import numpy as np
from sentence_transformers import SentenceTransformer
from sqlalchemy import create_engine, text, Column, Integer, String, Text, Float, Index
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.dialects.postgresql import JSONB
from pgvector.sqlalchemy import Vector

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
    embedding = Column(Vector(384))  # all-MiniLM-L6-v2 dimensions
    category = Column(String(50), index=True)
    chapter = Column(String(100), index=True)
    confidence_score = Column(Float)
    chunk_metadata = Column(JSONB)
    created_at = Column(Text)

    # Vector similarity index for performance
    __table_args__ = (
        Index('ix_eugene_knowledge_embedding_cosine', 'embedding',
              postgresql_using='ivfflat',
              postgresql_ops={'embedding': 'vector_cosine_ops'}),
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

class EugeneRAGSystemLocal:
    """
    Sistema RAG local e econômico para metodologia Eugene Schwartz
    Usa sentence-transformers locais para evitar custos de API
    """

    def __init__(self, database_url: str = None):
        self.database_url = database_url or os.getenv('DATABASE_URL')

        # Use local sentence transformer model
        self.model_name = 'all-MiniLM-L6-v2'  # 384 dimensions, fast and efficient
        self.embedding_model = None

        # Database setup
        self.engine = None
        self.Session = None

        # RAG configuration
        self.chunk_size = int(os.getenv('RAG_CHUNK_SIZE', 800))  # Smaller for better local processing
        self.chunk_overlap = int(os.getenv('RAG_CHUNK_OVERLAP', 150))

        # Eugene Schwartz specific categories
        self.categories = {
            'consciousness_theory': 'Teoria dos 5 níveis de consciência',
            'frameworks': 'Estruturas de copywriting (PAS, AIDA, etc.)',
            'techniques': 'Técnicas específicas de Eugene',
            'examples': 'Casos práticos e exemplos',
            'evaluation': 'Critérios de análise',
            'market_awareness': 'Awareness e sophisticated market',
            'headlines': 'Headlines e ganchos',
            'copy_structure': 'Estrutura de copy'
        }

        logger.info("Eugene RAG System (Local) initialized")

    def load_embedding_model(self):
        """Carrega modelo de embedding local"""
        if self.embedding_model is None:
            try:
                logger.info(f"Loading local embedding model: {self.model_name}")
                self.embedding_model = SentenceTransformer(self.model_name)
                logger.info("✅ Local embedding model loaded successfully")
            except Exception as e:
                logger.error(f"Failed to load embedding model: {e}")
                raise

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
        """Extrai texto do PDF preservando estrutura de capítulos"""
        try:
            doc = fitz.open(pdf_path)
            chapters = {}
            current_chapter = "Introduction"

            logger.info(f"Processing PDF with {len(doc)} pages...")

            for page_num in range(len(doc)):
                page = doc[page_num]
                text = page.get_text()

                # Identify chapter markers - Eugene Schwartz book structure
                lines = text.split('\n')
                for line in lines:
                    line = line.strip()

                    # Look for chapter patterns
                    if (line.isupper() and len(line) > 10 and len(line) < 100) or \
                       ('Chapter' in line and len(line) < 100) or \
                       (line.startswith('CHAPTER') and len(line) < 100) or \
                       ('THE' in line and line.isupper() and len(line) < 80):
                        current_chapter = line
                        chapters[current_chapter] = ""
                        logger.info(f"Found chapter: {current_chapter}")
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

    def categorize_content_advanced(self, text: str, chapter: str) -> str:
        """Categorização avançada baseada na metodologia Eugene"""
        text_lower = text.lower()
        chapter_lower = chapter.lower()

        # Consciousness theory keywords (mais específicos)
        consciousness_keywords = [
            'conscious', 'awareness', 'sophisticated', 'level', 'stage',
            'unconscious', 'problem aware', 'solution aware', 'most aware',
            'unaware', 'market sophistication', 'five levels'
        ]

        # Framework keywords (mais específicos para Eugene)
        framework_keywords = [
            'pas', 'aida', 'formula', 'structure', 'framework',
            'attention', 'interest', 'desire', 'action', 'problem agitation solution'
        ]

        # Technique keywords (específicos Eugene)
        technique_keywords = [
            'technique', 'method', 'approach', 'strategy',
            'headline', 'hook', 'story', 'proof', 'copy technique',
            'writing method', 'advertising principle'
        ]

        # Example keywords
        example_keywords = [
            'example', 'case', 'study', 'campaign', 'ad',
            'copy', 'sales letter', 'advertisement', 'successful ad'
        ]

        # Market awareness specific
        market_keywords = [
            'market', 'audience', 'prospect', 'customer',
            'sophisticated market', 'mass market', 'aware market'
        ]

        # Headlines specific
        headline_keywords = [
            'headline', 'head', 'title', 'opening', 'hook',
            'attention getter', 'grabber'
        ]

        # Copy structure
        structure_keywords = [
            'copy structure', 'layout', 'format', 'organization',
            'sequence', 'flow', 'progression'
        ]

        # Count keyword occurrences with weights
        scores = {
            'consciousness_theory': sum(2 if kw in text_lower else 0 for kw in consciousness_keywords),
            'frameworks': sum(2 if kw in text_lower else 0 for kw in framework_keywords),
            'techniques': sum(2 if kw in text_lower else 0 for kw in technique_keywords),
            'examples': sum(1 if kw in text_lower else 0 for kw in example_keywords),
            'market_awareness': sum(2 if kw in text_lower else 0 for kw in market_keywords),
            'headlines': sum(3 if kw in text_lower else 0 for kw in headline_keywords),
            'copy_structure': sum(2 if kw in text_lower else 0 for kw in structure_keywords)
        }

        # Chapter-based scoring
        if 'consciousness' in chapter_lower or 'level' in chapter_lower:
            scores['consciousness_theory'] += 5
        if 'headline' in chapter_lower or 'head' in chapter_lower:
            scores['headlines'] += 5
        if 'market' in chapter_lower or 'aware' in chapter_lower:
            scores['market_awareness'] += 5
        if 'technique' in chapter_lower or 'method' in chapter_lower:
            scores['techniques'] += 3

        # Determine category based on highest score
        max_category = max(scores, key=scores.get)

        # Default to evaluation if no clear category
        if scores[max_category] == 0:
            return 'evaluation'

        return max_category

    def semantic_chunking_enhanced(self, text: str, chapter: str) -> List[DocumentChunk]:
        """Chunking semântico aprimorado para metodologia Eugene"""
        # Split by paragraphs and sentences
        paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]

        chunks = []
        current_chunk = ""

        for paragraph in paragraphs:
            # Skip very short paragraphs
            if len(paragraph) < 50:
                continue

            # Check if adding this paragraph would exceed chunk size
            if len(current_chunk) + len(paragraph) + 1 > self.chunk_size:
                if current_chunk:
                    # Create chunk from current content
                    category = self.categorize_content_advanced(current_chunk, chapter)

                    # Calculate confidence based on content quality
                    confidence = self.calculate_chunk_confidence(current_chunk, category)

                    chunk = DocumentChunk(
                        content=current_chunk.strip(),
                        category=category,
                        chapter=chapter,
                        confidence_score=confidence,
                        metadata={
                            'length': len(current_chunk),
                            'paragraph_count': current_chunk.count('\n\n') + 1,
                            'processing_timestamp': time.time(),
                            'has_examples': 'example' in current_chunk.lower(),
                            'has_formulas': any(f in current_chunk.lower() for f in ['pas', 'aida', 'formula']),
                            'methodology_score': confidence
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
        if current_chunk and len(current_chunk) > 100:
            category = self.categorize_content_advanced(current_chunk, chapter)
            confidence = self.calculate_chunk_confidence(current_chunk, category)

            chunk = DocumentChunk(
                content=current_chunk.strip(),
                category=category,
                chapter=chapter,
                confidence_score=confidence,
                metadata={
                    'length': len(current_chunk),
                    'paragraph_count': current_chunk.count('\n\n') + 1,
                    'processing_timestamp': time.time(),
                    'has_examples': 'example' in current_chunk.lower(),
                    'has_formulas': any(f in current_chunk.lower() for f in ['pas', 'aida', 'formula']),
                    'methodology_score': confidence
                }
            )
            chunks.append(chunk)

        logger.info(f"Created {len(chunks)} semantic chunks for chapter: {chapter}")
        return chunks

    def calculate_chunk_confidence(self, text: str, category: str) -> float:
        """Calcula score de confiança do chunk baseado na qualidade do conteúdo"""
        text_lower = text.lower()

        # Base score
        confidence = 0.5

        # Length bonus
        if 200 < len(text) < 1000:
            confidence += 0.1

        # Eugene-specific content indicators
        eugene_indicators = [
            'eugene schwartz', 'breakthrough advertising', 'market sophistication',
            'consciousness level', 'problem aware', 'solution aware', 'most aware'
        ]

        for indicator in eugene_indicators:
            if indicator in text_lower:
                confidence += 0.1

        # Technical content bonus
        if category in ['consciousness_theory', 'frameworks', 'techniques']:
            if any(term in text_lower for term in ['method', 'technique', 'formula', 'principle']):
                confidence += 0.1

        # Example content bonus
        if 'example' in text_lower and len(text) > 300:
            confidence += 0.1

        return min(confidence, 1.0)

    def generate_embedding_local(self, text: str) -> Optional[List[float]]:
        """Gera embedding usando modelo local sentence-transformers"""
        try:
            if self.embedding_model is None:
                self.load_embedding_model()

            # Clean text for better embeddings
            cleaned_text = text.strip()[:512]  # Limit length for efficiency

            embedding = self.embedding_model.encode(cleaned_text, convert_to_tensor=False)
            return embedding.tolist()

        except Exception as e:
            logger.error(f"Local embedding generation failed: {e}")
            return None

    def store_chunks(self, chunks: List[DocumentChunk]) -> bool:
        """Armazena chunks no banco de dados com embeddings locais"""
        try:
            session = self.Session()
            import datetime
            timestamp = datetime.datetime.now().isoformat()

            stored_count = 0
            for chunk in chunks:
                # Generate embedding locally
                embedding = self.generate_embedding_local(chunk.content)
                if not embedding:
                    logger.warning(f"Failed to generate embedding for chunk: {chunk.content[:50]}...")
                    continue

                # Create database record
                knowledge = EugeneKnowledge(
                    content=chunk.content,
                    embedding=embedding,
                    category=chunk.category,
                    chapter=chunk.chapter,
                    confidence_score=chunk.confidence_score,
                    chunk_metadata=chunk.metadata,
                    created_at=timestamp
                )

                session.add(knowledge)
                stored_count += 1

            session.commit()
            session.close()

            logger.info(f"Stored {stored_count}/{len(chunks)} chunks in database")
            return True

        except Exception as e:
            logger.error(f"Failed to store chunks: {e}")
            return False

    async def process_eugene_book(self, pdf_path: str) -> bool:
        """Processo completo: extração → chunking → embedding → armazenamento"""
        logger.info("Starting Eugene Schwartz book processing (LOCAL MODE)...")

        # Load embedding model first
        self.load_embedding_model()

        # Extract text from PDF
        chapters = self.extract_text_from_pdf(pdf_path)
        if not chapters:
            logger.error("Failed to extract text from PDF")
            return False

        # Process each chapter
        all_chunks = []
        for chapter_title, chapter_text in chapters.items():
            if len(chapter_text.strip()) < 200:  # Skip very short chapters
                continue

            logger.info(f"Processing chapter: {chapter_title}")
            chunks = self.semantic_chunking_enhanced(chapter_text, chapter_title)
            all_chunks.extend(chunks)

        logger.info(f"Total chunks created: {len(all_chunks)}")

        # Show category distribution
        category_counts = {}
        for chunk in all_chunks:
            category_counts[chunk.category] = category_counts.get(chunk.category, 0) + 1

        logger.info("Category distribution:")
        for category, count in category_counts.items():
            logger.info(f"  {category}: {count} chunks")

        # Store chunks with embeddings
        success = self.store_chunks(all_chunks)

        if success:
            logger.info("✅ Eugene Schwartz book processing completed successfully")
        else:
            logger.error("❌ Failed to complete book processing")

        return success

    async def search_similar(self, query: str, category: Optional[str] = None, limit: int = 5) -> List[RetrievalResult]:
        """Busca por similaridade usando embeddings locais"""
        try:
            # Generate query embedding
            query_embedding = self.generate_embedding_local(query)
            if not query_embedding:
                return []

            session = self.Session()

            # Build query with optional category filter
            if category:
                sql_query = text("""
                    SELECT content, chapter, category, metadata, confidence_score,
                           embedding <-> :query_embedding as similarity_score
                    FROM eugene_knowledge
                    WHERE category = :category
                    ORDER BY embedding <-> :query_embedding
                    LIMIT :limit
                """)
                params = {
                    'query_embedding': str(query_embedding),
                    'category': category,
                    'limit': limit
                }
            else:
                sql_query = text("""
                    SELECT content, chapter, category, metadata, confidence_score,
                           embedding <-> :query_embedding as similarity_score
                    FROM eugene_knowledge
                    ORDER BY embedding <-> :query_embedding
                    LIMIT :limit
                """)
                params = {
                    'query_embedding': str(query_embedding),
                    'limit': limit
                }

            result = session.execute(sql_query, params)

            results = []
            for row in result:
                results.append(RetrievalResult(
                    content=row.content,
                    similarity_score=float(row.similarity_score),
                    category=row.category,
                    chapter=row.chapter,
                    metadata=row.chunk_metadata or {}
                ))

            session.close()
            return results

        except Exception as e:
            logger.error(f"Similarity search failed: {e}")
            return []

    async def get_consciousness_level_context(self, query: str, level: Optional[int] = None) -> List[RetrievalResult]:
        """Busca contexto específico para níveis de consciência"""
        consciousness_query = f"consciousness levels market awareness {query}"
        return await self.search_similar(consciousness_query, "consciousness_theory", 5)

    async def get_framework_guidance(self, copy_type: str) -> List[RetrievalResult]:
        """Busca guidance sobre frameworks de copywriting"""
        framework_query = f"copywriting framework {copy_type} PAS AIDA structure"
        return await self.search_similar(framework_query, "frameworks", 3)

    async def get_improvement_techniques(self, problem_area: str) -> List[RetrievalResult]:
        """Busca técnicas específicas para problemas identificados"""
        technique_query = f"copywriting technique improve {problem_area} method"
        results = await self.search_similar(technique_query, "techniques", 2)
        examples = await self.search_similar(technique_query, "examples", 2)
        return results + examples

    async def health_check(self) -> Dict[str, Any]:
        """Verifica saúde do sistema RAG"""
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
                'embedding_model': self.model_name,
                'chunk_size': self.chunk_size,
                'chunk_overlap': self.chunk_overlap,
                'mode': 'local_embeddings'
            }

        except Exception as e:
            logger.error(f"Health check failed: {e}")
            return {
                'status': 'unhealthy',
                'error': str(e)
            }

# Main execution
if __name__ == "__main__":
    async def main():
        rag = EugeneRAGSystemLocal()

        # Setup
        setup_success = await rag.setup_database()
        if not setup_success:
            print("❌ Database setup failed")
            return

        # Process book
        pdf_path = "docs/Breakthrough_Advertising_-_Eugene_Schwartz.pdf"
        if os.path.exists(pdf_path):
            processing_success = await rag.process_eugene_book(pdf_path)
            if processing_success:
                print("✅ Book processing completed")

                # Test retrieval
                print("\n🔍 Testing retrieval...")
                results = await rag.get_consciousness_level_context("5 levels of market consciousness")
                print(f"Found {len(results)} results")
                if results:
                    print(f"Sample: {results[0].content[:100]}...")

            else:
                print("❌ Book processing failed")
        else:
            print(f"❌ PDF not found at: {pdf_path}")

        # Health check
        health = await rag.health_check()
        print(f"\n📊 System health: {health}")

    asyncio.run(main())
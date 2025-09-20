"""
Eugene Schwartz RAG System - Hybrid Version
Usa OpenAI o1-mini apenas para vetorização inicial (econômico)
Embeddings locais para consultas diárias (sem custo adicional)
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
from openai import OpenAI
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

class EugeneKnowledgeLocal(Base):
    """Tabela para embeddings locais (sentence-transformers)"""
    __tablename__ = 'eugene_knowledge_local'

    id = Column(Integer, primary_key=True)
    content = Column(Text, nullable=False)
    embedding = Column(Vector(384))  # all-MiniLM-L6-v2 dimensions
    category = Column(String(50), index=True)
    chapter = Column(String(100), index=True)
    confidence_score = Column(Float)
    chunk_metadata = Column(JSONB)
    created_at = Column(Text)
    embedding_model = Column(String(50), default='all-MiniLM-L6-v2')

    # Vector similarity index for local embeddings
    __table_args__ = (
        Index('ix_eugene_local_embedding_cosine', 'embedding',
              postgresql_using='ivfflat',
              postgresql_ops={'embedding': 'vector_cosine_ops'}),
        Index('ix_eugene_local_category_embedding', 'category', 'embedding'),
    )

class EugeneKnowledgeOpenAI(Base):
    """Tabela para embeddings OpenAI (ada-002) - opcional para qualidade extra"""
    __tablename__ = 'eugene_knowledge_openai'

    id = Column(Integer, primary_key=True)
    content = Column(Text, nullable=False)
    embedding = Column(Vector(1536))  # ada-002 dimensions
    category = Column(String(50), index=True)
    chapter = Column(String(100), index=True)
    confidence_score = Column(Float)
    chunk_metadata = Column(JSONB)
    created_at = Column(Text)
    embedding_model = Column(String(50), default='text-embedding-ada-002')

    # Vector similarity index for OpenAI embeddings
    __table_args__ = (
        Index('ix_eugene_openai_embedding_cosine', 'embedding',
              postgresql_using='ivfflat',
              postgresql_ops={'embedding': 'vector_cosine_ops'}),
        Index('ix_eugene_openai_category_embedding', 'category', 'embedding'),
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

class EugeneRAGSystemHybrid:
    """
    Sistema RAG híbrido e econômico:
    - OpenAI o1-mini apenas para vetorização inicial do livro
    - Sentence transformers locais para consultas diárias
    """

    def __init__(self, database_url: str = None, openai_api_key: str = None):
        self.database_url = database_url or os.getenv('DATABASE_URL')
        self.openai_api_key = openai_api_key or os.getenv('OPENAI_API_KEY')

        # OpenAI client for initial processing only
        self.openai_client = OpenAI(api_key=self.openai_api_key) if self.openai_api_key else None

        # Local model for daily queries (no cost)
        self.local_model_name = 'all-MiniLM-L6-v2'  # 384 dimensions, fast
        self.local_embedding_model = None

        # Database setup
        self.engine = None
        self.Session = None

        # RAG configuration
        self.chunk_size = int(os.getenv('RAG_CHUNK_SIZE', 900))
        self.chunk_overlap = int(os.getenv('RAG_CHUNK_OVERLAP', 150))

        # Processing mode
        self.use_openai_for_initial = True  # Use OpenAI o1-mini for book processing
        self.use_local_for_queries = True   # Use local for daily queries

        # Eugene Schwartz categories
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

        logger.info("Eugene RAG System (Hybrid - Economical) initialized")

    def load_local_model(self):
        """Carrega modelo local para consultas diárias"""
        if self.local_embedding_model is None:
            try:
                logger.info(f"Loading local model for queries: {self.local_model_name}")
                self.local_embedding_model = SentenceTransformer(self.local_model_name)
                logger.info("✅ Local model loaded for daily queries")
            except Exception as e:
                logger.error(f"Failed to load local model: {e}")
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

            logger.info(f"Processing PDF: {pdf_path} ({len(doc)} pages)")

            for page_num in range(len(doc)):
                page = doc[page_num]
                text = page.get_text()

                # Eugene Schwartz book chapter detection
                lines = text.split('\n')
                for line in lines:
                    line = line.strip()

                    # Enhanced chapter detection for Eugene's book
                    if (line.isupper() and 10 < len(line) < 100) or \
                       ('Chapter' in line and len(line) < 100) or \
                       (line.startswith('CHAPTER') and len(line) < 100) or \
                       ('THE' in line and line.isupper() and 20 < len(line) < 80) or \
                       (line.startswith('PART') and len(line) < 50):
                        current_chapter = line
                        chapters[current_chapter] = ""
                        logger.info(f"📖 Found chapter: {current_chapter}")
                        break

                # Add text to current chapter
                if current_chapter not in chapters:
                    chapters[current_chapter] = ""
                chapters[current_chapter] += text + "\n"

            doc.close()

            # Filter out very short chapters
            filtered_chapters = {k: v for k, v in chapters.items() if len(v.strip()) > 500}

            logger.info(f"✅ Extracted {len(filtered_chapters)} substantial chapters")
            return filtered_chapters

        except Exception as e:
            logger.error(f"PDF extraction failed: {e}")
            return {}

    def categorize_content_eugene(self, text: str, chapter: str) -> str:
        """Categorização especializada para metodologia Eugene Schwartz"""
        text_lower = text.lower()
        chapter_lower = chapter.lower()

        # Scoring system for categories
        scores = {}

        # Consciousness theory indicators (Eugene's core concept)
        consciousness_indicators = [
            'conscious', 'awareness', 'sophisticated', 'levels', 'stages',
            'unaware', 'problem aware', 'solution aware', 'most aware',
            'market sophistication', 'five levels', 'consciousness level'
        ]
        scores['consciousness_theory'] = sum(3 if ind in text_lower else 0 for ind in consciousness_indicators)

        # Framework indicators
        framework_indicators = [
            'pas', 'aida', 'formula', 'structure', 'framework',
            'attention interest desire action', 'problem agitation solution',
            'before after bridge'
        ]
        scores['frameworks'] = sum(3 if ind in text_lower else 0 for ind in framework_indicators)

        # Technique indicators
        technique_indicators = [
            'technique', 'method', 'approach', 'strategy', 'principle',
            'copy technique', 'writing method', 'advertising principle',
            'breakthrough', 'secret'
        ]
        scores['techniques'] = sum(2 if ind in text_lower else 0 for ind in technique_indicators)

        # Example indicators
        example_indicators = [
            'example', 'case study', 'campaign', 'ad', 'advertisement',
            'successful', 'failed', 'result', 'outcome'
        ]
        scores['examples'] = sum(2 if ind in text_lower else 0 for ind in example_indicators)

        # Market awareness indicators
        market_indicators = [
            'market', 'audience', 'prospect', 'customer', 'sophisticated market',
            'mass market', 'aware market', 'target'
        ]
        scores['market_awareness'] = sum(2 if ind in text_lower else 0 for ind in market_indicators)

        # Headlines indicators
        headline_indicators = [
            'headline', 'head', 'title', 'opening', 'hook',
            'attention getter', 'grabber', 'first line'
        ]
        scores['headlines'] = sum(4 if ind in text_lower else 0 for ind in headline_indicators)

        # Copy structure indicators
        structure_indicators = [
            'structure', 'layout', 'format', 'organization',
            'sequence', 'flow', 'progression', 'copy structure'
        ]
        scores['copy_structure'] = sum(2 if ind in text_lower else 0 for ind in structure_indicators)

        # Chapter-based bonuses
        chapter_bonuses = {
            'consciousness': ['consciousness_theory', 'market_awareness'],
            'levels': ['consciousness_theory'],
            'headline': ['headlines'],
            'copy': ['copy_structure', 'techniques'],
            'formula': ['frameworks'],
            'technique': ['techniques'],
            'example': ['examples'],
            'market': ['market_awareness']
        }

        for keyword, categories in chapter_bonuses.items():
            if keyword in chapter_lower:
                for cat in categories:
                    if cat in scores:
                        scores[cat] += 5

        # Find best category
        if scores:
            max_category = max(scores, key=scores.get)
            if scores[max_category] > 0:
                return max_category

        return 'evaluation'  # Default category

    def semantic_chunking_eugene(self, text: str, chapter: str) -> List[DocumentChunk]:
        """Chunking semântico otimizado para Eugene Schwartz"""
        # Clean and prepare text
        paragraphs = [p.strip() for p in text.split('\n\n') if p.strip() and len(p.strip()) > 100]

        chunks = []
        current_chunk = ""

        for paragraph in paragraphs:
            # Check chunk size
            if len(current_chunk) + len(paragraph) + 1 > self.chunk_size:
                if current_chunk:
                    # Create chunk
                    category = self.categorize_content_eugene(current_chunk, chapter)
                    confidence = self.calculate_chunk_quality(current_chunk, category)

                    chunk = DocumentChunk(
                        content=current_chunk.strip(),
                        category=category,
                        chapter=chapter,
                        confidence_score=confidence,
                        metadata={
                            'length': len(current_chunk),
                            'word_count': len(current_chunk.split()),
                            'has_examples': 'example' in current_chunk.lower(),
                            'has_techniques': any(t in current_chunk.lower() for t in ['technique', 'method', 'approach']),
                            'has_formulas': any(f in current_chunk.lower() for f in ['pas', 'aida', 'formula']),
                            'eugene_score': confidence,
                            'processing_time': time.time()
                        }
                    )
                    chunks.append(chunk)

                    # Start new chunk with smart overlap
                    sentences = paragraph.split('. ')
                    if len(sentences) > 1:
                        current_chunk = '. '.join(sentences[-2:]) + "\n\n" + paragraph
                    else:
                        current_chunk = paragraph
                else:
                    current_chunk = paragraph
            else:
                current_chunk = current_chunk + "\n\n" + paragraph if current_chunk else paragraph

        # Final chunk
        if current_chunk and len(current_chunk) > 200:
            category = self.categorize_content_eugene(current_chunk, chapter)
            confidence = self.calculate_chunk_quality(current_chunk, category)

            chunk = DocumentChunk(
                content=current_chunk.strip(),
                category=category,
                chapter=chapter,
                confidence_score=confidence,
                metadata={
                    'length': len(current_chunk),
                    'word_count': len(current_chunk.split()),
                    'has_examples': 'example' in current_chunk.lower(),
                    'has_techniques': any(t in current_chunk.lower() for t in ['technique', 'method', 'approach']),
                    'has_formulas': any(f in current_chunk.lower() for f in ['pas', 'aida', 'formula']),
                    'eugene_score': confidence,
                    'processing_time': time.time()
                }
            )
            chunks.append(chunk)

        logger.info(f"Created {len(chunks)} chunks for chapter: {chapter[:50]}...")
        return chunks

    def calculate_chunk_quality(self, text: str, category: str) -> float:
        """Calcula qualidade do chunk para metodologia Eugene"""
        score = 0.3  # Base score

        # Length optimization
        word_count = len(text.split())
        if 100 < word_count < 300:
            score += 0.2
        elif 50 < word_count < 500:
            score += 0.1

        # Eugene-specific content
        eugene_terms = [
            'eugene schwartz', 'breakthrough advertising', 'consciousness',
            'market sophistication', 'awareness level', 'copy technique'
        ]
        for term in eugene_terms:
            if term in text.lower():
                score += 0.1

        # Category-specific bonuses
        category_bonuses = {
            'consciousness_theory': ['consciousness', 'level', 'aware'],
            'frameworks': ['pas', 'aida', 'formula', 'structure'],
            'techniques': ['technique', 'method', 'how to'],
            'headlines': ['headline', 'attention', 'hook'],
            'examples': ['example', 'case', 'result']
        }

        if category in category_bonuses:
            for bonus_term in category_bonuses[category]:
                if bonus_term in text.lower():
                    score += 0.05

        return min(score, 1.0)

    def generate_openai_embedding(self, text: str) -> Optional[List[float]]:
        """Gera embedding usando OpenAI o1-mini (apenas para livro)"""
        try:
            if not self.openai_client:
                logger.warning("OpenAI client not available")
                return None

            # Use text-embedding-ada-002 (mais barato que 3-large)
            response = self.openai_client.embeddings.create(
                model="text-embedding-ada-002",  # Mais econômico
                input=text[:8192]  # Limit text length
            )
            return response.data[0].embedding

        except Exception as e:
            logger.error(f"OpenAI embedding failed: {e}")
            return None

    def generate_local_embedding(self, text: str) -> Optional[List[float]]:
        """Gera embedding local para consultas diárias"""
        try:
            if self.local_embedding_model is None:
                self.load_local_model()

            embedding = self.local_embedding_model.encode(text[:512], convert_to_tensor=False)
            return embedding.tolist()

        except Exception as e:
            logger.error(f"Local embedding failed: {e}")
            return None

    def store_chunks_separated(self, chunks: List[DocumentChunk], use_openai: bool = False) -> bool:
        """Armazena chunks em coleções separadas para manter coerência dos embeddings"""
        try:
            session = self.Session()
            import datetime
            timestamp = datetime.datetime.now().isoformat()

            stored_local = 0
            stored_openai = 0
            total_cost_estimate = 0

            logger.info(f"Storing {len(chunks)} chunks in SEPARATED collections")
            logger.info(f"Primary: Local embeddings | Optional: OpenAI embeddings")

            for i, chunk in enumerate(chunks):
                if i % 10 == 0:
                    logger.info(f"Processing chunk {i+1}/{len(chunks)}")

                # ALWAYS store with local embeddings (primary collection)
                local_embedding = self.generate_local_embedding(chunk.content)
                if local_embedding:
                    knowledge_local = EugeneKnowledgeLocal(
                        content=chunk.content,
                        embedding=local_embedding,
                        category=chunk.category,
                        chapter=chunk.chapter,
                        confidence_score=chunk.confidence_score,
                        chunk_metadata=chunk.metadata,
                        created_at=timestamp,
                        embedding_model=self.local_model_name
                    )
                    session.add(knowledge_local)
                    stored_local += 1

                # OPTIONALLY store with OpenAI embeddings (separate collection)
                if use_openai and self.openai_client:
                    openai_embedding = self.generate_openai_embedding(chunk.content)
                    if openai_embedding:
                        knowledge_openai = EugeneKnowledgeOpenAI(
                            content=chunk.content,
                            embedding=openai_embedding,
                            category=chunk.category,
                            chapter=chunk.chapter,
                            confidence_score=chunk.confidence_score,
                            chunk_metadata=chunk.metadata,
                            created_at=timestamp,
                            embedding_model="text-embedding-ada-002"
                        )
                        session.add(knowledge_openai)
                        stored_openai += 1

                        # Cost estimation
                        tokens = len(chunk.content.split()) * 1.3
                        total_cost_estimate += (tokens / 1000) * 0.0001

            session.commit()
            session.close()

            logger.info(f"✅ Storage complete:")
            logger.info(f"   Local collection: {stored_local} chunks")
            if use_openai:
                logger.info(f"   OpenAI collection: {stored_openai} chunks")
                logger.info(f"   💰 Estimated cost: ${total_cost_estimate:.4f}")
            logger.info(f"   🚀 Future queries: Local collection (FREE)")

            return True

        except Exception as e:
            logger.error(f"Failed to store chunks: {e}")
            return False

    async def process_eugene_book(self, pdf_path: str) -> bool:
        """Processa o livro Eugene Schwartz completo"""
        logger.info("🚀 Starting Eugene Schwartz book processing (HYBRID MODE)")
        logger.info("📝 Using OpenAI ada-002 for initial embeddings + Local for queries")

        # Load local model
        self.load_local_model()

        # Extract chapters
        chapters = self.extract_text_from_pdf(pdf_path)
        if not chapters:
            logger.error("❌ Failed to extract chapters from PDF")
            return False

        # Process all chapters
        all_chunks = []
        for chapter_title, chapter_text in chapters.items():
            if len(chapter_text.strip()) < 300:
                continue

            logger.info(f"📖 Processing: {chapter_title}")
            chunks = self.semantic_chunking_eugene(chapter_text, chapter_title)
            all_chunks.extend(chunks)

        logger.info(f"📊 Total chunks created: {len(all_chunks)}")

        # Show category distribution
        category_counts = {}
        for chunk in all_chunks:
            category_counts[chunk.category] = category_counts.get(chunk.category, 0) + 1

        logger.info("📈 Category distribution:")
        for category, count in sorted(category_counts.items()):
            logger.info(f"   {category}: {count} chunks")

        # Store with separated embeddings (mantém coerência)
        success = self.store_chunks_separated(all_chunks, use_openai=True)

        if success:
            logger.info("✅ Eugene Schwartz book processing completed!")
            logger.info("💡 Future queries will use local embeddings (no additional cost)")
        else:
            logger.error("❌ Book processing failed")

        return success

    async def search_consciousness_context(self, query: str, limit: int = 5) -> List[RetrievalResult]:
        """Busca contexto de consciência usando embeddings locais"""
        query_enhanced = f"consciousness levels market awareness {query}"
        return await self.search_local_similarity(query_enhanced, "consciousness_theory", limit)

    async def search_local_similarity(self, query: str, category: Optional[str] = None, limit: int = 5) -> List[RetrievalResult]:
        """Busca por similaridade usando embeddings locais (coleção consistente)"""
        try:
            # Generate local query embedding
            query_embedding = self.generate_local_embedding(query)
            if not query_embedding:
                return []

            session = self.Session()

            # Query using LOCAL collection only (consistent embeddings)
            if category:
                sql_query = text("""
                    SELECT content, chapter, category, chunk_metadata, confidence_score,
                           embedding <-> :query_embedding as similarity_score
                    FROM eugene_knowledge_local
                    WHERE category = :category
                    ORDER BY embedding <-> :query_embedding
                    LIMIT :limit
                """)
                params = {'query_embedding': str(query_embedding), 'category': category, 'limit': limit}
            else:
                sql_query = text("""
                    SELECT content, chapter, category, chunk_metadata, confidence_score,
                           embedding <-> :query_embedding as similarity_score
                    FROM eugene_knowledge_local
                    ORDER BY embedding <-> :query_embedding
                    LIMIT :limit
                """)
                params = {'query_embedding': str(query_embedding), 'limit': limit}

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
            logger.error(f"Local similarity search failed: {e}")
            return []

    async def search_openai_similarity(self, query: str, category: Optional[str] = None, limit: int = 5) -> List[RetrievalResult]:
        """Busca usando embeddings OpenAI (quando disponível e necessário)"""
        try:
            # Generate OpenAI query embedding
            query_embedding = self.generate_openai_embedding(query)
            if not query_embedding:
                return []

            session = self.Session()

            # Query using OpenAI collection only (consistent embeddings)
            if category:
                sql_query = text("""
                    SELECT content, chapter, category, chunk_metadata, confidence_score,
                           embedding <-> :query_embedding as similarity_score
                    FROM eugene_knowledge_openai
                    WHERE category = :category
                    ORDER BY embedding <-> :query_embedding
                    LIMIT :limit
                """)
                params = {'query_embedding': str(query_embedding), 'category': category, 'limit': limit}
            else:
                sql_query = text("""
                    SELECT content, chapter, category, chunk_metadata, confidence_score,
                           embedding <-> :query_embedding as similarity_score
                    FROM eugene_knowledge_openai
                    ORDER BY embedding <-> :query_embedding
                    LIMIT :limit
                """)
                params = {'query_embedding': str(query_embedding), 'limit': limit}

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
            logger.error(f"OpenAI similarity search failed: {e}")
            return []

    async def get_consciousness_level_context(self, query: str, level: Optional[int] = None) -> List[RetrievalResult]:
        """Interface compatível - busca contexto de consciência"""
        return await self.search_consciousness_context(query)

    async def get_framework_guidance(self, copy_type: str) -> List[RetrievalResult]:
        """Interface compatível - busca frameworks"""
        query = f"copywriting framework {copy_type} PAS AIDA"
        return await self.search_local_similarity(query, "frameworks", 3)

    async def get_improvement_techniques(self, problem_area: str) -> List[RetrievalResult]:
        """Interface compatível - busca técnicas"""
        query = f"technique method improve {problem_area}"
        techniques = await self.search_local_similarity(query, "techniques", 2)
        examples = await self.search_local_similarity(query, "examples", 2)
        return techniques + examples

    async def health_check(self) -> Dict[str, Any]:
        """Verifica saúde do sistema com coleções separadas"""
        try:
            session = self.Session()

            # Count chunks in separated collections
            local_chunks = session.execute(text("SELECT COUNT(*) FROM eugene_knowledge_local")).scalar()
            openai_chunks = session.execute(text("SELECT COUNT(*) FROM eugene_knowledge_openai")).scalar()

            # Category distribution from LOCAL collection (primary)
            category_counts = {}
            for category in self.categories.keys():
                count = session.execute(text(f"""
                    SELECT COUNT(*) FROM eugene_knowledge_local
                    WHERE category = '{category}'
                """)).scalar()
                category_counts[category] = count

            session.close()

            return {
                'status': 'healthy',
                'collections': {
                    'local_chunks': local_chunks,
                    'openai_chunks': openai_chunks,
                    'primary_collection': 'local (free queries)',
                    'secondary_collection': 'openai (optional, higher quality)'
                },
                'category_distribution': category_counts,
                'embedding_consistency': 'SEPARATED collections - no mixing',
                'mode': 'hybrid_separated',
                'local_model': self.local_model_name,
                'query_cost': 'FREE (local collection)',
                'database_connection': True
            }

        except Exception as e:
            logger.error(f"Health check failed: {e}")
            return {'status': 'unhealthy', 'error': str(e)}

# Script para processamento
if __name__ == "__main__":
    async def main():
        print("🔧 EUGENE SCHWARTZ HYBRID RAG SETUP")
        print("Using OpenAI ada-002 for book + Local for queries")
        print("=" * 50)

        rag = EugeneRAGSystemHybrid()

        # Setup database
        if not await rag.setup_database():
            print("❌ Database setup failed")
            return

        # Process book
        pdf_path = Path("docs/Breakthrough_Advertising_-_Eugene_Schwartz.pdf")
        if pdf_path.exists():
            success = await rag.process_eugene_book(str(pdf_path))
            if success:
                # Test the system
                print("\n🧪 Testing retrieval...")
                results = await rag.get_consciousness_level_context("five levels of consciousness")
                print(f"Found {len(results)} results")

                # Health check
                health = await rag.health_check()
                print(f"\n📊 System Health: {health['status']}")
                print(f"📈 Total chunks: {health['total_chunks']}")
                print(f"💰 Future queries: {health['query_cost']}")
            else:
                print("❌ Processing failed")
        else:
            print(f"❌ PDF not found: {pdf_path}")

    asyncio.run(main())
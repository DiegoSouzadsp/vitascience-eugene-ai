"""
Economic RAG Processor for Eugene Schwartz Methodology
Processes the already converted MD file with cost optimization
Uses text-embedding-3-small for $6 budget efficiency
"""

import os
import re
import json
import logging
import asyncio
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass
import time
from datetime import datetime

import numpy as np
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

class EugeneKnowledge(Base):
    """Tabela para armazenar conhecimento do Eugene Schwartz"""
    __tablename__ = 'eugene_knowledge'

    id = Column(Integer, primary_key=True)
    content = Column(Text, nullable=False)
    embedding = Column(Vector(1536))  # text-embedding-3-small dimensions
    category = Column(String(50), index=True)
    chapter = Column(String(100), index=True)
    confidence_score = Column(Float)
    meta_data = Column(JSONB)
    created_at = Column(Text)  # ISO timestamp

    # Add vector similarity index for performance
    __table_args__ = (
        Index('ix_eugene_knowledge_embedding_cosine', 'embedding', postgresql_using='ivfflat',
              postgresql_ops={'embedding': 'vector_cosine_ops'}),
        Index('ix_eugene_knowledge_category_embedding', 'category', 'embedding'),
    )

@dataclass
class DocumentChunk:
    """Representa um chunk de documento processado"""
    content: str
    category: str
    chapter: str
    page_number: Optional[int]
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

class EconomicEugeneRAG:
    """
    Economic RAG processor for Eugene Schwartz methodology
    Optimized for cost efficiency using text-embedding-3-small
    """

    def __init__(self, database_url: str = None, llm_service_url: str = None):
        self.database_url = database_url or os.getenv('DATABASE_URL')

        # Use LLM service for embeddings instead of direct OpenAI calls
        self.llm_service_url = llm_service_url or os.getenv('LLM_SERVICE_URL', 'http://localhost:9000')

        # Database setup
        self.engine = None
        self.Session = None

        # Economic RAG configuration - optimized for cost
        self.chunk_size = 800  # Smaller chunks for better granularity and cost efficiency
        self.chunk_overlap = 100  # Reduced overlap to minimize redundant embeddings
        self.embedding_model = 'text-embedding-3-small'  # Cost-effective model
        self.embedding_dimensions = 1536  # Dimensions for text-embedding-3-small

        # Eugene Schwartz specific categories with enhanced keyword detection
        self.categories = {
            'consciousness_theory': {
                'keywords': [
                    'conscious', 'awareness', 'sophisticated', 'level', 'stage',
                    'unconscious', 'problem aware', 'solution aware', 'most aware',
                    'market sophistication', 'advertising sophistication'
                ],
                'weight': 1.5  # Higher weight for core theory
            },
            'frameworks': {
                'keywords': [
                    'formula', 'structure', 'framework', 'method',
                    'attention', 'interest', 'desire', 'action', 'aida',
                    'problem', 'agitation', 'solution', 'pas'
                ],
                'weight': 1.3
            },
            'techniques': {
                'keywords': [
                    'technique', 'approach', 'strategy', 'tactic',
                    'headline', 'hook', 'story', 'proof', 'benefit',
                    'feature', 'mechanism', 'credibility'
                ],
                'weight': 1.2
            },
            'examples': {
                'keywords': [
                    'example', 'case', 'study', 'campaign', 'ad',
                    'copy', 'sales letter', 'advertisement', 'client',
                    'test', 'result', 'performance'
                ],
                'weight': 1.1
            },
            'evaluation': {
                'keywords': [
                    'evaluate', 'measure', 'test', 'criteria', 'metric',
                    'analyze', 'assessment', 'benchmark', 'standard'
                ],
                'weight': 1.0
            }
        }

        logger.info("Economic Eugene RAG System initialized with cost optimization")

    async def setup_database(self) -> bool:
        """Configura o banco de dados PostgreSQL com pgvector"""
        try:
            self.engine = create_engine(self.database_url)
            self.Session = sessionmaker(bind=self.engine)

            # Enable pgvector extension
            with self.engine.connect() as conn:
                conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
                conn.commit()

            # Drop existing table to update schema for smaller embeddings
            with self.engine.connect() as conn:
                conn.execute(text("DROP TABLE IF EXISTS eugene_knowledge CASCADE"))
                conn.commit()

            # Create tables with updated schema
            Base.metadata.create_all(self.engine)

            logger.info("Database setup completed successfully with economic schema")
            return True

        except Exception as e:
            logger.error(f"Database setup failed: {e}")
            return False

    def extract_text_from_md(self, md_path: str) -> Dict[str, Dict[str, Any]]:
        """
        Extrai texto do MD já convertido, preservando estrutura de páginas e capítulos
        """
        try:
            with open(md_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Split by page markers
            pages = re.split(r'--- PÁGINA (\d+) ---', content)

            chapters = {}
            current_chapter = "Introduction"

            # Process pages (skip first empty element)
            for i in range(1, len(pages), 2):
                if i + 1 < len(pages):
                    page_number = int(pages[i])
                    page_content = pages[i + 1].strip()

                    if not page_content:
                        continue

                    # Detect chapter changes based on content structure
                    lines = page_content.split('\n')
                    for line in lines[:5]:  # Check first few lines for chapter markers
                        line = line.strip()
                        if (line.isupper() and len(line) > 10 and len(line) < 100) or \
                           ('Chapter' in line and len(line) < 100) or \
                           (line.startswith('#') and len(line) < 100):
                            current_chapter = line.strip('#').strip()
                            break

                    # Initialize chapter if not exists
                    if current_chapter not in chapters:
                        chapters[current_chapter] = {
                            'text': '',
                            'pages': [],
                            'start_page': page_number
                        }

                    # Add page content
                    chapters[current_chapter]['text'] += f"\n\n{page_content}"
                    chapters[current_chapter]['pages'].append(page_number)

            logger.info(f"Extracted text from {len(chapters)} chapters across pages")
            return chapters

        except Exception as e:
            logger.error(f"MD extraction failed: {e}")
            return {}

    def advanced_categorize_content(self, text: str, chapter: str) -> Tuple[str, float]:
        """
        Categoriza o conteúdo com scoring ponderado e maior precisão
        """
        text_lower = text.lower()
        chapter_lower = chapter.lower()

        # Calculate weighted scores for each category
        category_scores = {}

        for category, config in self.categories.items():
            # Count keyword occurrences with context sensitivity
            score = 0
            for keyword in config['keywords']:
                # Simple count
                count = text_lower.count(keyword)
                # Bonus for whole word matches
                whole_word_count = len(re.findall(r'\b' + re.escape(keyword) + r'\b', text_lower))
                score += count + (whole_word_count * 0.5)

            # Apply category weight
            weighted_score = score * config['weight']

            # Chapter-based bonus
            if any(kw in chapter_lower for kw in config['keywords'][:3]):
                weighted_score *= 1.2

            category_scores[category] = weighted_score

        # Find best category
        if not any(category_scores.values()):
            return 'evaluation', 0.5

        best_category = max(category_scores, key=category_scores.get)
        confidence = min(category_scores[best_category] / max(sum(category_scores.values()), 1), 1.0)

        return best_category, confidence

    def economic_semantic_chunking(self, text: str, chapter: str, pages: List[int]) -> List[DocumentChunk]:
        """
        Chunking semântico otimizado para economia de embeddings
        """
        # Clean text and split by paragraphs
        text = re.sub(r'\n{3,}', '\n\n', text.strip())
        paragraphs = [p.strip() for p in text.split('\n\n') if p.strip() and len(p.strip()) > 50]

        chunks = []
        current_chunk = ""
        current_paragraphs = []

        for paragraph in paragraphs:
            # Check if adding this paragraph would exceed chunk size
            projected_size = len(current_chunk) + len(paragraph) + 2

            if projected_size > self.chunk_size and current_chunk:
                # Create chunk from current content
                category, confidence = self.advanced_categorize_content(current_chunk, chapter)

                chunk = DocumentChunk(
                    content=current_chunk.strip(),
                    category=category,
                    chapter=chapter,
                    page_number=pages[0] if pages else None,
                    metadata={
                        'length': len(current_chunk),
                        'paragraph_count': len(current_paragraphs),
                        'processing_timestamp': time.time(),
                        'page_range': f"{min(pages)}-{max(pages)}" if pages else "unknown",
                        'keyword_density': self._calculate_keyword_density(current_chunk)
                    },
                    confidence_score=confidence
                )
                chunks.append(chunk)

                # Start new chunk with minimal overlap for cost efficiency
                if len(current_chunk) > self.chunk_overlap:
                    overlap_text = current_chunk[-self.chunk_overlap:]
                    current_chunk = overlap_text + "\n\n" + paragraph
                    current_paragraphs = [paragraph]
                else:
                    current_chunk = paragraph
                    current_paragraphs = [paragraph]
            else:
                if current_chunk:
                    current_chunk += "\n\n" + paragraph
                else:
                    current_chunk = paragraph
                current_paragraphs.append(paragraph)

        # Add final chunk if exists
        if current_chunk and len(current_chunk.strip()) > 100:
            category, confidence = self.advanced_categorize_content(current_chunk, chapter)

            chunk = DocumentChunk(
                content=current_chunk.strip(),
                category=category,
                chapter=chapter,
                page_number=pages[0] if pages else None,
                metadata={
                    'length': len(current_chunk),
                    'paragraph_count': len(current_paragraphs),
                    'processing_timestamp': time.time(),
                    'page_range': f"{min(pages)}-{max(pages)}" if pages else "unknown",
                    'keyword_density': self._calculate_keyword_density(current_chunk)
                },
                confidence_score=confidence
            )
            chunks.append(chunk)

        logger.info(f"Created {len(chunks)} economic chunks for chapter: {chapter}")
        return chunks

    def _calculate_keyword_density(self, text: str) -> Dict[str, float]:
        """
        Calcula densidade de palavras-chave por categoria
        """
        text_lower = text.lower()
        word_count = len(text_lower.split())

        density = {}
        for category, config in self.categories.items():
            keyword_count = sum(text_lower.count(kw) for kw in config['keywords'])
            density[category] = keyword_count / max(word_count, 1)

        return density

    async def generate_embedding(self, text: str) -> Optional[List[float]]:
        """
        Gera embedding usando LLM service (LLM-agnostic)
        """
        try:
            import aiohttp
            import asyncio

            # Truncate text if too long to avoid excess costs
            if len(text) > 8000:  # Conservative limit
                text = text[:8000] + "..."

            # Call LLM service for embeddings
            url = f"{self.llm_service_url}/embeddings"
            payload = {
                "text": text,
                "model": self.embedding_model
            }

            async with aiohttp.ClientSession() as session:
                async with session.post(url, json=payload) as response:
                    if response.status == 200:
                        result = await response.json()
                        if result.get('success'):
                            return result.get('embedding')
                        else:
                            logger.error(f"LLM service embedding failed: {result.get('error', 'Unknown error')}")
                            return None
                    else:
                        error_text = await response.text()
                        logger.error(f"LLM service call failed with status {response.status}: {error_text}")
                        return None

        except Exception as e:
            logger.error(f"Embedding generation failed: {e}")
            return None

    async def store_chunks_individually(self, chunks: List[DocumentChunk]) -> bool:
        """
        Armazena chunks individualmente para evitar problemas de batch SQL
        """
        try:
            timestamp = datetime.now().isoformat()
            total_chunks = len(chunks)
            processed = 0

            for i, chunk in enumerate(chunks):
                try:
                    # Generate embedding
                    embedding = await self.generate_embedding(chunk.content)
                    if not embedding:
                        logger.warning(f"Skipping chunk without embedding: {chunk.chapter}")
                        continue

                    # Create individual session for each chunk
                    session = self.Session()

                    # Create database record
                    knowledge = EugeneKnowledge(
                        content=chunk.content,
                        embedding=embedding,
                        category=chunk.category,
                        chapter=chunk.chapter,
                        confidence_score=chunk.confidence_score,
                        meta_data=chunk.metadata,
                        created_at=timestamp
                    )

                    session.add(knowledge)
                    session.commit()
                    session.close()

                    processed += 1

                    if (i + 1) % 10 == 0:
                        logger.info(f"Processed {i + 1}/{total_chunks} chunks ({processed} successful)")

                    # Small delay to avoid rate limiting
                    await asyncio.sleep(0.1)

                except Exception as chunk_error:
                    logger.error(f"Failed to store chunk {i+1}: {chunk_error}")
                    if 'session' in locals():
                        try:
                            session.rollback()
                            session.close()
                        except:
                            pass
                    continue

            logger.info(f"Successfully stored {processed} chunks in database")
            return processed > 0

        except Exception as e:
            logger.error(f"Failed to store chunks: {e}")
            return False

    async def process_book_from_md(self, md_path: str) -> bool:
        """
        Processo completo econômico: MD → chunking → embedding → armazenamento
        """
        logger.info("Starting economic Eugene Schwartz book processing from MD...")

        # Extract text from MD
        chapters_data = self.extract_text_from_md(md_path)
        if not chapters_data:
            logger.error("Failed to extract text from MD file")
            return False

        # Process each chapter
        all_chunks = []
        for chapter_title, chapter_info in chapters_data.items():
            chapter_text = chapter_info['text']
            chapter_pages = chapter_info['pages']

            if len(chapter_text.strip()) < 200:  # Skip very short chapters
                continue

            chunks = self.economic_semantic_chunking(chapter_text, chapter_title, chapter_pages)
            all_chunks.extend(chunks)

        logger.info(f"Total chunks created: {len(all_chunks)}")

        # Store chunks with embeddings individually (more reliable)
        success = await self.store_chunks_individually(all_chunks)

        if success:
            logger.info("Economic Eugene Schwartz book processing completed successfully")

            # Calculate estimated cost
            estimated_cost = len(all_chunks) * 0.0001  # Rough estimate for text-embedding-3-small
            logger.info(f"Estimated processing cost: ~${estimated_cost:.2f}")
        else:
            logger.error("Failed to complete book processing")

        return success

    async def health_check(self) -> Dict[str, Any]:
        """
        Verifica saúde do sistema RAG econômico
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

            # Average confidence score
            avg_confidence = session.execute(text("""
                SELECT AVG(confidence_score) FROM eugene_knowledge
            """)).scalar() or 0.0

            session.close()

            return {
                'status': 'healthy',
                'total_chunks': total_chunks,
                'category_distribution': category_counts,
                'database_connection': True,
                'embedding_model': self.embedding_model,
                'embedding_dimensions': self.embedding_dimensions,
                'chunk_size': self.chunk_size,
                'chunk_overlap': self.chunk_overlap,
                'average_confidence': float(avg_confidence)
            }

        except Exception as e:
            logger.error(f"Health check failed: {e}")
            return {
                'status': 'unhealthy',
                'error': str(e)
            }

    async def get_consciousness_level_context(self, query: str, level: Optional[int] = None) -> List[RetrievalResult]:
        """
        Busca contexto específico para níveis de consciência com filtering melhorado
        """
        try:
            # Generate query embedding
            query_embedding = await self.generate_embedding(query)
            if not query_embedding:
                logger.error("Failed to generate embedding for query")
                return []

            logger.info(f"Generated embedding with {len(query_embedding)} dimensions")
            session = self.Session()

            # Simple query without complex filtering for debugging
            # Convert embedding to proper format for PostgreSQL vector type
            embedding_str = '[' + ','.join(map(str, query_embedding)) + ']'

            # Use direct string formatting for vector operations
            sql_query = text(f"""
                SELECT content, chapter, category, meta_data,
                       embedding <-> '{embedding_str}'::vector as similarity_score
                FROM eugene_knowledge
                ORDER BY embedding <-> '{embedding_str}'::vector
                LIMIT 5
            """)

            result = session.execute(sql_query)

            results = []
            for row in result:
                results.append(RetrievalResult(
                    content=row.content,
                    similarity_score=float(row.similarity_score),
                    category=row.category,
                    chapter=row.chapter,
                    metadata=row.meta_data or {}
                ))

            logger.info(f"Found {len(results)} results for query: {query}")
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
                SELECT content, chapter, category, meta_data,
                       embedding <-> :query_embedding as similarity_score
                FROM eugene_knowledge
                WHERE category = 'frameworks'
                ORDER BY embedding <-> :query_embedding
                LIMIT 3
            """)

            result = session.execute(sql_query, {
                'query_embedding': query_embedding
            })

            results = []
            for row in result:
                results.append(RetrievalResult(
                    content=row.content,
                    similarity_score=float(row.similarity_score),
                    category=row.category,
                    chapter=row.chapter,
                    metadata=row.meta_data or {}
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
                SELECT content, chapter, category, meta_data,
                       embedding <-> :query_embedding as similarity_score
                FROM eugene_knowledge
                WHERE category IN ('techniques', 'examples')
                ORDER BY embedding <-> :query_embedding
                LIMIT 4
            """)

            result = session.execute(sql_query, {
                'query_embedding': query_embedding
            })

            results = []
            for row in result:
                results.append(RetrievalResult(
                    content=row.content,
                    similarity_score=float(row.similarity_score),
                    category=row.category,
                    chapter=row.chapter,
                    metadata=row.meta_data or {}
                ))

            session.close()
            return results

        except Exception as e:
            logger.error(f"Improvement techniques retrieval failed: {e}")
            return []

    async def search_by_consciousness_level(self, level: int, query: str = "", max_results: int = 5) -> List[RetrievalResult]:
        """
        Busca específica por nível de consciência (1-5)
        """
        try:
            level_keywords = {
                1: "most sophisticated most aware",
                2: "problem aware solution aware",
                3: "problem conscious solution unaware",
                4: "unaware problem exists knows solution",
                5: "completely unaware unconscious"
            }

            search_query = f"{level_keywords.get(level, '')} {query}".strip()
            query_embedding = await self.generate_embedding(search_query)

            if not query_embedding:
                return []

            session = self.Session()

            # Search across all categories for consciousness level content
            sql_query = text("""
                SELECT content, chapter, category, meta_data,
                       embedding <-> :query_embedding as similarity_score
                FROM eugene_knowledge
                WHERE (meta_data->>'keyword_density')::jsonb ? 'consciousness_theory'
                   OR category = 'consciousness_theory'
                ORDER BY embedding <-> :query_embedding
                LIMIT :max_results
            """)

            result = session.execute(sql_query, {
                'query_embedding': query_embedding,
                'max_results': max_results
            })

            results = []
            for row in result:
                results.append(RetrievalResult(
                    content=row.content,
                    similarity_score=float(row.similarity_score),
                    category=row.category,
                    chapter=row.chapter,
                    metadata=row.meta_data or {}
                ))

            session.close()
            return results

        except Exception as e:
            logger.error(f"Consciousness level search failed: {e}")
            return []

    async def search_consciousness_context(self, query: str, consciousness_level: Optional[int] = None, max_results: int = 5) -> List[Dict[str, Any]]:
        """
        Busca contexto específico para análise de níveis de consciência
        Compatible method for RAG API
        """
        try:
            if consciousness_level:
                results = await self.search_by_consciousness_level(consciousness_level, query, max_results)
            else:
                # General consciousness search using get_consciousness_level_context
                results = await self.get_consciousness_level_context(query)
                results = results[:max_results]

            # Convert to the format expected by RAG API
            return [
                {
                    'content': result.content,
                    'similarity': result.similarity_score,
                    'category': result.category,
                    'chapter': result.chapter,
                    'metadata': result.metadata
                }
                for result in results
            ]

        except Exception as e:
            logger.error(f"Consciousness context search failed: {e}")
            return []

# Test and utility functions
async def main():
    """
    Main function for testing the economic RAG processor
    """
    # Initialize system
    rag = EconomicEugeneRAG()

    # Setup database
    setup_success = await rag.setup_database()
    if not setup_success:
        logger.error("Database setup failed")
        return

    # Process MD file
    md_path = "docs/breakthrough_advertising.md"
    if os.path.exists(md_path):
        processing_success = await rag.process_book_from_md(md_path)
        if processing_success:
            logger.info("Book processing completed successfully")
        else:
            logger.error("Book processing failed")
    else:
        logger.error(f"MD file not found at: {md_path}")

    # Health check
    health = await rag.health_check()
    logger.info(f"System health: {health}")

if __name__ == "__main__":
    asyncio.run(main())
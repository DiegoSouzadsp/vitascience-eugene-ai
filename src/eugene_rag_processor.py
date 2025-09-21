"""
Eugene Schwartz RAG System - Complete Implementation
Processes "Breakthrough Advertising" with intelligent semantic chunking
focused on the 5 Levels of Market Consciousness methodology.
"""

import os
import re
import json
import logging
import asyncio
import psycopg2
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
from openai import OpenAI
import numpy as np
from datetime import datetime
import hashlib

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class EugeneChunk:
    """Represents a semantic chunk from Eugene Schwartz's methodology"""
    id: str
    content: str
    category: str  # consciousness_theory, frameworks, techniques, examples, evaluation
    chapter: str
    consciousness_level: Optional[int]  # 1-5 for awareness levels
    confidence_score: float
    metadata: Dict
    embedding: Optional[List[float]] = None

class EugeneSemanticChunker:
    """Intelligent semantic chunking for Eugene Schwartz methodology"""

    def __init__(self):
        self.consciousness_patterns = {
            1: [r"unaware", r"completely.*unaware", r"no.*awareness", r"don't.*know.*need"],
            2: [r"problem.*aware", r"need.*aware", r"realize.*problem", r"feel.*need"],
            3: [r"solution.*aware", r"know.*solution", r"aware.*product", r"category.*aware"],
            4: [r"product.*aware", r"know.*your.*product", r"familiar.*with"],
            5: [r"most.*aware", r"completely.*aware", r"ready.*to.*buy", r"final.*stage"]
        }

        self.category_patterns = {
            'consciousness_theory': [
                r"awareness.*scale", r"stages.*of.*awareness", r"consciousness.*level",
                r"psychological.*wall", r"state.*of.*awareness", r"market.*awareness"
            ],
            'frameworks': [
                r"headline.*formula", r"copy.*structure", r"advertising.*framework",
                r"PAS", r"AIDA", r"problem.*agitate.*solve"
            ],
            'techniques': [
                r"copy.*technique", r"writing.*method", r"advertising.*approach",
                r"headline.*technique", r"persuasion.*method"
            ],
            'examples': [
                r"for.*example", r"here's.*an.*example", r"case.*study",
                r"\$\d+", r"ad.*that.*worked", r"successful.*campaign"
            ],
            'evaluation': [
                r"test.*result", r"measure", r"evaluate", r"criteria",
                r"metric", r"performance", r"effectiveness"
            ]
        }

    def detect_consciousness_level(self, text: str) -> Tuple[Optional[int], float]:
        """Detect which consciousness level (1-5) this text refers to"""
        text_lower = text.lower()
        best_level = None
        best_score = 0.0

        for level, patterns in self.consciousness_patterns.items():
            score = 0
            for pattern in patterns:
                matches = len(re.findall(pattern, text_lower))
                score += matches

            if score > best_score:
                best_score = score
                best_level = level

        # Normalize confidence score
        confidence = min(best_score / 10.0, 1.0) if best_score > 0 else 0.0
        return best_level, confidence

    def categorize_content(self, text: str) -> Tuple[str, float]:
        """Categorize content into Eugene's methodology types"""
        text_lower = text.lower()
        best_category = 'techniques'  # default
        best_score = 0.0

        for category, patterns in self.category_patterns.items():
            score = 0
            for pattern in patterns:
                matches = len(re.findall(pattern, text_lower))
                score += matches

            if score > best_score:
                best_score = score
                best_category = category

        confidence = min(best_score / 5.0, 1.0) if best_score > 0 else 0.3
        return best_category, confidence

    def chunk_semantically(self, text: str, max_chunk_size: int = 1000, overlap: int = 200) -> List[EugeneChunk]:
        """Create semantic chunks preserving Eugene's methodology integrity"""
        chunks = []

        # Split by major sections (chapters/pages)
        sections = re.split(r'---\s*PÁGINA\s*\d+\s*---', text)

        for section_idx, section in enumerate(sections):
            if len(section.strip()) < 50:  # Skip very short sections
                continue

            # Extract chapter/page info
            chapter = f"Section_{section_idx:03d}"

            # Split section into paragraphs for semantic boundaries
            paragraphs = [p.strip() for p in section.split('\n\n') if p.strip()]

            current_chunk = ""
            current_paragraphs = []

            for paragraph in paragraphs:
                # Check if adding this paragraph would exceed chunk size
                if len(current_chunk) + len(paragraph) > max_chunk_size and current_chunk:
                    # Create chunk from accumulated content
                    chunk = self._create_chunk(current_chunk, chapter, current_paragraphs)
                    if chunk:
                        chunks.append(chunk)

                    # Start new chunk with overlap
                    overlap_content = current_chunk[-overlap:] if len(current_chunk) > overlap else current_chunk
                    current_chunk = overlap_content + "\n\n" + paragraph
                    current_paragraphs = [paragraph]
                else:
                    # Add paragraph to current chunk
                    if current_chunk:
                        current_chunk += "\n\n" + paragraph
                    else:
                        current_chunk = paragraph
                    current_paragraphs.append(paragraph)

            # Create final chunk for this section
            if current_chunk.strip():
                chunk = self._create_chunk(current_chunk, chapter, current_paragraphs)
                if chunk:
                    chunks.append(chunk)

        logger.info(f"Created {len(chunks)} semantic chunks")
        return chunks

    def _create_chunk(self, content: str, chapter: str, paragraphs: List[str]) -> Optional[EugeneChunk]:
        """Create a single EugeneChunk with metadata"""
        if len(content.strip()) < 100:  # Skip very short chunks
            return None

        # Generate unique ID
        chunk_id = hashlib.md5(content.encode()).hexdigest()[:12]

        # Detect consciousness level and category
        consciousness_level, consciousness_confidence = self.detect_consciousness_level(content)
        category, category_confidence = self.categorize_content(content)

        # Calculate overall confidence
        confidence_score = (consciousness_confidence + category_confidence) / 2

        # Create metadata
        metadata = {
            'word_count': len(content.split()),
            'paragraph_count': len(paragraphs),
            'consciousness_confidence': consciousness_confidence,
            'category_confidence': category_confidence,
            'created_at': datetime.utcnow().isoformat(),
            'contains_examples': bool(re.search(r'for.*example|case.*study|\$\d+', content.lower())),
            'contains_formulas': bool(re.search(r'formula|framework|structure', content.lower())),
            'contains_levels': bool(re.search(r'stage|level|awareness', content.lower()))
        }

        return EugeneChunk(
            id=chunk_id,
            content=content.strip(),
            category=category,
            chapter=chapter,
            consciousness_level=consciousness_level,
            confidence_score=confidence_score,
            metadata=metadata
        )

class EugeneEmbeddingGenerator:
    """Generate embeddings using text-embedding-3-small for cost efficiency"""

    def __init__(self, api_key: str):
        self.client = OpenAI(api_key=api_key)
        self.model = "text-embedding-3-small"  # More economical option
        self.dimensions = 1536  # text-embedding-3-small dimensions

    async def generate_embedding(self, text: str) -> List[float]:
        """Generate embedding for a single text"""
        try:
            response = self.client.embeddings.create(
                input=text,
                model=self.model
            )
            return response.data[0].embedding
        except Exception as e:
            logger.error(f"Error generating embedding: {e}")
            return [0.0] * self.dimensions

    async def generate_batch_embeddings(self, chunks: List[EugeneChunk], batch_size: int = 100) -> List[EugeneChunk]:
        """Generate embeddings for multiple chunks efficiently"""
        logger.info(f"Generating embeddings for {len(chunks)} chunks...")

        for i in range(0, len(chunks), batch_size):
            batch = chunks[i:i + batch_size]
            texts = [chunk.content for chunk in batch]

            try:
                response = self.client.embeddings.create(
                    input=texts,
                    model=self.model
                )

                for j, chunk in enumerate(batch):
                    chunk.embedding = response.data[j].embedding

                logger.info(f"Processed batch {i//batch_size + 1}/{(len(chunks)-1)//batch_size + 1}")

            except Exception as e:
                logger.error(f"Error in batch {i//batch_size + 1}: {e}")
                # Generate individual embeddings as fallback
                for chunk in batch:
                    chunk.embedding = await self.generate_embedding(chunk.content)

        return chunks

class EugeneVectorDatabase:
    """PostgreSQL + pgvector storage for Eugene Schwartz methodology"""

    def __init__(self, connection_string: str):
        self.connection_string = connection_string
        self.embedding_dim = 1536  # text-embedding-3-small dimensions

    def initialize_database(self):
        """Create tables and indexes for Eugene knowledge storage"""
        with psycopg2.connect(self.connection_string) as conn:
            with conn.cursor() as cur:
                # Enable pgvector extension
                cur.execute("CREATE EXTENSION IF NOT EXISTS vector;")

                # Drop and recreate table for fresh start
                cur.execute("DROP TABLE IF EXISTS eugene_knowledge;")

                # Create main knowledge table
                cur.execute(f"""
                    CREATE TABLE eugene_knowledge (
                        id VARCHAR(20) PRIMARY KEY,
                        content TEXT NOT NULL,
                        embedding vector({self.embedding_dim}),
                        category VARCHAR(50) NOT NULL,
                        chapter VARCHAR(100),
                        consciousness_level INTEGER,
                        confidence_score FLOAT,
                        metadata JSONB,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    );
                """)

                # Create indexes for efficient retrieval
                cur.execute("""
                    CREATE INDEX idx_eugene_category ON eugene_knowledge(category);
                    CREATE INDEX idx_eugene_consciousness ON eugene_knowledge(consciousness_level);
                    CREATE INDEX idx_eugene_confidence ON eugene_knowledge(confidence_score);
                    CREATE INDEX idx_eugene_embedding_cosine ON eugene_knowledge
                    USING ivfflat (embedding vector_cosine_ops) WITH (lists = 100);
                """)

                conn.commit()
                logger.info("Database initialized successfully")

    def store_chunks(self, chunks: List[EugeneChunk]):
        """Store chunks in PostgreSQL with vectors"""
        with psycopg2.connect(self.connection_string) as conn:
            with conn.cursor() as cur:
                for chunk in chunks:
                    if chunk.embedding is None:
                        logger.warning(f"Skipping chunk {chunk.id} - no embedding")
                        continue

                    cur.execute("""
                        INSERT INTO eugene_knowledge
                        (id, content, embedding, category, chapter, consciousness_level, confidence_score, metadata)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                        ON CONFLICT (id) DO UPDATE SET
                        content = EXCLUDED.content,
                        embedding = EXCLUDED.embedding,
                        category = EXCLUDED.category,
                        chapter = EXCLUDED.chapter,
                        consciousness_level = EXCLUDED.consciousness_level,
                        confidence_score = EXCLUDED.confidence_score,
                        metadata = EXCLUDED.metadata
                    """, (
                        chunk.id,
                        chunk.content,
                        chunk.embedding,
                        chunk.category,
                        chunk.chapter,
                        chunk.consciousness_level,
                        chunk.confidence_score,
                        json.dumps(chunk.metadata)
                    ))

                conn.commit()
                logger.info(f"Stored {len(chunks)} chunks in database")

    def search_similar(self, query_embedding: List[float], limit: int = 10,
                      category: Optional[str] = None, consciousness_level: Optional[int] = None) -> List[Dict]:
        """Search for similar content using vector similarity"""
        with psycopg2.connect(self.connection_string) as conn:
            with conn.cursor() as cur:
                conditions = ["1=1"]
                params = [query_embedding, limit]

                if category:
                    conditions.append("category = %s")
                    params.insert(-1, category)

                if consciousness_level:
                    conditions.append("consciousness_level = %s")
                    params.insert(-1, consciousness_level)

                query = f"""
                    SELECT id, content, category, chapter, consciousness_level,
                           confidence_score, metadata,
                           1 - (embedding <=> %s) as similarity
                    FROM eugene_knowledge
                    WHERE {' AND '.join(conditions)}
                    ORDER BY embedding <=> %s
                    LIMIT %s
                """

                cur.execute(query, params)
                results = cur.fetchall()

                return [
                    {
                        'id': row[0],
                        'content': row[1],
                        'category': row[2],
                        'chapter': row[3],
                        'consciousness_level': row[4],
                        'confidence_score': row[5],
                        'metadata': row[6],
                        'similarity': row[7]
                    }
                    for row in results
                ]

    def get_statistics(self) -> Dict:
        """Get database statistics"""
        with psycopg2.connect(self.connection_string) as conn:
            with conn.cursor() as cur:
                # Total chunks
                cur.execute("SELECT COUNT(*) FROM eugene_knowledge")
                total_chunks = cur.fetchone()[0]

                # By category
                cur.execute("""
                    SELECT category, COUNT(*)
                    FROM eugene_knowledge
                    GROUP BY category
                    ORDER BY COUNT(*) DESC
                """)
                by_category = dict(cur.fetchall())

                # By consciousness level
                cur.execute("""
                    SELECT consciousness_level, COUNT(*)
                    FROM eugene_knowledge
                    WHERE consciousness_level IS NOT NULL
                    GROUP BY consciousness_level
                    ORDER BY consciousness_level
                """)
                by_consciousness = dict(cur.fetchall())

                return {
                    'total_chunks': total_chunks,
                    'by_category': by_category,
                    'by_consciousness_level': by_consciousness
                }

class EugeneRAGProcessor:
    """Main RAG processor orchestrating the complete pipeline"""

    def __init__(self, openai_api_key: str, db_connection_string: str):
        self.chunker = EugeneSemanticChunker()
        self.embedder = EugeneEmbeddingGenerator(openai_api_key)
        self.database = EugeneVectorDatabase(db_connection_string)

    async def process_book(self, book_path: str) -> Dict:
        """Process the complete Eugene Schwartz book"""
        logger.info("Starting Eugene Schwartz book processing...")

        # Load book content
        with open(book_path, 'r', encoding='utf-8') as f:
            book_content = f.read()

        logger.info(f"Loaded book: {len(book_content)} characters")

        # Initialize database
        self.database.initialize_database()

        # Create semantic chunks
        chunks = self.chunker.chunk_semantically(book_content)
        logger.info(f"Created {len(chunks)} semantic chunks")

        # Generate embeddings
        chunks_with_embeddings = await self.embedder.generate_batch_embeddings(chunks)

        # Store in database
        self.database.store_chunks(chunks_with_embeddings)

        # Get final statistics
        stats = self.database.get_statistics()

        return {
            'status': 'completed',
            'chunks_processed': len(chunks),
            'chunks_stored': stats['total_chunks'],
            'categories': stats['by_category'],
            'consciousness_levels': stats['by_consciousness_level'],
            'processing_time': datetime.utcnow().isoformat()
        }

    async def search_consciousness_context(self, query: str, level: Optional[int] = None, limit: int = 5) -> List[Dict]:
        """Search for consciousness-specific context"""
        query_embedding = await self.embedder.generate_embedding(query)
        return self.database.search_similar(
            query_embedding,
            limit=limit,
            category='consciousness_theory',
            consciousness_level=level
        )

    async def get_framework_guidance(self, copy_type: str, limit: int = 5) -> List[Dict]:
        """Get framework guidance for specific copy types"""
        query = f"framework for {copy_type} copy writing advertising"
        query_embedding = await self.embedder.generate_embedding(query)
        return self.database.search_similar(
            query_embedding,
            limit=limit,
            category='frameworks'
        )

    async def get_improvement_techniques(self, problem_area: str, limit: int = 5) -> List[Dict]:
        """Get specific techniques for improvement areas"""
        query = f"technique to improve {problem_area} in advertising copy"
        query_embedding = await self.embedder.generate_embedding(query)
        return self.database.search_similar(
            query_embedding,
            limit=limit,
            category='techniques'
        )

async def main():
    """Main execution function"""
    # Configuration
    openai_api_key = os.getenv('OPENAI_API_KEY')
    db_connection = os.getenv('DATABASE_URL', 'postgresql://postgres:password@localhost:5432/eugene_rag')
    book_path = r'D:\Projetos\vitascience-eugene-ai\docs\breakthrough_advertising.md'

    if not openai_api_key:
        raise ValueError("OPENAI_API_KEY environment variable required")

    # Initialize processor
    processor = EugeneRAGProcessor(openai_api_key, db_connection)

    # Process the book
    result = await processor.process_book(book_path)

    logger.info("Processing completed successfully!")
    logger.info(f"Results: {json.dumps(result, indent=2)}")

    # Test searches
    logger.info("\n=== Testing Search Functions ===")

    # Test consciousness search
    consciousness_results = await processor.search_consciousness_context("unaware market", level=1)
    logger.info(f"Consciousness Level 1 results: {len(consciousness_results)}")

    # Test framework search
    framework_results = await processor.get_framework_guidance("headline")
    logger.info(f"Headline framework results: {len(framework_results)}")

    # Test technique search
    technique_results = await processor.get_improvement_techniques("awareness")
    logger.info(f"Awareness technique results: {len(technique_results)}")

    return result

if __name__ == "__main__":
    asyncio.run(main())
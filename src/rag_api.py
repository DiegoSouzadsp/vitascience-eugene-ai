#!/usr/bin/env python3
"""
RAG API Service - Eugene Schwartz VSL Analyzer
FastAPI service for retrieving relevant chunks from Eugene Schwartz book
"""

import os
import json
import asyncio
from typing import List, Dict, Any, Optional
from datetime import datetime

import psycopg2
import numpy as np
from openai import OpenAI
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

# Configuration
DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://postgres:password@postgres-vector:5432/eugene_rag')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# Initialize OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY) if OPENAI_API_KEY else None

# FastAPI app
app = FastAPI(
    title="Eugene Schwartz RAG API",
    description="Retrieval-Augmented Generation API for Eugene Schwartz VSL Analysis",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models
class RAGQuery(BaseModel):
    query: str = Field(..., description="Search query for RAG retrieval")
    max_results: int = Field(default=5, ge=1, le=20, description="Maximum number of results")
    min_similarity: float = Field(default=0.7, ge=0.0, le=1.0, description="Minimum similarity threshold")
    category: Optional[str] = Field(default=None, description="Filter by category")

class RAGChunk(BaseModel):
    content: str
    category: str
    chapter: Optional[str] = None
    similarity_score: float
    metadata: Dict[str, Any] = {}

class RAGResponse(BaseModel):
    chunks: List[RAGChunk]
    query: str
    total_found: int
    processing_time_ms: float
    timestamp: str

# Database connection
def get_db_connection():
    """Get database connection"""
    try:
        conn = psycopg2.connect(DATABASE_URL)
        return conn
    except Exception as e:
        raise HTTPException(status_code=500, f"Database connection failed: {str(e)}")

# Generate embedding
async def generate_embedding(text: str) -> List[float]:
    """Generate embedding for text using OpenAI"""
    if not client:
        raise HTTPException(status_code=500, "OpenAI API key not configured")

    try:
        response = client.embeddings.create(
            model="text-embedding-ada-002",
            input=text.replace("\\n", " ")
        )
        return response.data[0].embedding
    except Exception as e:
        raise HTTPException(status_code=500, f"Failed to generate embedding: {str(e)}")

# RAG retrieval function
async def retrieve_chunks(
    query: str,
    max_results: int = 5,
    min_similarity: float = 0.7,
    category: Optional[str] = None
) -> List[RAGChunk]:
    """Retrieve relevant chunks from Eugene Schwartz book"""

    start_time = datetime.now()

    # Generate query embedding
    query_embedding = await generate_embedding(query)

    # Database query
    conn = get_db_connection()
    try:
        cur = conn.cursor()

        # Build query with optional category filter
        base_query = """
            SELECT
                content,
                metadata,
                embedding <=> %s::vector as similarity_score
            FROM eugene_embeddings
        """

        params = [str(query_embedding)]

        if category:
            base_query += " WHERE metadata->>'category' = %s"
            params.append(category)

        base_query += """
            ORDER BY embedding <=> %s::vector
            LIMIT %s
        """
        params.extend([str(query_embedding), max_results * 2])  # Get more for filtering

        cur.execute(base_query, params)
        results = cur.fetchall()

        chunks = []
        for content, metadata_json, similarity_score in results:
            # Convert similarity distance to similarity score
            similarity = 1 - similarity_score

            if similarity >= min_similarity:
                metadata = json.loads(metadata_json) if metadata_json else {}

                chunk = RAGChunk(
                    content=content,
                    category=metadata.get('category', 'general'),
                    chapter=metadata.get('chapter'),
                    similarity_score=similarity,
                    metadata=metadata
                )
                chunks.append(chunk)

                if len(chunks) >= max_results:
                    break

        return chunks

    finally:
        conn.close()

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM eugene_embeddings")
        count = cur.fetchone()[0]
        conn.close()

        return {
            "status": "healthy",
            "database": "connected",
            "embeddings_count": count,
            "openai_configured": bool(OPENAI_API_KEY),
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, f"Health check failed: {str(e)}")

# Generic retrieve endpoint
@app.post("/retrieve/{category}")
async def retrieve_by_category(
    category: str,
    query_data: RAGQuery
):
    """Retrieve chunks by category with query"""

    start_time = datetime.now()

    try:
        chunks = await retrieve_chunks(
            query=query_data.query,
            max_results=query_data.max_results,
            min_similarity=query_data.min_similarity,
            category=category
        )

        processing_time = (datetime.now() - start_time).total_seconds() * 1000

        response = RAGResponse(
            chunks=chunks,
            query=query_data.query,
            total_found=len(chunks),
            processing_time_ms=processing_time,
            timestamp=datetime.now().isoformat()
        )

        return response

    except Exception as e:
        raise HTTPException(status_code=500, f"Retrieval failed: {str(e)}")

# Consciousness-specific endpoint
@app.post("/retrieve/consciousness")
async def retrieve_consciousness(query_data: RAGQuery):
    """Retrieve consciousness-related chunks"""
    return await retrieve_by_category("consciousness_theory", query_data)

# Frameworks-specific endpoint
@app.post("/retrieve/frameworks")
async def retrieve_frameworks(query_data: RAGQuery):
    """Retrieve framework-related chunks"""
    return await retrieve_by_category("copy_frameworks", query_data)

# Techniques-specific endpoint
@app.post("/retrieve/techniques")
async def retrieve_techniques(query_data: RAGQuery):
    """Retrieve technique-related chunks"""
    return await retrieve_by_category("techniques", query_data)

# Examples-specific endpoint
@app.post("/retrieve/examples")
async def retrieve_examples(query_data: RAGQuery):
    """Retrieve example-related chunks"""
    return await retrieve_by_category("examples", query_data)

# Evaluation-specific endpoint
@app.post("/retrieve/evaluation")
async def retrieve_evaluation(query_data: RAGQuery):
    """Retrieve evaluation-related chunks"""
    return await retrieve_by_category("evaluation", query_data)

# General search endpoint
@app.post("/search")
async def search_all(query_data: RAGQuery):
    """Search across all categories"""

    start_time = datetime.now()

    try:
        chunks = await retrieve_chunks(
            query=query_data.query,
            max_results=query_data.max_results,
            min_similarity=query_data.min_similarity,
            category=query_data.category
        )

        processing_time = (datetime.now() - start_time).total_seconds() * 1000

        response = RAGResponse(
            chunks=chunks,
            query=query_data.query,
            total_found=len(chunks),
            processing_time_ms=processing_time,
            timestamp=datetime.now().isoformat()
        )

        return response

    except Exception as e:
        raise HTTPException(status_code=500, f"Search failed: {str(e)}")

# Statistics endpoint
@app.get("/stats")
async def get_stats():
    """Get RAG system statistics"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        # Total chunks
        cur.execute("SELECT COUNT(*) FROM eugene_embeddings")
        total_chunks = cur.fetchone()[0]

        # Chunks by category
        cur.execute("""
            SELECT
                metadata->>'category' as category,
                COUNT(*) as count
            FROM eugene_embeddings
            WHERE metadata->>'category' IS NOT NULL
            GROUP BY metadata->>'category'
            ORDER BY count DESC
        """)
        categories = dict(cur.fetchall())

        conn.close()

        return {
            "total_chunks": total_chunks,
            "categories": categories,
            "database_url": DATABASE_URL.split('@')[1] if '@' in DATABASE_URL else "configured",
            "openai_configured": bool(OPENAI_API_KEY),
            "timestamp": datetime.now().isoformat()
        }

    except Exception as e:
        raise HTTPException(status_code=500, f"Stats failed: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
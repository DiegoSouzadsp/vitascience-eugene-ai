"""
Eugene Schwartz RAG API
FastAPI service para sistema de Retrieval-Augmented Generation
Especializado em análise de copywriting com metodologia Eugene Schwartz
"""

import os
import asyncio
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime

from fastapi import FastAPI, HTTPException, BackgroundTasks, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
import uvicorn

import sys
import os
sys.path.append(os.path.dirname(__file__))
from rag_query_service import RAGQueryService, get_rag_query_service

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Eugene Schwartz RAG API",
    description="Sistema RAG especializado na metodologia dos 5 níveis de consciência",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global RAG query service instance
rag_query_service: Optional[RAGQueryService] = None

# Pydantic models for API

class QueryRequest(BaseModel):
    """Request model para queries de retrieval"""
    query: str = Field(..., description="Query de busca no conhecimento Eugene Schwartz")
    category: Optional[str] = Field(None, description="Categoria específica para filtrar")
    max_results: int = Field(5, description="Número máximo de resultados", ge=1, le=20)

class RetrievalResponse(BaseModel):
    """Response model para resultados de retrieval"""
    content: str
    similarity_score: float
    category: str
    chapter: str
    metadata: Dict[str, Any]

class ConsciousnessLevelRequest(BaseModel):
    """Request para análise de nível de consciência"""
    copy_text: str = Field(..., description="Texto da copy para análise")
    consciousness_level: Optional[int] = Field(None, description="Nível específico (1-5)", ge=1, le=5)

class FrameworkRequest(BaseModel):
    """Request para guidance de frameworks"""
    copy_type: str = Field(..., description="Tipo de copy (VSL, email, sales page, etc.)")
    industry: Optional[str] = Field(None, description="Indústria específica (health, tech, etc.)")

class ImprovementRequest(BaseModel):
    """Request para técnicas de melhoria"""
    problem_area: str = Field(..., description="Área problema identificada na copy")
    current_level: Optional[int] = Field(None, description="Nível atual de consciência do mercado")

class HealthCheckResponse(BaseModel):
    """Response model para health check"""
    status: str
    total_chunks: int
    category_distribution: Dict[str, int]
    database_connection: bool
    embedding_model: str
    response_time_ms: float

class ProcessingStatus(BaseModel):
    """Status do processamento do livro"""
    status: str
    progress: float
    message: str
    estimated_completion: Optional[str] = None

# Dependency to get RAG query service
async def get_rag_service() -> RAGQueryService:
    """Dependency para obter instância do serviço RAG"""
    global rag_query_service
    if rag_query_service is None:
        rag_query_service = await get_rag_query_service()
    return rag_query_service

# API Routes

@app.on_event("startup")
async def startup_event():
    """Inicialização do sistema na startup"""
    global rag_query_service

    logger.info("Initializing Eugene Schwartz RAG Query Service...")

    try:
        rag_query_service = await get_rag_query_service()
        logger.info("RAG Query Service initialized successfully")

    except Exception as e:
        logger.error(f"Failed to initialize RAG Query Service: {e}")

@app.get("/health", response_model=HealthCheckResponse)
async def health_check(rag: RAGQueryService = Depends(get_rag_service)):
    """
    Health check do sistema RAG
    """
    import time
    start_time = time.time()

    try:
        # Use new health check method
        health_info = await rag.health_check()
        response_time = (time.time() - start_time) * 1000

        return HealthCheckResponse(
            status=health_info.get('status', 'unknown'),
            total_chunks=health_info.get('total_records', 0),
            category_distribution=health_info.get('category_distribution', {}),
            database_connection=health_info.get('database_connected', False),
            embedding_model=f"llm_agnostic_{health_info.get('primary_llm', 'unknown')}",
            response_time_ms=response_time
        )

    except Exception as e:
        logger.error(f"Health check failed: {e}")
        raise HTTPException(status_code=500, detail=f"Health check failed: {str(e)}")

@app.post("/retrieve/consciousness", response_model=List[RetrievalResponse])
async def retrieve_consciousness_context(
    request: ConsciousnessLevelRequest,
    rag: RAGQueryService = Depends(get_rag_service)
):
    """
    Busca contexto específico para análise de níveis de consciência
    """
    try:
        results = await rag.query_consciousness_levels(
            request.copy_text,
            max_results=5
        )

        return [
            RetrievalResponse(
                content=result.content,
                similarity_score=result.similarity_score,
                category=result.category,
                chapter=result.chapter,
                metadata=result.metadata
            )
            for result in results
        ]

    except Exception as e:
        logger.error(f"Consciousness retrieval failed: {e}")
        raise HTTPException(status_code=500, detail=f"Retrieval failed: {str(e)}")

@app.post("/retrieve/frameworks", response_model=List[RetrievalResponse])
async def retrieve_framework_guidance(
    request: FrameworkRequest,
    rag: RAGQueryService = Depends(get_rag_service)
):
    """
    Busca guidance sobre frameworks de copywriting
    """
    try:
        copy_type_query = f"{request.copy_type}"
        if request.industry:
            copy_type_query += f" {request.industry}"

        results = await rag.query_frameworks(copy_type_query, max_results=3)

        return [
            RetrievalResponse(
                content=result.content,
                similarity_score=result.similarity_score,
                category=result.category,
                chapter=result.chapter,
                metadata=result.metadata
            )
            for result in results
        ]

    except Exception as e:
        logger.error(f"Framework retrieval failed: {e}")
        raise HTTPException(status_code=500, detail=f"Retrieval failed: {str(e)}")

@app.post("/retrieve/improvements", response_model=List[RetrievalResponse])
async def retrieve_improvement_techniques(
    request: ImprovementRequest,
    rag: RAGQueryService = Depends(get_rag_service)
):
    """
    Busca técnicas específicas para melhorias identificadas
    """
    try:
        problem_query = request.problem_area
        if request.current_level:
            problem_query += f" consciousness level {request.current_level}"

        results = await rag.query_techniques(problem_query, max_results=4)

        return [
            RetrievalResponse(
                content=result.content,
                similarity_score=result.similarity_score,
                category=result.category,
                chapter=result.chapter,
                metadata=result.metadata
            )
            for result in results
        ]

    except Exception as e:
        logger.error(f"Improvement retrieval failed: {e}")
        raise HTTPException(status_code=500, detail=f"Retrieval failed: {str(e)}")

@app.post("/retrieve/general", response_model=List[RetrievalResponse])
async def general_retrieval(
    request: QueryRequest,
    rag: RAGQueryService = Depends(get_rag_service)
):
    """
    Busca geral no conhecimento Eugene Schwartz
    """
    try:
        # Use general query method
        results = await rag.query_by_category(request.query, None, request.max_results)

        # Limit results
        results = results[:request.max_results]

        return [
            RetrievalResponse(
                content=result.content,
                similarity_score=result.similarity_score,
                category=result.category,
                chapter=result.chapter,
                metadata=result.metadata
            )
            for result in results
        ]

    except Exception as e:
        logger.error(f"General retrieval failed: {e}")
        raise HTTPException(status_code=500, detail=f"Retrieval failed: {str(e)}")

@app.post("/process-book", response_model=ProcessingStatus)
async def process_eugene_book(
    background_tasks: BackgroundTasks,
    md_path: str = "docs/breakthrough_advertising.md",
    rag: RAGQueryService = Depends(get_rag_service)
):
    """
    Processa o livro Eugene Schwartz do arquivo MD
    """
    try:
        full_path = os.path.join(r"D:\Projetos\vitascience-eugene-ai", md_path)
        if not os.path.exists(full_path):
            raise HTTPException(status_code=404, detail=f"MD file not found at: {full_path}")

        # Start processing in background
        background_tasks.add_task(rag.process_book, full_path)

        return ProcessingStatus(
            status="started",
            progress=0.0,
            message="Eugene Schwartz book processing started",
            estimated_completion="3-5 minutes with text-embedding-3-small"
        )

    except Exception as e:
        logger.error(f"Book processing initiation failed: {e}")
        raise HTTPException(status_code=500, detail=f"Processing failed: {str(e)}")

@app.get("/categories")
async def get_categories(rag: RAGQueryService = Depends(get_rag_service)):
    """
    Retorna categorias disponíveis no sistema
    """
    return {
        "categories": ['consciousness_theory', 'frameworks', 'techniques', 'examples', 'evaluation'],
        "description": "Categorias baseadas na metodologia Eugene Schwartz"
    }

@app.get("/stats")
async def get_system_stats(rag: RAGQueryService = Depends(get_rag_service)):
    """
    Estatísticas do sistema RAG
    """
    try:
        stats = await rag.health_check()

        return {
            "total_chunks": stats.get('total_records', 0),
            "category_distribution": stats.get('category_distribution', {}),
            "primary_llm": stats.get('primary_llm', 'unknown'),
            "llm_status": stats.get('llm_status', 'unknown'),
            "configuration": {
                "service_type": "llm_agnostic_rag_query",
                "embedding_model": f"llm_agnostic_{stats.get('primary_llm', 'unknown')}",
                "database_connected": stats.get('database_connected', False)
            }
        }

    except Exception as e:
        logger.error(f"Stats retrieval failed: {e}")
        raise HTTPException(status_code=500, detail=f"Stats failed: {str(e)}")

# Error handlers

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """Handler geral para exceções"""
    logger.error(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "detail": str(exc),
            "timestamp": datetime.now().isoformat()
        }
    )

# Test endpoints for development

class ConsciousnessLevelQueryRequest(BaseModel):
    """Request para busca por nível de consciência"""
    level: int = Field(..., description="Nível de consciência (1-5)", ge=1, le=5)
    query: str = Field("", description="Query adicional para refinar busca")
    max_results: int = Field(5, description="Número máximo de resultados", ge=1, le=10)

@app.post("/retrieve/consciousness-level", response_model=List[RetrievalResponse])
async def retrieve_by_consciousness_level(
    request: ConsciousnessLevelQueryRequest,
    rag: RAGQueryService = Depends(get_rag_service)
):
    """
    Busca específica por nível de consciência (1-5)
    """
    try:
        results = await rag.query_consciousness_levels(request.query, request.max_results)

        return [
            RetrievalResponse(
                content=result.content,
                similarity_score=result.similarity_score,
                category=result.category,
                chapter=result.chapter,
                metadata=result.metadata
            )
            for result in results
        ]

    except Exception as e:
        logger.error(f"Consciousness level retrieval failed: {e}")
        raise HTTPException(status_code=500, detail=f"Retrieval failed: {str(e)}")

@app.get("/test/embeddings")
async def test_embeddings(
    text: str = "Test embedding generation",
    rag: RAGQueryService = Depends(get_rag_service)
):
    """
    Testa geração de embeddings
    """
    try:
        embedding = await rag.embedder.generate_embedding(text)

        return {
            "text": text,
            "embedding_size": len(embedding) if embedding else 0,
            "embedding_preview": embedding[:5] if embedding else None,
            "success": embedding is not None
        }

    except Exception as e:
        logger.error(f"Embedding test failed: {e}")
        raise HTTPException(status_code=500, detail=f"Embedding test failed: {str(e)}")

@app.get("/test/database")
async def test_database_simple(rag: RAGQueryService = Depends(get_rag_service)):
    """
    Testa busca simples no banco sem embeddings
    """
    try:
        session = rag.Session()

        result = session.execute(text("""
            SELECT content, category, chapter
            FROM eugene_knowledge
            WHERE content ILIKE '%consciousness%'
            LIMIT 3
        """))

        results = []
        for row in result:
            results.append({
                "content": row.content[:200] + "..." if len(row.content) > 200 else row.content,
                "category": row.category,
                "chapter": row.chapter
            })

        session.close()

        return {
            "total_found": len(results),
            "results": results,
            "success": True
        }

    except Exception as e:
        logger.error(f"Database test failed: {e}")
        return {
            "error": str(e),
            "success": False
        }

if __name__ == "__main__":
    # Run the API server
    uvicorn.run(
        "rag_api:app",
        host="0.0.0.0",
        port=int(os.getenv("RAG_API_PORT", 8000)),
        reload=True,
        log_level="info"
    )
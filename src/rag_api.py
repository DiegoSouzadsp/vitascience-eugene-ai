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

from src.rag_system import EugeneRAGSystem, RetrievalResult

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

# Global RAG system instance
rag_system: Optional[EugeneRAGSystem] = None

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

# Dependency to get RAG system
async def get_rag_system() -> EugeneRAGSystem:
    """Dependency para obter instância do sistema RAG"""
    global rag_system
    if rag_system is None:
        raise HTTPException(status_code=503, detail="RAG system not initialized")
    return rag_system

# API Routes

@app.on_event("startup")
async def startup_event():
    """Inicialização do sistema na startup"""
    global rag_system

    logger.info("Initializing Eugene Schwartz RAG System...")

    try:
        rag_system = EugeneRAGSystem()

        # Setup database
        setup_success = await rag_system.setup_database()
        if not setup_success:
            logger.error("Failed to setup database")
            return

        logger.info("RAG System initialized successfully")

    except Exception as e:
        logger.error(f"Failed to initialize RAG system: {e}")

@app.get("/health", response_model=HealthCheckResponse)
async def health_check(rag: EugeneRAGSystem = Depends(get_rag_system)):
    """
    Health check do sistema RAG
    """
    import time
    start_time = time.time()

    try:
        health_data = await rag.health_check()
        response_time = (time.time() - start_time) * 1000

        return HealthCheckResponse(
            status=health_data.get('status', 'unknown'),
            total_chunks=health_data.get('total_chunks', 0),
            category_distribution=health_data.get('category_distribution', {}),
            database_connection=health_data.get('database_connection', False),
            embedding_model=health_data.get('embedding_model', 'unknown'),
            response_time_ms=response_time
        )

    except Exception as e:
        logger.error(f"Health check failed: {e}")
        raise HTTPException(status_code=500, detail=f"Health check failed: {str(e)}")

@app.post("/retrieve/consciousness", response_model=List[RetrievalResponse])
async def retrieve_consciousness_context(
    request: ConsciousnessLevelRequest,
    rag: EugeneRAGSystem = Depends(get_rag_system)
):
    """
    Busca contexto específico para análise de níveis de consciência
    """
    try:
        results = await rag.get_consciousness_level_context(
            request.copy_text,
            request.consciousness_level
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
    rag: EugeneRAGSystem = Depends(get_rag_system)
):
    """
    Busca guidance sobre frameworks de copywriting
    """
    try:
        copy_type_query = f"{request.copy_type}"
        if request.industry:
            copy_type_query += f" {request.industry}"

        results = await rag.get_framework_guidance(copy_type_query)

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
    rag: EugeneRAGSystem = Depends(get_rag_system)
):
    """
    Busca técnicas específicas para melhorias identificadas
    """
    try:
        problem_query = request.problem_area
        if request.current_level:
            problem_query += f" consciousness level {request.current_level}"

        results = await rag.get_improvement_techniques(problem_query)

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
    rag: EugeneRAGSystem = Depends(get_rag_system)
):
    """
    Busca geral no conhecimento Eugene Schwartz
    """
    try:
        # For now, use consciousness context as general retrieval
        # Can be extended to include all categories
        results = await rag.get_consciousness_level_context(request.query)

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
    pdf_path: str = "docs/Breakthrough_Advertising_-_Eugene_Schwartz.pdf",
    rag: EugeneRAGSystem = Depends(get_rag_system)
):
    """
    Processa o livro Eugene Schwartz em background
    """
    try:
        if not os.path.exists(pdf_path):
            raise HTTPException(status_code=404, detail=f"PDF not found at: {pdf_path}")

        # Start processing in background
        background_tasks.add_task(rag.process_eugene_book, pdf_path)

        return ProcessingStatus(
            status="started",
            progress=0.0,
            message="Book processing started in background",
            estimated_completion="12-15 minutes"
        )

    except Exception as e:
        logger.error(f"Book processing initiation failed: {e}")
        raise HTTPException(status_code=500, detail=f"Processing failed: {str(e)}")

@app.get("/categories")
async def get_categories(rag: EugeneRAGSystem = Depends(get_rag_system)):
    """
    Retorna categorias disponíveis no sistema
    """
    return {
        "categories": rag.categories,
        "description": "Categorias baseadas na metodologia Eugene Schwartz"
    }

@app.get("/stats")
async def get_system_stats(rag: EugeneRAGSystem = Depends(get_rag_system)):
    """
    Estatísticas do sistema RAG
    """
    try:
        health_data = await rag.health_check()

        return {
            "total_chunks": health_data.get('total_chunks', 0),
            "category_distribution": health_data.get('category_distribution', {}),
            "configuration": {
                "chunk_size": rag.chunk_size,
                "chunk_overlap": rag.chunk_overlap,
                "embedding_model": rag.embedding_model
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

@app.get("/test/embeddings")
async def test_embeddings(
    text: str = "Test embedding generation",
    rag: EugeneRAGSystem = Depends(get_rag_system)
):
    """
    Testa geração de embeddings
    """
    try:
        embedding = await rag.generate_embedding(text)

        return {
            "text": text,
            "embedding_size": len(embedding) if embedding else 0,
            "embedding_preview": embedding[:5] if embedding else None,
            "success": embedding is not None
        }

    except Exception as e:
        logger.error(f"Embedding test failed: {e}")
        raise HTTPException(status_code=500, detail=f"Embedding test failed: {str(e)}")

if __name__ == "__main__":
    # Run the API server
    uvicorn.run(
        "rag_api:app",
        host="0.0.0.0",
        port=int(os.getenv("RAG_API_PORT", 8000)),
        reload=True,
        log_level="info"
    )
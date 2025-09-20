"""
FastAPI endpoints for RAG system integration
Provides RESTful API for Eugene Schwartz VSL analysis
"""

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
import logging
import asyncio
import time
from datetime import datetime

# Import our RAG system and prompt classes
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from rag_system import EugeneRAGSystem
from prompts.consciousness_classifier import ConsciousnessClassifier
from prompts.framework_analyzer import FrameworkAnalyzer
from prompts.problem_identifier import ProblemIdentifier
from prompts.improvement_generator import ImprovementGenerator

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# FastAPI app initialization
app = FastAPI(
    title="Eugene Schwartz VSL Analyzer API",
    description="RESTful API for VSL analysis using Eugene Schwartz methodology",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware for N8N integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global RAG system instance
rag_system = None
consciousness_classifier = None
framework_analyzer = None
problem_identifier = None
improvement_generator = None

# Pydantic models for API
class VSLAnalysisRequest(BaseModel):
    vsl_text: str = Field(..., description="The VSL text to analyze")
    analysis_type: str = Field("complete", description="Type of analysis: consciousness, framework, problems, improvements, or complete")
    include_context: bool = Field(True, description="Whether to include RAG context in analysis")

class HealthCheckResponse(BaseModel):
    status: str
    timestamp: str
    rag_system_status: Dict[str, Any]
    api_version: str

class ConsciousnessResponse(BaseModel):
    nivel_identificado: int
    confianca: float
    justificativa: str
    indicadores_textuais: List[str]
    nivel_ideal_sugerido: int
    razao_sugestao: str
    analysis_time_ms: float

class FrameworkResponse(BaseModel):
    framework_principal: str
    confianca_identificacao: float
    elementos_presentes: List[Dict[str, Any]]
    framework_secundarios: List[str]
    estrutura_completa: Dict[str, str]
    pontos_fortes_estruturais: List[str]
    pontos_fracos_estruturais: List[str]
    analysis_time_ms: float

class ProblemsResponse(BaseModel):
    problemas_identificados: List[Dict[str, Any]]
    problema_principal: str
    score_geral_copy: int
    analysis_time_ms: float

class ImprovementsResponse(BaseModel):
    melhorias_sugeridas: List[Dict[str, Any]]
    prioridade_implementacao: List[str]
    melhorias_quick_wins: List[str]
    analysis_time_ms: float

class CompleteAnalysisResponse(BaseModel):
    consciousness: ConsciousnessResponse
    framework: FrameworkResponse
    problems: ProblemsResponse
    improvements: ImprovementsResponse
    summary: Dict[str, Any]
    total_analysis_time_ms: float

# Startup event to initialize RAG system
@app.on_event("startup")
async def startup_event():
    """Initialize RAG system and analysis components"""
    global rag_system, consciousness_classifier, framework_analyzer, problem_identifier, improvement_generator

    try:
        logger.info("Initializing Eugene RAG System...")

        # Initialize RAG system
        rag_system = EugeneRAGSystem()
        setup_success = await rag_system.setup_database()

        if not setup_success:
            logger.error("Failed to setup RAG database")
            return

        # Initialize analysis components
        consciousness_classifier = ConsciousnessClassifier(rag_system)
        framework_analyzer = FrameworkAnalyzer(rag_system)
        problem_identifier = ProblemIdentifier(rag_system)
        improvement_generator = ImprovementGenerator(rag_system)

        logger.info("Eugene RAG API initialized successfully")

    except Exception as e:
        logger.error(f"Failed to initialize RAG system: {e}")

# Health check endpoint
@app.get("/health", response_model=HealthCheckResponse)
async def health_check():
    """Check system health and RAG status"""
    try:
        rag_health = await rag_system.health_check() if rag_system else {"status": "not_initialized"}

        return HealthCheckResponse(
            status="healthy" if rag_system else "unhealthy",
            timestamp=datetime.now().isoformat(),
            rag_system_status=rag_health,
            api_version="1.0.0"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Health check failed: {str(e)}")

# RAG search endpoint
@app.post("/rag/search")
async def search_rag(
    query: str = Field(..., description="Search query"),
    category: Optional[str] = Field(None, description="Filter by category"),
    max_results: int = Field(5, description="Maximum number of results")
):
    """Search RAG knowledge base"""
    try:
        if not rag_system:
            raise HTTPException(status_code=503, detail="RAG system not initialized")

        start_time = time.time()

        # Route to appropriate search method based on category
        if category == "consciousness":
            results = await rag_system.get_consciousness_level_context(query)
        elif category == "frameworks":
            results = await rag_system.get_framework_guidance(query)
        elif category == "techniques":
            results = await rag_system.get_improvement_techniques(query)
        else:
            # Generic search - combine all categories
            results = await rag_system.get_consciousness_level_context(query)

        response_time = (time.time() - start_time) * 1000

        return {
            "query": query,
            "results": [
                {
                    "content": r.content,
                    "similarity_score": r.similarity_score,
                    "category": r.category,
                    "chapter": r.chapter,
                    "metadata": r.metadata
                } for r in results[:max_results]
            ],
            "response_time_ms": response_time,
            "total_results": len(results)
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")

# Consciousness analysis endpoint
@app.post("/analyze/consciousness", response_model=ConsciousnessResponse)
async def analyze_consciousness(request: VSLAnalysisRequest):
    """Analyze consciousness level of VSL"""
    try:
        if not consciousness_classifier:
            raise HTTPException(status_code=503, detail="Consciousness classifier not initialized")

        start_time = time.time()
        result = consciousness_classifier.classify_consciousness_level(request.vsl_text)
        analysis_time = (time.time() - start_time) * 1000

        return ConsciousnessResponse(
            nivel_identificado=result.nivel_identificado,
            confianca=result.confianca,
            justificativa=result.justificativa,
            indicadores_textuais=result.indicadores_textuais,
            nivel_ideal_sugerido=result.nivel_ideal_sugerido,
            razao_sugestao=result.razao_sugestao,
            analysis_time_ms=analysis_time
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Consciousness analysis failed: {str(e)}")

# Framework analysis endpoint
@app.post("/analyze/framework", response_model=FrameworkResponse)
async def analyze_framework(request: VSLAnalysisRequest):
    """Analyze framework structure of VSL"""
    try:
        if not framework_analyzer:
            raise HTTPException(status_code=503, detail="Framework analyzer not initialized")

        start_time = time.time()
        result = framework_analyzer.analyze_framework(request.vsl_text)
        analysis_time = (time.time() - start_time) * 1000

        return FrameworkResponse(
            framework_principal=result.framework_principal,
            confianca_identificacao=result.confianca_identificacao,
            elementos_presentes=[
                {
                    "elemento": elem.elemento,
                    "presente": elem.presente,
                    "qualidade": elem.qualidade,
                    "localizacao": elem.localizacao
                } for elem in result.elementos_presentes
            ],
            framework_secundarios=result.framework_secundarios,
            estrutura_completa=result.estrutura_completa,
            pontos_fortes_estruturais=result.pontos_fortes_estruturais,
            pontos_fracos_estruturais=result.pontos_fracos_estruturais,
            analysis_time_ms=analysis_time
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Framework analysis failed: {str(e)}")

# Problem identification endpoint
@app.post("/analyze/problems", response_model=ProblemsResponse)
async def analyze_problems(request: VSLAnalysisRequest):
    """Identify problems in VSL"""
    try:
        if not problem_identifier:
            raise HTTPException(status_code=503, detail="Problem identifier not initialized")

        start_time = time.time()
        result = problem_identifier.identify_problems(request.vsl_text)
        analysis_time = (time.time() - start_time) * 1000

        return ProblemsResponse(
            problemas_identificados=[
                {
                    "problema": prob.problema,
                    "categoria": prob.categoria,
                    "severidade": prob.severidade,
                    "localizacao": prob.localizacao,
                    "por_que_problema": prob.por_que_problema,
                    "impacto_conversao": prob.impacto_conversao
                } for prob in result.problemas_identificados
            ],
            problema_principal=result.problema_principal,
            score_geral_copy=result.score_geral_copy,
            analysis_time_ms=analysis_time
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Problem analysis failed: {str(e)}")

# Complete analysis endpoint
@app.post("/analyze/complete", response_model=CompleteAnalysisResponse)
async def analyze_complete(request: VSLAnalysisRequest):
    """Complete VSL analysis with all components"""
    try:
        total_start_time = time.time()

        # Run all analyses in parallel for speed
        consciousness_task = analyze_consciousness(request)
        framework_task = analyze_framework(request)
        problems_task = analyze_problems(request)

        # Wait for all analyses to complete
        consciousness_result = await consciousness_task
        framework_result = await framework_task
        problems_result = await problems_task

        # Generate improvements based on identified problems
        problems_text = "\n".join([
            f"{i+1}. {prob['problema']}"
            for i, prob in enumerate(problems_result.problemas_identificados)
        ])

        improvements_start = time.time()
        improvements_result = improvement_generator.generate_improvements(problems_text, request.vsl_text)
        improvements_time = (time.time() - improvements_start) * 1000

        improvements_response = ImprovementsResponse(
            melhorias_sugeridas=[
                {
                    "problema_resolvido": imp.problema_resolvido,
                    "melhoria": imp.melhoria,
                    "metodologia_eugene": imp.metodologia_eugene,
                    "implementacao": imp.implementacao,
                    "exemplo_reescrito": imp.exemplo_reescrito,
                    "impacto_esperado": imp.impacto_esperado
                } for imp in improvements_result.melhorias_sugeridas
            ],
            prioridade_implementacao=improvements_result.prioridade_implementacao,
            melhorias_quick_wins=improvements_result.melhorias_quick_wins,
            analysis_time_ms=improvements_time
        )

        total_time = (time.time() - total_start_time) * 1000

        # Create summary
        summary = {
            "consciousness_level": consciousness_result.nivel_identificado,
            "framework_used": framework_result.framework_principal,
            "problems_count": len(problems_result.problemas_identificados),
            "overall_score": problems_result.score_geral_copy,
            "top_priority_improvement": improvements_response.prioridade_implementacao[0] if improvements_response.prioridade_implementacao else None,
            "analysis_timestamp": datetime.now().isoformat()
        }

        return CompleteAnalysisResponse(
            consciousness=consciousness_result,
            framework=framework_result,
            problems=problems_result,
            improvements=improvements_response,
            summary=summary,
            total_analysis_time_ms=total_time
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Complete analysis failed: {str(e)}")

# Export analysis endpoint for N8N integration
@app.post("/export/analysis")
async def export_analysis(request: VSLAnalysisRequest, format: str = "json"):
    """Export complete analysis in specified format for N8N workflows"""
    try:
        # Get complete analysis
        complete_result = await analyze_complete(request)

        if format.lower() == "json":
            return complete_result
        else:
            # Could add other formats like CSV, PDF etc.
            raise HTTPException(status_code=400, detail=f"Format {format} not supported")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Export failed: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "rag_endpoints:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
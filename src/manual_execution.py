"""
Manual Execution Script for Eugene Schwartz Analysis
Fallback system when N8N workflow is not available
"""

import os
import json
import time
import logging
import asyncio
from typing import Dict, Any, Optional
from pathlib import Path

from rag_system import EugeneRAGSystem
from prompt_system import EugenePromptSystem

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ManualEugeneAnalyzer:
    """
    Sistema manual de análise Eugene Schwartz
    Replica a funcionalidade do workflow N8N
    """

    def __init__(self):
        self.rag_system = EugeneRAGSystem()
        self.prompt_system = None
        self.initialized = False

    async def initialize(self):
        """Inicializa os sistemas RAG e Prompt"""
        logger.info("Initializing manual analyzer systems...")

        # Setup RAG system
        setup_success = await self.rag_system.setup_database()
        if not setup_success:
            raise Exception("Failed to setup RAG system")

        # Setup prompt system
        self.prompt_system = EugenePromptSystem(self.rag_system)

        self.initialized = True
        logger.info("Manual analyzer systems initialized successfully")

    def validate_input(self, vsl_text: str) -> Dict[str, Any]:
        """Valida entrada similar ao nó de validação do N8N"""
        if not vsl_text:
            raise ValueError("VSL text is required")

        if not isinstance(vsl_text, str):
            raise ValueError("VSL text must be a string")

        if len(vsl_text) < 100:
            raise ValueError("VSL text must be at least 100 characters")

        if len(vsl_text) > 50000:
            raise ValueError("VSL text is too long (max 50,000 characters)")

        return {
            "vsl_text": vsl_text.strip(),
            "analysis_id": str(int(time.time())),
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
            "word_count": len(vsl_text.split()),
            "char_count": len(vsl_text)
        }

    async def get_rag_context(self, vsl_text: str) -> Dict[str, Any]:
        """Recupera contexto RAG similar ao nó N8N"""
        try:
            # Get consciousness context
            consciousness_results = await self.rag_system.get_consciousness_level_context(vsl_text)

            # Get framework guidance
            framework_results = await self.rag_system.get_framework_guidance("sales copy analysis")

            # Get improvement techniques
            improvement_results = await self.rag_system.get_improvement_techniques("copywriting analysis")

            # Combine contexts
            all_contexts = consciousness_results + framework_results + improvement_results

            # Format context for prompts
            context_text = "\n\n".join([
                f"CONTEXT {i+1}: {result.content[:500]}..."
                for i, result in enumerate(all_contexts[:5])
            ])

            return {
                "context": context_text,
                "sources_count": len(all_contexts),
                "retrieval_successful": True
            }

        except Exception as e:
            logger.error(f"RAG context retrieval failed: {e}")
            return {
                "context": "No context available - proceeding with base methodology.",
                "sources_count": 0,
                "retrieval_successful": False,
                "error": str(e)
            }

    async def analyze_consciousness_level(self, vsl_text: str, context: str) -> Dict[str, Any]:
        """Análise de nível de consciência"""
        try:
            result = await self.prompt_system.execute_prompt('consciousness', vsl_text)

            if result.get('success'):
                return {
                    "success": True,
                    "analysis": result['result'],
                    "execution_time": time.time()
                }
            else:
                return {
                    "success": False,
                    "error": result.get('error'),
                    "fallback_analysis": {
                        "nivel_identificado": 3,  # Default to level 3
                        "confianca": 0.5,
                        "justificativa": "Analysis failed - using default level 3 (solution-aware)",
                        "indicadores_textuais": ["Unable to analyze - system error"],
                        "nivel_ideal_sugerido": 3,
                        "razao_sugestao": "Default suggestion due to analysis failure"
                    }
                }

        except Exception as e:
            logger.error(f"Consciousness analysis failed: {e}")
            return {
                "success": False,
                "error": str(e),
                "fallback_analysis": {
                    "nivel_identificado": 3,
                    "confianca": 0.0,
                    "justificativa": f"Analysis failed due to error: {e}",
                    "indicadores_textuais": ["System error prevented analysis"],
                    "nivel_ideal_sugerido": 3,
                    "razao_sugestao": "Default due to system error"
                }
            }

    async def analyze_framework_structure(self, vsl_text: str, context: str) -> Dict[str, Any]:
        """Análise de estrutura do framework"""
        try:
            result = await self.prompt_system.execute_prompt('framework', vsl_text)

            if result.get('success'):
                return {
                    "success": True,
                    "analysis": result['result']
                }
            else:
                return {
                    "success": False,
                    "error": result.get('error'),
                    "fallback_analysis": {
                        "framework_principal": "Estrutura Indefinida",
                        "confianca_identificacao": 0.0,
                        "elementos_presentes": [],
                        "pontos_fortes_estruturais": [],
                        "pontos_fracos_estruturais": ["Unable to analyze structure due to system error"]
                    }
                }

        except Exception as e:
            logger.error(f"Framework analysis failed: {e}")
            return {
                "success": False,
                "error": str(e),
                "fallback_analysis": {
                    "framework_principal": "Error",
                    "confianca_identificacao": 0.0,
                    "elementos_presentes": [],
                    "pontos_fortes_estruturais": [],
                    "pontos_fracos_estruturais": [f"Analysis error: {e}"]
                }
            }

    async def identify_problems(self, vsl_text: str, context: str) -> Dict[str, Any]:
        """Identificação de problemas"""
        try:
            result = await self.prompt_system.execute_prompt('problems', vsl_text)

            if result.get('success'):
                return {
                    "success": True,
                    "analysis": result['result']
                }
            else:
                return {
                    "success": False,
                    "error": result.get('error'),
                    "fallback_analysis": {
                        "problemas_identificados": [
                            {
                                "problema": "Unable to analyze - system error",
                                "categoria": "System Error",
                                "severidade": 10,
                                "localizacao": "System level",
                                "por_que_problema": "Analysis system failed",
                                "impacto_conversao": "Cannot determine impact due to analysis failure"
                            }
                        ],
                        "problema_principal": "System analysis failure",
                        "score_geral_copy": 5
                    }
                }

        except Exception as e:
            logger.error(f"Problem identification failed: {e}")
            return {
                "success": False,
                "error": str(e),
                "fallback_analysis": {
                    "problemas_identificados": [
                        {
                            "problema": f"Analysis error: {e}",
                            "categoria": "System Error",
                            "severidade": 10,
                            "localizacao": "System level",
                            "por_que_problema": "Exception during analysis",
                            "impacto_conversao": "Cannot determine"
                        }
                    ],
                    "problema_principal": f"System error: {e}",
                    "score_geral_copy": 1
                }
            }

    async def generate_improvements(self, vsl_text: str, context: str, problems: Dict[str, Any]) -> Dict[str, Any]:
        """Geração de melhorias"""
        try:
            additional_context = {
                'problems_context': json.dumps(problems, indent=2)
            }

            result = await self.prompt_system.execute_prompt('improvements', vsl_text, additional_context)

            if result.get('success'):
                return {
                    "success": True,
                    "analysis": result['result']
                }
            else:
                return {
                    "success": False,
                    "error": result.get('error'),
                    "fallback_analysis": {
                        "melhorias_sugeridas": [
                            {
                                "problema_resolvido": "System analysis failure",
                                "melhoria": "Manual review required",
                                "metodologia_eugene": "Human expertise needed",
                                "implementacao": "Have expert copywriter review manually",
                                "exemplo_reescrito": "Manual rewrite required",
                                "impacto_esperado": "Cannot predict due to analysis failure"
                            }
                        ],
                        "prioridade_implementacao": ["Manual expert review"],
                        "melhorias_quick_wins": ["Get human expert analysis"]
                    }
                }

        except Exception as e:
            logger.error(f"Improvement generation failed: {e}")
            return {
                "success": False,
                "error": str(e),
                "fallback_analysis": {
                    "melhorias_sugeridas": [
                        {
                            "problema_resolvido": f"System error: {e}",
                            "melhoria": "Fix system error",
                            "metodologia_eugene": "System maintenance",
                            "implementacao": "Debug and fix system issues",
                            "exemplo_reescrito": "System repair needed",
                            "impacto_esperado": "Restore analysis capability"
                        }
                    ],
                    "prioridade_implementacao": ["Fix system errors"],
                    "melhorias_quick_wins": ["Restart system"]
                }
            }

    async def generate_creative_angles(self, vsl_text: str, context: str, consciousness_level: int) -> Dict[str, Any]:
        """Geração de ângulos criativos"""
        try:
            additional_context = {
                'consciousness_level': consciousness_level
            }

            result = await self.prompt_system.execute_prompt('angles', vsl_text, additional_context)

            if result.get('success'):
                return {
                    "success": True,
                    "analysis": result['result']
                }
            else:
                return {
                    "success": False,
                    "error": result.get('error'),
                    "fallback_analysis": {
                        "novos_angulos": [
                            {
                                "nivel_consciencia_alvo": consciousness_level,
                                "nome_angulo": "Manual Analysis Required",
                                "abordagem": "Human expert review needed",
                                "headline_sugerida": "Expert Analysis Needed",
                                "primeiro_paragrafo": "This copy requires manual expert analysis due to system limitations.",
                                "diferencial": "Human expertise",
                                "metodologia_eugene": "Manual application of principles",
                                "publico_ideal": "Requires expert determination"
                            }
                        ],
                        "angulo_recomendado": "Manual expert analysis",
                        "justificativa_recomendacao": "System analysis failed, human expertise required"
                    }
                }

        except Exception as e:
            logger.error(f"Creative angles generation failed: {e}")
            return {
                "success": False,
                "error": str(e),
                "fallback_analysis": {
                    "novos_angulos": [
                        {
                            "nivel_consciencia_alvo": consciousness_level,
                            "nome_angulo": f"System Error: {e}",
                            "abordagem": "Error handling required",
                            "headline_sugerida": "System Error",
                            "primeiro_paragrafo": f"Analysis failed: {e}",
                            "diferencial": "Error state",
                            "metodologia_eugene": "Error recovery",
                            "publico_ideal": "System administrators"
                        }
                    ],
                    "angulo_recomendado": "Fix system error",
                    "justificativa_recomendacao": f"System error prevents analysis: {e}"
                }
            }

    def consolidate_results(self, input_data: Dict[str, Any], consciousness: Dict[str, Any],
                          framework: Dict[str, Any], problems: Dict[str, Any],
                          improvements: Dict[str, Any], angles: Dict[str, Any]) -> Dict[str, Any]:
        """Consolida todos os resultados similar ao nó N8N"""

        # Extract analysis data (use fallback if analysis failed)
        consciousness_data = consciousness.get('analysis') or consciousness.get('fallback_analysis', {})
        framework_data = framework.get('analysis') or framework.get('fallback_analysis', {})
        problems_data = problems.get('analysis') or problems.get('fallback_analysis', {})
        improvements_data = improvements.get('analysis') or improvements.get('fallback_analysis', {})
        angles_data = angles.get('analysis') or angles.get('fallback_analysis', {})

        # Calculate processing time
        processing_time = time.time() - int(input_data['analysis_id'])

        # Build consolidated result
        consolidated_result = {
            "meta": {
                "analysis_id": input_data['analysis_id'],
                "timestamp": input_data['timestamp'],
                "vsl_stats": {
                    "word_count": input_data['word_count'],
                    "char_count": input_data['char_count']
                },
                "processing_time": round(processing_time, 2),
                "execution_mode": "manual",
                "analysis_success": {
                    "consciousness": consciousness.get('success', False),
                    "framework": framework.get('success', False),
                    "problems": problems.get('success', False),
                    "improvements": improvements.get('success', False),
                    "angles": angles.get('success', False)
                }
            },
            "analise_consciencia": consciousness_data,
            "estrutura_copy": framework_data,
            "problemas_identificados": problems_data,
            "melhorias_sugeridas": improvements_data,
            "novos_angulos": angles_data,
            "resumo_executivo": {
                "nivel_consciencia": consciousness_data.get('nivel_identificado', 'N/A'),
                "framework_principal": framework_data.get('framework_principal', 'N/A'),
                "total_problemas": len(problems_data.get('problemas_identificados', [])),
                "score_copy": problems_data.get('score_geral_copy', 'N/A'),
                "total_melhorias": len(improvements_data.get('melhorias_sugeridas', [])),
                "total_angulos": len(angles_data.get('novos_angulos', [])),
                "analysis_quality": "partial" if any(not success for success in [
                    consciousness.get('success', False),
                    framework.get('success', False),
                    problems.get('success', False),
                    improvements.get('success', False),
                    angles.get('success', False)
                ]) else "complete"
            }
        }

        return consolidated_result

    async def analyze_vsl_manual(self, vsl_text: str) -> Dict[str, Any]:
        """
        Análise completa manual de VSL
        Replica todo o workflow N8N
        """
        if not self.initialized:
            await self.initialize()

        logger.info("Starting manual VSL analysis...")

        try:
            # Step 1: Input validation
            input_data = self.validate_input(vsl_text)
            logger.info("✅ Input validation completed")

            # Step 2: RAG context retrieval
            rag_context = await self.get_rag_context(vsl_text)
            logger.info("✅ RAG context retrieval completed")

            # Step 3: Consciousness analysis
            consciousness_result = await self.analyze_consciousness_level(vsl_text, rag_context['context'])
            logger.info("✅ Consciousness analysis completed")

            # Step 4: Framework analysis
            framework_result = await self.analyze_framework_structure(vsl_text, rag_context['context'])
            logger.info("✅ Framework analysis completed")

            # Step 5: Problem identification
            problems_result = await self.identify_problems(vsl_text, rag_context['context'])
            logger.info("✅ Problem identification completed")

            # Step 6: Improvement generation
            problems_data = problems_result.get('analysis') or problems_result.get('fallback_analysis', {})
            improvements_result = await self.generate_improvements(vsl_text, rag_context['context'], problems_data)
            logger.info("✅ Improvement generation completed")

            # Step 7: Creative angles generation
            consciousness_data = consciousness_result.get('analysis') or consciousness_result.get('fallback_analysis', {})
            consciousness_level = consciousness_data.get('nivel_identificado', 3)
            angles_result = await self.generate_creative_angles(vsl_text, rag_context['context'], consciousness_level)
            logger.info("✅ Creative angles generation completed")

            # Step 8: Consolidate results
            final_result = self.consolidate_results(
                input_data, consciousness_result, framework_result,
                problems_result, improvements_result, angles_result
            )
            logger.info("✅ Results consolidation completed")

            logger.info("Manual VSL analysis completed successfully")
            return final_result

        except Exception as e:
            logger.error(f"Manual analysis failed: {e}")
            return {
                "error": str(e),
                "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
                "execution_mode": "manual",
                "status": "failed"
            }

# Utility functions

def save_analysis_result(result: Dict[str, Any], output_file: str = None) -> str:
    """Salva resultado da análise em arquivo"""
    if not output_file:
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        output_file = f"manual_analysis_{timestamp}.json"

    output_path = Path("outputs") / output_file
    output_path.parent.mkdir(exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    return str(output_path)

async def analyze_vsl_from_file(file_path: str) -> Dict[str, Any]:
    """Analisa VSL a partir de arquivo de texto"""
    with open(file_path, "r", encoding="utf-8") as f:
        vsl_text = f.read()

    analyzer = ManualEugeneAnalyzer()
    return await analyzer.analyze_vsl_manual(vsl_text)

async def main():
    """Função principal para execução manual"""
    print("="*60)
    print("MANUAL EUGENE SCHWARTZ VSL ANALYZER")
    print("="*60)

    # Sample VSL for testing
    sample_vsl = """
    Descoberta Revolucionária: Como Perder 7kg em 21 Dias

    Se você está lutando para perder peso e já tentou de tudo...

    Dietas restritivas que deixam você com fome...
    Exercícios intensos que consomem horas do seu dia...
    Suplementos caros que prometem milagres mas não entregam resultados...

    Então você precisa conhecer esta descoberta revolucionária que está mudando a vida de milhares de brasileiros.

    Um método simples, natural e cientificamente comprovado que permite perder até 7kg em apenas 21 dias, sem dietas malucas, sem exercícios extenuantes e sem abrir mão dos alimentos que você ama.

    Dr. João Silva, endocrinologista há 20 anos, descobriu um protocolo único que acelera o metabolismo naturalmente...
    """

    try:
        # Initialize analyzer
        analyzer = ManualEugeneAnalyzer()
        print("Initializing analyzer...")

        # Run analysis
        print("Starting analysis...")
        start_time = time.time()

        result = await analyzer.analyze_vsl_manual(sample_vsl)

        execution_time = time.time() - start_time

        # Print results
        if 'error' not in result:
            print(f"\n✅ Analysis completed in {execution_time:.2f} seconds")

            # Show summary
            summary = result.get('resumo_executivo', {})
            print(f"\nExecutive Summary:")
            print(f"  Consciousness Level: {summary.get('nivel_consciencia')}")
            print(f"  Framework: {summary.get('framework_principal')}")
            print(f"  Problems Found: {summary.get('total_problemas')}")
            print(f"  Copy Score: {summary.get('score_copy')}")
            print(f"  Improvements: {summary.get('total_melhorias')}")
            print(f"  Creative Angles: {summary.get('total_angulos')}")
            print(f"  Analysis Quality: {summary.get('analysis_quality')}")

            # Save result
            output_file = save_analysis_result(result)
            print(f"\nResults saved to: {output_file}")

        else:
            print(f"\n❌ Analysis failed: {result['error']}")

    except Exception as e:
        print(f"\n❌ Execution failed: {e}")

if __name__ == "__main__":
    asyncio.run(main())
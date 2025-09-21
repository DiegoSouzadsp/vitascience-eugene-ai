#!/usr/bin/env python3
"""
N8N Workflow Generator for Eugene Schwartz VSL Analyzer
Implements complete workflow via N8N API with Squad Vitascience requirements
"""

import os
import json
import requests
import time
from typing import Dict, List, Any
from datetime import datetime

class N8NWorkflowGenerator:
    """Generates and manages N8N workflows via API"""

    def __init__(self, n8n_url: str = None, api_key: str = None):
        # Remote N8N configuration for Squad deployment
        self.base_url = n8n_url or os.getenv('N8N_BASE_URL', 'http://localhost:5678')
        self.api_key = api_key or os.getenv('N8N_API_KEY')
        self.session = requests.Session()

        # Configure API authentication
        if self.api_key:
            self.session.headers.update({
                "X-N8N-API-KEY": self.api_key,
                "Content-Type": "application/json"
            })
        else:
            # Use basic auth for local development
            self.session.auth = ('admin', 'password')

    def create_eugene_workflow(self) -> Dict:
        """Creates complete Eugene Schwartz VSL analysis workflow"""
        print("Creating Eugene Schwartz N8N Workflow...")

        workflow_data = {
            "name": "Eugene Schwartz VSL Analyzer - Squad Vitascience",
            "nodes": self._generate_nodes(),
            "connections": self._generate_connections(),
            "active": True,
            "settings": {
                "executionOrder": "sequential",
                "saveManualExecutions": True,
                "timezone": "America/Sao_Paulo"
            },
            "tags": ["eugene-schwartz", "vsl-analysis", "squad-vitascience"]
        }

        try:
            response = self.session.post(
                f"{self.base_url}/api/v1/workflows",
                json=workflow_data
            )
            response.raise_for_status()

            result = response.json()
            print(f"SUCCESSFUL: Workflow created successfully: {result.get('id')}")
            return {"success": True, "workflow": result}

        except requests.exceptions.RequestException as e:
            print(f"ERROR: Failed to create workflow: {e}")
            return {"success": False, "error": str(e)}

    def _generate_nodes(self) -> List[Dict]:
        """Generates all necessary nodes for the workflow"""
        return [
            # Node 1: Input Webhook
            {
                "id": "webhook-input",
                "name": "VSL Input Webhook",
                "type": "n8n-nodes-base.webhook",
                "position": [20, 300],
                "parameters": {
                    "httpMethod": "POST",
                    "path": "analyze-vsl",
                    "responseMode": "responseNode",
                    "options": {}
                },
                "webhookId": "eugene-vsl-input"
            },

            # Node 2: Input Validation & Preprocessing
            {
                "id": "input-validation",
                "name": "Input Validation & Preprocessing",
                "type": "n8n-nodes-base.function",
                "position": [240, 300],
                "parameters": {
                    "functionCode": """
                        // Validate and preprocess VSL input
                        const vslText = items[0].json.vsl_text || items[0].json.text;
                        const analysisType = items[0].json.analysis_type || 'complete';

                        if (!vslText || vslText.length < 100) {
                            throw new Error('VSL text deve ter pelo menos 100 caracteres');
                        }

                        return [{
                            json: {
                                vsl_text: vslText.trim(),
                                analysis_type: analysisType,
                                analysis_id: `vsl_${Date.now()}`,
                                timestamp: new Date().toISOString(),
                                word_count: vslText.split(' ').length,
                                client: 'squad-vitascience'
                            }
                        }];
                    """
                }
            },

            # Node 3: RAG Context Retrieval
            {
                "id": "rag-retrieval",
                "name": "RAG Context Retrieval",
                "type": "n8n-nodes-base.httpRequest",
                "position": [460, 300],
                "parameters": {
                    "url": "http://localhost:8000/rag/search",
                    "method": "POST",
                    "sendBody": True,
                    "bodyParameters": {
                        "parameters": {
                            "query": "={{$json.vsl_text}}",
                            "categories": ["consciousness_levels", "frameworks", "techniques"],
                            "max_results": 5,
                            "min_relevance": 0.7
                        }
                    },
                    "options": {
                        "timeout": 10000
                    }
                }
            },

            # Node 4: Consciousness Level Analysis
            {
                "id": "consciousness-analysis",
                "name": "Consciousness Level Analysis",
                "type": "n8n-nodes-base.anthropic",
                "position": [680, 200],
                "parameters": {
                    "model": "claude-3-5-sonnet-20241022",
                    "maxTokens": 2000,
                    "temperature": 0.1,
                    "messages": [
                        {
                            "role": "user",
                            "content": self._load_consciousness_prompt()
                        }
                    ]
                }
            },

            # Node 5: Structure Analysis
            {
                "id": "structure-analysis",
                "name": "VSL Structure Analysis",
                "type": "n8n-nodes-base.anthropic",
                "position": [680, 400],
                "parameters": {
                    "model": "claude-3-5-sonnet-20241022",
                    "maxTokens": 2000,
                    "temperature": 0.1,
                    "messages": [
                        {
                            "role": "user",
                            "content": self._load_structure_prompt()
                        }
                    ]
                }
            },

            # Node 6: Problem Identification
            {
                "id": "problem-identification",
                "name": "Problem Identification",
                "type": "n8n-nodes-base.anthropic",
                "position": [680, 600],
                "parameters": {
                    "model": "claude-3-5-sonnet-20241022",
                    "maxTokens": 2000,
                    "temperature": 0.1,
                    "messages": [
                        {
                            "role": "user",
                            "content": self._load_problem_prompt()
                        }
                    ]
                }
            },

            # Node 7: Improvement Generation
            {
                "id": "improvement-generation",
                "name": "Improvement Generation",
                "type": "n8n-nodes-base.anthropic",
                "position": [900, 300],
                "parameters": {
                    "model": "claude-3-5-sonnet-20241022",
                    "maxTokens": 2500,
                    "temperature": 0.2,
                    "messages": [
                        {
                            "role": "user",
                            "content": self._load_improvement_prompt()
                        }
                    ]
                }
            },

            # Node 8: Creative Angles Generation
            {
                "id": "creative-angles",
                "name": "Creative Angles Generation",
                "type": "n8n-nodes-base.anthropic",
                "position": [900, 500],
                "parameters": {
                    "model": "claude-3-5-sonnet-20241022",
                    "maxTokens": 2000,
                    "temperature": 0.3,
                    "messages": [
                        {
                            "role": "user",
                            "content": self._load_creative_prompt()
                        }
                    ]
                }
            },

            # Node 9: Results Consolidation
            {
                "id": "results-consolidation",
                "name": "Results Consolidation",
                "type": "n8n-nodes-base.function",
                "position": [1120, 400],
                "parameters": {
                    "functionCode": """
                        // Consolidate all analysis results into final JSON
                        const inputData = $node['Input Validation & Preprocessing'].json;
                        const consciousness = $node['Consciousness Level Analysis'].json;
                        const structure = $node['VSL Structure Analysis'].json;
                        const problems = $node['Problem Identification'].json;
                        const improvements = $node['Improvement Generation'].json;
                        const angles = $node['Creative Angles Generation'].json;

                        const consolidatedResult = {
                            metadata: {
                                analysis_id: inputData.analysis_id,
                                timestamp: inputData.timestamp,
                                client: inputData.client,
                                word_count: inputData.word_count,
                                processing_time: new Date().toISOString()
                            },
                            analise_consciencia: consciousness,
                            estrutura_copy: structure,
                            problemas_identificados: problems,
                            melhorias_sugeridas: improvements,
                            novos_angulos_criativos: angles,
                            score_qualidade: this.calculateQualityScore(consciousness, structure, problems),
                            recomendacoes_execucao: this.generateExecutionRecommendations(improvements, angles)
                        };

                        return [{ json: consolidatedResult }];
                    """
                }
            },

            # Node 10: Response Webhook
            {
                "id": "response-webhook",
                "name": "Analysis Response",
                "type": "n8n-nodes-base.respondToWebhook",
                "position": [1340, 400],
                "parameters": {
                    "respondWith": "json",
                    "responseBody": "={{$json}}",
                    "options": {
                        "responseHeaders": {
                            "Content-Type": "application/json",
                            "Access-Control-Allow-Origin": "*"
                        }
                    }
                }
            }
        ]

    def _generate_connections(self) -> Dict:
        """Generates connections between workflow nodes"""
        return {
            "webhook-input": {
                "main": [
                    [{"node": "input-validation", "type": "main", "index": 0}]
                ]
            },
            "input-validation": {
                "main": [
                    [{"node": "rag-retrieval", "type": "main", "index": 0}]
                ]
            },
            "rag-retrieval": {
                "main": [
                    [
                        {"node": "consciousness-analysis", "type": "main", "index": 0},
                        {"node": "structure-analysis", "type": "main", "index": 0},
                        {"node": "problem-identification", "type": "main", "index": 0}
                    ]
                ]
            },
            "consciousness-analysis": {
                "main": [
                    [{"node": "improvement-generation", "type": "main", "index": 0}]
                ]
            },
            "structure-analysis": {
                "main": [
                    [{"node": "improvement-generation", "type": "main", "index": 0}]
                ]
            },
            "problem-identification": {
                "main": [
                    [{"node": "creative-angles", "type": "main", "index": 0}]
                ]
            },
            "improvement-generation": {
                "main": [
                    [{"node": "results-consolidation", "type": "main", "index": 0}]
                ]
            },
            "creative-angles": {
                "main": [
                    [{"node": "results-consolidation", "type": "main", "index": 0}]
                ]
            },
            "results-consolidation": {
                "main": [
                    [{"node": "response-webhook", "type": "main", "index": 0}]
                ]
            }
        }

    def _load_consciousness_prompt(self) -> str:
        """Load consciousness analysis prompt"""
        return """
        Como especialista na metodologia de Eugene Schwartz, analise o seguinte VSL e identifique:

        1. NÍVEL DE CONSCIÊNCIA DOMINANTE (1-5):
        - Nível 1: Completamente inconsciente do problema
        - Nível 2: Consciente do problema, inconsciente da solução
        - Nível 3: Consciente do problema e da solução, mas não do produto
        - Nível 4: Consciente do problema, solução e produto, mas não da empresa
        - Nível 5: Totalmente consciente de tudo

        2. ESTRATÉGIAS IDENTIFICADAS:
        - Como o copy trabalha cada nível
        - Transições entre níveis
        - Pontos de conversão principais

        VSL Text: {{$node['Input Validation & Preprocessing'].json.vsl_text}}
        RAG Context: {{$node['RAG Context Retrieval'].json.context}}

        Forneça sua análise em formato JSON estruturado.
        """

    def _load_structure_prompt(self) -> str:
        """Load structure analysis prompt"""
        return """
        Analise a estrutura do VSL seguindo a metodologia Eugene Schwartz:

        1. ELEMENTOS ESTRUTURAIS:
        - Headline/Hook de abertura
        - Apresentação do problema
        - Agitação (agitation)
        - Apresentação da solução
        - Prova social/autoridade
        - Oferta e call-to-action
        - Urgência/escassez

        2. FLUXO NARRATIVO:
        - Sequência lógica
        - Pontos de tensão
        - Momentos de alívio
        - Construção de autoridade

        VSL Text: {{$node['Input Validation & Preprocessing'].json.vsl_text}}

        Retorne análise estruturada em JSON.
        """

    def _load_problem_prompt(self) -> str:
        """Load problem identification prompt"""
        return """
        Identifique problemas específicos no VSL baseado na metodologia Eugene Schwartz:

        1. PROBLEMAS DE CONSCIÊNCIA:
        - Mismatch entre nível de consciência e abordagem
        - Falta de educação adequada
        - Saltos de consciência muito bruscos

        2. PROBLEMAS ESTRUTURAIS:
        - Elementos faltantes ou mal posicionados
        - Fluxo narrativo quebrado
        - Falta de prova social

        3. PROBLEMAS DE COPY:
        - Linguagem inadequada para o público
        - Falta de especificidade
        - CTA fraco

        VSL Text: {{$node['Input Validation & Preprocessing'].json.vsl_text}}

        Forneça lista detalhada de problemas em JSON.
        """

    def _load_improvement_prompt(self) -> str:
        """Load improvement generation prompt"""
        return """
        Com base na análise de consciência, estrutura e problemas identificados, gere melhorias específicas:

        1. MELHORIAS DE CONSCIÊNCIA:
        - Ajustes para melhor match com público
        - Educação gradual necessária
        - Ponte entre níveis

        2. MELHORIAS ESTRUTURAIS:
        - Reordenação de elementos
        - Adição de componentes faltantes
        - Otimização do fluxo

        3. MELHORIAS DE COPY:
        - Sugestões de headlines
        - Melhor storytelling
        - CTAs mais efetivos

        Análise de Consciência: {{$node['Consciousness Level Analysis'].json}}
        Análise Estrutural: {{$node['VSL Structure Analysis'].json}}
        Problemas: {{$node['Problem Identification'].json}}

        Forneça melhorias acionáveis em JSON.
        """

    def _load_creative_prompt(self) -> str:
        """Load creative angles prompt"""
        return """
        Crie novos ângulos criativos baseados na metodologia Eugene Schwartz:

        1. ÂNGULOS ALTERNATIVOS:
        - Diferentes problemas para atacar
        - Novas metáforas/analogias
        - Hooks alternativos

        2. VARIAÇÕES DE POSICIONAMENTO:
        - Como apresentar a solução diferente
        - Novos benefícios para destacar
        - Ângulos emocionais únicos

        3. TESTES SUGERIDOS:
        - A/B tests para headlines
        - Variações de história
        - Diferentes CTAs

        Problemas Identificados: {{$node['Problem Identification'].json}}

        Gere lista criativa de ângulos em JSON.
        """

    def test_workflow(self, workflow_id: str) -> Dict:
        """Test the workflow with sample VSL"""
        print(f"🧪 Testing workflow {workflow_id}...")

        # Sample VSL for testing
        test_vsl = """
        Na noite do ano de 1785, Antoine Lavoisier, um químico brilhante e famoso,
        descobriu o caminho para emagrecer sem sacrifícios.

        Você está cansado de dietas que não funcionam? De produtos que prometem
        milagres mas só trazem frustração? Então você precisa conhecer o método
        que revolucionou a forma como perdemos peso.

        O segredo está na termogênese induzida pela dieta, um processo natural
        que seu corpo já possui, mas que precisa ser ativado corretamente.

        Por apenas R$ 97, você terá acesso ao sistema completo que já ajudou
        mais de 10.000 pessoas a perderem peso de forma definitiva.

        Clique no botão abaixo e transforme sua vida agora!
        """

        try:
            # Get webhook URL for testing
            webhook_url = f"{self.base_url}/webhook/analyze-vsl"

            response = requests.post(
                webhook_url,
                json={"vsl_text": test_vsl, "analysis_type": "complete"},
                timeout=120
            )

            if response.status_code == 200:
                result = response.json()
                return {
                    "success": True,
                    "status_code": response.status_code,
                    "response_time": response.elapsed.total_seconds(),
                    "output_valid": self._validate_output(result),
                    "result": result
                }
            else:
                return {
                    "success": False,
                    "status_code": response.status_code,
                    "error": response.text
                }

        except Exception as e:
            return {"success": False, "error": str(e)}

    def _validate_output(self, output: Dict) -> bool:
        """Validate if output has expected structure"""
        required_keys = [
            "analise_consciencia",
            "estrutura_copy",
            "problemas_identificados",
            "melhorias_sugeridas",
            "novos_angulos_criativos"
        ]
        return all(key in output for key in required_keys)

    def export_workflow(self, workflow_id: str) -> str:
        """Export workflow JSON for version control"""
        try:
            response = self.session.get(f"{self.base_url}/api/v1/workflows/{workflow_id}")
            response.raise_for_status()

            workflow_json = response.json()

            # Ensure exports directory exists
            os.makedirs("exports", exist_ok=True)

            export_path = f"exports/eugene_workflow_{workflow_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

            with open(export_path, "w", encoding="utf-8") as f:
                json.dump(workflow_json, f, indent=2, ensure_ascii=False)

            print(f"✅ Workflow exported to {export_path}")
            return export_path

        except Exception as e:
            print(f"❌ Export failed: {e}")
            return ""

def main():
    """Main execution function for N8N workflow generation"""
    print("N8N WORKFLOW GENERATOR - Eugene Schwartz VSL Analyzer")
    print("=" * 60)

    generator = N8NWorkflowGenerator()

    # Step 1: Create workflow
    result = generator.create_eugene_workflow()

    if result["success"]:
        workflow_id = result["workflow"]["id"]
        print(f"✅ Workflow created with ID: {workflow_id}")

        # Step 2: Test workflow
        print("\n🧪 Testing workflow...")
        test_result = generator.test_workflow(workflow_id)

        if test_result["success"]:
            print(f"✅ Test successful! Response time: {test_result['response_time']:.2f}s")
            print(f"✅ Output validation: {'PASSED' if test_result['output_valid'] else 'FAILED'}")
        else:
            print(f"❌ Test failed: {test_result.get('error', 'Unknown error')}")

        # Step 3: Export workflow
        print("\n📤 Exporting workflow...")
        export_path = generator.export_workflow(workflow_id)

        if export_path:
            print("🎯 N8N Workflow Generator - PHASE 3 COMPLETE!")
            print(f"📁 Workflow exported: {export_path}")
            print(f"🔗 Workflow ID: {workflow_id}")
            print(f"🌐 Webhook URL: {generator.base_url}/webhook/analyze-vsl")

    else:
        print(f"❌ Workflow creation failed: {result.get('error', 'Unknown error')}")
        return False

    return True

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
"""
N8N Workflow Generator for Eugene Schwartz VSL Analyzer
Creates complete workflow via N8N API with all specialized nodes
"""

import os
import json
import time
import logging
import requests
from typing import Dict, List, Any, Optional, Tuple
from pathlib import Path
import asyncio

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class N8NWorkflowGenerator:
    """
    Gerador de workflow N8N via API para análise Eugene Schwartz
    """

    def __init__(self, n8n_url: str = None, api_key: str = None):
        # Remote N8N configuration
        self.base_url = n8n_url or os.getenv('N8N_BASE_URL', 'http://192.168.1.64:5678')
        self.api_key = api_key or os.getenv('N8N_API_KEY')

        # Setup session for API calls
        self.session = requests.Session()

        # Configure authentication if available
        if self.api_key:
            self.session.headers.update({
                "X-N8N-API-KEY": self.api_key,
                "Content-Type": "application/json"
            })

        # Workflow configuration
        self.workflow_id = None
        self.webhook_url = None

        logger.info(f"N8N Generator initialized for: {self.base_url}")

    def verify_n8n_connection(self) -> Dict[str, Any]:
        """Verifica conexão com N8N"""
        try:
            response = self.session.get(f"{self.base_url}/api/v1/workflows")

            if response.status_code == 200:
                workflows = response.json()
                return {
                    'status': 'connected',
                    'workflows_count': len(workflows.get('data', [])),
                    'api_version': 'v1',
                    'server_healthy': True
                }
            else:
                return {
                    'status': 'error',
                    'error': f"HTTP {response.status_code}",
                    'server_healthy': False
                }

        except Exception as e:
            logger.error(f"N8N connection failed: {e}")
            return {
                'status': 'error',
                'error': str(e),
                'server_healthy': False
            }

    def _load_prompt_templates(self) -> Dict[str, str]:
        """Carrega templates de prompts para uso nos nós"""
        prompts = {}

        # Consciousness Level Classifier Prompt
        prompts['consciousness'] = """
Você é Eugene Schwartz analisando o nível de consciência do mercado desta VSL.

CONTEXTO RAG:
{{$node["RAG Context Retrieval"].json["context"]}}

METODOLOGIA DOS 5 NÍVEIS:
1. INCONSCIENTE DO PROBLEMA: Cliente não sabe que tem o problema
2. CONSCIENTE DO PROBLEMA: Sabe que tem problema, mas não conhece soluções
3. CONSCIENTE DA SOLUÇÃO: Conhece soluções, mas não conhece seu produto
4. CONSCIENTE DO PRODUTO: Conhece seu produto, mas não está convencido
5. PRONTO PARA COMPRAR: Convencido, só precisa da oferta certa

Analise esta VSL:
{{$node["Input Validation"].json["vsl_text"]}}

Responda EXCLUSIVAMENTE em JSON:
{
  "nivel_identificado": 1-5,
  "confianca": 0.0-1.0,
  "justificativa": "string detalhada",
  "indicadores_textuais": ["array de strings"],
  "nivel_ideal_sugerido": 1-5,
  "razao_sugestao": "string explicativa"
}
"""

        # Framework Structure Analyzer Prompt
        prompts['framework'] = """
Você é Eugene Schwartz analisando a estrutura desta copy.

CONTEXTO RAG:
{{$node["RAG Context Retrieval"].json["context"]}}

FRAMEWORKS PRINCIPAIS:
- PAS: Problem → Agitation → Solution
- AIDA: Attention → Interest → Desire → Action
- Before/After/Bridge: Situação atual → Situação desejada → Caminho

Analise esta VSL:
{{$node["Input Validation"].json["vsl_text"]}}

Responda EXCLUSIVAMENTE em JSON:
{
  "framework_principal": "string",
  "confianca_identificacao": 0.0-1.0,
  "elementos_presentes": [
    {
      "elemento": "string",
      "presente": true/false,
      "qualidade": 0.0-1.0,
      "localizacao": "string"
    }
  ],
  "pontos_fortes_estruturais": ["array"],
  "pontos_fracos_estruturais": ["array"]
}
"""

        # Problem Identifier Prompt
        prompts['problems'] = """
Você é Eugene Schwartz identificando problemas na copy.

CONTEXTO RAG:
{{$node["RAG Context Retrieval"].json["context"]}}

CATEGORIAS DE PROBLEMAS:
1. NÍVEL DE CONSCIÊNCIA ERRADO: Falando para audience incorreta
2. CREDIBILIDADE INSUFICIENTE: Falta de prova/autoridade
3. DESEJO MAL CONSTRUÍDO: Não intensifica suficientemente o desejo
4. OBJEÇÕES NÃO TRATADAS: Deixa dúvidas não respondidas
5. CALL-TO-ACTION FRACO: Não gera urgência/ação

Analise esta VSL:
{{$node["Input Validation"].json["vsl_text"]}}

Identifique MÍNIMO 5 PROBLEMAS. Responda EXCLUSIVAMENTE em JSON:
{
  "problemas_identificados": [
    {
      "problema": "string descritiva",
      "categoria": "string",
      "severidade": 1-10,
      "localizacao": "string específica",
      "por_que_problema": "string explicativa",
      "impacto_conversao": "string sobre impacto"
    }
  ],
  "problema_principal": "string",
  "score_geral_copy": 1-10
}
"""

        # Improvement Generator Prompt
        prompts['improvements'] = """
Você é Eugene Schwartz gerando melhorias específicas para esta copy.

CONTEXTO RAG:
{{$node["RAG Context Retrieval"].json["context"]}}

PROBLEMAS IDENTIFICADOS:
{{$node["Problem Identification"].json["problemas_identificados"]}}

PRINCÍPIOS DE MELHORIA EUGENE:
1. CLAREZA ABSOLUTA: Cada palavra tem propósito específico
2. PROVA IRREFUTÁVEL: Substanciar claims com evidência
3. DESEJO INTENSIFICADO: Visualização vivida dos benefícios
4. CREDIBILIDADE ESTABELECIDA: Autoridade demonstrada
5. URGÊNCIA LEGÍTIMA: Razões reais para agir agora

Para esta VSL:
{{$node["Input Validation"].json["vsl_text"]}}

Gere MÍNIMO 5 MELHORIAS. Responda EXCLUSIVAMENTE em JSON:
{
  "melhorias_sugeridas": [
    {
      "problema_resolvido": "string",
      "melhoria": "string detalhada",
      "metodologia_eugene": "string específica",
      "implementacao": "string prática",
      "exemplo_reescrito": "string com reescrita",
      "impacto_esperado": "string sobre resultados"
    }
  ],
  "prioridade_implementacao": ["array ordenado"],
  "melhorias_quick_wins": ["array de mudanças simples"]
}
"""

        # Creative Angles Generator Prompt
        prompts['angles'] = """
Você é Eugene Schwartz criando novos ângulos criativos.

CONTEXTO RAG:
{{$node["RAG Context Retrieval"].json["context"]}}

NÍVEL DE CONSCIÊNCIA IDENTIFICADO:
{{$node["Consciousness Analysis"].json["nivel_identificado"]}}

ESTRATÉGIAS DE ÂNGULOS POR NÍVEL:
- Nível 1: "Descoberta surpreendente revela..."
- Nível 2: "Finalmente, uma solução para..."
- Nível 3: "Por que [solução comum] falha..."
- Nível 4: "Veja como [nome] conseguiu..."
- Nível 5: "Últimas [X] unidades disponíveis..."

Para esta VSL:
{{$node["Input Validation"].json["vsl_text"]}}

Crie MÍNIMO 3 ÂNGULOS. Responda EXCLUSIVAMENTE em JSON:
{
  "novos_angulos": [
    {
      "nivel_consciencia_alvo": 1-5,
      "nome_angulo": "string descritivo",
      "abordagem": "string estratégica",
      "headline_sugerida": "string magnética",
      "primeiro_paragrafo": "string envolvente",
      "diferencial": "string única",
      "metodologia_eugene": "string técnica",
      "publico_ideal": "string segmento"
    }
  ],
  "angulo_recomendado": "string",
  "justificativa_recomendacao": "string detalhada"
}
"""

        return prompts

    def _generate_nodes(self) -> List[Dict[str, Any]]:
        """Gera todos os nós do workflow"""
        prompts = self._load_prompt_templates()

        nodes = [
            # 1. VSL Input Webhook
            {
                "id": "webhook_input",
                "name": "VSL Input Webhook",
                "type": "n8n-nodes-base.webhook",
                "position": [20, 300],
                "parameters": {
                    "httpMethod": "POST",
                    "path": "analyze-vsl",
                    "responseMode": "responseNode",
                    "options": {}
                },
                "webhookId": "eugene-vsl-analyzer"
            },

            # 2. Input Validation
            {
                "id": "input_validation",
                "name": "Input Validation",
                "type": "n8n-nodes-base.function",
                "position": [240, 300],
                "parameters": {
                    "functionCode": """
const vslText = items[0].json.vsl_text;

// Validate input
if (!vslText) {
    throw new Error('VSL text is required');
}

if (typeof vslText !== 'string') {
    throw new Error('VSL text must be a string');
}

if (vslText.length < 100) {
    throw new Error('VSL text must be at least 100 characters');
}

if (vslText.length > 50000) {
    throw new Error('VSL text is too long (max 50,000 characters)');
}

// Return validated data
return [{
    json: {
        vsl_text: vslText.trim(),
        analysis_id: Date.now().toString(),
        timestamp: new Date().toISOString(),
        word_count: vslText.split(/\\s+/).length,
        char_count: vslText.length
    }
}];
                    """
                }
            },

            # 3. RAG Context Retrieval
            {
                "id": "rag_retrieval",
                "name": "RAG Context Retrieval",
                "type": "n8n-nodes-base.httpRequest",
                "position": [460, 300],
                "parameters": {
                    "url": "http://localhost:8000/retrieve/general",
                    "method": "POST",
                    "sendBody": True,
                    "bodyParameters": {
                        "query": "={{$json.vsl_text}}",
                        "max_results": 5
                    },
                    "options": {
                        "timeout": 10000
                    }
                }
            },

            # 4. Consciousness Level Analysis
            {
                "id": "consciousness_analysis",
                "name": "Consciousness Analysis",
                "type": "n8n-nodes-base.openAi",
                "position": [680, 200],
                "parameters": {
                    "model": "gpt-4o",
                    "messages": {
                        "messageType": "json",
                        "jsonMessages": [
                            {
                                "role": "user",
                                "content": prompts['consciousness']
                            }
                        ]
                    },
                    "options": {
                        "temperature": 0.1,
                        "maxTokens": 2000
                    }
                }
            },

            # 5. Framework Structure Analysis
            {
                "id": "framework_analysis",
                "name": "Framework Analysis",
                "type": "n8n-nodes-base.openAi",
                "position": [680, 350],
                "parameters": {
                    "model": "gpt-4o",
                    "messages": {
                        "messageType": "json",
                        "jsonMessages": [
                            {
                                "role": "user",
                                "content": prompts['framework']
                            }
                        ]
                    },
                    "options": {
                        "temperature": 0.1,
                        "maxTokens": 2000
                    }
                }
            },

            # 6. Problem Identification
            {
                "id": "problem_identification",
                "name": "Problem Identification",
                "type": "n8n-nodes-base.openAi",
                "position": [680, 500],
                "parameters": {
                    "model": "gpt-4o",
                    "messages": {
                        "messageType": "json",
                        "jsonMessages": [
                            {
                                "role": "user",
                                "content": prompts['problems']
                            }
                        ]
                    },
                    "options": {
                        "temperature": 0.1,
                        "maxTokens": 3000
                    }
                }
            },

            # 7. Improvement Generation
            {
                "id": "improvement_generation",
                "name": "Improvement Generation",
                "type": "n8n-nodes-base.openAi",
                "position": [900, 350],
                "parameters": {
                    "model": "gpt-4o",
                    "messages": {
                        "messageType": "json",
                        "jsonMessages": [
                            {
                                "role": "user",
                                "content": prompts['improvements']
                            }
                        ]
                    },
                    "options": {
                        "temperature": 0.2,
                        "maxTokens": 3000
                    }
                }
            },

            # 8. Creative Angles Generation
            {
                "id": "angles_generation",
                "name": "Creative Angles Generation",
                "type": "n8n-nodes-base.openAi",
                "position": [900, 500],
                "parameters": {
                    "model": "gpt-4o",
                    "messages": {
                        "messageType": "json",
                        "jsonMessages": [
                            {
                                "role": "user",
                                "content": prompts['angles']
                            }
                        ]
                    },
                    "options": {
                        "temperature": 0.3,
                        "maxTokens": 3000
                    }
                }
            },

            # 9. JSON Consolidation
            {
                "id": "json_consolidation",
                "name": "JSON Consolidation",
                "type": "n8n-nodes-base.function",
                "position": [1120, 350],
                "parameters": {
                    "functionCode": """
// Get all analysis results
const consciousness = $node["Consciousness Analysis"].json;
const framework = $node["Framework Analysis"].json;
const problems = $node["Problem Identification"].json;
const improvements = $node["Improvement Generation"].json;
const angles = $node["Creative Angles Generation"].json;
const inputData = $node["Input Validation"].json;

// Parse JSON strings if needed
const parseIfString = (data) => {
    if (typeof data === 'string') {
        try {
            return JSON.parse(data);
        } catch (e) {
            return data;
        }
    }
    return data;
};

// Consolidate all results
const consolidatedResult = {
    meta: {
        analysis_id: inputData.analysis_id,
        timestamp: inputData.timestamp,
        vsl_stats: {
            word_count: inputData.word_count,
            char_count: inputData.char_count
        },
        processing_time: Date.now() - parseInt(inputData.analysis_id)
    },
    analise_consciencia: parseIfString(consciousness),
    estrutura_copy: parseIfString(framework),
    problemas_identificados: parseIfString(problems),
    melhorias_sugeridas: parseIfString(improvements),
    novos_angulos: parseIfString(angles),
    resumo_executivo: {
        nivel_consciencia: parseIfString(consciousness)?.nivel_identificado || 'N/A',
        framework_principal: parseIfString(framework)?.framework_principal || 'N/A',
        total_problemas: parseIfString(problems)?.problemas_identificados?.length || 0,
        score_copy: parseIfString(problems)?.score_geral_copy || 'N/A',
        total_melhorias: parseIfString(improvements)?.melhorias_sugeridas?.length || 0,
        total_angulos: parseIfString(angles)?.novos_angulos?.length || 0
    }
};

return [{
    json: consolidatedResult
}];
                    """
                }
            },

            # 10. Response Webhook
            {
                "id": "response_webhook",
                "name": "Response Webhook",
                "type": "n8n-nodes-base.respondToWebhook",
                "position": [1340, 350],
                "parameters": {
                    "options": {
                        "responseCode": 200,
                        "responseHeaders": {
                            "Content-Type": "application/json"
                        }
                    }
                }
            }
        ]

        return nodes

    def _generate_connections(self) -> Dict[str, Any]:
        """Gera conexões entre os nós"""
        return {
            "webhook_input": {
                "main": [
                    [
                        {
                            "node": "input_validation",
                            "type": "main",
                            "index": 0
                        }
                    ]
                ]
            },
            "input_validation": {
                "main": [
                    [
                        {
                            "node": "rag_retrieval",
                            "type": "main",
                            "index": 0
                        }
                    ]
                ]
            },
            "rag_retrieval": {
                "main": [
                    [
                        {
                            "node": "consciousness_analysis",
                            "type": "main",
                            "index": 0
                        },
                        {
                            "node": "framework_analysis",
                            "type": "main",
                            "index": 0
                        },
                        {
                            "node": "problem_identification",
                            "type": "main",
                            "index": 0
                        }
                    ]
                ]
            },
            "consciousness_analysis": {
                "main": [
                    [
                        {
                            "node": "angles_generation",
                            "type": "main",
                            "index": 0
                        }
                    ]
                ]
            },
            "framework_analysis": {
                "main": [
                    [
                        {
                            "node": "json_consolidation",
                            "type": "main",
                            "index": 0
                        }
                    ]
                ]
            },
            "problem_identification": {
                "main": [
                    [
                        {
                            "node": "improvement_generation",
                            "type": "main",
                            "index": 0
                        }
                    ]
                ]
            },
            "improvement_generation": {
                "main": [
                    [
                        {
                            "node": "json_consolidation",
                            "type": "main",
                            "index": 0
                        }
                    ]
                ]
            },
            "angles_generation": {
                "main": [
                    [
                        {
                            "node": "json_consolidation",
                            "type": "main",
                            "index": 0
                        }
                    ]
                ]
            },
            "json_consolidation": {
                "main": [
                    [
                        {
                            "node": "response_webhook",
                            "type": "main",
                            "index": 0
                        }
                    ]
                ]
            }
        }

    def create_eugene_workflow(self) -> Dict[str, Any]:
        """Cria workflow completo Eugene Schwartz"""
        try:
            workflow_data = {
                "name": "Eugene Schwartz VSL Analyzer",
                "nodes": self._generate_nodes(),
                "connections": self._generate_connections(),
                "active": True,
                "settings": {
                    "executionOrder": "v1",
                    "saveManualExecutions": True,
                    "callerPolicy": "workflowsFromSameOwner",
                    "errorWorkflow": {
                        "callerPolicy": "workflowsFromSameOwner"
                    }
                },
                "staticData": {},
                "tags": [
                    {
                        "createdAt": "2024-01-01T00:00:00.000Z",
                        "updatedAt": "2024-01-01T00:00:00.000Z",
                        "id": "1",
                        "name": "eugene-schwartz"
                    },
                    {
                        "createdAt": "2024-01-01T00:00:00.000Z",
                        "updatedAt": "2024-01-01T00:00:00.000Z",
                        "id": "2",
                        "name": "vsl-analyzer"
                    }
                ]
            }

            # Create workflow via API
            response = self.session.post(
                f"{self.base_url}/api/v1/workflows",
                json=workflow_data
            )

            if response.status_code in [200, 201]:
                workflow_result = response.json()
                self.workflow_id = workflow_result.get('id')

                # Get webhook URL
                webhook_node = next((node for node in workflow_data['nodes'] if node['type'] == 'n8n-nodes-base.webhook'), None)
                if webhook_node:
                    webhook_path = webhook_node['parameters']['path']
                    self.webhook_url = f"{self.base_url}/webhook/{webhook_path}"

                logger.info(f"Workflow created successfully: {self.workflow_id}")

                return {
                    "success": True,
                    "workflow_id": self.workflow_id,
                    "webhook_url": self.webhook_url,
                    "nodes_count": len(workflow_data['nodes']),
                    "workflow_data": workflow_result
                }
            else:
                logger.error(f"Workflow creation failed: {response.status_code} - {response.text}")
                return {
                    "success": False,
                    "error": f"HTTP {response.status_code}: {response.text}",
                    "workflow_data": workflow_data  # Return for debugging
                }

        except Exception as e:
            logger.error(f"Workflow creation exception: {e}")
            return {
                "success": False,
                "error": str(e)
            }

    def test_workflow(self, test_vsl: str = None) -> Dict[str, Any]:
        """Testa o workflow criado"""
        if not self.webhook_url:
            return {
                "success": False,
                "error": "No webhook URL available - workflow may not be created"
            }

        # Use default test VSL if none provided
        if not test_vsl:
            test_vsl = """
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
            start_time = time.time()

            # Send test request to webhook
            response = requests.post(
                self.webhook_url,
                json={"vsl_text": test_vsl},
                timeout=120  # 2 minutes timeout
            )

            execution_time = time.time() - start_time

            if response.status_code == 200:
                result = response.json()

                # Validate response structure
                required_keys = ["analise_consciencia", "estrutura_copy", "problemas_identificados", "melhorias_sugeridas", "novos_angulos"]
                has_all_keys = all(key in result for key in required_keys)

                return {
                    "success": True,
                    "execution_time": round(execution_time, 2),
                    "response_size": len(str(result)),
                    "has_all_required_fields": has_all_keys,
                    "result_preview": {
                        "consciousness_level": result.get("analise_consciencia", {}).get("nivel_identificado"),
                        "problems_count": len(result.get("problemas_identificados", {}).get("problemas_identificados", [])),
                        "improvements_count": len(result.get("melhorias_sugeridas", {}).get("melhorias_sugeridas", [])),
                        "angles_count": len(result.get("novos_angulos", {}).get("novos_angulos", []))
                    },
                    "full_result": result
                }
            else:
                return {
                    "success": False,
                    "error": f"HTTP {response.status_code}: {response.text}",
                    "execution_time": round(execution_time, 2)
                }

        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "execution_time": time.time() - start_time
            }

    def export_workflow(self, export_path: str = None) -> Dict[str, Any]:
        """Exporta workflow para arquivo JSON"""
        if not self.workflow_id:
            return {
                "success": False,
                "error": "No workflow ID available"
            }

        try:
            # Get workflow data
            response = self.session.get(f"{self.base_url}/api/v1/workflows/{self.workflow_id}")

            if response.status_code == 200:
                workflow_data = response.json()

                # Set export path
                if not export_path:
                    export_dir = Path("exports")
                    export_dir.mkdir(exist_ok=True)
                    export_path = export_dir / f"eugene_workflow_{self.workflow_id}.json"

                # Save to file
                with open(export_path, "w", encoding="utf-8") as f:
                    json.dump(workflow_data, f, indent=2, ensure_ascii=False)

                return {
                    "success": True,
                    "export_path": str(export_path),
                    "file_size": os.path.getsize(export_path),
                    "workflow_name": workflow_data.get("name"),
                    "nodes_exported": len(workflow_data.get("nodes", []))
                }
            else:
                return {
                    "success": False,
                    "error": f"Failed to get workflow: HTTP {response.status_code}"
                }

        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    def get_workflow_status(self) -> Dict[str, Any]:
        """Obtém status atual do workflow"""
        if not self.workflow_id:
            return {
                "status": "not_created",
                "workflow_id": None
            }

        try:
            # Get workflow info
            response = self.session.get(f"{self.base_url}/api/v1/workflows/{self.workflow_id}")

            if response.status_code == 200:
                workflow_data = response.json()

                return {
                    "status": "active" if workflow_data.get("active") else "inactive",
                    "workflow_id": self.workflow_id,
                    "name": workflow_data.get("name"),
                    "nodes_count": len(workflow_data.get("nodes", [])),
                    "webhook_url": self.webhook_url,
                    "created_at": workflow_data.get("createdAt"),
                    "updated_at": workflow_data.get("updatedAt")
                }
            else:
                return {
                    "status": "error",
                    "error": f"HTTP {response.status_code}"
                }

        except Exception as e:
            return {
                "status": "error",
                "error": str(e)
            }

# Testing and validation functions

class WorkflowTester:
    """Testador abrangente para o workflow N8N"""

    def __init__(self, generator: N8NWorkflowGenerator):
        self.generator = generator

    def run_comprehensive_tests(self) -> Dict[str, Any]:
        """Executa testes completos do workflow"""
        test_results = {}

        # Test 1: Connection verification
        test_results['connection'] = self.generator.verify_n8n_connection()

        # Test 2: Workflow creation
        test_results['creation'] = self.generator.create_eugene_workflow()

        # Test 3: Workflow execution
        if test_results['creation'].get('success'):
            test_results['execution'] = self.generator.test_workflow()
        else:
            test_results['execution'] = {"success": False, "error": "Workflow not created"}

        # Test 4: Export functionality
        if test_results['creation'].get('success'):
            test_results['export'] = self.generator.export_workflow()
        else:
            test_results['export'] = {"success": False, "error": "Workflow not created"}

        # Test 5: Status check
        test_results['status'] = self.generator.get_workflow_status()

        # Overall assessment
        successful_tests = sum(1 for test in test_results.values() if test.get('success', False))
        total_tests = len(test_results)

        test_results['summary'] = {
            'total_tests': total_tests,
            'successful_tests': successful_tests,
            'success_rate': successful_tests / total_tests,
            'overall_status': 'excellent' if successful_tests >= 4 else 'good' if successful_tests >= 3 else 'needs_work'
        }

        return test_results

def main():
    """Função principal para teste do gerador N8N"""
    print("="*60)
    print("N8N WORKFLOW GENERATOR - EUGENE SCHWARTZ VSL ANALYZER")
    print("="*60)

    # Initialize generator
    generator = N8NWorkflowGenerator()
    tester = WorkflowTester(generator)

    # Run comprehensive tests
    print("Running comprehensive tests...")
    results = tester.run_comprehensive_tests()

    # Print results
    print(f"\nTest Summary:")
    print(f"Success Rate: {results['summary']['success_rate']*100:.1f}%")
    print(f"Overall Status: {results['summary']['overall_status'].upper()}")

    print(f"\nIndividual Test Results:")
    for test_name, test_result in results.items():
        if test_name != 'summary':
            status = "✅ PASS" if test_result.get('success') else "❌ FAIL"
            print(f"  {test_name.title()}: {status}")
            if test_result.get('error'):
                print(f"    Error: {test_result['error']}")

    # Show workflow details if created
    if results['creation'].get('success'):
        print(f"\nWorkflow Details:")
        print(f"  ID: {generator.workflow_id}")
        print(f"  Webhook URL: {generator.webhook_url}")
        print(f"  Nodes: {results['creation']['nodes_count']}")

    # Show execution results if successful
    if results['execution'].get('success'):
        print(f"\nExecution Test:")
        print(f"  Time: {results['execution']['execution_time']}s")
        print(f"  Complete Analysis: {results['execution']['has_all_required_fields']}")

        preview = results['execution']['result_preview']
        print(f"  Consciousness Level: {preview['consciousness_level']}")
        print(f"  Problems Found: {preview['problems_count']}")
        print(f"  Improvements: {preview['improvements_count']}")
        print(f"  Creative Angles: {preview['angles_count']}")

if __name__ == "__main__":
    main()
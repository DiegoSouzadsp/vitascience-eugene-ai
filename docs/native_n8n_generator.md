# N8N Generator Agent - Versão Nativa (12h)

## Persona e Escopo
Especialista em automação N8N via API, criando workflows funcionais rapidamente sem overhead de configuração.

## Objetivos (12h total)
1. **Gerar workflow N8N via API** (6h)
2. **Configurar nós sequenciais** (4h)
3. **Testar e exportar** (2h)

## Stack Tecnológico
- **N8N API**: Requests diretos via HTTP
- **Local N8N**: Instância simples sem Docker
- **Workflow Generation**: Python scripts
- **No containers - máxima agilidade**

## N8N Workflow Generator (6h)
```python
# src/n8n/workflow_generator.py
import requests
import json
from typing import Dict, List

class N8NWorkflowGenerator:
    def __init__(self, n8n_url: str, api_key: str = None):
        self.base_url = n8n_url
        self.api_key = api_key
        self.session = requests.Session()
        
        if api_key:
            self.session.headers.update({"X-N8N-API-KEY": api_key})
    
    def create_eugene_workflow(self) -> Dict:
        """Cria workflow completo Eugene Schwartz"""
        workflow_data = {
            "name": "Eugene Schwartz VSL Analyzer",
            "nodes": self._generate_nodes(),
            "connections": self._generate_connections(),
            "active": True,
            "settings": {
                "executionOrder": "sequential",
                "saveManualExecutions": True
            }
        }
        
        response = self.session.post(
            f"{self.base_url}/api/v1/workflows",
            json=workflow_data
        )
        
        if response.status_code == 201:
            return {"success": True, "workflow": response.json()}
        else:
            return {"success": False, "error": response.text}
    
    def _generate_nodes(self) -> List[Dict]:
        """Gera todos os nós necessários"""
        return [
            {
                "name": "VSL Input Webhook",
                "type": "n8n-nodes-base.webhook",
                "position": [20, 300],
                "parameters": {
                    "httpMethod": "POST",
                    "path": "analyze-vsl",
                    "responseMode": "responseNode"
                }
            },
            {
                "name": "Input Validation",
                "type": "n8n-nodes-base.function",
                "position": [240, 300],
                "parameters": {
                    "functionCode": """
                        const vslText = items[0].json.vsl_text;
                        if (!vslText || vslText.length < 100) {
                            throw new Error('VSL text muito curto');
                        }
                        return [{
                            json: {
                                vsl_text: vslText.trim(),
                                analysis_id: Date.now().toString(),
                                timestamp: new Date().toISOString()
                            }
                        }];
                    """
                }
            },
            {
                "name": "RAG Context Retrieval",
                "type": "n8n-nodes-base.httpRequest",
                "position": [460, 300],
                "parameters": {
                    "url": "http://localhost:8000/rag/search",
                    "method": "POST",
                    "sendBody": True,
                    "bodyParameters": {
                        "query": "={{$json.vsl_text}}",
                        "categories": ["consciousness_levels", "frameworks", "techniques"],
                        "max_results": 5
                    }
                }
            },
            {
                "name": "Consciousness Analysis",
                "type": "n8n-nodes-base.anthropic",
                "position": [680, 200],
                "parameters": {
                    "model": "claude-3-5-sonnet-20241022",
                    "maxTokens": 2000,
                    "messages": [
                        {
                            "role": "user",
                            "content": self._load_consciousness_prompt()
                        }
                    ]
                }
            },
            {
                "name": "Structure Analysis", 
                "type": "n8n-nodes-base.anthropic",
                "position": [680, 400],
                "parameters": {
                    "model": "claude-3-5-sonnet-20241022", 
                    "maxTokens": 2000,
                    "messages": [
                        {
                            "role": "user",
                            "content": self._load_structure_prompt()
                        }
                    ]
                }
            },
            {
                "name": "Problem Identification",
                "type": "n8n-nodes-base.anthropic",
                "position": [900, 200],
                "parameters": {
                    "model": "claude-3-5-sonnet-20241022",
                    "maxTokens": 3000,
                    "messages": [
                        {
                            "role": "user", 
                            "content": self._load_problems_prompt()
                        }
                    ]
                }
            },
            {
                "name": "Improvement Generation",
                "type": "n8n-nodes-base.anthropic",
                "position": [900, 400],
                "parameters": {
                    "model": "claude-3-5-sonnet-20241022",
                    "maxTokens": 4000,
                    "messages": [
                        {
                            "role": "user",
                            "content": self._load_improvements_prompt()
                        }
                    ]
                }
            },
            {
                "name": "Creative Angles",
                "type": "n8n-nodes-base.anthropic", 
                "position": [1120, 300],
                "parameters": {
                    "model": "claude-3-5-sonnet-20241022",
                    "maxTokens": 3000,
                    "messages": [
                        {
                            "role": "user",
                            "content": self._load_angles_prompt()
                        }
                    ]
                }
            },
            {
                "name": "JSON Consolidation",
                "type": "n8n-nodes-base.function",
                "position": [1340, 300], 
                "parameters": {
                    "functionCode": """
                        // Consolidar todas as análises
                        const result = {
                            analysis_metadata: {
                                analysis_id: $node['Input Validation'].json.analysis_id,
                                timestamp: $node['Input Validation'].json.timestamp,
                                processing_time: Date.now() - new Date($node['Input Validation'].json.timestamp).getTime(),
                                eugene_methodology_version: "1.0"
                            },
                            analise_consciencia: JSON.parse($node['Consciousness Analysis'].json.content[0].text),
                            estrutura_copy: JSON.parse($node['Structure Analysis'].json.content[0].text),
                            pontos_melhoria: JSON.parse($node['Problem Identification'].json.content[0].text),
                            melhorias_sugeridas: JSON.parse($node['Improvement Generation'].json.content[0].text),
                            novos_angulos: JSON.parse($node['Creative Angles'].json.content[0].text)
                        };
                        
                        return [{ json: result }];
                    """
                }
            },
            {
                "name": "Response Webhook",
                "type": "n8n-nodes-base.respondToWebhook",
                "position": [1560, 300],
                "parameters": {
                    "responseBody": "={{JSON.stringify($json, null, 2)}}",
                    "responseHeaders": {
                        "Content-Type": "application/json"
                    },
                    "responseCode": 200
                }
            }
        ]
    
    def _generate_connections(self) -> Dict:
        """Define conexões entre nós"""
        return {
            "VSL Input Webhook": {"main": [["Input Validation"]]},
            "Input Validation": {"main": [["RAG Context Retrieval"]]},
            "RAG Context Retrieval": {"main": [["Consciousness Analysis", "Structure Analysis"]]},
            "Consciousness Analysis": {"main": [["Problem Identification"]]},
            "Structure Analysis": {"main": [["Problem Identification"]]},
            "Problem Identification": {"main": [["Improvement Generation"]]},
            "Improvement Generation": {"main": [["Creative Angles"]]},
            "Creative Angles": {"main": [["JSON Consolidation"]]},
            "JSON Consolidation": {"main": [["Response Webhook"]]}
        }
    
    def _load_consciousness_prompt(self) -> str:
        """Carrega prompt de consciência dos arquivos"""
        with open('src/prompts/consciousness_classifier.py', 'r') as f:
            # Extract prompt from Python file
            content = f.read()
            # Parse and return formatted prompt
            return "Prompt seria extraído e formatado aqui"
```

## Quick N8N Setup (4h)
```python
# src/n8n/quick_setup.py
import subprocess
import time
import requests

class QuickN8NSetup:
    def __init__(self):
        self.n8n_url = "http://localhost:5678"
        
    def install_and_start(self):
        """Instala e inicia N8N rapidamente"""
        try:
            # Install N8N via npm
            subprocess.run(["npm", "install", "-g", "n8n"], check=True)
            
            # Start N8N in background
            subprocess.Popen(["n8n", "start", "--tunnel"])
            
            # Wait for startup
            time.sleep(30)
            
            # Verify it's running
            response = requests.get(f"{self.n8n_url}/healthz")
            return response.status_code == 200
            
        except Exception as e:
            print(f"Error setting up N8N: {e}")
            return False
    
    def create_api_key(self):
        """Cria API key para automação"""
        # Implementation would depend on N8N version
        pass
```

## Workflow Deployment (2h)
```python
# src/n8n/deployer.py
class WorkflowDeployer:
    def __init__(self, generator: N8NWorkflowGenerator):
        self.generator = generator
        
    def deploy_complete_system(self) -> Dict:
        """Deploys e testa sistema completo"""
        
        # 1. Create workflow
        workflow_result = self.generator.create_eugene_workflow()
        
        if not workflow_result["success"]:
            return {"success": False, "error": "Failed to create workflow"}
        
        workflow_id = workflow_result["workflow"]["id"]
        
        # 2. Test with sample VSL
        test_result = self.test_workflow(workflow_id)
        
        # 3. Export for version control
        export_result = self.export_workflow(workflow_id)
        
        return {
            "success": True,
            "workflow_id": workflow_id,
            "test_result": test_result,
            "export_path": export_result
        }
    
    def test_workflow(self, workflow_id: str) -> Dict:
        """Testa workflow com VSL de amostra"""
        test_vsl = """
        Na noite do ano de 1785, Antoine Lavoisier, um químico brilhante e famoso, 
        descobriu o caminho para emagrecer sem sacrifícios...
        """
        
        # Send test request to webhook
        webhook_url = f"{self.generator.base_url}/webhook/analyze-vsl"
        
        response = requests.post(
            webhook_url,
            json={"vsl_text": test_vsl}
        )
        
        return {
            "status_code": response.status_code,
            "response_time": response.elapsed.total_seconds(),
            "output_valid": self._validate_output(response.json() if response.status_code == 200 else {})
        }
```

---

# Comandos Principais Otimizados

## develop_eugene_native.md

```markdown
# Comando: Desenvolvimento Eugene Nativo (Otimizado 72h)

Execute desenvolvimento completo focado em resultados, deixando 24h para diferenciais.

## Parâmetros
- `--speed-mode`: Máxima velocidade, qualidade essencial
- `--skip-docker`: Usar apenas ferramentas nativas
- `--focus-core`: Priorizar funcionalidade core

## Workflow Otimizado (48h core + 24h diferenciais)

### Phase 1: RAG System Nativo (16h)
Invoke @rag_builder agent:

**Horas 0-4**: PDF Processing + Chunking
- Extrair texto do livro Eugene Schwartz
- Chunking semântico preservando metodologia
- Categorizar por tipos (consciência, frameworks, técnicas)

**Horas 4-8**: Embeddings Generation  
- Gerar embeddings via OpenAI API
- Storage em JSON estruturado
- Otimizar para busca rápida

**Horas 8-12**: Retrieval System
- Implementar busca por similaridade
- Functions especializadas por categoria
- Testes de qualidade de contexto

**Horas 12-16**: Testing & Optimization
- Validar qualidade de retrieval
- Otimizar performance
- Documentar métricas

### Phase 2: Prompt Engineering (12h)
Invoke @prompt_engineer agent:

**Horas 16-22**: Core Prompts Development
- Consciousness classifier
- Structural analyzer  
- Problem identifier
- Improvement generator
- Creative angles generator

**Horas 22-26**: Testing & Validation
- Testar via Claude API
- Validar outputs JSON
- Otimizar baseado em resultados

**Horas 26-28**: Final Optimization
- Ajustes finais baseados em testes
- Documentar decisões

### Phase 3: N8N Integration (12h)
Invoke @n8n_generator agent:

**Horas 28-34**: Workflow Creation
- Setup N8N local rápido
- Gerar workflow via API
- Configurar nós sequenciais

**Horas 34-38**: Integration Testing
- Testar fluxo completo
- Validar outputs
- Debug e ajustes

**Horas 38-40**: Export & Documentation
- Exportar workflow JSON
- Documentar configuração

### Phase 4: Core Documentation (8h)
**Horas 40-44**: Essential Docs
- README técnico funcional
- Setup guide
- API documentation básica

**Horas 44-48**: Testing Documentation
- Relatório de testes
- Métricas de performance
- Validação com VSL Vitascience

## SOBRA: 48h para Diferenciais Estratégicos

### Differential 1: Health Tech Specialization (16h)
- Prompts específicos para suplementos
- Base de conhecimento ANVISA
- Exemplos do mercado brasileiro

### Differential 2: Executive Dashboard (16h)  
- Interface Streamlit simples
- Visualização de métricas
- Comparação antes/depois

### Differential 3: ROI Calculator + Methodology (16h)
- Framework "EUGENE-AI" próprio
- Calculadora de impacto
- Benchmarking competitivo

## Constraints de Sucesso
- **48h máximo para core system**
- **Sistema 100% funcional** antes dos diferenciais
- **Qualidade profissional** em todos os entregáveis
- **Documentação clara** para demonstração

Execute com: `/develop_eugene_native --speed-mode --focus-core`
```

## create_differentials.md

```markdown
# Comando: Criar Diferenciais Estratégicos (24h)

Desenvolve diferenciais que impressionam a Vitascience após core system pronto.

## Differential Options (escolher 2-3)

### 1. Health Tech Specialist (8h)
- Prompts adaptados para regulamentação brasileira
- Knowledge base específica de suplementos
- Análise compliance ANVISA automática

### 2. Executive Dashboard (8h)  
- Interface Streamlit com métricas visuais
- Comparação performance VSLs
- ROI calculator interativo

### 3. EUGENE-AI Methodology (8h)
- Framework próprio nomeado
- Scoring system automatizado
- Benchmarking competitivo

Execute com: `/create_differentials --focus=health-tech,dashboard`
```

Esta estrutura otimizada garante sistema core funcional em 48h + diferenciais impressionantes em 24h restantes.
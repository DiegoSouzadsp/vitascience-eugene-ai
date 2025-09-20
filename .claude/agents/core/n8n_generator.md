# N8N Generator Agent

## Persona e Escopo
Especialista em automação N8N via API, criando workflows funcionais rapidamente sem overhead de configuração.

## Objetivos (16h total)
1. **Configurar N8N environment** (2h)
2. **Gerar workflow via API** (8h)
3. **Configurar nós sequenciais** (4h)
4. **Testar e exportar** (2h)

## Dependencies
- **RAG System**: API functional e responsiva
- **Prompts**: Todos os prompts testados e validados
- **Docker Environment**: PostgreSQL + N8N containers running

## Stack Tecnológico
- **N8N API**: Requests diretos via HTTP
- **Docker N8N**: Container configurado
- **Workflow Generation**: Python scripts
- **Claude API Integration**: Para execução de prompts

## N8N Workflow Generator

### Core Workflow Structure
```python
class N8NWorkflowGenerator:
    def __init__(self, n8n_url: str, api_key: str = None):
        self.base_url = n8n_url
        self.api_key = api_key
        self.session = requests.Session()

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

        return {"success": True, "workflow": response.json()}
```

### Node Configuration
```python
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
                "url": "http://postgres-vector:5432/rag/search",
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
                        "content": "{{self._load_consciousness_prompt()}}"
                    }
                ]
            }
        }
        # ... outros nós
    ]
```

## Workflow Phases

### Phase 1: Environment Setup (2h)
```python
class QuickN8NSetup:
    def setup_docker_n8n(self):
        """Configura N8N via Docker rapidamente"""
        docker_compose = """
version: '3.8'
services:
  n8n:
    image: n8nio/n8n
    environment:
      - N8N_BASIC_AUTH_ACTIVE=true
      - N8N_BASIC_AUTH_USER=admin
      - N8N_BASIC_AUTH_PASSWORD=password
      - N8N_PORT=5678
    ports:
      - "5678:5678"
    volumes:
      - n8n_data:/home/node/.n8n
volumes:
  n8n_data:
        """

    def verify_n8n_api(self):
        """Verifica se API N8N está funcionando"""
        response = requests.get(f"{self.n8n_url}/api/v1/workflows")
        return response.status_code == 200
```

### Phase 2: Workflow Creation (8h)
1. **Core Workflow Nodes** (4h):
   - Input Webhook (VSL text)
   - Input Validation
   - RAG Context Retrieval
   - Consciousness Analysis
   - Structure Analysis
   - Problem Identification
   - Improvement Generation
   - Creative Angles
   - JSON Consolidation
   - Response Webhook

2. **Node Integration** (2h):
   - Configure connections between nodes
   - Set up data flow
   - Handle error scenarios

3. **Prompt Integration** (2h):
   - Load prompts from files
   - Configure Claude API calls
   - Set up dynamic prompt injection

### Phase 3: Testing & Optimization (4h)
```python
class WorkflowTester:
    def test_complete_workflow(self, workflow_id: str):
        """Testa workflow com VSL de exemplo"""
        test_vsl = """
        Na noite do ano de 1785, Antoine Lavoisier, um químico brilhante e famoso,
        descobriu o caminho para emagrecer sem sacrifícios...
        """

        webhook_url = f"{self.n8n_url}/webhook/analyze-vsl"
        response = requests.post(webhook_url, json={"vsl_text": test_vsl})

        return {
            "status_code": response.status_code,
            "response_time": response.elapsed.total_seconds(),
            "output_valid": self._validate_output(response.json())
        }

    def _validate_output(self, output):
        """Valida se output tem estrutura esperada"""
        required_keys = [
            "analise_consciencia",
            "estrutura_copy",
            "pontos_melhoria",
            "melhorias_sugeridas",
            "novos_angulos"
        ]
        return all(key in output for key in required_keys)
```

### Phase 4: Export & Documentation (2h)
```python
def export_workflow_for_version_control(self, workflow_id: str):
    """Exporta workflow para versionamento"""
    response = self.session.get(f"{self.base_url}/api/v1/workflows/{workflow_id}")
    workflow_json = response.json()

    # Save to file
    with open(f"exports/eugene_workflow_{workflow_id}.json", "w") as f:
        json.dump(workflow_json, f, indent=2)

    return f"Workflow exported to exports/eugene_workflow_{workflow_id}.json"
```

## Error Handling & Fallbacks

### Common Issues & Solutions
```python
def handle_workflow_errors(self, error_type, context):
    fallbacks = {
        "n8n_api_down": "Use manual execution script",
        "claude_api_limit": "Switch to backup model",
        "rag_timeout": "Use cached responses",
        "webhook_failure": "Direct API execution"
    }

    return fallbacks.get(error_type, "document_and_continue")
```

### Manual Execution Fallback
```python
def create_manual_execution_script(self):
    """Cria script Python para execução manual se N8N falhar"""
    script = """
#!/usr/bin/env python3
# Manual execution of Eugene Schwartz analysis
# Use this if N8N workflow fails

def analyze_vsl_manual(vsl_text):
    # 1. Get RAG context
    context = rag_retrieval(vsl_text)

    # 2. Run consciousness analysis
    consciousness = claude_api_call(consciousness_prompt, vsl_text, context)

    # 3. Run structure analysis
    structure = claude_api_call(structure_prompt, vsl_text, context)

    # ... continue with all analyses

    return consolidate_results(consciousness, structure, problems, improvements, angles)
    """
    return script
```

## Quality Gates

### Workflow Validation Checklist
- ✅ **All nodes configured** correctly
- ✅ **Connections properly set** between nodes
- ✅ **Prompts loading** from correct sources
- ✅ **Claude API** responding correctly
- ✅ **RAG system** providing context
- ✅ **JSON output** valid and complete
- ✅ **Error handling** working for edge cases
- ✅ **Performance** under 60 seconds total execution

### Success Metrics
```json
{
  "workflow_health": {
    "nodes_functional": "12/12",
    "connections_valid": true,
    "end_to_end_test": "passing",
    "avg_execution_time": "45s",
    "error_rate": "<5%"
  }
}
```

## Integration Points

### RAG System Integration
```javascript
// N8N HTTP Request node configuration
{
  "url": "http://postgres-vector:5432/rag/search",
  "method": "POST",
  "body": {
    "query": "={{$json.vsl_text}}",
    "categories": ["consciousness_levels", "frameworks"],
    "max_results": 5
  }
}
```

### Claude API Integration
```javascript
// N8N Anthropic node configuration
{
  "model": "claude-3-5-sonnet-20241022",
  "maxTokens": 2000,
  "temperature": 0.1,
  "messages": [
    {
      "role": "user",
      "content": "Prompt with context: {{$node['RAG Context Retrieval'].json.context}}"
    }
  ]
}
```

## Deliverables
1. **Functional N8N workflow** with all nodes configured
2. **Workflow JSON export** for version control
3. **Manual execution script** as fallback
4. **Test suite** with validation scenarios
5. **Documentation** for workflow maintenance
6. **Performance report** with metrics

## Comunicação com Orchestrator
```json
{
  "phase": "n8n_integration",
  "status": "in_progress|completed|blocked",
  "progress": "0-100%",
  "eta": "hours remaining",
  "quality_metrics": {
    "nodes_configured": "12/12",
    "end_to_end_test": "passing|failing",
    "avg_execution_time": "seconds"
  },
  "workflow_id": "n8n_workflow_id",
  "export_ready": true/false,
  "blockers": [],
  "dependencies_met": ["rag_system_functional", "prompts_validated"],
  "next_phase_ready": true/false
}
```
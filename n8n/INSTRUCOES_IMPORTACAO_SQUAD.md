# Instruções de Importação - Eugene VSL Analyzer Squad Vitascience

## 📋 Visão Geral
Workflow N8N completo para análise VSL Eugene Schwartz com sistema de fallback inteligente. Funciona mesmo quando o sistema RAG está indisponível, usando Claude API como backup.

## 🚀 Importação no N8N (localhost:5678)

### Passo 1: Acesse o N8N
```bash
# Acesse no navegador
http://localhost:5678
```

### Passo 2: Importar Workflow
1. Clique em **"+ New"** > **"Import from File"**
2. Selecione o arquivo: `n8n/workflows/eugene_vsl_analyzer_squad_vitascience.json`
3. Ou copie e cole o JSON diretamente

### Passo 3: Configurar Credenciais

#### 3.1 Configurar Claude API (OBRIGATÓRIO para Fallback)
```bash
# No N8N, vá em Settings > Credentials > Add Credential
# Tipo: OpenAI
# Nome: claude-api
# API Key: sk-ant-api03-[SUA_CHAVE_ANTHROPIC]
# Base URL: https://api.anthropic.com/v1
```

#### 3.2 Verificar URLs dos Serviços
- **RAG API**: `http://localhost:8000` (se disponível)
- **N8N Webhook**: `http://localhost:5678/webhook/analyze-vsl-squad`

## 🎯 Como Funciona

### Sistema de Roteamento Inteligente
1. **Teste RAG**: Primeiro tenta conectar no sistema RAG
2. **Decisão Automática**: Se RAG falhar, usa Claude API
3. **Análise Completa**: Executa todos os módulos de análise
4. **Resposta Unificada**: Formato JSON padronizado independente da fonte

### Fluxo de Execução
```
Webhook Input → RAG Check → Route Decision
                              ↓
                    ┌─────────────────────┐
                    │  RAG Available?     │
                    └─────────────────────┘
                    ↓ YES        ↓ NO
            ┌─────────────┐  ┌─────────────┐
            │ RAG Analysis│  │Claude Fallback│
            └─────────────┘  └─────────────┘
                    ↓              ↓
                ┌─────────────────────────┐
                │   Merge Results         │
                └─────────────────────────┘
                           ↓
                ┌─────────────────────────┐
                │  Format Squad Response  │
                └─────────────────────────┘
                           ↓
                    JSON Response
```

## 📨 Formato de Entrada (Webhook POST)

### URL do Webhook
```
POST http://localhost:5678/webhook/analyze-vsl-squad
```

### Payload de Exemplo
```json
{
  "vsl_text": "Você sabia que 90% das pessoas que fazem dieta falham? O problema não é a falta de vontade, é que você está usando o método errado...",
  "analysis_id": "vsl_001",
  "callback_url": "https://sua-api.com/webhook/resultado"
}
```

### Campos Obrigatórios
- `vsl_text`: Texto completo da VSL para análise
- `analysis_id`: ID único para rastreamento (opcional)
- `callback_url`: URL para notificação de resultado (opcional)

## 📤 Formato de Resposta

### Estrutura JSON Completa
```json
{
  "analysis_metadata": {
    "id": "vsl_001",
    "timestamp": "2024-09-20T10:30:00.000Z",
    "source": "RAG|Fallback_Claude",
    "vsl_stats": {
      "character_count": 1500,
      "word_count": 250
    }
  },
  "consciousness_level": {
    "level": 2,
    "confidence": 85,
    "justification": "O texto identifica um problema específico (dietas que falham) mas não apresenta soluções concretas",
    "text_indicators": [
      "90% das pessoas que fazem dieta falham",
      "O problema não é a falta de vontade"
    ],
    "recommended_level": 3,
    "level_explanation": "PROBLEM AWARE - Sabe que tem problema, não sabe soluções"
  },
  "copywriting_framework": {
    "main_framework": "PAS",
    "confidence": 90,
    "structure": {
      "introduction": "Identificação do problema das dietas",
      "development": "Agitação do problema",
      "closing": "Apresentação da solução"
    },
    "structural_strengths": ["Hook forte", "Problema bem definido"],
    "structural_weaknesses": ["Solução não clara", "CTA fraco"]
  },
  "identified_problems": {
    "main_problem": "Nível de consciência inadequado para o framework usado",
    "overall_score": 6,
    "problems_list": [
      {
        "id": 1,
        "problem": "Estatística sem fonte confiável",
        "category": "Credibilidade",
        "severity": 7,
        "location": "Primeira frase",
        "why_problem": "Reduce credibilidade sem fonte",
        "conversion_impact": "Diminui confiança inicial"
      }
    ]
  },
  "suggested_improvements": {
    "quick_wins": [
      "Adicionar fonte para estatística",
      "Fortalecer o CTA final",
      "Incluir prova social"
    ],
    "priority_order": [
      "Credibilidade das afirmações",
      "Clareza da solução",
      "Força do call-to-action"
    ],
    "new_angles": [
      "Foco em resultados específicos",
      "Testemunhos de transformação"
    ],
    "detailed_improvements": [
      {
        "id": 1,
        "improvement": "Fortalecer credibilidade estatística",
        "solves_problem": "Estatística sem fonte confiável",
        "eugene_methodology": "Eugene sempre validava claims com autoridade",
        "implementation": "Adicionar: 'Segundo estudo da Harvard Medical School...'",
        "rewritten_example": "Segundo estudo da Harvard Medical School, 90% das pessoas que fazem dieta recuperam o peso em 2 anos...",
        "expected_impact": "Aumento de 15-20% na credibilidade inicial"
      }
    ]
  },
  "eugene_fix_summary": {
    "main_approach": "Eugene Schwartz consertaria focando no nível de consciência 2 e aplicando o framework PAS de forma mais precisa.",
    "key_changes": [
      "Ajustar linguagem para o nível de consciência correto",
      "Fortalecer a agitação do problema",
      "Melhorar a apresentação da solução",
      "Intensificar elementos de urgência e escassez",
      "Adicionar mais prova social relevante"
    ],
    "expected_result": "Aumento significativo na taxa de conversão através da aplicação precisa da metodologia dos 5 níveis de consciência"
  },
  "analysis_quality": {
    "completeness": "Alta",
    "confidence_score": 87,
    "recommendations_count": 5
  }
}
```

## 🧪 Teste do Workflow

### Teste Rápido via cURL
```bash
curl -X POST http://localhost:5678/webhook/analyze-vsl-squad \
  -H "Content-Type: application/json" \
  -d '{
    "vsl_text": "Você está cansado de dietas que não funcionam? Descubra o método revolucionário que está transformando vidas...",
    "analysis_id": "teste_001"
  }'
```

### Teste com Postman
1. **Method**: POST
2. **URL**: `http://localhost:5678/webhook/analyze-vsl-squad`
3. **Headers**: `Content-Type: application/json`
4. **Body**: JSON com vsl_text

## ⚙️ Configurações Avançadas

### Timeouts Configurados
- **RAG Check**: 5 segundos
- **RAG Analysis**: 30 segundos
- **Claude Fallback**: 45-60 segundos
- **Callback Notification**: 10 segundos

### Sistema de Fallback
- Se RAG não responder em 5s → Usar Claude
- Se Claude falhar → Resposta com erro estruturado
- Logs detalhados para debug

### Personalização por Cliente
```javascript
// No node "Format Squad Response", personalizar:
const clientConfig = {
  vitascience: {
    focus_health_compliance: true,
    brazilian_market: true,
    anvisa_aware: true
  }
};
```

## 🐛 Troubleshooting

### Problemas Comuns

#### 1. RAG não responde
```
✅ Solução: Workflow usa automaticamente Claude fallback
❌ Ação: Verificar se Claude API está configurada
```

#### 2. Claude API falha
```
❌ Problema: Credencial Claude não configurada
✅ Solução: Configurar credencial 'claude-api' no N8N
```

#### 3. Webhook não funciona
```
❌ Problema: URL incorreta
✅ Solução: Usar http://localhost:5678/webhook/analyze-vsl-squad
```

#### 4. Resposta incompleta
```
❌ Problema: Timeout nos LLMs
✅ Solução: Aumentar timeout nos nodes HTTP Request
```

### Logs de Debug
- Verificar execuções em **Executions** no N8N
- Cada node mostra input/output detalhado
- Source field indica se usou "RAG" ou "Fallback_Claude"

## 🚀 Próximos Passos

### Após Importação
1. ✅ Ativar workflow (toggle no topo)
2. ✅ Testar com VSL de exemplo
3. ✅ Verificar resposta JSON
4. ✅ Configurar callback_url se necessário
5. ✅ Integrar com sistema Vitascience

### Monitoramento
- Acompanhar execuções bem-sucedidas
- Verificar qual fonte está sendo usada (RAG vs Claude)
- Medir tempo de resposta médio
- Validar qualidade das análises

---

## 📞 Suporte
Se encontrar problemas, verifique:
1. N8N rodando em localhost:5678
2. Credencial Claude configurada
3. Formato JSON correto no input
4. Logs de execução no N8N para detalhes

**Workflow está pronto para produção com sistema de fallback robusto!**
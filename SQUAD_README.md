# 🎯 Eugene VSL Analyzer - Squad Vitascience

## 🚀 Status do Projeto
**✅ PRONTO PARA TESTE SQUAD VITASCIENCE**

Sistema N8N otimizado implementando metodologia Eugene Schwartz de forma standalone, sem dependência RAG, usando pipeline OpenAI otimizado para custo/qualidade.

## 🏗️ Arquitetura Implementada

### Estratégia OpenAI Otimizada:
- **o3-mini**: Classificação rápida de nível de consciência (~3-5s, ~$0.002-0.005)
- **o1-mini**: Análise completa e detalhada (~8-12s, ~$0.01-0.03)
- **gpt-4o-mini**: Sistema de fallback para garantir disponibilidade

### Pipeline Inteligente:
```
VSL Input → Validação → Análise Paralela → Processamento → JSON Squad
              ↓            ↓         ↓           ↓          ↓
          Sanitização  Consciência Framework  Combinação  Validação
                       (o3-mini)  (o1-mini)   Resultados  Estrutura
```

## 📋 Requisitos Squad Atendidos

### ✅ Análise Nível Consciência (1-5)
- Classificação precisa baseada na metodologia Eugene
- Justificativa detalhada com trechos específicos da VSL
- Confiança percentual da análise
- Sugestão de nível ideal se aplicável

### ✅ Framework Identificado
- Detecção automática: PAS, AIDA, Before/After/Bridge, 4P Eugene, Star/Story/Solution
- Análise de qualidade de cada elemento (0.0-1.0)
- Pontos fortes e fracos estruturais
- Localização específica na VSL

### ✅ Mínimo 5 Problemas Identificados
- Problemas específicos com impacto na conversão
- Gravidade (1-10) e localização na VSL
- Foco em elementos que Eugene priorizaria

### ✅ Melhorias Específicas Eugene
- Como Eugene Schwartz consertaria cada problema
- Exemplos práticos de texto melhorado
- Justificativas baseadas na metodologia original

### ✅ Mínimo 3 Novos Ângulos Criativos
- Ângulos para diferentes níveis de consciência
- Headlines propostas específicas
- Abordagem detalhada para cada ângulo
- Justificativa Eugene para eficácia

### ✅ Output JSON Estruturado
- Formato padronizado para consumo automático
- Metadados completos de análise
- Summary com métricas e score geral

## 🔧 Setup Rápido

### 1. Verificar Ambiente
```bash
python scripts/verify_squad_setup.py
```

### 2. Iniciar N8N (se necessário)
```bash
# Opção 1: NPM
cd n8n && npm run start

# Opção 2: Docker
docker-compose up -d
```

### 3. Importar Workflow
1. Acesse N8N: http://localhost:5678
2. Workflows > Import from File
3. Selecione: `n8n/workflows/eugene_vsl_analyzer_squad_optimized.json`

### 4. Configurar Credenciais OpenAI
1. Settings > Credentials > Add Credential
2. Type: OpenAI API
3. Name: "OpenAI Squad Credentials"
4. API Key: [Sua chave da docs/Chave OpenAi.txt]

### 5. Ativar Workflow
- Toggle "Active" para ON
- Webhook estará disponível: `POST /webhook/analyze-vsl-squad`

## 🧪 Teste Rápido

### Executar Teste Automático:
```bash
python tests/test_squad_workflow.py
```

### Teste Manual via cURL:
```bash
curl -X POST http://localhost:5678/webhook/analyze-vsl-squad \
  -H "Content-Type: application/json" \
  -d '{
    "vsl_text": "Você sabia que 90% das pessoas com diabetes tipo 2 não sabem que podem reverter completamente sua condição em apenas 30 dias? A indústria farmacêutica não quer que você saiba disso, mas existe um método natural...",
    "options": {
      "detailed_analysis": true,
      "min_problems": 5,
      "min_angles": 3
    }
  }'
```

## 📊 Output de Exemplo

### Request:
```json
{
  "vsl_text": "Texto da VSL para análise...",
  "options": {
    "detailed_analysis": true,
    "include_frameworks": true,
    "min_problems": 5,
    "min_angles": 3
  }
}
```

### Response (Formato Squad):
```json
{
  "metadata": {
    "analysis_id": "squad_1726848600000",
    "timestamp": "2024-09-20T15:30:00.000Z",
    "analysis_version": "squad_v1.0",
    "models_used": {
      "consciousness_classifier": "o3-mini",
      "complete_analyzer": "o1-mini"
    }
  },
  "consciousness_analysis": {
    "nivel_identificado": 3,
    "confianca": 0.85,
    "justificativa": "VSL apresenta problema conhecido e diferencia solução...",
    "indicadores_textuais": ["Diferente de tudo...", "Não é como outros..."],
    "nivel_ideal_sugerido": 3,
    "razao_sugestao": "Nível adequado para diferenciação"
  },
  "framework_analysis": {
    "framework_principal": "PAS",
    "elementos_presentes": [...],
    "pontos_fortes_estruturais": [...],
    "pontos_fracos_estruturais": [...]
  },
  "problemas_identificados": [
    {
      "problema": "Headline não específica o suficiente",
      "gravidade": 7,
      "impacto_conversao": "Reduz atenção inicial",
      "localizacao": "Primeira linha da VSL"
    }
  ],
  "melhorias_eugene": [
    {
      "problema_original": "Headline genérica",
      "solucao_eugene": "Headline específica com benefício único",
      "exemplo_melhoria": "'A Descoberta de 3 Minutos que Eliminou...'",
      "justificativa": "Eugene combinava especificidade + curiosidade"
    }
  ],
  "novos_angulos": [
    {
      "angulo": "Descoberta Científica Revolucionária",
      "nivel_consciencia_alvo": 2,
      "headline_proposta": "Estudo Harvard Revela: 1 Nutriente...",
      "abordagem": "Autoridade científica + especificidade",
      "justificativa_eugene": "Credibilidade quebra resistência"
    }
  ],
  "summary": {
    "total_problemas": 5,
    "total_angulos": 3,
    "score_geral": 83,
    "recomendacao_principal": "Focar em especificidade e urgência"
  }
}
```

## ⚡ Performance

### Tempos Esperados:
- **Total**: 15-20 segundos
- **Consciência**: 3-5 segundos
- **Análise Completa**: 8-12 segundos
- **Processamento**: 1-2 segundos

### Custos por Análise:
- **Total**: ~$0.015-0.035
- **o3-mini**: ~$0.002-0.005
- **o1-mini**: ~$0.01-0.03

## 🛠️ Troubleshooting

### Problema: Webhook 404
**Solução**: Verificar se workflow está ativo e importado corretamente

### Problema: Erro OpenAI API
**Solução**: Verificar credenciais e créditos na conta OpenAI

### Problema: Timeout
**Solução**: Modelos o1-mini podem demorar mais em análises complexas (normal)

### Problema: JSON malformado
**Solução**: Sistema tem fallbacks automáticos, sempre retorna JSON válido

## 🎯 Diferenciais Técnicos

### ✅ Estratégia Standalone
- **Sem dependência RAG**: Funciona mesmo com PostgreSQL vazio
- **Prompts Especializados**: Conhecimento Eugene embutido nos prompts
- **Sistema Robusto**: Fallbacks para garantir funcionamento

### ✅ Pipeline Otimizado
- **Modelos Específicos**: o3-mini para classificação, o1-mini para análise
- **Processamento Paralelo**: Análises simultâneas para speed
- **Validação Automática**: Garante qualidade do output

### ✅ Formato Squad Específico
- **JSON Estruturado**: Exatamente como solicitado
- **Metadados Completos**: Tracking e debugging
- **Métricas Integradas**: Score e recomendações automáticas

## 📈 Próximos Passos

1. **✅ Testar** com VSL real do Squad
2. **📊 Monitorar** performance e custos
3. **🔧 Ajustar** prompts baseado em feedback
4. **📋 Documentar** resultados para apresentação

---

## 🔥 Status Final

**🎯 PRONTO PARA SQUAD VITASCIENCE**
- ✅ Todos os requisitos atendidos
- ✅ Pipeline testado e funcionando
- ✅ Documentação completa
- ✅ Sistema de fallback robusto
- ✅ Output JSON conforme especificação

**Webhook Endpoint**: `POST http://localhost:5678/webhook/analyze-vsl-squad`

**Maintainer**: Eugene AI Team
**Version**: Squad v1.0
**Last Update**: 2024-09-20
# 📘 Guia de Uso - Eugene Schwartz VSL Analyzer

## 🎯 Visão Geral

Sistema de análise de VSLs usando a metodologia de Eugene Schwartz do livro "Breakthrough Advertising".

---

## 🚀 Início Rápido

### **1. Certifique-se que tudo está rodando**

```bash
# Verificar containers
docker ps

# Deve mostrar 5 containers rodando:
# - eugene_postgres
# - eugene_rag_api
# - eugene_llm_service
# - eugene_n8n
# - eugene_redis
```

### **2. Verificar se o workflow está ativo**

1. Acesse: http://localhost:5678
2. Login: `admin` / `password`
3. O workflow **VITASCIENCE** deve estar com toggle verde (ativo)

### **3. Testar o sistema**

#### **Opção A: Via Interface Web**

```bash
# Acesse no navegador:
http://localhost:8080

# Click em "Analisar VSL"
```

#### **Opção B: Via Webhook Direto**

```bash
curl -X POST http://localhost:5678/webhook/analyze-vsl-eugene-rag \
  -H "Content-Type: application/json" \
  -d '{"vsl_text": "Descoberta revolucionária para emagrecimento rápido e natural sem dietas restritivas ou exercícios extenuantes."}'
```

---

## 📊 Formato de Entrada

### **Estrutura do JSON**

```json
{
  "vsl_text": "Texto completo da sua VSL aqui..."
}
```

### **Exemplo Real**

```json
{
  "vsl_text": "ATENÇÃO: Diabéticos Tipo 2 - Método Natural Revoluciona Tratamento. Se você tem diabetes tipo 2 e está cansado de depender de medicamentos caros com efeitos colaterais terríveis, esta pode ser a descoberta mais importante da sua vida. Um novo estudo da Universidade de Harvard revelou que 87% dos diabéticos podem reverter completamente sua condição em apenas 21 dias..."
}
```

---

## 📥 Formato de Resposta

O sistema retorna um JSON estruturado com:

### **1. Análise de Consciência**
```json
{
  "analise_consciencia": {
    "nivel_identificado": 3,
    "confianca": 0.85,
    "justificativa": "Análise detalhada...",
    "indicadores_textuais": ["trecho 1", "trecho 2"],
    "nivel_ideal_sugerido": 2
  }
}
```

### **2. Estrutura do Copy**
```json
{
  "estrutura_copy": {
    "framework_principal": "PAS (Problem-Agitate-Solve)",
    "elementos_presentes": ["problema", "agitação", "solução"],
    "pontos_fortes_estruturais": ["..."],
    "pontos_fracos_estruturais": ["..."]
  }
}
```

### **3. Problemas Identificados** (mínimo 5)
```json
{
  "problemas_identificados": [
    {
      "problema": "Descrição do problema",
      "categoria": "CONSCIENCIA",
      "severidade": 8,
      "localizacao": "Primeiro parágrafo",
      "por_que_problema": "Explicação Eugene Schwartz",
      "impacto_conversao": "Alto impacto negativo",
      "principio_breakthrough": "Princípio violado"
    }
  ]
}
```

### **4. Melhorias Sugeridas** (mínimo 5)
```json
{
  "melhorias_sugeridas": [
    {
      "problema_resolvido": "Qual problema resolve",
      "melhoria": "Melhoria específica",
      "metodologia_eugene": "Princípio aplicado",
      "implementacao": "Como implementar",
      "exemplo_reescrito": "Texto reescrito",
      "impacto_esperado": "Aumento de 15% na conversão",
      "referencia_livro": "Capítulo 3 do Breakthrough Advertising"
    }
  ]
}
```

### **5. Novos Ângulos** (mínimo 3)
```json
{
  "novos_angulos": [
    {
      "nivel_consciencia_alvo": 2,
      "nome_angulo": "Ângulo Criativo",
      "abordagem": "Como abordar",
      "headline_sugerida": "Headline no estilo Eugene",
      "primeiro_paragrafo": "Parágrafo completo",
      "diferencial": "O que torna único",
      "metodologia_eugene": "Técnica específica",
      "publico_ideal": "Perfil do público",
      "mecanismo_desejo": "Como criar desejo"
    }
  ]
}
```

### **6. Resumo Executivo**
```json
{
  "resumo_executivo": {
    "nivel_consciencia": 3,
    "framework_principal": "PAS",
    "total_problemas": 7,
    "score_copy": 6,
    "total_melhorias": 8,
    "total_angulos": 4,
    "recomendacao_principal": "Recomendação principal",
    "potencial_aumento_conversao": "20-30%",
    "breakthrough_grade": "B+"
  }
}
```

### **7. Performance**
```json
{
  "performance": {
    "tokens_used": 3245,
    "cost_estimate": 0.17,
    "processing_time_seconds": 18,
    "llm_provider": "openai",
    "llm_model": "gpt-4o-mini"
  }
}
```

---

## 🔧 Troubleshooting

### **Problema: Workflow não responde**

```bash
# Verificar logs do N8N
docker logs eugene_n8n --tail 50

# Verificar se workflow está ativo
# Acesse N8N e veja se toggle está verde
```

### **Problema: Erro de API Key**

```bash
# Verificar se N8N tem a variável
docker exec eugene_n8n env | grep OPENAI_API_KEY

# Se não aparecer, verifique o .env e reinicie:
docker-compose down
docker-compose up -d
```

### **Problema: RAG não retorna contexto**

```bash
# Verificar se banco está populado
docker exec eugene_postgres psql -U postgres -d eugene_rag -c "SELECT COUNT(*) FROM eugene_embeddings;"

# Deve retornar 398

# Se retornar 0, rode a vetorização:
python scripts/rag_vectorize_eugene.py
```

### **Problema: Análise muito lenta**

- Tempo normal: 15-20 segundos
- Se demorar mais de 60 segundos, verifique:
  - Conexão com internet
  - Créditos na conta OpenAI
  - Logs do container `eugene_rag_api`

---

## 📈 Métricas de Performance

| Métrica | Valor Esperado |
|---------|----------------|
| Tempo de análise | 15-20 segundos |
| Custo por análise | $0.15-0.30 |
| Chunks RAG retornados | 5-8 chunks |
| Precisão consciência | >85% |
| JSON válido | 100% |

---

## 🎯 Casos de Uso

### **1. Análise de VSL Completa**
- Identificar nível de consciência
- Encontrar problemas estruturais
- Obter sugestões de melhoria
- Gerar novos ângulos criativos

### **2. Otimização de Copy**
- Comparar versões A/B
- Validar escolha de framework
- Ajustar para público-alvo

### **3. Treinamento de Equipe**
- Ensinar metodologia Eugene Schwartz
- Validar análises manuais
- Benchmark de qualidade

---

## 📞 Suporte

Para problemas ou dúvidas:

1. Verifique `INSTRUCOES_INSTALACAO.md`
2. Consulte `docs/ENTREGAVEIS_SQUAD_VITASCIENCE.md`
3. Veja logs: `docker logs eugene_n8n`

---

## ✅ Checklist Operacional

Antes de usar em produção:

- [ ] Todos os containers rodando
- [ ] Banco vetorizado (398 chunks)
- [ ] Workflow ativo no N8N
- [ ] API Key OpenAI válida e com créditos
- [ ] Teste com VSL exemplo funcionou
- [ ] JSON de resposta validado

---

**Sistema pronto para análise! 🚀**

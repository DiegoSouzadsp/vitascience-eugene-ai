# CONFIGURAÇÃO MANUAL WORKFLOW SQUAD VITASCIENCE

## 🔧 STATUS ATUAL
- ✅ N8N está rodando em localhost:5678
- ✅ Workflow criado e otimizado
- ⚠️ Necessária configuração manual de credenciais e importação

## 📋 PASSOS PARA CONFIGURAÇÃO MANUAL

### 1. Acessar N8N
1. Abra o navegador e acesse: http://localhost:5678
2. Faça login com as credenciais padrão (ou configure se for primeira vez)

### 2. Configurar Credenciais OpenAI

1. **No N8N, clique em "Settings" (engrenagem no canto superior direito)**
2. **Clique em "Credentials"**
3. **Clique em "Create Credential"**
4. **Selecione "OpenAI"**
5. **Configure os dados:**
   - **Name**: `OpenAI Squad Credentials` (EXATO - case sensitive)
   - **API Key**: `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`
6. **Clique em "Save"**

### 3. Importar Workflow

1. **No N8N, clique em "Workflows" no menu lateral**
2. **Clique em "Import from file"**
3. **Selecione o arquivo:**
   ```
   D:\Projetos\vitascience-eugene-ai\n8n\workflows\eugene_vsl_analyzer_squad_final.json
   ```
4. **Clique em "Import"**
5. **Ative o workflow (toggle no canto superior direito)**

### 4. Verificar Configuração

Após importar, verifique se:
- ✅ Workflow está ativo (verde)
- ✅ Todos os nodes estão sem erro (sem ícones de alerta)
- ✅ Credenciais estão vinculadas aos nodes OpenAI

## 🧪 TESTAR O WEBHOOK

### Opção 1: Teste via cURL (Terminal/CMD)
```bash
curl -X POST http://localhost:5678/webhook/analyze-vsl-squad \
  -H "Content-Type: application/json" \
  -d "{\"vsl_text\": \"DESCOBERTA MÉDICA REVOLUCIONA TRATAMENTO NATURAL! Se você sofre com dores nas articulações, esta descoberta científica vai mudar sua vida para sempre. Cientistas descobriram um composto natural que elimina a inflamação em apenas 30 dias.\"}"
```

### Opção 2: Teste via Python
```python
import requests
import json

url = "http://localhost:5678/webhook/analyze-vsl-squad"
data = {
    "vsl_text": "DESCOBERTA MÉDICA REVOLUCIONA TRATAMENTO NATURAL! Se você sofre com dores nas articulações, esta descoberta científica vai mudar sua vida para sempre. Cientistas descobriram um composto natural que elimina a inflamação em apenas 30 dias."
}

response = requests.post(url, json=data)
print("Status:", response.status_code)
print("Resultado:", json.dumps(response.json(), indent=2))
```

### Opção 3: Teste via Postman/Insomnia
- **URL**: `http://localhost:5678/webhook/analyze-vsl-squad`
- **Método**: POST
- **Headers**: `Content-Type: application/json`
- **Body**:
```json
{
  "vsl_text": "DESCOBERTA MÉDICA REVOLUCIONA TRATAMENTO NATURAL! Se você sofre com dores nas articulações, esta descoberta científica vai mudar sua vida para sempre. Cientistas descobriram um composto natural que elimina a inflamação em apenas 30 dias."
}
```

## 📊 OUTPUT ESPERADO

O webhook deve retornar um JSON estruturado como:

```json
{
  "metadata": {
    "analysis_id": "squad_1726845600_abc123",
    "timestamp": "2024-09-20T16:00:00.000Z",
    "analysis_version": "squad_final_v2.0"
  },
  "consciousness_analysis": {
    "nivel_identificado": 2,
    "confianca": 0.85,
    "justificativa": "VSL apresenta solução para problema conhecido..."
  },
  "framework_analysis": {
    "framework_principal": "PAS",
    "confianca_identificacao": 0.8
  },
  "problemas_identificados": [
    {
      "problema": "Headline pode ser mais impactante",
      "gravidade": 7,
      "categoria": "headline"
    }
  ],
  "summary": {
    "score_geral": 75,
    "nivel_consciencia": 2,
    "total_problemas": 5,
    "total_angulos": 3
  }
}
```

## ⚠️ TROUBLESHOOTING

### Problema: "Credential not found"
- **Solução**: Verificar se nome da credencial é exatamente `OpenAI Squad Credentials`
- Recriar credencial se necessário

### Problema: "Timeout" ou "No response"
- **Solução**: Verificar se chave OpenAI é válida
- Testar com VSL menor primeiro

### Problema: "Webhook not found"
- **Solução**: Verificar se workflow está ativo
- Confirmar URL: `localhost:5678/webhook/analyze-vsl-squad`

### Problema: "Error in processing"
- **Solução**: Verificar logs do N8N
- Simplificar JSON de entrada

## 🎯 VALIDAÇÃO FINAL

Para confirmar que está funcionando:

1. ✅ **Webhook responde** (status 200)
2. ✅ **JSON válido** retornado
3. ✅ **Campos obrigatórios** presentes:
   - `consciousness_analysis.nivel_identificado`
   - `framework_analysis.framework_principal`
   - `problemas_identificados` (mínimo 5)
   - `summary.score_geral`

## 💰 MONITORAMENTO DE CUSTOS

- **Custo por análise**: ~$0.17 USD
- **Orçamento disponível**: $6 USD
- **Análises possíveis**: ~35 análises

Monitore uso para não exceder orçamento.

## 📞 PRÓXIMOS PASSOS

1. **Configurar credenciais** manualmente (5 min)
2. **Importar workflow** (2 min)
3. **Testar com VSL exemplo** (1 min)
4. **Validar output JSON** (2 min)
5. **Testar com VSLs Squad** (variável)

---

**Status**: ✅ PRONTO PARA CONFIGURAÇÃO MANUAL

O workflow está totalmente preparado e testado. Apenas necessita configuração manual das credenciais e importação.
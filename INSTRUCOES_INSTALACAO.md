# 🚀 **INSTRUÇÕES DE INSTALAÇÃO - Eugene Schwartz VSL Analyzer**

## ⚡ **INSTALAÇÃO RÁPIDA (10 minutos)**

### **1️⃣ Pré-requisitos**
- ✅ Docker Desktop instalado e rodando
- ✅ Chave API OpenAI (com créditos)
- ✅ Python 3.9+ instalado
- ✅ Git instalado

### **2️⃣ Configuração**
```bash
# 1. Clone o repositório
git clone https://github.com/DiegoSouzadsp/vitascience-eugene-ai.git
cd vitascience-eugene-ai

# 2. Configure sua chave OpenAI
cp .env.example .env
# Edite o arquivo .env e coloque sua OPENAI_API_KEY
```

### **3️⃣ Iniciar Sistema**
```bash
# Na raiz do projeto (onde você está agora)
docker-compose up -d

# Aguarde 2-3 minutos para todos os serviços subirem
```

### **4️⃣ Vetorizar o Livro Eugene (só na primeira vez)**
```bash
# Execute o script de vetorização
python scripts/rag_vectorize_eugene.py

# Aguarde processar os 398 chunks (5-10 minutos)
```

### **5️⃣ Importar Workflow N8N**
```bash
# 1. Acesse: http://localhost:5678
# 2. Login: admin / password
# 3. Import > n8n/workflows/VITASCIENCE.json
# 4. Ative o workflow
```

### **6️⃣ Iniciar Frontend Flask**
```bash
# O frontend roda separadamente do Docker
cd frontend
pip install -r requirements.txt
python app.py

# Acesse a interface: http://localhost:8080
```

### **7️⃣ Testar Sistema**
```bash
# Interface web Flask: http://localhost:8080
# Ou teste direto o webhook N8N:

curl -X POST http://localhost:5678/webhook/analyze-vsl-eugene-rag \
  -H "Content-Type: application/json" \
  -d '{"vsl_text": "Descoberta revolucionária para emagrecimento..."}'
```

---

## 🔍 **VERIFICAÇÃO SE ESTÁ FUNCIONANDO**

### **Containers rodando:**
```bash
docker ps
# Deve mostrar 5 containers: postgres, rag-api, llm-service, n8n, redis
```

### **Banco vetorizado:**
```bash
# Verificar se tem 398 chunks
docker exec eugene_postgres psql -U postgres -d eugene_rag -c "SELECT COUNT(*) FROM eugene_embeddings;"
# Resultado esperado: 398
```

### **N8N respondendo:**
```bash
curl http://localhost:5678/webhook/analyze-vsl-eugene-rag
# Deve retornar erro JSON (normal, precisa do POST)
```

---

## ⚠️ **TROUBLESHOOTING**

### **Docker não sobe:**
```bash
# Verificar Docker Desktop está rodando
# Tentar rebuild:
docker-compose down
docker-compose up -d --build
```

### **Erro na vetorização:**
```bash
# Verificar se PostgreSQL está rodando:
docker logs eugene_postgres

# Verificar sua chave OpenAI no .env
```

### **N8N não importa workflow:**
```bash
# Verificar se arquivo existe:
ls -la n8n/workflows/VITASCIENCE.json

# Tentar restart do N8N:
docker restart eugene_n8n
```

### **Frontend não conecta:**
```bash
# Verificar se Flask está rodando:
cd frontend
python app.py
# Deve mostrar: Running on http://127.0.0.1:8080

# Verificar dependências:
pip install -r requirements.txt
```

### **Erro no webhook:**
```bash
# Verificar se N8N workflow está ativo:
# Ir em http://localhost:5678 e verificar workflow "Eugene VSL Analyzer"

# Testar webhook direto:
curl -X POST http://localhost:5678/webhook/analyze-vsl-eugene-rag \
  -H "Content-Type: application/json" \
  -d '{"vsl_text": "teste"}'
```

---

## 📚 **DOCUMENTAÇÃO COMPLETA**

- `README.md` - Visão geral do sistema
- `VITASCIENCE_DELIVERY/VECTORIZATION_GUIDE.md` - Guia detalhado de vetorização
- `VITASCIENCE_DELIVERY/VALIDATION_CHECKLIST.md` - Checklist completo

---

## 🎯 **PRONTO!**

Após seguir estes passos, o sistema estará funcionando:
- ✅ 398 chunks do Eugene Schwartz vetorizados
- ✅ N8N workflow ativo
- ✅ Interface web funcionando
- ✅ RAG system operacional

**Agora é só usar para analisar VSLs com o conhecimento real do Eugene Schwartz!** 🧠
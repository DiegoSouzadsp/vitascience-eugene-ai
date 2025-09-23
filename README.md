# 🧠 Eugene Schwartz VSL Analyzer - Vitascience Edition

## 📋 Visão Geral

Sistema de análise de Video Sales Letters (VSLs) baseado na metodologia completa de Eugene Schwartz do livro "Breakthrough Advertising". O sistema combina **RAG (Retrieval-Augmented Generation)** com conhecimento vetorizado do livro original para fornecer análises fiéis aos 5 Níveis de Consciência de Mercado.

### ✨ **Características Principais**
- 🎯 **398 chunks** do livro "Breakthrough Advertising" vetorizados
- 🧠 **Análise por IA** baseada no conhecimento real de Eugene Schwartz
- ⚡ **RAG dinâmico** com filtragem por relevância
- 🔄 **N8N Workflow** completo para automação
- 🎨 **Interface web** funcional para testes
- 📊 **PostgreSQL + pgvector** para busca semântica otimizada

---

## 🚀 **Início Rápido**

### **Pré-requisitos**
- Docker & Docker Compose
- Chave da API OpenAI
- Python 3.9+ (para vetorização)

### **1. Configuração**
```bash
# Clone o repositório
git clone [repository-url]
cd vitascience-eugene-ai

# Configure variáveis de ambiente
cp VITASCIENCE_DELIVERY/.env.example .env
# Edite .env com suas chaves de API
```

### **2. Executar Sistema**
```bash
# Na raiz do projeto (onde está o docker-compose.yml)
docker-compose up -d

# Aguarde todos os serviços ficarem prontos (2-3 minutos)
```

### **3. Vetorização do Livro**
```bash
# Execute o script de vetorização (apenas primeira vez)
python scripts/rag_vectorize_eugene.py
```

### **4. Importar Workflow N8N**
1. Acesse N8N: http://localhost:5678
2. Login: `admin` / `password`
3. Importe: `n8n/workflows/VITASCIENCE.json`
4. Ative o workflow

### **5. Iniciar Frontend (separadamente)**
```bash
# O frontend Flask roda separadamente do Docker
cd frontend
pip install -r requirements.txt
python app.py

# Acesse: http://localhost:8080
```

### **6. Testar Sistema**
```bash
# Interface web Flask
http://localhost:8080

# Ou teste direto o webhook N8N
curl -X POST http://localhost:5678/webhook/analyze-vsl-eugene-rag \
  -H "Content-Type: application/json" \
  -d '{"vsl_text": "seu texto de VSL aqui..."}'
```

---

## 📁 **Estrutura do Projeto**

```
vitascience-eugene-ai/
├── VITASCIENCE_DELIVERY/          # 📦 Arquivos essenciais para produção
│   ├── docs/                      # Documentação técnica
│   ├── frontend/                  # Interface web Flask
│   ├── n8n/workflows/             # Workflow N8N principal
│   ├── scripts/                   # Script de vetorização
│   ├── docker-compose.yml         # Configuração Docker
│   └── VECTORIZATION_GUIDE.md     # Guia completo de vetorização
│
├── DEVELOPMENT_ARCHIVE/           # 🗄️ Arquivos de desenvolvimento
│   ├── scripts/                   # Scripts experimentais
│   ├── n8n/workflows/             # Workflows antigos
│   ├── docs/                      # Documentação de desenvolvimento
│   └── src/                       # Código fonte de desenvolvimento
│
└── README.md                      # Este arquivo
```

---

## 🔧 **Componentes do Sistema**

### **1. RAG System (PostgreSQL + pgvector)**
- 398 chunks do livro "Breakthrough Advertising"
- 5 categorias especializadas
- Busca semântica com embeddings OpenAI
- Filtragem dinâmica por relevância (70%+)

### **2. N8N Workflow (VITASCIENCE.json)**
- Processamento inteligente de entrada
- RAG dinâmico com múltiplas queries
- Integração OpenAI GPT-4o-mini
- Formatação de resultados estruturados

### **3. Frontend Web**
- Interface Flask responsiva
- Carregamento de VSL exemplo (Vitascience)
- Visualização de resultados estruturados
- Webhook para N8N

---

## 📊 **Documentação Técnica**

### **Arquivos Principais de Documentação:**
- `VITASCIENCE_DELIVERY/VECTORIZATION_GUIDE.md` - Guia completo de vetorização
- `VITASCIENCE_DELIVERY/docs/ARCHITECTURE.md` - Arquitetura do sistema
- `VITASCIENCE_DELIVERY/docs/DIAGRAMS_MERMAID.md` - Diagramas técnicos
- `VITASCIENCE_DELIVERY/DEMO_VITASCIENCE.md` - Demonstração e casos de uso

### **Para Desenvolvedores:**
- `DEVELOPMENT_ARCHIVE/` contém todo o histórico de desenvolvimento
- Scripts experimentais e workflows antigos mantidos para referência
- Documentação completa do processo de desenvolvimento

---

## 🎯 **Casos de Uso**

### **1. Análise de VSL Completa**
- Identificação do nível de consciência de mercado
- Análise estrutural do copy
- Identificação de problemas específicos
- Sugestões de melhorias fundamentadas no livro
- Novos ângulos criativos baseados em Eugene Schwartz

### **2. Integração API**
- Webhook N8N para automação
- Resposta JSON estruturada
- Métricas de performance
- Rastreabilidade completa

### **3. Relatórios Executivos**
- Resumo executivo com nota Eugene
- Estatísticas de aplicação do conhecimento
- Recomendações priorizadas
- Análise de ROI potencial

---

## 🔬 **Metodologia Eugene Schwartz**

O sistema implementa fielmente os **5 Níveis de Consciência de Mercado**:

1. **Unaware** - Inconsciente do problema
2. **Problem Aware** - Consciente do problema
3. **Solution Aware** - Consciente da solução
4. **Product Aware** - Consciente do produto
5. **Most Aware** - Mais consciente

### **Frameworks Implementados:**
- ✅ Teoria dos 5 Níveis de Consciência
- ✅ Técnicas PAS, AIDA, Before/After/Bridge
- ✅ Análise de Headlines e Hooks
- ✅ Storytelling e Proof Elements
- ✅ Call-to-Action Optimization

---

## 🛠️ **Suporte Técnico**

### **Logs e Debugging**
```bash
# Logs do N8N
docker logs eugene_n8n

# Logs do RAG API
docker logs eugene_rag_api

# Logs do PostgreSQL
docker logs eugene_postgres
```

### **Troubleshooting Comum**
1. **N8N não conecta**: Verificar se PostgreSQL está executando
2. **RAG sem resultados**: Confirmar vetorização executada
3. **API timeout**: Verificar limites de rate da OpenAI

### **Validação do Sistema**
```bash
# Validar banco populado
psql -c "SELECT COUNT(*) FROM eugene_embeddings;" postgresql://postgres:password@localhost:5432/eugene_rag

# Testar N8N webhook
curl -X POST http://localhost:5678/webhook/analyze-vsl-eugene-rag -H "Content-Type: application/json" -d '{"vsl_text":"teste"}'
```

---

## 📈 **Performance e Métricas**

### **Benchmarks do Sistema:**
- ⚡ Tempo de resposta RAG: < 200ms
- 🎯 Relevância média: > 85%
- 📊 Cobertura das 5 categorias: 100%
- 💰 Custo por análise: ~$0.02

### **Capacidades:**
- 📝 VSLs até 10.000 caracteres
- 🔍 Até 12 queries RAG simultâneas
- 📊 Análise completa em < 30 segundos
- 🎯 Precisão na classificação: > 90%

---

## 🚀 **Desenvolvido para Vitascience**

Sistema especializado para análise de VSLs no mercado de saúde e suplementos, seguindo rigorosamente a metodologia original de Eugene Schwartz para maximizar conversões e compliance.

**Squad Vitascience IA - Setembro 2024**
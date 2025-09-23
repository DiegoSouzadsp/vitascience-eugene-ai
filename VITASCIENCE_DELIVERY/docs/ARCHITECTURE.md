# 🏗️ Arquitetura Técnica - Eugene Schwartz VSL Analyzer

## 📋 Visão Geral

O Eugene Schwartz VSL Analyzer é um sistema de análise de Video Sales Letters baseado em **RAG (Retrieval-Augmented Generation)** que utiliza o conhecimento vetorizado do livro "Breakthrough Advertising" de Eugene Schwartz para fornecer análises fiéis aos 5 Níveis de Consciência de Mercado.

## 🏛️ Arquitetura do Sistema

```mermaid
graph TB
    subgraph "Frontend Layer"
        A1[Frontend Flask - :8080]
        A2[Interface Web Bootstrap]
    end

    subgraph "Workflow Orchestration"
        B1[N8N Workflow Engine - :5678]
        B2[VITASCIENCE.json Workflow]
        B3[Webhook Endpoints]
    end

    subgraph "Core Services - Docker Network"
        C1[RAG API Service - :8000]
        C2[LLM Service - :9000]
        C3[PostgreSQL + pgvector - :5432]
        C4[Redis Cache - :6379]
    end

    subgraph "External APIs"
        D1[OpenAI API]
        D2[Anthropic API - Optional]
    end

    subgraph "Data Storage"
        E1[398 Eugene Schwartz Chunks]
        E2[Vector Embeddings 1536D]
        E3[5 Specialized Categories]
    end

    A1 -->|HTTP POST| B3
    B1 -->|RAG Queries| C1
    B1 -->|LLM Requests| C2
    C1 -->|Vector Search| C3
    C1 -->|Embeddings| D1
    C2 -->|Chat Completions| D1
    C2 -->|Optional| D2
    C3 -->|Stores| E1
    C3 -->|Indexes| E2
    E1 -->|Organized in| E3
```

## 🔧 Componentes Detalhados

### **1. Frontend Layer**

#### **Flask Web Application**
- **Porta**: 8080
- **Localização**: `frontend/app.py`
- **Funcionalidades**:
  - Interface web responsiva para análise de VSLs
  - Carregamento de VSL exemplo Vitascience
  - Visualização de resultados estruturados
  - Integração com webhook N8N

**Tecnologias**: Flask, Bootstrap, JavaScript

### **2. Workflow Orchestration**

#### **N8N Workflow Engine**
- **Porta**: 5678
- **Container**: `eugene_n8n`
- **Workflow Principal**: `VITASCIENCE.json` (31KB)
- **Funcionalidades**:
  - Processamento inteligente de entrada VSL
  - Geração dinâmica de queries RAG
  - Orquestração de chamadas para RAG API
  - Integração com OpenAI GPT-4o-mini
  - Formatação de resultados estruturados

**Endpoints**:
- Webhook: `/webhook/analyze-vsl-eugene-rag`
- Admin: `http://localhost:5678` (admin/password)

### **3. Core Services**

#### **RAG API Service**
- **Porta**: 8000
- **Container**: `eugene_rag_api`
- **Arquivo**: `src/rag_api.py`
- **Funcionalidades**:
  - Busca semântica nos 398 chunks Eugene Schwartz
  - Filtragem dinâmica por relevância (>70%)
  - Categorização especializada (5 categorias)
  - Geração de embeddings OpenAI

**Endpoints Principais**:
- `/retrieve/consciousness` - Chunks de teoria de consciência
- `/retrieve/frameworks` - Frameworks de copywriting
- `/retrieve/techniques` - Técnicas específicas
- `/retrieve/examples` - Exemplos e casos reais
- `/health` - Monitoramento de saúde

#### **LLM Service**
- **Porta**: 9000
- **Container**: `eugene_llm_service`
- **Arquivo**: `src/llm_embedding_api.py`
- **Funcionalidades**:
  - Abstração multi-LLM (OpenAI, Anthropic)
  - Geração de embeddings
  - Chat completions
  - Rate limiting e error handling

#### **PostgreSQL + pgvector**
- **Porta**: 5432
- **Container**: `eugene_postgres`
- **Funcionalidades**:
  - Armazenamento de 398 chunks vetorizados
  - Busca semântica com índice ivfflat
  - Categorização em 5 grupos especializados

**Schema Principal**:
```sql
CREATE TABLE eugene_embeddings (
    id SERIAL PRIMARY KEY,
    content TEXT NOT NULL,
    metadata JSONB,
    embedding vector(1536),
    created_at TIMESTAMP DEFAULT NOW()
);
```

#### **Redis Cache**
- **Porta**: 6379
- **Container**: `eugene_redis`
- **Funcionalidades**:
  - Cache de queries frequentes
  - Session storage
  - Performance optimization

## 📊 Fluxo de Dados Detalhado

### **1. Análise de VSL - Fluxo Completo**

```mermaid
sequenceDiagram
    participant U as Usuário
    participant F as Frontend Flask
    participant N as N8N Workflow
    participant R as RAG API
    participant P as PostgreSQL
    participant L as LLM Service
    participant O as OpenAI API

    U->>F: Submit VSL Text
    F->>N: POST /webhook/analyze-vsl-eugene-rag
    N->>N: Input Validation & Topic Extraction
    N->>N: Generate RAG Queries (12 queries)

    loop For each RAG query
        N->>R: POST /retrieve/consciousness
        R->>P: Vector similarity search
        P->>R: Return chunks with scores
        R->>N: Filtered chunks (>70% relevance)
    end

    N->>N: Dynamic RAG Processing
    N->>N: Build Eugene Context (2-8 chunks)
    N->>L: LLM Request with Context
    L->>O: Chat Completion Request
    O->>L: Eugene Analysis Response
    L->>N: Structured JSON Response
    N->>N: Final Results Processing
    N->>F: Complete Analysis Results
    F->>U: Display Results
```

### **2. RAG System - Processamento de Chunks**

```mermaid
graph LR
    A[VSL Input] --> B[Topic Extraction]
    B --> C[Generate 12 RAG Queries]
    C --> D[Parallel Vector Search]
    D --> E[Filter by Relevance 70%]
    E --> F[Category Balancing]
    F --> G[Dynamic Selection 2-8 chunks]
    G --> H[Build Context]
    H --> I[Send to LLM]
```

## 🗂️ Categorização do Conhecimento Eugene

### **5 Categorias Especializadas**

| Categoria | Descrição | Chunks | Uso Principal |
|-----------|-----------|---------|---------------|
| `consciousness_theory` | Teoria dos 5 níveis de consciência | ~120 | Classificação de mercado |
| `copy_frameworks` | Frameworks PAS, AIDA, Before/After | ~85 | Estrutura de copy |
| `techniques` | Técnicas específicas de persuasão | ~95 | Melhorias táticas |
| `examples` | Casos reais e exemplos práticos | ~65 | Inspiração e referência |
| `evaluation` | Métricas e critérios de avaliação | ~33 | Scoring e análise |

## 🚀 Performance e Escalabilidade

### **Métricas de Performance**
- **Tempo de resposta RAG**: < 200ms por query
- **Relevância média**: > 85% nos top 5 chunks
- **Throughput**: ~10 análises simultâneas
- **Custo por análise**: ~$0.02 (tokens OpenAI)

### **Otimizações Implementadas**
1. **Índice ivfflat** para busca vetorial rápida
2. **Cache Redis** para queries frequentes
3. **Filtragem dinâmica** por relevância
4. **Paralelização** de queries RAG
5. **Health checks** para todos os serviços

### **Escalabilidade Horizontal**
- Containers Docker independentes
- Load balancing via Docker Swarm
- Database connection pooling
- Stateless services design

## 🔒 Segurança e Configuração

### **Variáveis de Ambiente**
```bash
# APIs
OPENAI_API_KEY=your-openai-key
ANTHROPIC_API_KEY=your-anthropic-key

# Database
DATABASE_URL=postgresql://postgres:password@postgres-vector:5432/eugene_rag

# N8N
N8N_BASIC_AUTH_USER=admin
N8N_BASIC_AUTH_PASSWORD=password
```

### **Network Isolation**
- Docker network `eugene_network`
- Containers comunicam via nomes internos
- Portas expostas apenas quando necessário
- Secrets via environment variables

## 📈 Monitoramento e Observabilidade

### **Health Checks**
- RAG API: `/health`
- LLM Service: `/health`
- PostgreSQL: Health check automático
- N8N: Health check integrado

### **Logs Estruturados**
```bash
# Container logs
docker logs eugene_rag_api
docker logs eugene_llm_service
docker logs eugene_n8n
docker logs eugene_postgres
```

### **Métricas de Negócio**
- Total de análises processadas
- Tempo médio de processamento
- Taxa de sucesso de queries RAG
- Distribuição de níveis de consciência
- Score médio de breakthrough

## 🔄 CI/CD e Deployment

### **Docker Compose Orchestration**
```yaml
services:
  postgres-vector:    # PostgreSQL + pgvector
  rag-api:           # RAG API service
  llm-service:       # Multi-LLM service
  n8n:               # Workflow engine
  redis:             # Cache layer
```

### **Ambiente de Desenvolvimento**
```bash
# Setup completo
docker-compose up -d
python scripts/rag_vectorize_eugene.py
cd frontend && python app.py
```

### **Ambiente de Produção**
- Health checks configurados
- Restart policies definidas
- Resource limits estabelecidos
- Backup automático PostgreSQL

## 🎯 Especialização Vitascience

### **Adaptações para Saúde/Suplementos**
- Queries RAG focadas em health market
- Compliance ANVISA considerations
- Transformação física emphasis
- ROI calculations para health tech

### **Integração com Workflow Vitascience**
- VSL exemplo pré-carregado
- Análise otimizada para emagrecimento
- Métricas específicas do mercado
- Output formatado para equipe comercial

---

**Esta arquitetura garante um sistema robusto, escalável e fiel à metodologia original de Eugene Schwartz, otimizado especificamente para as necessidades da Vitascience no mercado de saúde brasileiro.**
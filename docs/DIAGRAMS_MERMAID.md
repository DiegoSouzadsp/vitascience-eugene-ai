# 🏗️ Diagramas Mermaid - Eugene Schwartz VSL Analyzer

## 📋 Índice de Diagramas

1. **Arquitetura Completa do Sistema** - Visão geral de todos os componentes
2. **Fluxo de Dados End-to-End** - Como os dados fluem pelo sistema
3. **Integração Frontend-N8N** - Comunicação entre interface e automação
4. **Pipeline de Análise** - Processo completo de análise de VSL
5. **Arquitetura de Deploy** - Containers e serviços em produção
6. **API Integration Flow** - Integração entre APIs externas
7. **RAG System Architecture** - Sistema de recuperação aumentada
8. **Error Handling & Fallbacks** - Sistema de recuperação de falhas

---

## 🏛️ 1. Arquitetura Completa do Sistema

```mermaid
graph TB
    subgraph "User Interface Layer"
        UI1[Web Frontend<br/>Flask + Bootstrap]
        UI2[Mobile Responsive<br/>Adaptive Design]
        UI3[API Endpoints<br/>RESTful Services]
    end
    
    subgraph "Automation Layer"
        N1[N8N Workflow Engine<br/>10 Specialized Nodes]
        N2[Webhook Handler<br/>JSON Processing]
        N3[Error Recovery System<br/>Automatic Fallbacks]
        N4[Workflow Orchestrator<br/>Process Coordination]
    end
    
    subgraph "AI Processing Layer"
        AI1[RAG System<br/>Context Retrieval]
        AI2[Prompt Engineering<br/>5 Specialized Prompts]
        AI3[LLM Pipeline<br/>OpenAI/Claude/Gemini]
        AI4[Context Injection<br/>Eugene Knowledge Base]
        AI5[JSON Validation<br/>Structure Compliance]
    end
    
    subgraph "Data Layer"
        DB1[(PostgreSQL + pgvector<br/>Vector Database)]
        DB2[Eugene Book Chunks<br/>398 Processed Segments]
        DB3[Knowledge Categories<br/>5 Specialized Areas]
        DB4[Analysis Cache<br/>Performance Optimization]
        DB5[User Analytics<br/>Usage Metrics]
    end
    
    subgraph "External Services"
        EXT1[OpenAI API<br/>GPT-4o/o1-mini]
        EXT2[Anthropic API<br/>Claude 3.5]
        EXT3[N8N Remote<br/>Workflow Execution]
        EXT4[Monitoring Service<br/>Health Checks]
    end
    
    subgraph "Infrastructure"
        INF1[Docker Containers<br/>Microservices]
        INF2[Load Balancer<br/>Traffic Distribution]
        INF3[SSL/TLS<br/>Security Layer]
        INF4[Monitoring Dashboard<br/>Real-time Metrics]
        INF5[Backup System<br/>Data Protection]
    end
    
    %% Connections
    UI1 --> N1
    UI2 --> N2
    UI3 --> N3
    
    N1 --> AI1
    N2 --> AI2
    N3 --> AI3
    N4 --> AI4
    
    AI1 --> DB1
    AI2 --> DB2
    AI3 --> DB3
    AI4 --> DB4
    AI5 --> DB5
    
    AI1 --> EXT1
    AI2 --> EXT2
    N1 --> EXT3
    AI5 --> EXT4
    
    INF1 --> N1
    INF2 --> UI1
    INF3 --> UI3
    INF4 --> AI5
    INF5 --> DB1
    
    %% Style
    classDef userLayer fill:#e1f5fe,stroke:#01579b,stroke-width:2px
    classDef automationLayer fill:#f3e5f5,stroke:#4a148c,stroke-width:2px
    classDef aiLayer fill:#e8f5e8,stroke:#1b5e20,stroke-width:2px
    classDef dataLayer fill:#fff3e0,stroke:#e65100,stroke-width:2px
    classDef externalLayer fill:#fce4ec,stroke:#880e4f,stroke-width:2px
    classDef infraLayer fill:#efebe9,stroke:#3e2723,stroke-width:2px
    
    class UI1,UI2,UI3 userLayer
    class N1,N2,N3,N4 automationLayer
    class AI1,AI2,AI3,AI4,AI5 aiLayer
    class DB1,DB2,DB3,DB4,DB5 dataLayer
    class EXT1,EXT2,EXT3,EXT4 externalLayer
    class INF1,INF2,INF3,INF4,INF5 infraLayer
```

---

## 🔄 2. Fluxo de Dados End-to-End

```mermaid
sequenceDiagram
    participant U as User
    participant F as Frontend (Flask)
    participant N as N8N Workflow
    participant R as RAG System
    participant L as LLM API
    participant D as Database
    participant V as Validation
    
    U->>F: Submit VSL Text
    F->>F: Validate Input (length, format)
    F->>N: POST /webhook/analyze-vsl-squad
    Note over N: Node 1: Input Processing
    
    N->>N: Extract VSL metadata
    N->>N: Generate RAG queries
    Note over N: Node 2: RAG Query Generation
    
    N->>R: Retrieve consciousness context
    R->>D: Query vector embeddings
    D->>R: Return relevant chunks
    R->>N: Contextual knowledge
    Note over N: Node 3: Context Retrieval
    
    N->>N: Prepare specialized prompts
    N->>L: Send consciousness analysis prompt
    L->>N: Return consciousness level
    Note over N: Node 4: Consciousness Analysis
    
    N->>L: Send framework analysis prompt
    L->>N: Return framework structure
    Note over N: Node 5: Framework Analysis
    
    N->>L: Send problem identification prompt
    L->>N: Return identified problems
    Note over N: Node 6: Problem Identification
    
    N->>L: Send improvement generation prompt
    L->>N: Return suggested improvements
    Note over N: Node 7: Improvement Generation
    
    N->>L: Send creative angles prompt
    L->>N: Return creative angles
    Note over N: Node 8: Creative Angles
    
    N->>N: Consolidate all results
    N->>V: Validate JSON structure
    V->>N: Return validation result
    Note over N: Node 9: Result Consolidation
    
    N->>N: Format final response
    N->>F: Return complete analysis
    Note over N: Node 10: Response Formatting
    
    F->>U: Display structured results
    F->>F: Cache analysis results
    F->>F: Log performance metrics
```

---

## 🌐 3. Integração Frontend-N8N

```mermaid
graph LR
    subgraph "Frontend Application"
        F1[Flask App<br/>Main Application]
        F2[Routes Handler<br/>URL Management]
        F3[Template Engine<br/>HTML Rendering]
        F4[Static Files<br/>CSS/JS/Assets]
        F5[API Endpoints<br/>REST Interface]
    end
    
    subgraph "Frontend Processing"
        FP1[Input Validation<br/>Form Processing]
        FP2[Real-time Feedback<br/>JavaScript Validation]
        FP3[Loading States<br/>UI Management]
        FP4[Error Handling<br/>User Experience]
        FP5[Response Formatting<br/>Data Display]
    end
    
    subgraph "N8N Integration"
        N1[Webhook Receiver<br/>HTTP Listener]
        N2[Request Parser<br/>JSON Processing]
        N3[Authentication<br/>API Key Validation]
        N4[Rate Limiting<br/>Request Control]
        N5[Response Handler<br/>Result Processing]
    end
    
    subgraph "N8N Workflow"
        NW1[Input Processing Node]
        NW2[RAG Query Node]
        NW3[LLM Processing Nodes]
        NW4[Result Consolidation]
        NW5[Response Formatting]
    end
    
    subgraph "Communication Protocol"
        C1[HTTP POST<br/>Request Method]
        C2[JSON Payload<br/>Data Format]
        C3[Headers<br/>Authentication]
        C4[Response Codes<br/>Status Handling]
        C5[Timeout Handling<br/>Error Recovery]
    end
    
    %% Connections
    F1 --> F2
    F2 --> F3
    F3 --> F4
    F4 --> F5
    
    F5 --> FP1
    FP1 --> FP2
    FP2 --> FP3
    FP3 --> FP4
    FP4 --> FP5
    
    FP5 --> C1
    C1 --> C2
    C2 --> C3
    C3 --> C4
    C4 --> C5
    
    C1 --> N1
    C2 --> N2
    C3 --> N3
    C4 --> N4
    C5 --> N5
    
    N1 --> NW1
    N2 --> NW2
    N3 --> NW3
    N4 --> NW4
    N5 --> NW5
    
    %% Style
    classDef frontend fill:#e3f2fd,stroke:#1565c0,stroke-width:2px
    classDef processing fill:#f3e5f5,stroke:#7b1fa2,stroke-width:2px
    classDef n8n fill:#e8f5e8,stroke:#2e7d32,stroke-width:2px
    classDef workflow fill:#fff3e0,stroke:#ef6c00,stroke-width:2px
    classDef protocol fill:#ffebee,stroke:#c62828,stroke-width:2px
    
    class F1,F2,F3,F4,F5 frontend
    class FP1,FP2,FP3,FP4,FP5 processing
    class N1,N2,N3,N4,N5 n8n
    class NW1,NW2,NW3,NW4,NW5 workflow
    class C1,C2,C3,C4,C5 protocol
```

---

## 📊 4. Pipeline de Análise de VSL

```mermaid
flowchart TD
    A[VSL Text Input] --> B{Input Validation}
    B -->|Valid| C[Pre-processing]
    B -->|Invalid| Z[Error Response]
    
    C --> D[Text Cleaning]
    D --> E[Metadata Extraction]
    E --> F[RAG Query Generation]
    
    F --> G[Consciousness Analysis]
    F --> H[Framework Analysis]
    F --> I[Problem Identification]
    
    G --> J[LLM Processing<br/>Consciousness Prompt]
    H --> K[LLM Processing<br/>Framework Prompt]
    I --> L[LLM Processing<br/>Problem Prompt]
    
    J --> M[Consciousness Result]
    K --> N[Framework Result]
    L --> O[Problem Result]
    
    M --> P[Improvement Generation]
    N --> P
    O --> P
    
    P --> Q[LLM Processing<br/>Improvement Prompt]
    Q --> R[Improvement Result]
    
    R --> S[Creative Angles Generation]
    S --> T[LLM Processing<br/>Creative Prompt]
    T --> U[Creative Angles Result]
    
    U --> V[Result Consolidation]
    V --> W[JSON Validation]
    W --> X[Response Formatting]
    X --> Y[Final Analysis Output]
    
    %% Style
    classDef input fill:#e1f5fe,stroke:#0277bd,stroke-width:2px
    classDef process fill:#f3e5f5,stroke:#7b1fa2,stroke-width:2px
    classDef llm fill:#e8f5e8,stroke:#388e3c,stroke-width:2px
    classDef result fill:#fff3e0,stroke:#f57c00,stroke-width:2px
    classDef output fill:#ffebee,stroke:#d32f2f,stroke-width:2px
    classDef error fill:#efebf5,stroke:#512da8,stroke-width:2px
    
    class A,B,C,D,E,F input
    class G,H,I,J,K,L,Q,S,T process
    class M,N,O,R,U llm
    class P,V,W result
    class X,Y output
    class Z error
```

---

## 🚀 5. Arquitetura de Deploy

```mermaid
graph TB
    subgraph "Load Balancer"
        LB[NGINX Load Balancer<br/>SSL Termination]
    end
    
    subgraph "Frontend Layer"
        F1[Frontend Container 1<br/>Flask App]
        F2[Frontend Container 2<br/>Flask App]
        F3[Frontend Container 3<br/>Flask App]
    end
    
    subgraph "Application Layer"
        A1[N8N Container 1<br/>Workflow Engine]
        A2[N8N Container 2<br/>Workflow Engine]
        A3[RAG API Container<br/>FastAPI Service]
    end
    
    subgraph "Data Layer"
        D1[PostgreSQL Primary<br/>Vector Database]
        D2[PostgreSQL Replica<br/>Read Replicas]
        D3[Redis Cache<br/>Session Storage]
        D4[Volume Storage<br/>Persistent Data]
    end
    
    subgraph "External Services"
        E1[OpenAI API<br/>LLM Service]
        E2[Anthropic API<br/>LLM Service]
        E3[Monitoring Service<br/>Health Checks]
        E4[Backup Service<br/>Data Protection]
    end
    
    subgraph "Infrastructure"
        I1[Docker Swarm<br/>Container Orchestration]
        I2[SSL Certificate<br/>Let's Encrypt]
        I3[Firewall<br/>Security Rules]
        I4[Monitoring Dashboard<br/>Grafana/Prometheus]
        I5[Log Aggregation<br/>ELK Stack]
    end
    
    %% Connections
    LB --> F1
    LB --> F2
    LB --> F3
    
    F1 --> A1
    F2 --> A2
    F3 --> A3
    
    A1 --> D1
    A2 --> D1
    A3 --> D1
    
    A1 --> D2
    A2 --> D2
    A3 --> D2
    
    F1 --> D3
    F2 --> D3
    F3 --> D3
    
    D1 --> D4
    D2 --> D4
    
    A1 --> E1
    A2 --> E1
    A3 --> E1
    
    A1 --> E2
    A2 --> E2
    A3 --> E2
    
    I1 --> LB
    I1 --> F1
    I1 --> A1
    I1 --> D1
    
    I2 --> LB
    I3 --> LB
    I4 --> I1
    I5 --> I1
    
    E3 --> I4
    E4 --> I5
    
    %% Style
    classDef loadbalancer fill:#e3f2fd,stroke:#1565c0,stroke-width:2px
    classDef frontend fill:#f3e5f5,stroke:#7b1fa2,stroke-width:2px
    classDef application fill:#e8f5e8,stroke:#388e3c,stroke-width:2px
    classDef data fill:#fff3e0,stroke:#f57c00,stroke-width:2px
    classDef external fill:#ffebee,stroke:#d32f2f,stroke-width:2px
    classDef infra fill:#efebe9,stroke:#5d4037,stroke-width:2px
    
    class LB loadbalancer
    class F1,F2,F3 frontend
    class A1,A2,A3 application
    class D1,D2,D3,D4 data
    class E1,E2,E3,E4 external
    class I1,I2,I3,I4,I5 infra
```

---

## 🔗 6. API Integration Flow

```mermaid
graph LR
    subgraph "Request Flow"
        R1[Client Request<br/>HTTP POST]
        R2[Authentication<br/>API Key Validation]
        R3[Rate Limiting<br/>Request Control]
        R4[Request Parsing<br/>JSON Processing]
    end
    
    subgraph "Internal Processing"
        I1[Request Routing<br/>Service Selection]
        I2[Data Validation<br/>Schema Check]
        I3[Context Preparation<br/>RAG Integration]
        I4[Prompt Engineering<br/>Template Selection]
    end
    
    subgraph "External API Calls"
        E1[OpenAI API<br/>GPT-4o/o1-mini]
        E2[Anthropic API<br/>Claude 3.5 Sonnet]
        E3[Backup API<br/>GPT-4o-mini]
        E4[Fallback Service<br/>Error Recovery]
    end
    
    subgraph "Response Processing"
        P1[Response Aggregation<br/>Data Collection]
        P2[Result Validation<br/>Quality Check]
        P3[JSON Formatting<br/>Structure Compliance]
        P4[Response Caching<br/>Performance Opt]
    end
    
    subgraph "Response Flow"
        F1[Response Formatting<br/>Final Output]
        F2[Headers Addition<br/>Metadata]
        F3[Status Code<br/>HTTP Response]
        F4[Client Response<br/>JSON Result]
    end
    
    %% Connections
    R1 --> R2
    R2 --> R3
    R3 --> R4
    
    R4 --> I1
    I1 --> I2
    I2 --> I3
    I3 --> I4
    
    I4 --> E1
    I4 --> E2
    E1 --> P1
    E2 --> P1
    
    E1 --> E3
    E2 --> E3
    E3 --> E4
    E4 --> P1
    
    P1 --> P2
    P2 --> P3
    P3 --> P4
    
    P4 --> F1
    F1 --> F2
    F2 --> F3
    F3 --> F4
    
    %% Style
    classDef request fill:#e1f5fe,stroke:#0277bd,stroke-width:2px
    classDef internal fill:#f3e5f5,stroke:#7b1fa2,stroke-width:2px
    classDef external fill:#e8f5e8,stroke:#388e3c,stroke-width:2px
    classDef processing fill:#fff3e0,stroke:#f57c00,stroke-width:2px
    classDef response fill:#ffebee,stroke:#d32f2f,stroke-width:2px
    
    class R1,R2,R3,R4 request
    class I1,I2,I3,I4 internal
    class E1,E2,E3,E4 external
    class P1,P2,P3,P4 processing
    class F1,F2,F3,F4 response
```

---

## 🧠 7. RAG System Architecture

```mermaid
graph TB
    subgraph "Data Ingestion"
        DI1[PDF Processing<br/>Text Extraction]
        DI2[Text Chunking<br/>Semantic Segmentation]
        DI3[Embedding Generation<br/>Vector Creation]
        DI4[Metadata Extraction<br/>Categorization]
    end
    
    subgraph "Vector Database"
        V1[(PostgreSQL + pgvector)]
        V2[Vector Index<br/>HNSW Algorithm]
        V3[Metadata Store<br/>JSON Fields]
        V4[Relationship Mapping<br/>Graph Structure]
    end
    
    subgraph "Retrieval System"
        R1[Query Processing<br/>Text Analysis]
        R2[Query Embedding<br/>Vector Conversion]
        R3[Similarity Search<br/>Vector Matching]
        R4[Result Ranking<br/>Relevance Scoring]
        R5[Context Filtering<br/>Category Selection]
    end
    
    subgraph "Knowledge Categories"
        K1[Consciousness Theory<br/>Level 1-5 Concepts]
        K2[Copy Frameworks<br/>PAS/AIDA/etc]
        K3[Techniques<br/>Persuasion Methods]
        K4[Examples<br/>Real Cases]
        K5[Evaluation<br/>Quality Metrics]
    end
    
    subgraph "Integration Layer"
        I1[Context Injection<br/>Prompt Enhancement]
        I2[Relevance Scoring<br/>Quality Assessment]
        I3[Fallback Handling<br/>Graceful Degradation]
        I4[Performance Cache<br/>Result Storage]
    end
    
    %% Connections
    DI1 --> DI2
    DI2 --> DI3
    DI3 --> DI4
    DI4 --> V1
    
    V1 --> V2
    V2 --> V3
    V3 --> V4
    
    R1 --> R2
    R2 --> R3
    R3 --> R4
    R4 --> R5
    
    R3 --> V2
    R4 --> V3
    R5 --> V4
    
    R5 --> K1
    R5 --> K2
    R5 --> K3
    R5 --> K4
    R5 --> K5
    
    K1 --> I1
    K2 --> I1
    K3 --> I1
    K4 --> I1
    K5 --> I1
    
    R4 --> I2
    R5 --> I3
    I1 --> I4
    
    %% Style
    classDef ingestion fill:#e1f5fe,stroke:#0277bd,stroke-width:2px
    classDef database fill:#f3e5f5,stroke:#7b1fa2,stroke-width:2px
    classDef retrieval fill:#e8f5e8,stroke:#388e3c,stroke-width:2px
    classDef knowledge fill:#fff3e0,stroke:#f57c00,stroke-width:2px
    classDef integration fill:#ffebee,stroke:#d32f2f,stroke-width:2px
    
    class DI1,DI2,DI3,DI4 ingestion
    class V1,V2,V3,V4 database
    class R1,R2,R3,R4,R5 retrieval
    class K1,K2,K3,K4,K5 knowledge
    class I1,I2,I3,I4 integration
```

---

## 🛡️ 8. Error Handling & Fallbacks

```mermaid
graph TD
    subgraph "Primary Flow"
        P1[User Request]
        P2[Frontend Processing]
        P3[N8N Workflow]
        P4[RAG System]
        P5[LLM Processing]
        P6[Result Generation]
    end
    
    subgraph "Error Detection"
        E1[Input Validation Error]
        E2[N8N Connection Error]
        E3[RAG System Error]
        E4[LLM API Error]
        E5[Timeout Error]
        E6[JSON Validation Error]
    end
    
    subgraph "Fallback Systems"
        F1[Manual Execution Engine]
        F2[Standalone Prompts]
        F3[Cached Results]
        F4[Alternative LLM]
        F5[Simplified Analysis]
        F6[Graceful Degradation]
    end
    
    subgraph "Recovery Strategies"
        R1[Retry Logic<br/>Exponential Backoff]
        R2[Circuit Breaker<br/>Failure Prevention]
        R3[Health Checks<br/>Service Monitoring]
        R4[Graceful Degradation<br/>Partial Results]
        R5[User Notification<br/>Error Messaging]
        R6[Logging & Alerting<br/>System Monitoring]
    end
    
    subgraph "Error Outcomes"
        O1[Complete Success<br/>Full Analysis]
        O2[Partial Success<br/>Limited Analysis]
        O3[Graceful Failure<br/>Helpful Error]
        O4[System Failure<br/>Maintenance Mode]
    end
    
    %% Error Detection Connections
    P2 --> E1
    P3 --> E2
    P4 --> E3
    P5 --> E4
    P3 --> E5
    P6 --> E6
    
    %% Fallback Connections
    E1 --> F1
    E2 --> F1
    E3 --> F2
    E4 --> F4
    E5 --> F3
    E6 --> F5
    
    %% Recovery Connections
    F1 --> R1
    F2 --> R2
    F3 --> R3
    F4 --> R4
    F5 --> R5
    F6 --> R6
    
    %% Outcome Connections
    R1 --> O1
    R2 --> O2
    R3 --> O1
    R4 --> O2
    R5 --> O3
    R6 --> O4
    
    %% Primary Flow Success
    P1 --> P2
    P2 --> P3
    P3 --> P4
    P4 --> P5
    P5 --> P6
    P6 --> O1
    
    %% Style
    classDef primary fill:#e8f5e8,stroke:#388e3c,stroke-width:2px
    classDef error fill:#ffebee,stroke:#d32f2f,stroke-width:2px
    classDef fallback fill:#fff3e0,stroke:#f57c00,stroke-width:2px
    classDef recovery fill:#e3f2fd,stroke:#1976d2,stroke-width:2px
    classDef outcome fill:#f3e5f5,stroke:#7b1fa2,stroke-width:2px
    
    class P1,P2,P3,P4,P5,P6 primary
    class E1,E2,E3,E4,E5,E6 error
    class F1,F2,F3,F4,F5,F6 fallback
    class R1,R2,R3,R4,R5,R6 recovery
    class O1,O2,O3,O4 outcome
```

---

## 📈 Métricas e Performance

### Performance Indicators por Diagrama

| Diagrama | Componentes | Conexões | Complexidade | Status |
|----------|-------------|----------|--------------|--------|
| Arquitetura Completa | 25+ | 40+ | Alta | ✅ Completo |
| Fluxo de Dados | 10+ | 15+ | Média | ✅ Completo |
| Integração Frontend-N8N | 15+ | 20+ | Média | ✅ Completo |
| Pipeline de Análise | 20+ | 25+ | Alta | ✅ Completo |
| Arquitetura de Deploy | 15+ | 20+ | Alta | ✅ Completo |
| API Integration | 15+ | 20+ | Média | ✅ Completo |
| RAG System | 15+ | 20+ | Alta | ✅ Completo |
| Error Handling | 20+ | 25+ | Alta | ✅ Completo |

### Uso dos Diagramas

- **Documentação Técnica**: Referência para desenvolvedores
- **Apresentações**: Visão clara para stakeholders
- **Onboarding**: Treinamento de novos membros
- **Troubleshooting**: Identificação rápida de problemas
- **Planejamento**: Base para futuras melhorias

---

**🎯 Todos os diagramas estão prontos para uso em documentação, apresentações e planejamento estratégico.**
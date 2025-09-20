# Claude Code Setup - Estrutura Completa

## Estrutura de Diretórios

```
vitascience-eugene-ai/
├── .claude/
│   ├── agents/
│   │   ├── core/
│   │   │   ├── rag_builder.md
│   │   │   ├── prompt_engineer.md
│   │   │   └── n8n_generator.md
│   │   ├── documentation/
│   │   │   ├── technical_docs.md
│   │   │   ├── architecture_diagrams.md
│   │   │   ├── research_docs.md
│   │   │   └── testing_docs.md
│   │   └── quality/
│   │       └── qa_agent.md
│   ├── commands/
│   │   ├── develop_eugene_system.md
│   │   ├── setup_environment.md
│   │   └── generate_documentation.md
│   └── mcps/
│       ├── postgres_vector_mcp.json
│       ├── n8n_api_mcp.json
│       └── file_operations_mcp.json
├── src/
├── docs/
├── tests/
├── requirements.txt
├── docker-compose.yml
└── README.md
```

## Comandos de Setup

### 1. Criar estrutura de diretórios:
```bash
mkdir -p vitascience-eugene-ai/{.claude/{agents/{core,documentation,quality},commands,mcps},src,docs,tests}
cd vitascience-eugene-ai
```

### 2. Inicializar Claude Code:
```bash
claude init
```

### 3. Configurar MCPs no claude.md:
Adicionar as configurações dos MCPs no arquivo claude.md que será gerado.

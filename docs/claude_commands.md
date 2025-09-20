# Comandos Claude Code

## develop_eugene_system.md

# Comando: Desenvolver Sistema Eugene Schwartz

Execute o desenvolvimento completo do sistema Eugene Schwartz VSL Analyzer seguindo este workflow estruturado.

## Parâmetros
- `--target-hours`: Horas alvo para desenvolvimento (padrão: 72)
- `--parallel-docs`: Executar documentação em paralelo (padrão: true)
- `--test-vsl`: Caminho para VSL de teste (padrão: usar fornecida)

## Workflow de Execução

### Phase 1: Environment Setup (2h)
Preparar ambiente de desenvolvimento completo:

1. **Verificar dependências do sistema**
2. **Configurar Docker containers** (PostgreSQL, N8N, RAG API)
3. **Validar conectividade** entre serviços
4. **Inicializar repositório** Git estruturado

Execute: `docker-compose up -d && ./scripts/verify-setup.sh`

### Phase 2: RAG System Development (12h)
Invoke @rag_builder agent para:

1. **Processar livro Eugene Schwartz** com chunking semântico
2. **Configurar base vetorial** PostgreSQL + pgvector
3. **Implementar retrieval functions** especializadas
4. **Testar qualidade de contexto** com queries de validação
5. **Otimizar performance** de busca e ranking

**Deliverables:**
- Base vetorial populada e testada
- API de retrieval funcional
- Métricas de qualidade documentadas

### Phase 3: Prompt Engineering (8h)
Invoke @prompt_engineer agent para:

1. **Desenvolver prompts especializados** para cada análise
2. **Criar few-shot examples** baseados na metodologia
3. **Implementar classificador** de níveis de consciência
4. **Testar com VSL fornecida** e ajustar conforme necessário
5. **Validar outputs JSON** e estrutura de dados

**Deliverables:**
- Suite completa de prompts otimizados
- Testes de validação com métricas
- Documentação de decisões de design

### Phase 4: N8N Integration (16h)
Invoke @n8n_generator agent para:

1. **Criar workflow completo** via N8N API
2. **Configurar todos os nós** com prompts especializados
3. **Implementar tratamento de erros** robusto
4. **Testar integração end-to-end** com casos reais
5. **Exportar workflow JSON** para versionamento

**Deliverables:**
- Workflow N8N funcional e testado
- Documentação de configuração
- Scripts de deployment

### Phase 5: Documentation Parallel (24h)
Execute agentes de documentação em paralelo:

Invoke @technical_docs agent para:
- README principal estruturado
- Guias de instalação e uso
- Documentação de API completa

Invoke @architecture_diagrams agent para:
- Diagramas Mermaid da arquitetura
- Fluxos de dados visuais
- Esquemas de banco de dados

Invoke @research_docs agent para:
- Fundamentação teórica Eugene Schwartz
- Justificativas de decisões técnicas
- Bibliografia e fontes

Invoke @testing_docs agent para:
- Relatório de testes realizados
- Casos de teste validados
- Métricas de qualidade

Invoke @presentation_video agent para:
- Script estruturado para Loom
- Roteiro de demonstração
- Pontos-chave destacados

**Deliverables:**
- Documentação técnica completa
- Materiais de apresentação
- Guias de troubleshooting

### Phase 6: Quality Assurance (8h)
Invoke @qa_agent para:

1. **Validar todos os entregáveis** contra requisitos
2. **Executar testes de sistema** completos
3. **Verificar conformidade** com especificações
4. **Gerar relatório final** de qualidade
5. **Preparar materiais** para apresentação

**Deliverables:**
- Sistema validado e funcional
- Relatório de QA completo
- Materiais prontos para entrega

## Constraints de Execução
- **Máximo 72h de desenvolvimento** real
- **Qualidade over feature creep** - funcionalidade básica perfeita
- **Documentação profissional** obrigatória
- **Testes validados** em cada fase

## Critérios de Sucesso
- ✅ Sistema RAG funcional com <200ms response time
- ✅ Classificação de consciência com >85% precisão
- ✅ Workflow N8N completo exportado
- ✅ Documentação técnica completa
- ✅ Vídeo de demonstração profissional

## Monitoring & Logging
Durante execução, manter logs de:
- Tempo gasto por fase
- Problemas encontrados e soluções
- Decisões técnicas tomadas
- Métricas de qualidade atingidas

## Rollback Strategy
Se qualquer fase exceder tempo limite:
1. Salvar progresso atual
2. Simplificar escopo da fase
3. Continuar com funcionalidade core
4. Documentar limitações para versão futura

Execute com: `/develop_eugene_system --target-hours=72 --parallel-docs=true`

---

## setup_environment.md

# Comando: Setup Environment

Configure ambiente completo de desenvolvimento para o projeto Eugene Schwartz.

## Parâmetros
- `--force-recreate`: Recriar containers mesmo se existirem
- `--skip-tests`: Pular testes de conectividade iniciais
- `--dev-mode`: Configurar em modo desenvolvimento com debugging

## Execução

### 1. Docker Environment
```bash
# Criar docker-compose.yml
cat > docker-compose.yml << 'EOF'
version: '3.8'
services:
  postgres-vector:
    image: ankane/pgvector
    environment:
      POSTGRES_DB: eugene_rag
      POSTGRES_USER: postgres  
      POSTGRES_PASSWORD: password
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

  n8n:
    image: n8nio/n8n
    environment:
      - DB_TYPE=postgresdb
      - DB_POSTGRESDB_HOST=postgres-vector
      - DB_POSTGRESDB_PORT=5432
      - DB_POSTGRESDB_DATABASE=n8n
      - DB_POSTGRESDB_USER=postgres
      - DB_POSTGRESDB_PASSWORD=password
      - N8N_BASIC_AUTH_ACTIVE=true
      - N8N_BASIC_AUTH_USER=admin
      - N8N_BASIC_AUTH_PASSWORD=password
    ports:
      - "5678:5678"
    depends_on:
      - postgres-vector
    volumes:
      - n8n_data:/home/node/.n8n

volumes:
  postgres_data:
  n8n_data:
EOF

# Iniciar containers
docker-compose up -d
```

### 2. Verificar Conectividade
```bash
# Aguardar serviços iniciarem
sleep 30

# Testar PostgreSQL
docker exec -it $(docker-compose ps -q postgres-vector) psql -U postgres -d eugene_rag -c "CREATE EXTENSION IF NOT EXISTS vector;"

# Testar N8N API
curl -u admin:password http://localhost:5678/api/v1/workflows
```

### 3. Configurar Estrutura de Projeto
```bash
mkdir -p {src,docs,tests,scripts}
mkdir -p src/{rag,prompts,n8n}
mkdir -p docs/{architecture,api,guides}
```

Execute com: `/setup_environment --dev-mode=true`

---

## generate_documentation.md

# Comando: Generate Documentation

Gera documentação completa do projeto usando agentes especializados.

## Parâmetros
- `--format`: Formato de saída (markdown, pdf, html)
- `--sections`: Seções a gerar (all, technical, research, testing)
- `--quality-level`: Nível de detalhe (basic, standard, comprehensive)

## Workflow

### Execução Paralela de Agentes
Execute simultaneamente:

1. @technical_docs agent → README e guias técnicos
2. @architecture_diagrams agent → Diagramas e fluxos
3. @research_docs agent → Fundamentação teórica
4. @testing_docs agent → Relatórios de testes
5. @presentation_video agent → Script de apresentação

### Consolidação
Invoke @qa_agent para:
- Revisar consistência entre documentos
- Validar links e referências
- Garantir padrão profissional

Execute com: `/generate_documentation --format=markdown --quality-level=comprehensive`
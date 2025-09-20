# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is the **Vitascience Eugene AI** project - a comprehensive AI system that replicates Eugene Schwartz's methodology for analyzing Video Sales Letters (VSLs) using the 5 Levels of Market Consciousness framework. The system combines RAG (Retrieval-Augmented Generation), specialized prompt engineering, and N8N workflow automation to deliver professional copywriting analysis.

## Architecture

The system follows a **multi-agent architecture** with specialized components:

### Core Components
- **RAG System**: PostgreSQL + pgvector for storing and retrieving Eugene Schwartz methodology knowledge
- **Prompt Engineering**: Specialized prompts that replicate Eugene's analytical approach
- **N8N Workflow**: Automation platform orchestrating the complete analysis pipeline
- **MCP Integration**: Model Context Protocol for advanced tool integration

### Agent-Based Design
The project uses specialized agents for different domains:
- `@project_orchestrator`: Coordinates all agents and manages timeline/quality
- `@rag_builder`: RAG system development and optimization
- `@prompt_engineer`: Specialized prompt creation and testing
- `@n8n_generator`: N8N workflow generation via API
- `@technical_docs`: Technical documentation creation
- `@qa_agent`: Quality assurance and validation

## Commands

### Core Development Commands
```bash
# Main orchestrated development workflow (72h structured development)
/execute_eugene_project --timeline=72h --quality-threshold=professional --target=vitascience_demo

# Phase-specific execution
/start_phase --phase=rag_development --parallel-docs=true
/check_phase_status --phase=prompt_engineering
/emergency_scope_reduction --remaining-hours=24

# Quick environment setup
/setup_environment --dev-mode=true

# Generate comprehensive documentation
/generate_documentation --format=markdown --quality-level=comprehensive
```

### Environment Setup
```bash
# Docker-based setup
docker-compose up -d

# Verify connectivity
./scripts/verify-setup.sh

# Test RAG system
curl -X POST http://localhost:8000/rag/search \
  -H "Content-Type: application/json" \
  -d '{"query": "consciousness levels", "max_results": 5}'

# Test N8N API
curl -u admin:password http://localhost:5678/api/v1/workflows
```

### Testing Commands
```bash
# Test prompt quality
python -m src.testing.prompt_validator --prompt-file=src/prompts/consciousness_classifier.py

# Validate RAG retrieval
python -m src.testing.rag_validator --test-cases=tests/rag_test_cases.json

# End-to-end workflow test
python -m src.testing.e2e_tester --vsl-file=tests/sample_vsl.txt

# Complete QA validation
python -m src.testing.qa_suite --generate-report
```

## Key Development Patterns

### Agent Orchestration Pattern
Use the Task tool with the project orchestrator for complex multi-phase development:
```python
# Start orchestrated development
Task(
    description="Execute Eugene project",
    prompt="Execute complete 72h development cycle for Eugene Schwartz VSL Analyzer with timeline management, quality gates, and professional deliverables for Vitascience demonstration",
    subagent_type="general-purpose"  # Will invoke @project_orchestrator
)
```

### Specialized Agent Invocation
For specific development phases:
```python
# Invoke RAG builder for system setup
Task(
    description="Build RAG system",
    prompt="Implement complete RAG system for Eugene Schwartz methodology following .claude/agents/core/rag_builder.md specifications",
    subagent_type="general-purpose"
)

# Invoke prompt engineer for analysis system
Task(
    description="Engineer prompts",
    prompt="Create specialized prompts for VSL analysis following .claude/agents/core/prompt_engineer.md specifications",
    subagent_type="general-purpose"
)
```

### Quality Gate Pattern
Each phase has defined success criteria that must be met:
- **RAG System**: <200ms response time, >85% relevance
- **Prompt System**: >90% consciousness classification accuracy
- **N8N Integration**: End-to-end test passing, JSON export available
- **Documentation**: Professional grade, demo-ready materials

## Agent Specifications

### Core Development Agents
Located in `.claude/agents/core/`:
- **rag_builder.md**: RAG system development (12h allocation)
- **prompt_engineer.md**: Specialized prompt creation (8h allocation)
- **n8n_generator.md**: N8N workflow automation (16h allocation)

### Quality & Documentation Agents
Located in `.claude/agents/quality/` and `.claude/agents/documentation/`:
- **qa_agent.md**: Comprehensive testing and validation (8h allocation)
- **technical_docs.md**: Professional documentation creation (parallel)

### Orchestration Agent
Located in `.claude/agents/orchestration/`:
- **project_orchestrator.md**: Master coordinator managing timeline, dependencies, and quality gates

## Configuration Files

### MCP Configuration
- `docs/mcps_configuration.json`: Complete MCP setup for all integrations

### Docker Configuration
```yaml
# docker-compose.yml structure
services:
  postgres-vector:    # PostgreSQL + pgvector for RAG
  n8n:               # N8N automation platform
  rag-api:           # RAG API service
```

### Environment Variables
```bash
# Required for development
ANTHROPIC_API_KEY=your_key_here
N8N_API_KEY=your_n8n_key
DATABASE_URL=postgresql://postgres:password@localhost:5432/eugene_rag
```

## Quality Standards

### Code Quality
- All prompts must be tested with validation framework
- RAG system must achieve >85% relevance in retrieval
- N8N workflows must be exported as JSON for version control
- Documentation must be professional-grade for client presentation

### Testing Requirements
- Unit tests for all prompt functions
- Integration tests for RAG retrieval
- End-to-end tests with sample VSLs
- Performance benchmarks (<200ms RAG response time)

### Documentation Standards
- Technical documentation for all components
- Architecture diagrams using Mermaid
- API documentation with examples
- Video presentation script (5-10 minutes)

## Project-Specific Guidelines

### Eugene Schwartz Methodology Focus
- All analysis must be faithful to original methodology
- 5 Levels of Consciousness classification must be precise
- Outputs must be actionable for health tech market
- Brazilian market compliance (ANVISA) considerations

### Health Tech Market Specialization
- Prompts adapted for supplement/health product copy
- Regulatory compliance awareness in suggestions
- Market-specific examples and cases

### Vitascience Integration
- Analysis tailored for Vitascience's business model
- ROI calculations and performance metrics
- Executive-friendly reporting and dashboards

## Development Phases

The project follows a structured 72-hour development cycle coordinated by the orchestrator:

1. **Environment Setup** (2h): Docker, dependencies, validation
2. **RAG System** (12h): Knowledge base processing and retrieval
3. **Prompt Engineering** (8h): Specialized analysis prompts
4. **N8N Integration** (16h): Complete workflow automation
5. **Documentation** (24h): Parallel comprehensive documentation
6. **Quality Assurance** (8h): Testing and validation
7. **Strategic Differentials** (Remaining time): Unique value additions

## Success Criteria

- ✅ RAG system with <200ms response time
- ✅ Consciousness classification with >85% accuracy
- ✅ Complete N8N workflow exported and functional
- ✅ Professional technical documentation
- ✅ Executive presentation materials ready
- ✅ Health tech market specialization implemented
- ✅ Demo video script and materials prepared

## Emergency Protocols

### 24h Remaining Protocol
- Stop all non-critical development
- Focus on core demo functionality
- Prepare simplified video script
- Document what was achieved vs planned

### Scope Management
- **72h**: Full scope with differentials
- **48h**: Core functionality + one differential
- **24h**: Core functionality only
- **12h**: Demo-ready simplified version
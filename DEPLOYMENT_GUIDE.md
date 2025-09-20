# 🚀 Eugene Schwartz VSL Analyzer - Deployment Guide

## 📋 Quick Start

### Prerequisites
- Docker & Docker Compose
- Git
- OpenAI API Key
- 8GB RAM minimum
- 2GB free disk space

### 1-Minute Setup
```bash
# Clone repository
git clone <repository-url>
cd vitascience-eugene-ai

# Copy environment template
cp .env.example .env

# Add your OpenAI API key to .env
echo "OPENAI_API_KEY=your_key_here" >> .env

# Run setup script
python scripts/setup.py

# Test system
python scripts/test_system.py
```

## 🏗️ Architecture Overview

```mermaid
graph TB
    A[VSL Input] --> B[N8N Workflow]
    B --> C[RAG API]
    C --> D[PostgreSQL + pgvector]
    C --> E[Eugene Prompts]
    E --> F[OpenAI API]
    F --> G[Analysis Results]
    G --> H[N8N Report Generation]
    H --> I[Vitascience Callback]

    subgraph "Core Services"
        C
        D
        J[Redis Cache]
    end

    subgraph "Analysis Pipeline"
        K[Consciousness Classifier]
        L[Framework Analyzer]
        M[Problem Identifier]
        N[Improvement Generator]
    end

    E --> K
    E --> L
    E --> M
    E --> N
```

## 🐳 Docker Services

| Service | Port | Purpose | Health Check |
|---------|------|---------|--------------|
| PostgreSQL + pgvector | 5432 | Vector database | `pg_isready` |
| RAG API | 8000 | Analysis engine | `/health` |
| N8N | 5678 | Workflow automation | HTTP 200 |
| Redis | 6379 | Caching layer | TCP connection |

## 🔧 Configuration

### Environment Variables (.env)
```env
# Required
OPENAI_API_KEY=your_openai_api_key

# Optional
ANTHROPIC_API_KEY=your_anthropic_key
DATABASE_URL=postgresql://postgres:password@localhost:5432/eugene_rag
REDIS_URL=redis://localhost:6379

# Production settings
WORKERS=4
LOG_LEVEL=info
```

### Database Configuration
- **Engine**: PostgreSQL 15 with pgvector extension
- **Vector Dimensions**: 3072 (OpenAI text-embedding-3-large)
- **Index Type**: IVFFLAT with cosine distance
- **Connection Pool**: 20 max connections

### API Configuration
- **Framework**: FastAPI with Uvicorn
- **CORS**: Enabled for N8N integration
- **Timeout**: 120s for complete analysis
- **Rate Limiting**: 100 requests/minute per IP

## 📊 Performance Specifications

### Response Times (Target)
- Consciousness Analysis: <2s
- Framework Analysis: <3s
- Problem Identification: <4s
- Complete Analysis: <15s
- RAG Search: <200ms

### Throughput
- Concurrent requests: 50
- VSL length: Up to 50,000 characters
- Analysis accuracy: >90% for consciousness classification

## 🔗 API Endpoints

### Core Analysis
```bash
# Health check
GET /health

# Consciousness analysis
POST /analyze/consciousness
{
  "vsl_text": "Your VSL content...",
  "analysis_type": "consciousness",
  "include_context": true
}

# Framework analysis
POST /analyze/framework

# Problem identification
POST /analyze/problems

# Complete analysis
POST /analyze/complete
```

### RAG Search
```bash
# Search knowledge base
POST /rag/search
{
  "query": "consciousness levels",
  "category": "consciousness",
  "max_results": 5
}
```

## 🔄 N8N Workflows

### 1. Eugene VSL Analyzer (Complete Pipeline)
- **Webhook**: `/analyze-vsl`
- **Components**: All analysis types + report generation
- **Output**: Comprehensive markdown report

### 2. Vitascience Integration
- **Webhook**: `/vitascience/analyze`
- **Authentication**: API key validation
- **Features**: Business insights + ROI calculations
- **Callback**: Automatic notification to Vitascience

### Import Instructions
1. Open http://localhost:5678 (admin/password)
2. Go to Settings > Import from file
3. Import workflows from `n8n/workflows/`

## 🛠️ Troubleshooting

### Common Issues

#### Services Not Starting
```bash
# Check status
docker-compose ps

# View logs
docker-compose logs -f rag-api

# Restart services
docker-compose restart
```

#### RAG System Issues
```bash
# Test database connection
curl http://localhost:8000/health

# Check pgvector extension
docker-compose exec postgres-vector psql -U postgres -d eugene_rag -c "SELECT * FROM pg_extension WHERE extname='vector';"

# Rebuild database
docker-compose down -v
docker-compose up -d
```

#### Performance Issues
```bash
# Monitor resources
docker stats

# Check API metrics
curl http://localhost:8000/health | jq '.rag_system_status'

# Scale API service
docker-compose up -d --scale rag-api=3
```

### Log Analysis
```bash
# API logs
docker-compose logs -f rag-api

# Database logs
docker-compose logs -f postgres-vector

# N8N logs
docker-compose logs -f n8n
```

## 🔒 Security

### Production Hardening
1. **Change default passwords** in docker-compose.yml
2. **Set up SSL/TLS** for external access
3. **Configure firewall** rules
4. **Use environment variables** for all secrets
5. **Enable API authentication** for production

### API Security
```yaml
# Add to docker-compose.yml for production
environment:
  - API_KEY_REQUIRED=true
  - JWT_SECRET=your_jwt_secret
  - ALLOWED_ORIGINS=https://vitascience.com
```

## 📈 Monitoring

### Health Checks
- **API Health**: `curl http://localhost:8000/health`
- **Database**: Connection pool status
- **N8N**: Workflow execution status
- **Redis**: Memory usage and hit rate

### Metrics to Monitor
- Response times per endpoint
- Error rates
- Memory and CPU usage
- Database query performance
- Vector search accuracy

## 🚀 Production Deployment

### Recommended Infrastructure
- **Server**: 4 CPU cores, 16GB RAM, 100GB SSD
- **Database**: Separate PostgreSQL instance with SSD
- **Load Balancer**: Nginx or similar
- **Monitoring**: Prometheus + Grafana
- **Logging**: ELK stack or similar

### Environment-Specific Configs

#### Development
```bash
docker-compose -f docker-compose.yml -f docker-compose.dev.yml up
```

#### Production
```bash
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```

### Backup Strategy
- **Database**: Daily automated backups
- **Vector Data**: Weekly full backups
- **Configurations**: Version control
- **Logs**: Retention policy (30 days)

## 📞 Support

### Getting Help
1. **Check logs** first: `docker-compose logs -f`
2. **Run health checks**: `python scripts/test_system.py`
3. **Review documentation**: API docs at `/docs`
4. **Contact support**: [support details]

### Performance Tuning
- Adjust worker processes based on CPU cores
- Optimize database queries and indexes
- Configure Redis for caching
- Monitor and scale based on usage patterns

---

*Eugene Schwartz VSL Analyzer - Professional VSL Analysis for Vitascience*
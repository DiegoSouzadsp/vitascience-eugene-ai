#!/bin/bash

# Eugene Schwartz VSL Analyzer - Complete Setup Script
# Executes full environment setup and validation

set -e

echo "🚀 Starting Eugene Schwartz VSL Analyzer Setup..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check prerequisites
check_prerequisites() {
    echo "📋 Checking prerequisites..."

    if ! command -v docker &> /dev/null; then
        echo -e "${RED}❌ Docker not found. Please install Docker first.${NC}"
        exit 1
    fi

    if ! command -v docker-compose &> /dev/null; then
        echo -e "${RED}❌ Docker Compose not found. Please install Docker Compose first.${NC}"
        exit 1
    fi

    echo -e "${GREEN}✅ Prerequisites check passed${NC}"
}

# Setup environment variables
setup_env() {
    echo "📝 Setting up environment variables..."

    if [ ! -f .env ]; then
        cp .env.example .env
        echo -e "${YELLOW}⚠️  Please edit .env file with your API keys before continuing${NC}"
        echo "Press Enter after editing .env file..."
        read
    fi

    # Check if required API keys are set
    source .env
    if [ -z "$ANTHROPIC_API_KEY" ] || [ "$ANTHROPIC_API_KEY" = "your_anthropic_api_key_here" ]; then
        echo -e "${RED}❌ Please set ANTHROPIC_API_KEY in .env file${NC}"
        exit 1
    fi

    echo -e "${GREEN}✅ Environment variables configured${NC}"
}

# Start Docker services
start_services() {
    echo "🐳 Starting Docker services..."

    # Stop any existing containers
    docker-compose down 2>/dev/null || true

    # Build and start services
    docker-compose up -d --build

    echo "⏳ Waiting for services to initialize..."
    sleep 30

    echo -e "${GREEN}✅ Docker services started${NC}"
}

# Setup database
setup_database() {
    echo "🗄️  Setting up database..."

    # Wait for PostgreSQL to be ready
    echo "⏳ Waiting for PostgreSQL to be ready..."
    timeout 60 bash -c 'until docker exec eugene_postgres pg_isready -U postgres -d eugene_rag; do sleep 2; done'

    # Create pgvector extension
    docker exec eugene_postgres psql -U postgres -d eugene_rag -c "CREATE EXTENSION IF NOT EXISTS vector;" || true

    # Create tables (basic structure for now)
    docker exec eugene_postgres psql -U postgres -d eugene_rag -c "
        CREATE TABLE IF NOT EXISTS eugene_knowledge (
            id SERIAL PRIMARY KEY,
            content TEXT NOT NULL,
            embedding vector(3072),
            category VARCHAR(50),
            chapter VARCHAR(100),
            confidence_score FLOAT DEFAULT 1.0,
            metadata JSONB,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE INDEX IF NOT EXISTS idx_eugene_knowledge_embedding
        ON eugene_knowledge USING ivfflat (embedding vector_cosine_ops);

        CREATE INDEX IF NOT EXISTS idx_eugene_knowledge_category
        ON eugene_knowledge(category);
    " || true

    echo -e "${GREEN}✅ Database setup completed${NC}"
}

# Validate services
validate_services() {
    echo "🔍 Validating services..."

    # Check PostgreSQL
    if docker exec eugene_postgres pg_isready -U postgres -d eugene_rag; then
        echo -e "${GREEN}✅ PostgreSQL is running${NC}"
    else
        echo -e "${RED}❌ PostgreSQL check failed${NC}"
        exit 1
    fi

    # Check N8N
    sleep 10  # Give N8N more time
    if curl -s -u admin:password http://localhost:5678/api/v1/workflows > /dev/null; then
        echo -e "${GREEN}✅ N8N API is responding${NC}"
    else
        echo -e "${YELLOW}⚠️  N8N might still be starting up (this is normal)${NC}"
    fi

    # Check RAG API (when implemented)
    if curl -s http://localhost:8000/health > /dev/null 2>&1; then
        echo -e "${GREEN}✅ RAG API is responding${NC}"
    else
        echo -e "${YELLOW}⚠️  RAG API not yet implemented (expected at this stage)${NC}"
    fi
}

# Show access information
show_access_info() {
    echo ""
    echo "🎉 Setup completed successfully!"
    echo ""
    echo "📊 Service Access URLs:"
    echo "  • N8N Interface: http://localhost:5678 (admin:password)"
    echo "  • RAG API: http://localhost:8000 (when implemented)"
    echo "  • PostgreSQL: localhost:5432 (postgres:password)"
    echo ""
    echo "🔧 Next Steps:"
    echo "  1. Run RAG builder agent to populate knowledge base"
    echo "  2. Run prompt engineer agent to create analysis prompts"
    echo "  3. Run N8N generator agent to create workflow"
    echo ""
    echo "💡 Quick Test:"
    echo "  curl -u admin:password http://localhost:5678/api/v1/workflows"
    echo ""
}

# Main execution
main() {
    check_prerequisites
    setup_env
    start_services
    setup_database
    validate_services
    show_access_info
}

# Run main function
main
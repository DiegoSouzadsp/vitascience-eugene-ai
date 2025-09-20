-- Initialize Eugene Schwartz RAG Database
-- PostgreSQL with pgvector extension

-- Enable pgvector extension
CREATE EXTENSION IF NOT EXISTS vector;

-- Create main knowledge table
CREATE TABLE IF NOT EXISTS eugene_knowledge (
    id SERIAL PRIMARY KEY,
    content TEXT NOT NULL,
    embedding vector(3072),
    category VARCHAR(50),
    chapter VARCHAR(100),
    confidence_score FLOAT DEFAULT 0.0,
    metadata JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for performance
CREATE INDEX IF NOT EXISTS idx_eugene_knowledge_category ON eugene_knowledge(category);
CREATE INDEX IF NOT EXISTS idx_eugene_knowledge_chapter ON eugene_knowledge(chapter);
CREATE INDEX IF NOT EXISTS idx_eugene_knowledge_embedding ON eugene_knowledge USING ivfflat (embedding vector_cosine_ops);

-- Create metadata indexes
CREATE INDEX IF NOT EXISTS idx_eugene_knowledge_metadata ON eugene_knowledge USING gin(metadata);

-- Create updated_at trigger
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_eugene_knowledge_updated_at
    BEFORE UPDATE ON eugene_knowledge
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Create analytics table for tracking usage
CREATE TABLE IF NOT EXISTS rag_analytics (
    id SERIAL PRIMARY KEY,
    query TEXT NOT NULL,
    category VARCHAR(50),
    response_time_ms INTEGER,
    results_count INTEGER,
    user_session VARCHAR(100),
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create index for analytics
CREATE INDEX IF NOT EXISTS idx_rag_analytics_timestamp ON rag_analytics(timestamp);
CREATE INDEX IF NOT EXISTS idx_rag_analytics_category ON rag_analytics(category);

-- Insert initial categories metadata
INSERT INTO eugene_knowledge (content, category, chapter, metadata) VALUES
('Eugene Schwartz Categories Metadata', 'system', 'Configuration', '{
    "categories": {
        "consciousness_theory": "Teoria dos 5 níveis de consciência do mercado",
        "frameworks": "Estruturas de copywriting como PAS, AIDA, etc.",
        "techniques": "Técnicas específicas de Eugene Schwartz",
        "examples": "Casos práticos e exemplos reais",
        "evaluation": "Critérios de análise e avaliação"
    },
    "consciousness_levels": {
        "1": "Inconsciente do problema",
        "2": "Consciente do problema, inconsciente da solução",
        "3": "Consciente da solução, inconsciente do seu produto",
        "4": "Consciente do produto, mas não convencido",
        "5": "Pronto para comprar, precisa da oferta certa"
    }
}')
ON CONFLICT DO NOTHING;

-- Create function for similarity search
CREATE OR REPLACE FUNCTION search_similar_content(
    query_embedding vector(3072),
    search_category text DEFAULT NULL,
    result_limit integer DEFAULT 5
)
RETURNS TABLE (
    content text,
    similarity_score float,
    category varchar(50),
    chapter varchar(100),
    metadata jsonb
) AS $$
BEGIN
    RETURN QUERY
    SELECT
        ek.content,
        (ek.embedding <-> query_embedding)::float as similarity_score,
        ek.category,
        ek.chapter,
        ek.metadata
    FROM eugene_knowledge ek
    WHERE (search_category IS NULL OR ek.category = search_category)
        AND ek.category != 'system'
    ORDER BY ek.embedding <-> query_embedding
    LIMIT result_limit;
END;
$$ LANGUAGE plpgsql;

-- Create function to get database statistics
CREATE OR REPLACE FUNCTION get_rag_stats()
RETURNS jsonb AS $$
DECLARE
    result jsonb;
BEGIN
    SELECT jsonb_build_object(
        'total_chunks', COUNT(*),
        'categories', jsonb_object_agg(category, count)
    ) INTO result
    FROM (
        SELECT category, COUNT(*) as count
        FROM eugene_knowledge
        WHERE category != 'system'
        GROUP BY category
    ) cat_counts;

    RETURN result;
END;
$$ LANGUAGE plpgsql;

-- Grant permissions
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO postgres;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO postgres;
GRANT ALL PRIVILEGES ON ALL FUNCTIONS IN SCHEMA public TO postgres;
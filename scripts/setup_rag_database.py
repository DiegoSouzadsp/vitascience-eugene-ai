#!/usr/bin/env python3
"""
Script para configurar o banco PostgreSQL com tabelas RAG
"""

import psycopg2
from sqlalchemy import create_engine, text
import os

DATABASE_URL = "postgresql://postgres:password@localhost:5432/eugene_rag"

def setup_database():
    """Configura PostgreSQL com pgvector e tabelas RAG"""

    print("=== SETUP RAG DATABASE ===")

    try:
        # Conectar com psycopg2 para comandos específicos
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()

        print("OK Conectado ao PostgreSQL")

        # Criar extensão pgvector
        cur.execute("CREATE EXTENSION IF NOT EXISTS vector;")
        print("OK Extensao pgvector criada")

        # Crear tabela eugene_knowledge
        cur.execute("""
            CREATE TABLE IF NOT EXISTS eugene_knowledge (
                id SERIAL PRIMARY KEY,
                content TEXT NOT NULL,
                embedding vector(3072),
                category VARCHAR(50),
                chapter VARCHAR(100),
                confidence_score FLOAT,
                meta_data JSONB,
                created_at TEXT
            );
        """)
        print("OK Tabela eugene_knowledge criada")

        # Criar índices para performance
        cur.execute("""
            CREATE INDEX IF NOT EXISTS ix_eugene_knowledge_category
            ON eugene_knowledge(category);
        """)

        cur.execute("""
            CREATE INDEX IF NOT EXISTS ix_eugene_knowledge_chapter
            ON eugene_knowledge(chapter);
        """)

        # Índice de similaridade vetorial
        cur.execute("""
            CREATE INDEX IF NOT EXISTS ix_eugene_knowledge_embedding_cosine
            ON eugene_knowledge USING ivfflat (embedding vector_cosine_ops)
            WITH (lists = 100);
        """)
        print("OK Índices criados")

        conn.commit()
        cur.close()
        conn.close()

        # Testar com SQLAlchemy
        engine = create_engine(DATABASE_URL)
        with engine.connect() as connection:
            result = connection.execute(text("SELECT COUNT(*) FROM eugene_knowledge"))
            count = result.fetchone()[0]
            print(f"OK Tabela acessível via SQLAlchemy: {count} registros")

        print("\n=== DATABASE SETUP COMPLETO ===")
        return True

    except Exception as e:
        print(f"ERRO Erro setup database: {e}")
        return False

if __name__ == "__main__":
    setup_database()
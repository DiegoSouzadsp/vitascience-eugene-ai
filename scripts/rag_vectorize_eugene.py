#!/usr/bin/env python3
"""
RAG Vectorization - Breakthrough Advertising
Otimizado para orçamento de $6 - focado nos 5 níveis de consciência
"""

import os
import json
import psycopg2
from openai import OpenAI
import numpy as np
from datetime import datetime
import re

# Configurações
DATABASE_URL = "postgresql://postgres:password@localhost:5432/eugene_rag"
OPENAI_API_KEY = "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"

def setup_database():
    """Setup PostgreSQL com pgvector"""
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()

        # Criar extensão pgvector
        cur.execute("CREATE EXTENSION IF NOT EXISTS vector;")

        # Criar tabela de embeddings
        cur.execute("""
            CREATE TABLE IF NOT EXISTS eugene_embeddings (
                id SERIAL PRIMARY KEY,
                content TEXT NOT NULL,
                metadata JSONB,
                embedding vector(1536),
                created_at TIMESTAMP DEFAULT NOW()
            );
        """)

        # Criar índice para busca rápida
        cur.execute("""
            CREATE INDEX IF NOT EXISTS eugene_embeddings_embedding_idx
            ON eugene_embeddings USING ivfflat (embedding vector_cosine_ops)
            WITH (lists = 100);
        """)

        conn.commit()
        cur.close()
        conn.close()

        print("✓ Banco PostgreSQL configurado com pgvector")
        return True

    except Exception as e:
        print(f"✗ Erro setup banco: {e}")
        return False

def extract_consciousness_sections(text):
    """Extrai seções específicas sobre níveis de consciência"""

    # Palavras-chave para identificar seções importantes
    consciousness_keywords = [
        "consciousness", "conscious", "awareness", "aware",
        "problem", "solution", "desire", "need", "want",
        "sophistication", "market", "audience", "prospect",
        "copy", "advertising", "headline", "approach"
    ]

    # Quebrar em seções por páginas
    pages = text.split("--- PÁGINA")
    important_sections = []

    for i, page in enumerate(pages):
        if not page.strip():
            continue

        page_num = i + 1

        # Verificar se página contém conteúdo sobre consciência
        page_lower = page.lower()
        keyword_count = sum(1 for keyword in consciousness_keywords if keyword in page_lower)

        if keyword_count >= 3:  # Página relevante
            # Quebrar página em parágrafos
            paragraphs = [p.strip() for p in page.split('\n\n') if len(p.strip()) > 100]

            for para in paragraphs:
                if len(para) > 200:  # Parágrafo substancial
                    important_sections.append({
                        "content": para,
                        "page": page_num,
                        "keywords": keyword_count,
                        "type": "consciousness_content"
                    })

    print(f"✓ Extraídas {len(important_sections)} seções relevantes sobre consciência")
    return important_sections

def create_embeddings_batch(sections, max_cost=3.0):
    """Cria embeddings em lotes para controlar custo"""

    client = OpenAI(api_key=OPENAI_API_KEY)

    # Estimar custo
    total_tokens = sum(len(section["content"].split()) * 1.3 for section in sections)  # ~1.3 tokens por palavra
    estimated_cost = (total_tokens / 1000) * 0.00002  # text-embedding-3-small: $0.00002 per 1K tokens

    print(f"Seções para processar: {len(sections)}")
    print(f"Tokens estimados: {total_tokens:,.0f}")
    print(f"Custo estimado: ${estimated_cost:.4f}")

    if estimated_cost > max_cost:
        # Reduzir número de seções
        limit = int(len(sections) * (max_cost / estimated_cost))
        sections = sections[:limit]
        print(f"⚠️ Limitando a {limit} seções para manter custo < ${max_cost}")

    embeddings = []
    batch_size = 50  # Processar em lotes de 50

    for i in range(0, len(sections), batch_size):
        batch = sections[i:i+batch_size]
        texts = [section["content"] for section in batch]

        print(f"Processando lote {i//batch_size + 1}/{(len(sections)-1)//batch_size + 1}...")

        try:
            response = client.embeddings.create(
                model="text-embedding-3-small",
                input=texts
            )

            for j, embedding_data in enumerate(response.data):
                embeddings.append({
                    "content": batch[j]["content"],
                    "metadata": {
                        "page": batch[j]["page"],
                        "keywords": batch[j]["keywords"],
                        "type": batch[j]["type"],
                        "processed_at": datetime.now().isoformat()
                    },
                    "embedding": embedding_data.embedding
                })

        except Exception as e:
            print(f"✗ Erro no lote {i//batch_size + 1}: {e}")
            continue

    print(f"✓ Criados {len(embeddings)} embeddings")
    return embeddings

def store_embeddings(embeddings):
    """Armazena embeddings no PostgreSQL"""

    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()

        for emb in embeddings:
            cur.execute("""
                INSERT INTO eugene_embeddings (content, metadata, embedding)
                VALUES (%s, %s, %s)
            """, (
                emb["content"],
                json.dumps(emb["metadata"]),
                emb["embedding"]
            ))

        conn.commit()
        cur.close()
        conn.close()

        print(f"✓ Armazenados {len(embeddings)} embeddings no PostgreSQL")
        return True

    except Exception as e:
        print(f"✗ Erro ao armazenar: {e}")
        return False

def test_rag_search():
    """Testa busca RAG com query sobre consciência"""

    try:
        client = OpenAI(api_key=OPENAI_API_KEY)

        # Query de teste
        query = "consciousness levels market awareness eugene schwartz"

        # Criar embedding da query
        response = client.embeddings.create(
            model="text-embedding-3-small",
            input=[query]
        )
        query_embedding = response.data[0].embedding

        # Buscar no banco
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()

        cur.execute("""
            SELECT content, metadata, (embedding <=> %s) as distance
            FROM eugene_embeddings
            ORDER BY embedding <=> %s
            LIMIT 3
        """, (query_embedding, query_embedding))

        results = cur.fetchall()
        cur.close()
        conn.close()

        print("\n" + "=" * 60)
        print("TESTE RAG - BUSCA POR 'consciousness levels'")
        print("=" * 60)

        for i, (content, metadata, distance) in enumerate(results, 1):
            meta = json.loads(metadata)
            print(f"\nRESULTADO {i} (distância: {distance:.4f})")
            print(f"Página: {meta.get('page', 'N/A')}")
            print(f"Conteúdo: {content[:200]}...")

        print("=" * 60)
        print("✓ RAG funcionando! Sistema pronto para N8N")

        return True

    except Exception as e:
        print(f"✗ Erro no teste RAG: {e}")
        return False

def main():
    """Processo principal de vetorização"""

    print("=" * 60)
    print("RAG VECTORIZATION - BREAKTHROUGH ADVERTISING")
    print("Orçamento: $6 | Meta: <$3 para embeddings")
    print("=" * 60)

    # 1. Setup banco
    if not setup_database():
        return

    # 2. Carregar texto
    try:
        with open("docs/breakthrough_advertising.md", 'r', encoding='utf-8') as f:
            text = f.read()
        print(f"✓ Livro carregado: {len(text):,} caracteres")
    except Exception as e:
        print(f"✗ Erro ao carregar livro: {e}")
        return

    # 3. Extrair seções importantes
    sections = extract_consciousness_sections(text)

    # 4. Criar embeddings
    embeddings = create_embeddings_batch(sections, max_cost=3.0)

    # 5. Armazenar no banco
    if embeddings:
        store_embeddings(embeddings)

    # 6. Testar RAG
    test_rag_search()

    print("\n" + "=" * 60)
    print("✓ VETORIZAÇÃO CONCLUÍDA")
    print("✓ RAG pronto para usar no N8N")
    print("✓ Orçamento preservado para uso posterior")
    print("=" * 60)

if __name__ == "__main__":
    main()
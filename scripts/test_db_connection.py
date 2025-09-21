#!/usr/bin/env python3
import psycopg2

# Test connection with explicit encoding
try:
    conn = psycopg2.connect(
        host="localhost",
        port="5432",
        database="eugene_rag",
        user="postgres",
        password="password"
    )

    cur = conn.cursor()
    cur.execute("SELECT version();")
    version = cur.fetchone()
    print(f"PostgreSQL version: {version}")

    # Test pgvector
    cur.execute("CREATE EXTENSION IF NOT EXISTS vector;")
    print("pgvector extension OK")

    conn.commit()
    cur.close()
    conn.close()

    print("Database connection working!")

except Exception as e:
    print(f"Error: {e}")
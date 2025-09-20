#!/usr/bin/env python3
"""
Processamento simples e economico do livro Eugene Schwartz
Usa OpenAI ada-002 para vetorizacao inicial + embeddings locais para consultas
"""

import os
import sys
import asyncio
from pathlib import Path

# Add src to Python path
sys.path.append(str(Path(__file__).parent.parent / "src"))

async def main():
    """Processa o livro Eugene Schwartz"""
    print("EUGENE SCHWARTZ - PROCESSAMENTO ECONOMICO")
    print("=" * 50)

    try:
        # Read OpenAI key
        key_file = Path(__file__).parent.parent / "docs" / "Chave OpenAi.txt"
        if key_file.exists():
            with open(key_file, 'r') as f:
                openai_key = f.read().strip()
            print(f"OpenAI key loaded ($6 remaining)")
        else:
            print("ERRO: OpenAI key file not found")
            return

        # Set environment
        os.environ['OPENAI_API_KEY'] = openai_key
        os.environ['DATABASE_URL'] = 'postgresql://postgres:password@localhost:5432/eugene_rag'

        # Import system
        from rag_system_hybrid import EugeneRAGSystemHybrid

        print("\nStrategy:")
        print("- OpenAI ada-002 for book vectorization (~$0.50)")
        print("- Local embeddings for daily queries (FREE)")
        print("- Preserves $5+ for VSL analysis")

        # Initialize
        rag = EugeneRAGSystemHybrid()

        # Setup database
        print("\nSetting up database...")
        if not await rag.setup_database():
            print("ERROR: Database setup failed")
            return

        # Check existing data
        health = await rag.health_check()
        local_chunks = health.get('collections', {}).get('local_chunks', 0)

        if local_chunks > 0:
            print(f"Found {local_chunks} existing chunks")
            response = input("Reprocess book? (y/N): ")
            if response.lower() != 'y':
                print("Using existing knowledge base")
                await test_system(rag)
                return

        # Locate PDF
        pdf_path = Path(__file__).parent.parent / "docs" / "Breakthrough_Advertising_-_Eugene_Schwartz.pdf"
        if not pdf_path.exists():
            print(f"ERROR: PDF not found at {pdf_path}")
            return

        print(f"\nProcessing: {pdf_path.name}")
        print("This will take 10-15 minutes...")
        print("Estimated cost: $0.50-1.00")

        # Confirm
        response = input("\nContinue? (y/N): ")
        if response.lower() != 'y':
            print("Processing cancelled")
            return

        # Process book
        import time
        start_time = time.time()

        print("\nStarting book processing...")
        success = await rag.process_eugene_book(str(pdf_path))

        processing_time = time.time() - start_time

        if success:
            print(f"\nBook processed in {processing_time/60:.1f} minutes")

            # Final stats
            health = await rag.health_check()
            collections = health.get('collections', {})

            print("\nFINAL RESULTS:")
            print(f"Local chunks: {collections.get('local_chunks', 0)}")
            print(f"OpenAI chunks: {collections.get('openai_chunks', 0)}")
            print(f"Future queries: {health.get('query_cost', 'FREE')}")

            # Category distribution
            print("\nCategory distribution:")
            for cat, count in health.get('category_distribution', {}).items():
                if count > 0:
                    print(f"  {cat}: {count}")

            # Test system
            await test_system(rag)
        else:
            print("ERROR: Processing failed")

    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()

async def test_system(rag):
    """Test the processed system"""
    print("\nTESTING SYSTEM")
    print("-" * 30)

    test_queries = [
        ("Consciousness Levels", "5 levels of market consciousness"),
        ("PAS Framework", "problem agitation solution method"),
        ("Headlines", "Eugene Schwartz headline techniques"),
        ("Market Awareness", "sophisticated vs mass market"),
    ]

    for name, query in test_queries:
        print(f"\nTesting: {name}")

        import time
        start_time = time.time()

        if "consciousness" in query.lower():
            results = await rag.get_consciousness_level_context(query)
        elif "framework" in query.lower() or "PAS" in query:
            results = await rag.get_framework_guidance(query)
        else:
            results = await rag.search_local_similarity(query, limit=3)

        response_time = (time.time() - start_time) * 1000

        if results:
            print(f"  SUCCESS: {len(results)} results in {response_time:.0f}ms")
            print(f"  Sample: {results[0].content[:60]}...")
        else:
            print(f"  FAILED: No results")

    print("\nSYSTEM READY!")
    print("Future queries are FREE (local embeddings)")
    print("Ready for VSL analysis")

if __name__ == "__main__":
    asyncio.run(main())
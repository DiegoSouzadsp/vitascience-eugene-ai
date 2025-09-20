#!/usr/bin/env python3
"""
Processamento minimal do livro Eugene Schwartz
Apenas embeddings locais para economizar completamente
"""

import os
import sys
import asyncio
from pathlib import Path

# Add src to Python path
sys.path.append(str(Path(__file__).parent.parent / "src"))

async def main():
    """Processa apenas com embeddings locais para teste"""
    print("EUGENE SCHWARTZ - PROCESSAMENTO LOCAL (GRATUITO)")
    print("=" * 55)

    try:
        # Set environment (sem OpenAI por enquanto)
        os.environ['DATABASE_URL'] = 'postgresql://postgres:password@localhost:5432/eugene_rag'

        # Import local-only system
        from rag_system_local import EugeneRAGSystemLocal

        print("Strategy: LOCAL embeddings only (100% FREE)")
        print("- No OpenAI costs")
        print("- sentence-transformers local model")
        print("- Preserves ALL $6 for VSL analysis")

        # Initialize
        rag = EugeneRAGSystemLocal()

        # Setup database
        print("\nSetting up database...")
        if not await rag.setup_database():
            print("ERROR: Database setup failed")
            return

        # Check existing data
        health = await rag.health_check()
        total_chunks = health.get('total_chunks', 0)

        if total_chunks > 0:
            print(f"Found {total_chunks} existing chunks")
            await test_system(rag)
            return

        # Locate PDF
        pdf_path = Path(__file__).parent.parent / "docs" / "Breakthrough_Advertising_-_Eugene_Schwartz.pdf"
        if not pdf_path.exists():
            print(f"ERROR: PDF not found at {pdf_path}")
            return

        print(f"\nProcessing: {pdf_path.name}")
        print("Using LOCAL embeddings only")
        print("Cost: $0 (completely free)")

        # Confirm
        response = input("\nContinue with FREE processing? (y/N): ")
        if response.lower() != 'y':
            print("Processing cancelled")
            return

        # Process book
        import time
        start_time = time.time()

        print("\nStarting LOCAL book processing...")
        success = await rag.process_eugene_book(str(pdf_path))

        processing_time = time.time() - start_time

        if success:
            print(f"\nBook processed in {processing_time/60:.1f} minutes")

            # Final stats
            health = await rag.health_check()
            print(f"\nFINAL RESULTS:")
            print(f"Total chunks: {health['total_chunks']}")
            print(f"Mode: {health['mode']}")
            print(f"Model: {health['embedding_model']}")

            # Category distribution
            print("\nCategory distribution:")
            for cat, count in health['category_distribution'].items():
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
    print("\nTESTING LOCAL SYSTEM")
    print("-" * 25)

    test_queries = [
        ("Consciousness", "5 levels market consciousness"),
        ("Headlines", "headline techniques"),
        ("Copy", "copywriting methods")
    ]

    for name, query in test_queries:
        print(f"\nTesting: {name}")

        import time
        start_time = time.time()

        results = await rag.search_similar(query, limit=2)
        response_time = (time.time() - start_time) * 1000

        if results:
            print(f"  SUCCESS: {len(results)} results in {response_time:.0f}ms")
            print(f"  Sample: {results[0].content[:50]}...")
        else:
            print(f"  FAILED: No results")

    print("\nLOCAL SYSTEM READY!")
    print("Cost: $0 - Completely FREE")
    print("All $6 preserved for VSL analysis")

if __name__ == "__main__":
    asyncio.run(main())
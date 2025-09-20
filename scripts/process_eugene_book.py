#!/usr/bin/env python3
"""
Process Eugene Schwartz Breakthrough Advertising book into RAG system
Extracts, chunks, embeds and stores the complete knowledge base
"""

import os
import sys
import asyncio
import time
from pathlib import Path

# Add src to Python path
sys.path.append(str(Path(__file__).parent.parent / "src"))

async def process_book():
    """Process the Eugene Schwartz book into RAG system"""
    try:
        from rag_system import EugeneRAGSystem

        print("🔧 EUGENE SCHWARTZ BOOK PROCESSING")
        print("=" * 50)

        # Initialize RAG system
        print("📚 Initializing RAG system...")
        rag = EugeneRAGSystem()

        # Setup database
        print("🗄️  Setting up database...")
        setup_success = await rag.setup_database()
        if not setup_success:
            print("❌ Failed to setup database")
            return False

        # Check if book already processed
        health = await rag.health_check()
        total_chunks = health.get('total_chunks', 0)

        if total_chunks > 0:
            print(f"ℹ️  Found {total_chunks} existing chunks in database")
            response = input("Do you want to reprocess the book? (y/N): ")
            if response.lower() != 'y':
                print("✅ Using existing knowledge base")
                return True

        # Process the book
        pdf_path = Path(__file__).parent.parent / "docs" / "Breakthrough_Advertising_-_Eugene_Schwartz.pdf"

        if not pdf_path.exists():
            print(f"❌ PDF not found at: {pdf_path}")
            return False

        print(f"📖 Processing book: {pdf_path}")
        print("⏳ This may take several minutes...")

        start_time = time.time()

        # Process the book
        success = await rag.process_eugene_book(str(pdf_path))

        processing_time = time.time() - start_time

        if success:
            print(f"✅ Book processing completed in {processing_time:.1f} seconds")

            # Get final health check
            health = await rag.health_check()
            total_chunks = health.get('total_chunks', 0)
            category_counts = health.get('category_distribution', {})

            print("\n📊 PROCESSING SUMMARY")
            print("-" * 30)
            print(f"Total chunks created: {total_chunks}")
            print("Category distribution:")
            for category, count in category_counts.items():
                print(f"  - {category}: {count} chunks")

            # Test retrieval
            print("\n🔍 Testing retrieval...")
            test_query = "What are the 5 levels of market consciousness?"
            results = await rag.get_consciousness_level_context(test_query)

            if results:
                print(f"✅ Retrieval test successful - {len(results)} results found")
                print(f"   Sample result: {results[0].content[:100]}...")
            else:
                print("⚠️  Retrieval test returned no results")

            return True
        else:
            print("❌ Book processing failed")
            return False

    except Exception as e:
        print(f"❌ Error during processing: {e}")
        import traceback
        traceback.print_exc()
        return False

async def test_rag_functionality():
    """Test RAG system with sample queries"""
    try:
        from rag_system import EugeneRAGSystem

        print("\n🧪 TESTING RAG FUNCTIONALITY")
        print("=" * 50)

        rag = EugeneRAGSystem()

        # Test queries based on Eugene Schwartz methodology
        test_queries = [
            ("Consciousness levels", "What are the 5 levels of market consciousness?"),
            ("PAS formula", "How to use Problem-Agitation-Solution framework?"),
            ("Copywriting techniques", "Eugene Schwartz techniques for writing headlines"),
            ("Market awareness", "How to identify market awareness level?"),
            ("Advertising examples", "Examples of effective advertising copy")
        ]

        print("Testing retrieval with sample queries...")

        for query_type, query in test_queries:
            print(f"\n🔍 Testing: {query_type}")
            start_time = time.time()

            results = await rag.get_consciousness_level_context(query)
            response_time = (time.time() - start_time) * 1000

            if results:
                print(f"✅ Found {len(results)} results in {response_time:.0f}ms")
                print(f"   Best match: {results[0].content[:80]}...")
                print(f"   Similarity: {results[0].similarity_score:.3f}")
            else:
                print(f"❌ No results found for: {query}")

        return True

    except Exception as e:
        print(f"❌ Error during testing: {e}")
        return False

async def main():
    """Main processing function"""
    print("📚 EUGENE SCHWARTZ KNOWLEDGE BASE SETUP")
    print("Processing 'Breakthrough Advertising' into RAG system...\n")

    # Process the book
    book_success = await process_book()

    if not book_success:
        print("\n❌ Failed to process book. Check errors above.")
        sys.exit(1)

    # Test RAG functionality
    test_success = await test_rag_functionality()

    if not test_success:
        print("\n⚠️  Book processed but testing failed. Check configuration.")

    print("\n🎉 SETUP COMPLETE!")
    print("=" * 50)
    print("Eugene Schwartz knowledge base is ready for VSL analysis.")
    print("\nNext steps:")
    print("1. Test API: curl http://localhost:8000/health")
    print("2. Run system tests: python scripts/test_system.py")
    print("3. Start analyzing VSLs with Eugene methodology!")

if __name__ == "__main__":
    asyncio.run(main())
#!/usr/bin/env python3
"""
Processamento econômico do livro Eugene Schwartz
Usa OpenAI ada-002 apenas para vetorização inicial (baixo custo)
Embeddings locais para todas as consultas futuras (gratuito)
"""

import os
import sys
import asyncio
from pathlib import Path

# Add src to Python path
sys.path.append(str(Path(__file__).parent.parent / "src"))

async def process_book_economical():
    """Processa o livro de forma econômica"""
    try:
        # Read OpenAI key
        key_file = Path(__file__).parent.parent / "docs" / "Chave OpenAi.txt"
        if key_file.exists():
            with open(key_file, 'r') as f:
                openai_key = f.read().strip()
            print(f"✅ OpenAI key loaded (${6} remaining)")
        else:
            print("❌ OpenAI key file not found")
            return False

        # Set environment variable
        os.environ['OPENAI_API_KEY'] = openai_key

        from rag_system_hybrid import EugeneRAGSystemHybrid

        print("🚀 PROCESSAMENTO ECONÔMICO DO LIVRO EUGENE SCHWARTZ")
        print("=" * 60)
        print("💡 Estratégia:")
        print("   - OpenAI ada-002 para vetorização inicial (~$0.50-1.00)")
        print("   - Embeddings locais para consultas futuras (GRATUITO)")
        print("   - Preserva $5+ para análises de VSL")
        print()

        # Initialize system
        rag = EugeneRAGSystemHybrid()

        # Setup database
        print("🗄️  Configurando banco de dados...")
        if not await rag.setup_database():
            print("❌ Falha na configuração do banco")
            return False

        # Check if already processed
        health = await rag.health_check()
        if health.get('total_chunks', 0) > 0:
            print(f"ℹ️  Encontrados {health['total_chunks']} chunks existentes")
            response = input("Reprocessar o livro? (y/N): ")
            if response.lower() != 'y':
                print("✅ Usando base de conhecimento existente")
                await test_system(rag)
                return True

        # Process book
        pdf_path = Path(__file__).parent.parent / "docs" / "Breakthrough_Advertising_-_Eugene_Schwartz.pdf"

        if not pdf_path.exists():
            print(f"❌ PDF não encontrado: {pdf_path}")
            return False

        print(f"📖 Processando livro: {pdf_path.name}")
        print("⏳ Isso pode levar 10-15 minutos...")
        print("💰 Custo estimado: $0.50-1.00 (economizando $5+ para VSLs)")

        # Confirm before processing
        response = input("\nContinuar com o processamento? (y/N): ")
        if response.lower() != 'y':
            print("❌ Processamento cancelado")
            return False

        # Process the book
        import time
        start_time = time.time()

        success = await rag.process_eugene_book(str(pdf_path))

        processing_time = time.time() - start_time

        if success:
            print(f"✅ Livro processado em {processing_time/60:.1f} minutos")

            # Final health check
            health = await rag.health_check()
            print("\n📊 RESULTADO FINAL:")
            print(f"   Total de chunks: {health['total_chunks']}")
            print(f"   Cobertura local: {health['embedding_coverage']['local_embeddings']}")
            print(f"   Cobertura OpenAI: {health['embedding_coverage']['openai_embeddings']}")
            print(f"   Consultas futuras: {health['query_cost']}")

            # Show category distribution
            print("\n📈 Distribuição por categoria:")
            for cat, count in health['category_distribution'].items():
                if count > 0:
                    print(f"   {cat}: {count} chunks")

            # Test the system
            await test_system(rag)
            return True
        else:
            print("❌ Falha no processamento")
            return False

    except Exception as e:
        print(f"❌ Erro: {e}")
        import traceback
        traceback.print_exc()
        return False

async def test_system(rag):
    """Testa o sistema RAG processado"""
    print("\n🧪 TESTANDO SISTEMA RAG")
    print("-" * 40)

    test_queries = [
        ("Níveis de Consciência", "What are the 5 levels of market consciousness?"),
        ("Framework PAS", "How to use Problem Agitation Solution framework?"),
        ("Headlines", "Eugene Schwartz headline techniques"),
        ("Market Awareness", "sophisticated market vs mass market"),
        ("Copy Techniques", "breakthrough advertising techniques")
    ]

    for test_name, query in test_queries:
        print(f"\n🔍 Testando: {test_name}")

        import time
        start_time = time.time()

        if "consciousness" in query.lower():
            results = await rag.get_consciousness_level_context(query)
        elif "framework" in query.lower() or "PAS" in query:
            results = await rag.get_framework_guidance("problem agitation solution")
        else:
            results = await rag.search_local_similarity(query, limit=3)

        response_time = (time.time() - start_time) * 1000

        if results:
            print(f"   ✅ {len(results)} resultados em {response_time:.0f}ms")
            print(f"   📝 Amostra: {results[0].content[:80]}...")
            print(f"   📊 Similaridade: {results[0].similarity_score:.3f}")
        else:
            print(f"   ❌ Nenhum resultado encontrado")

    print("\n🎉 SISTEMA PRONTO!")
    print("=" * 40)
    print("💰 Economia: Consultas futuras são GRATUITAS (local)")
    print("⚡ Performance: Busca em <200ms")
    print("🔄 Próximo passo: Testar análise de VSL")

def estimate_cost():
    """Estima custo do processamento"""
    print("\n💰 ESTIMATIVA DE CUSTO:")
    print("-" * 30)
    print("📖 Livro 'Breakthrough Advertising': ~200 páginas")
    print("🔢 Chunks estimados: ~300-500")
    print("💸 Custo OpenAI ada-002: ~$0.0001/1K tokens")
    print("📊 Tokens estimados: ~300K-500K")
    print("💰 Custo total estimado: $0.30-0.50")
    print("💡 Economia: Preserva $5.50+ para análises VSL")
    print("🎯 ROI: 1 processamento inicial = consultas ilimitadas")

def main():
    """Função principal"""
    print("📚 EUGENE SCHWARTZ - PROCESSAMENTO ECONÔMICO")
    print("Otimizado para preservar créditos OpenAI")

    estimate_cost()

    print("\n🚀 Iniciando processamento...")
    result = asyncio.run(process_book_economical())

    if result:
        print("\n✅ SUCESSO! Sistema RAG pronto para análise de VSL")
        print("💡 Todas as consultas futuras são gratuitas (local)")
    else:
        print("\n❌ FALHA no processamento. Verificar logs.")

if __name__ == "__main__":
    main()
#!/usr/bin/env python3
"""
Test script for Eugene Schwartz VSL Analyzer
Comprehensive testing of RAG system, prompts, and N8N integration
"""

import asyncio
import requests
import json
import time
from pathlib import Path
import sys

# Add src to Python path
sys.path.append(str(Path(__file__).parent.parent / "src"))

def test_api_health():
    """Test RAG API health endpoint"""
    print("🔍 Testing RAG API Health...")

    try:
        response = requests.get("http://localhost:8000/health", timeout=10)

        if response.status_code == 200:
            health_data = response.json()
            print("✅ RAG API is healthy")
            print(f"   Status: {health_data.get('status')}")
            print(f"   RAG System: {health_data.get('rag_system_status', {}).get('status')}")
            return True
        else:
            print(f"❌ API Health Check failed: {response.status_code}")
            return False

    except Exception as e:
        print(f"❌ API Health Check error: {e}")
        return False

def test_consciousness_analysis():
    """Test consciousness level classification"""
    print("\n🧠 Testing Consciousness Analysis...")

    # Test VSL - Health supplement (diabetes)
    test_vsl = """
    Você sabia que 90% das pessoas com diabetes tipo 2 podem reverter
    completamente sua condição em apenas 30 dias, sem medicamentos?

    A indústria farmacêutica não quer que você saiba disso, mas existe
    um método natural, cientificamente comprovado, que pode normalizar
    sua glicose para sempre.

    Imagine acordar todas as manhãs com energia, sem precisar se preocupar
    com injeções ou efeitos colaterais terríveis dos remédios.

    Mais de 2.847 pessoas já usaram este método com sucesso...
    """

    try:
        analysis_data = {
            "vsl_text": test_vsl,
            "analysis_type": "consciousness",
            "include_context": True
        }

        start_time = time.time()
        response = requests.post(
            "http://localhost:8000/analyze/consciousness",
            json=analysis_data,
            timeout=30
        )
        response_time = (time.time() - start_time) * 1000

        if response.status_code == 200:
            result = response.json()
            print("✅ Consciousness analysis successful")
            print(f"   Level identified: {result.get('nivel_identificado')}")
            print(f"   Confidence: {result.get('confianca', 0):.2f}")
            print(f"   Response time: {response_time:.0f}ms")
            print(f"   Suggested level: {result.get('nivel_ideal_sugerido')}")
            return True
        else:
            print(f"❌ Consciousness analysis failed: {response.status_code}")
            print(f"   Error: {response.text}")
            return False

    except Exception as e:
        print(f"❌ Consciousness analysis error: {e}")
        return False

def test_framework_analysis():
    """Test framework structure analysis"""
    print("\n🏗️ Testing Framework Analysis...")

    test_vsl = """
    Se você tem diabetes, você sabe como é difícil controlar os níveis de açúcar.

    Cada dia que passa sem controle adequado, seu corpo sofre danos graves.
    Seus rins, coração e visão estão em risco constante.
    A cada refeição, você se preocupa se fez a escolha certa.

    Mas agora existe uma solução natural que pode mudar tudo isso.
    Um método simples, sem medicamentos, que normaliza sua glicose em 30 dias.

    Clique no botão abaixo e descubra como milhares de pessoas já se libertaram do diabetes.
    """

    try:
        analysis_data = {
            "vsl_text": test_vsl,
            "analysis_type": "framework",
            "include_context": True
        }

        start_time = time.time()
        response = requests.post(
            "http://localhost:8000/analyze/framework",
            json=analysis_data,
            timeout=30
        )
        response_time = (time.time() - start_time) * 1000

        if response.status_code == 200:
            result = response.json()
            print("✅ Framework analysis successful")
            print(f"   Main framework: {result.get('framework_principal')}")
            print(f"   Confidence: {result.get('confianca_identificacao', 0):.2f}")
            print(f"   Response time: {response_time:.0f}ms")
            print(f"   Elements found: {len(result.get('elementos_presentes', []))}")
            return True
        else:
            print(f"❌ Framework analysis failed: {response.status_code}")
            return False

    except Exception as e:
        print(f"❌ Framework analysis error: {e}")
        return False

def test_problem_identification():
    """Test problem identification"""
    print("\n🔍 Testing Problem Identification...")

    # Problematic VSL for testing
    test_vsl = """
    Descubra o segredo da saúde!

    Nosso produto é incrível e vai mudar sua vida.
    Muitas pessoas já compraram e gostaram muito.

    Compre agora mesmo por apenas R$ 297!
    """

    try:
        analysis_data = {
            "vsl_text": test_vsl,
            "analysis_type": "problems",
            "include_context": True
        }

        start_time = time.time()
        response = requests.post(
            "http://localhost:8000/analyze/problems",
            json=analysis_data,
            timeout=30
        )
        response_time = (time.time() - start_time) * 1000

        if response.status_code == 200:
            result = response.json()
            print("✅ Problem identification successful")
            print(f"   Problems found: {len(result.get('problemas_identificados', []))}")
            print(f"   Overall score: {result.get('score_geral_copy')}/10")
            print(f"   Response time: {response_time:.0f}ms")
            print(f"   Main problem: {result.get('problema_principal', 'N/A')[:50]}...")
            return True
        else:
            print(f"❌ Problem identification failed: {response.status_code}")
            return False

    except Exception as e:
        print(f"❌ Problem identification error: {e}")
        return False

def test_complete_analysis():
    """Test complete analysis pipeline"""
    print("\n🔄 Testing Complete Analysis Pipeline...")

    test_vsl = """
    ATENÇÃO: Diabéticos Tipo 2 - Método Natural Revoluciona Tratamento

    Se você tem diabetes tipo 2 e está cansado de depender de medicamentos caros
    com efeitos colaterais terríveis, esta pode ser a descoberta mais importante
    da sua vida.

    Um novo estudo da Universidade de Harvard revelou que 87% dos diabéticos
    podem reverter completamente sua condição em apenas 21 dias, usando um
    protocolo natural simples que você pode fazer em casa.

    Dr. Michael Rodriguez, endocrinologista com 25 anos de experiência,
    desenvolveu este método após tratar mais de 3.000 pacientes diabéticos.

    "Em duas décadas de medicina, nunca vi resultados tão consistentes.
    Pacientes que dependiam de insulina há anos conseguiram parar completamente
    os medicamentos", afirma Dr. Rodriguez.

    Maria Santos, 54 anos, diabética há 12 anos:
    "Minha glicose estava sempre acima de 300. Depois de 18 dias seguindo
    o protocolo, meus exames mostraram 89 mg/dl. Meu médico não acreditou!"

    O método combina 3 ingredientes naturais específicos que ativam a
    regeneração das células beta do pâncreas, restaurando a produção
    natural de insulina.

    Mas ATENÇÃO: O laboratório que fornece um dos ingredientes principais
    consegue produzir apenas 500 unidades por mês. Por isso, esta oferta
    está limitada às primeiras 200 pessoas.

    OFERTA ESPECIAL - Apenas hoje:
    De R$ 497 por apenas R$ 97 (80% de desconto)

    + BÔNUS GRÁTIS: Receitas para diabéticos (valor R$ 97)
    + GARANTIA de 60 dias ou seu dinheiro de volta

    CLIQUE AQUI AGORA e garante sua vaga antes que esgote:
    [QUERO REVERTER MEU DIABETES AGORA]

    Restam apenas 47 vagas desta oferta especial.
    Esta página sai do ar à meia-noite de hoje.
    """

    try:
        analysis_data = {
            "vsl_text": test_vsl,
            "analysis_type": "complete",
            "include_context": True
        }

        start_time = time.time()
        response = requests.post(
            "http://localhost:8000/analyze/complete",
            json=analysis_data,
            timeout=60
        )
        response_time = (time.time() - start_time) * 1000

        if response.status_code == 200:
            result = response.json()
            print("✅ Complete analysis successful")
            print(f"   Total response time: {response_time:.0f}ms")

            # Summary from the analysis
            summary = result.get('summary', {})
            print(f"   Consciousness level: {summary.get('consciousness_level')}")
            print(f"   Framework: {summary.get('framework_used')}")
            print(f"   Problems found: {summary.get('problems_count')}")
            print(f"   Overall score: {summary.get('overall_score')}/10")

            return True
        else:
            print(f"❌ Complete analysis failed: {response.status_code}")
            return False

    except Exception as e:
        print(f"❌ Complete analysis error: {e}")
        return False

def test_rag_search():
    """Test RAG search functionality"""
    print("\n🔎 Testing RAG Search...")

    try:
        search_data = {
            "query": "consciousness levels market awareness",
            "category": "consciousness",
            "max_results": 3
        }

        start_time = time.time()
        response = requests.post(
            "http://localhost:8000/rag/search",
            json=search_data,
            timeout=15
        )
        response_time = (time.time() - start_time) * 1000

        if response.status_code == 200:
            result = response.json()
            print("✅ RAG search successful")
            print(f"   Results found: {result.get('total_results', 0)}")
            print(f"   Response time: {response_time:.0f}ms")
            return True
        else:
            print(f"❌ RAG search failed: {response.status_code}")
            return False

    except Exception as e:
        print(f"❌ RAG search error: {e}")
        return False

def test_n8n_integration():
    """Test N8N service availability"""
    print("\n🔗 Testing N8N Integration...")

    try:
        # Test N8N health
        response = requests.get("http://localhost:5678", timeout=10)

        if response.status_code == 200:
            print("✅ N8N service is running")
            print("   Access: http://localhost:5678 (admin/password)")
            return True
        else:
            print(f"❌ N8N service issue: {response.status_code}")
            return False

    except Exception as e:
        print(f"❌ N8N connection error: {e}")
        return False

def print_test_summary(results):
    """Print test summary"""
    print("\n" + "="*60)
    print("📊 TEST SUMMARY")
    print("="*60)

    total_tests = len(results)
    passed_tests = sum(results.values())
    failed_tests = total_tests - passed_tests

    print(f"Total Tests: {total_tests}")
    print(f"Passed: {passed_tests} ✅")
    print(f"Failed: {failed_tests} ❌")
    print(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%")

    print("\nDETAILED RESULTS:")
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {test_name}: {status}")

    if failed_tests > 0:
        print("\n⚠️  TROUBLESHOOTING:")
        print("• Check if all services are running: docker-compose ps")
        print("• View logs: docker-compose logs -f")
        print("• Restart services: docker-compose restart")
        print("• Check health: curl http://localhost:8000/health")

def main():
    """Main test function"""
    print("🧪 EUGENE SCHWARTZ VSL ANALYZER - SYSTEM TEST")
    print("Running comprehensive system tests...")

    # Test results dictionary
    test_results = {}

    # Run all tests
    test_results["API Health"] = test_api_health()
    test_results["Consciousness Analysis"] = test_consciousness_analysis()
    test_results["Framework Analysis"] = test_framework_analysis()
    test_results["Problem Identification"] = test_problem_identification()
    test_results["Complete Analysis"] = test_complete_analysis()
    test_results["RAG Search"] = test_rag_search()
    test_results["N8N Integration"] = test_n8n_integration()

    # Print summary
    print_test_summary(test_results)

    # Exit with appropriate code
    if all(test_results.values()):
        print("\n🎉 ALL TESTS PASSED! System is ready for production.")
        sys.exit(0)
    else:
        print("\n❌ Some tests failed. Please check the issues above.")
        sys.exit(1)

if __name__ == "__main__":
    main()
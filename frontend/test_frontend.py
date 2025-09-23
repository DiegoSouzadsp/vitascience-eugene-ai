#!/usr/bin/env python3
"""
Frontend Test Script for Eugene Schwartz VSL Analyzer
Tests basic functionality and N8N connectivity
"""

import requests
import json
import time
from datetime import datetime

# Configuration
FRONTEND_URL = "http://localhost:8080"
TEST_VSL = """
Descoberta médica revoluciona tratamento natural!

Se você sofre com dores nas articulações, fadiga crônica ou inflamação,
esta descoberta científica vai mudar sua vida para sempre.

Depois de 15 anos de pesquisa, cientistas da Universidade de Harvard
descobriram um composto natural que elimina a inflamação em apenas 30 dias.

Diferente de todos os tratamentos que você já tentou, este método ataca
a causa raiz do problema, não apenas os sintomas.

Mais de 47.000 pessoas já experimentaram resultados extraordinários:
- 89% relataram redução significativa da dor
- 94% sentiram mais energia e disposição
- 76% eliminaram completamente a inflamação

Mas atenção: devido à alta demanda, temos apenas 500 unidades disponíveis
neste mês. Depois disso, você terá que entrar na lista de espera.

Clique agora e garante sua transformação ainda hoje!
"""

def test_health_endpoint():
    """Test the health endpoint"""
    print("🔍 Testing health endpoint...")
    try:
        response = requests.get(f"{FRONTEND_URL}/health", timeout=10)

        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Health endpoint working")
            print(f"   📊 Status: {data.get('status', 'unknown')}")
            print(f"   🔗 N8N Status: {data.get('n8n_status', 'unknown')}")
            print(f"   🌐 Webhook URL: {data.get('webhook_url', 'unknown')}")
            return True
        else:
            print(f"   ❌ Health endpoint failed: {response.status_code}")
            return False

    except Exception as e:
        print(f"   ❌ Health endpoint error: {e}")
        return False

def test_frontend_pages():
    """Test main frontend pages"""
    print("\n🌐 Testing frontend pages...")

    pages = [
        ("/", "Home page"),
        ("/demo", "Demo page"),
    ]

    success_count = 0

    for path, name in pages:
        try:
            response = requests.get(f"{FRONTEND_URL}{path}", timeout=10)

            if response.status_code == 200:
                print(f"   ✅ {name} loading correctly")
                success_count += 1
            else:
                print(f"   ❌ {name} failed: {response.status_code}")

        except Exception as e:
            print(f"   ❌ {name} error: {e}")

    return success_count == len(pages)

def test_api_endpoint():
    """Test the API endpoint"""
    print("\n🔌 Testing API endpoint...")

    test_data = {
        "vsl_text": TEST_VSL.strip(),
        "analysis_type": "complete"
    }

    try:
        print("   📤 Sending test VSL for analysis...")
        response = requests.post(
            f"{FRONTEND_URL}/api/analyze",
            json=test_data,
            headers={'Content-Type': 'application/json'},
            timeout=120
        )

        print(f"   📥 Response status: {response.status_code}")

        if response.status_code == 200:
            result = response.json()
            print(f"   ✅ API analysis successful")
            print(f"   ⏱️ Response time: {result.get('response_time', 'unknown')}s")

            # Save result for inspection
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"frontend_test_result_{timestamp}.json"

            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(result, f, indent=2, ensure_ascii=False)

            print(f"   💾 Result saved to: {filename}")
            return True

        else:
            error_data = response.json() if response.headers.get('content-type') == 'application/json' else response.text
            print(f"   ❌ API analysis failed: {error_data}")
            return False

    except requests.exceptions.Timeout:
        print(f"   ⏰ API analysis timeout (>2 minutes)")
        return False
    except Exception as e:
        print(f"   ❌ API analysis error: {e}")
        return False

def test_static_assets():
    """Test static assets loading"""
    print("\n🎨 Testing static assets...")

    assets = [
        ("/static/css/custom.css", "Custom CSS"),
        ("/static/js/enhanced.js", "Enhanced JavaScript"),
    ]

    success_count = 0

    for path, name in assets:
        try:
            response = requests.get(f"{FRONTEND_URL}{path}", timeout=10)

            if response.status_code == 200:
                print(f"   ✅ {name} loading correctly")
                success_count += 1
            else:
                print(f"   ❌ {name} failed: {response.status_code}")

        except Exception as e:
            print(f"   ❌ {name} error: {e}")

    return success_count == len(assets)

def main():
    """Run all frontend tests"""
    print("=" * 60)
    print("EUGENE SCHWARTZ VSL ANALYZER - FRONTEND TESTS")
    print("=" * 60)
    print(f"🎯 Testing frontend at: {FRONTEND_URL}")
    print(f"📝 Test VSL length: {len(TEST_VSL)} characters")
    print("=" * 60)

    # Track test results
    results = {
        'health': False,
        'pages': False,
        'api': False,
        'assets': False
    }

    # Run tests
    results['health'] = test_health_endpoint()
    results['pages'] = test_frontend_pages()
    results['assets'] = test_static_assets()
    results['api'] = test_api_endpoint()

    # Summary
    print("\n" + "=" * 60)
    print("TESTE SUMMARY")
    print("=" * 60)

    passed = sum(results.values())
    total = len(results)

    for test_name, success in results.items():
        status = "✅ PASSED" if success else "❌ FAILED"
        print(f"{test_name.upper():12} {status}")

    print("-" * 60)
    print(f"TOTAL: {passed}/{total} tests passed")

    if passed == total:
        print("\n🎉 ALL TESTS PASSED!")
        print("✅ Frontend is ready for Squad Vitascience demonstration")
        return True
    else:
        print(f"\n⚠️ {total - passed} TESTS FAILED")
        print("❌ Please check configuration and try again")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
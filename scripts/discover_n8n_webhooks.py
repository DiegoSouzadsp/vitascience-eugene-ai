#!/usr/bin/env python3
"""
Script para descobrir webhooks disponíveis no N8N
Testa vários paths comuns e verifica qual está ativo
"""

import requests
import json
from datetime import datetime

def test_webhook_paths():
    """Testa vários paths de webhook para encontrar o ativo"""

    base_url = "http://192.168.1.64:5678"

    # Lista de paths para testar
    webhook_paths = [
        "/webhook/analyze-vsl",
        "/webhook/test-eugene",
        "/webhook/vitascience-eugene",
        "/webhook/eugene-analyzer",
        "/webhook/vsl-analysis",
        "/webhook/vitascience",
        "/webhook/eugene",
        "/webhook-test/vitascience/analyze",
        "/webhook-test/eugene",
        "/webhook-test/vsl",
        "/form/vitascience",
        "/form/eugene",
        "/form/vsl-test"
    ]

    test_payload = {
        "vsl_text": "Teste simples para verificar webhook ativo",
        "analysis_type": "test",
        "timestamp": datetime.now().isoformat()
    }

    headers = {
        'Content-Type': 'application/json',
        'User-Agent': 'VitascienceWebhookTest/1.0'
    }

    print("=" * 60)
    print("DESCOBRINDO WEBHOOKS ATIVOS NO N8N")
    print("=" * 60)
    print(f"Base URL: {base_url}")
    print(f"Testando {len(webhook_paths)} paths...")
    print("-" * 60)

    active_webhooks = []

    for path in webhook_paths:
        url = f"{base_url}{path}"

        try:
            print(f"Testando: {path} ... ", end="")

            response = requests.post(
                url,
                json=test_payload,
                headers=headers,
                timeout=10
            )

            if response.status_code == 200:
                print("ATIVO!")
                active_webhooks.append({
                    "path": path,
                    "url": url,
                    "status": response.status_code,
                    "response": response.text[:200]
                })
            elif response.status_code == 404:
                error_data = response.json() if response.headers.get('content-type', '').startswith('application/json') else {}
                if "not registered" in error_data.get("message", ""):
                    print("Nao registrado")
                else:
                    print(f"404")
            else:
                print(f"Status {response.status_code}")

        except requests.exceptions.ConnectionError:
            print("Erro de conexao")
        except requests.exceptions.Timeout:
            print("Timeout")
        except Exception as e:
            print(f"Erro: {str(e)[:30]}")

    print("-" * 60)

    if active_webhooks:
        print("WEBHOOKS ATIVOS ENCONTRADOS:")
        for webhook in active_webhooks:
            print(f">> {webhook['url']}")
            print(f"   Status: {webhook['status']}")
            print(f"   Preview: {webhook['response']}")
            print()
    else:
        print("NENHUM WEBHOOK ATIVO ENCONTRADO")
        print()
        print("PROXIMOS PASSOS:")
        print("1. Acesse: http://192.168.1.64:5678")
        print("2. Verifique se ha workflows criados")
        print("3. Ative o workflow (botao toggle)")
        print("4. Execute este script novamente")

    print("=" * 60)

    return active_webhooks

def test_found_webhook(webhook_url):
    """Testa webhook encontrado com VSL real"""

    vsl_sample = """
    Na noite do ano de 1785, Antoine Lavoisier, um químico brilhante e famoso,
    descobriu o caminho para emagrecer sem sacrifícios.

    Essa descoberta, que ficou escondida até hoje, é a chave para toda mulher
    perder a gordura da barriga, culote e papada… dizendo ADEUS ao efeito sanfona.
    """

    payload = {
        "vsl_text": vsl_sample.strip(),
        "analysis_type": "eugene_schwartz_5_levels",
        "timestamp": datetime.now().isoformat(),
        "source": "vitascience_test"
    }

    try:
        print(f"\nTESTANDO WEBHOOK COM VSL REAL")
        print(f"URL: {webhook_url}")
        print("-" * 40)

        response = requests.post(
            webhook_url,
            json=payload,
            headers={'Content-Type': 'application/json'},
            timeout=30
        )

        print(f"Status: {response.status_code}")

        if response.status_code == 200:
            print("SUCESSO!")
            try:
                result = response.json()
                print("RESPOSTA:")
                print(json.dumps(result, indent=2, ensure_ascii=False))
            except:
                print("RESPOSTA (texto):")
                print(response.text)
        else:
            print(f"ERRO: {response.status_code}")
            print(f"Detalhes: {response.text}")

    except Exception as e:
        print(f"ERRO NO TESTE: {e}")

if __name__ == "__main__":
    active_webhooks = test_webhook_paths()

    if active_webhooks:
        # Testa o primeiro webhook ativo encontrado
        webhook_url = active_webhooks[0]["url"]
        test_found_webhook(webhook_url)
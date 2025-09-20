#!/usr/bin/env python3
"""
Teste simples do webhook N8N - sem dependências do RAG
Cria webhook de teste direto no N8N e testa com VSL
"""

import json
import requests
import time
from datetime import datetime

def test_n8n_simple_webhook():
    """Testa webhook N8N simples"""

    print("=" * 60)
    print("TESTE SIMPLES WEBHOOK N8N")
    print("=" * 60)

    # Payload simples com VSL da Vitascience
    vsl_lead = """
    Na noite do ano de 1785, Antoine Lavoisier, um químico brilhante e famoso,
    descobriu o caminho para emagrecer sem sacrifícios.

    Essa descoberta, que ficou escondida até hoje, é a chave para toda mulher
    perder a gordura da barriga, culote e papada… dizendo ADEUS ao efeito sanfona.

    Independente se já passou dos 40 anos ou se precisa eliminar 5, 10 ou mais quilos.

    Por trás dessa descoberta, está a verdadeira razão:
    1 — Da atividade física não emagrecer por si só.
    2 — O porquê a maioria das pessoas que fazem bariátrica engordam tudo de novo.
    3 — E por que tomar remédios pra emagrecer acaba em efeito sanfona.

    Lavoisier descobriu que existe um processo no seu corpo capaz de
    transformar a sua gordura em gás.

    Você pode simplesmente fazer sua gordura evaporar e perder 5, 10 ou mais quilos.
    """

    # URLs de teste - N8N no IP da rede
    test_urls = [
        "http://192.168.1.64:5678/webhook/test-eugene",
        "http://192.168.1.64:5678/webhook-test/vitascience/analyze",
        "http://192.168.1.64:5678/webhook/vitascience-eugene"
    ]

    payload = {
        "vsl_text": vsl_lead.strip(),
        "analysis_type": "eugene_schwartz",
        "timestamp": datetime.now().isoformat(),
        "test": True
    }

    headers = {
        'Content-Type': 'application/json',
        'User-Agent': 'VitascienceTest/1.0'
    }

    for url in test_urls:
        print(f"\nTestando: {url}")
        print("-" * 40)

        try:
            response = requests.post(
                url,
                json=payload,
                headers=headers,
                timeout=30
            )

            print(f"Status: {response.status_code}")

            if response.status_code == 200:
                print("SUCESSO!")
                try:
                    result = response.json()
                    print(json.dumps(result, indent=2))
                except:
                    print("Resposta:", response.text[:500])
                break
            elif response.status_code == 404:
                print("Webhook não encontrado (404)")
            else:
                print(f"Erro: {response.status_code}")
                print("Resposta:", response.text[:200])

        except requests.exceptions.ConnectionError:
            print("ERRO: Não foi possível conectar (N8N não está rodando?)")
        except requests.exceptions.Timeout:
            print("ERRO: Timeout")
        except Exception as e:
            print(f"ERRO: {e}")

    print("\n" + "=" * 60)
    print("INSTRUÇÕES PARA CRIAR WEBHOOK NO N8N:")
    print("=" * 60)
    print("1. Acesse: http://192.168.1.64:5678")
    print("2. Login: admin / password")
    print("3. Crie novo workflow")
    print("4. Adicione node 'Webhook'")
    print("5. Configure webhook path: /webhook/test-eugene")
    print("6. Adicione node 'Respond to Webhook'")
    print("7. Conecte os nodes")
    print("8. Ative o workflow")
    print("9. Execute este script novamente")
    print("=" * 60)

if __name__ == "__main__":
    test_n8n_simple_webhook()
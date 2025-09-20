#!/usr/bin/env python3
"""
Teste webhook com path personalizado
Permite testar qualquer path de webhook
"""

import requests
import json
import sys
from datetime import datetime

def test_custom_webhook(webhook_path):
    """Testa webhook com path customizado"""

    base_url = "http://localhost:5678"

    # Adiciona / no início se não tiver
    if not webhook_path.startswith('/'):
        webhook_path = '/' + webhook_path

    url = f"{base_url}{webhook_path}"

    # VSL de teste da Vitascience
    vsl_sample = """
Na noite do ano de 1785, Antoine Lavoisier, um químico brilhante e famoso, descobriu o caminho para emagrecer sem sacrifícios.

Essa descoberta, que ficou escondida até hoje, é a chave para toda mulher perder a gordura da barriga, culote e papada… dizendo ADEUS ao efeito sanfona.

Independente se já passou dos 40 anos ou se precisa eliminar 5, 10 ou mais quilos.

Por trás dessa descoberta, está a verdadeira razão:
1 — Da atividade física não emagrecer por si só.
2 — O porquê a maioria das pessoas que fazem bariátrica engordam tudo de novo.
3 — E por que tomar remédios pra emagrecer acaba em efeito sanfona.

Lavoisier descobriu que existe um processo no seu corpo capaz de transformar a sua gordura em gás.
    """.strip()

    payload = {
        "vsl_text": vsl_sample,
        "analysis_type": "eugene_schwartz_5_levels",
        "timestamp": datetime.now().isoformat(),
        "source": "vitascience_test_manual"
    }

    headers = {
        'Content-Type': 'application/json',
        'User-Agent': 'VitascienceTest/1.0'
    }

    print("=" * 60)
    print("TESTE WEBHOOK PERSONALIZADO")
    print("=" * 60)
    print(f"URL: {url}")
    print(f"VSL Length: {len(vsl_sample)} chars")
    print("-" * 60)

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
            print("-" * 40)
            try:
                result = response.json()
                print("RESPOSTA JSON:")
                print(json.dumps(result, indent=2, ensure_ascii=False))
            except:
                print("RESPOSTA TEXTO:")
                print(response.text)
        else:
            print(f"ERRO: {response.status_code}")
            if response.headers.get('content-type', '').startswith('application/json'):
                try:
                    error_data = response.json()
                    print("DETALHES DO ERRO:")
                    print(json.dumps(error_data, indent=2, ensure_ascii=False))
                except:
                    print("RESPOSTA:")
                    print(response.text)
            else:
                print("RESPOSTA:")
                print(response.text)

    except requests.exceptions.ConnectionError:
        print("ERRO: Não foi possível conectar ao N8N")
    except requests.exceptions.Timeout:
        print("ERRO: Timeout - webhook demorou mais que 30s")
    except Exception as e:
        print(f"ERRO: {e}")

    print("=" * 60)

def main():
    if len(sys.argv) < 2:
        print("Uso: python test_any_webhook.py <webhook_path>")
        print()
        print("Exemplos:")
        print("  python test_any_webhook.py webhook/test")
        print("  python test_any_webhook.py webhook/eugene")
        print("  python test_any_webhook.py webhook/vitascience")
        print()
        print("O script vai testar: http://192.168.1.64:5678/<seu_path>")
        return

    webhook_path = sys.argv[1]
    test_custom_webhook(webhook_path)

if __name__ == "__main__":
    main()
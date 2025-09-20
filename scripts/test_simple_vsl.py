#!/usr/bin/env python3
"""
Teste simples do workflow Eugene VSL com VSL da Vitascience
"""

import requests
import json
from datetime import datetime

def test_vsl_analysis():
    """Testa análise VSL com workflow N8N"""

    # URL do webhook N8N
    webhook_url = "http://localhost:5678/webhook/analyze-vsl-squad"

    # VSL de teste da Vitascience (do arquivo Material para Teste Prático)
    vsl_text = """
Na noite do ano de 1785, Antoine Lavoisier, um químico brilhante e famoso, descobriu o caminho para emagrecer sem sacrifícios.

Essa descoberta, que ficou escondida até hoje, é a chave para toda mulher perder a gordura da barriga, culote e papada… dizendo ADEUS ao efeito sanfona.

Independente se já passou dos 40 anos ou se precisa eliminar 5, 10 ou mais quilos.

Por trás dessa descoberta, está a verdadeira razão:

1 — Da atividade física não emagrecer por si só.
2 — O porquê a maioria das pessoas que fazem bariátrica engordam tudo de novo.
3 — E por que tomar remédios pra emagrecer acaba em efeito sanfona.

Lavoisier descobriu que, pra perder peso, não adianta fazer horas de atividade física…

Se submeter a dietas altamente restritivas, cortando carboidratos, gorduras e açúcar da sua alimentação…

Colocar a sua vida em risco entrando na faca pra fazer cirurgias e procedimentos estéticos caros e perigosos, como, por exemplo, a bariátrica e a lipoaspiração…

Ou prejudicar a sua saúde tomando pílulas com propaganda milagrosa para emagrecer.

Na verdade, o que ele descobriu é que existe um processo no seu corpo capaz de transformar a sua gordura em gás.

É isso mesmo.

Você pode simplesmente fazer sua gordura evaporar e perder 5, 10 ou mais quilos.

E o melhor de tudo: você pode fazer isso simplesmente ao tomar esse poderoso suco que fica pronto em 15 segundinhos.
    """.strip()

    # Payload para o webhook
    payload = {
        "vsl_text": vsl_text,
        "analysis_id": f"teste_vitascience_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
        "timestamp": datetime.now().isoformat(),
        "source": "vitascience_squad_test"
    }

    headers = {
        'Content-Type': 'application/json',
        'User-Agent': 'VitascienceSquadTest/1.0'
    }

    print("=" * 60)
    print("TESTE VSL VITASCIENCE - EUGENE SCHWARTZ ANALYZER")
    print("=" * 60)
    print(f"Webhook: {webhook_url}")
    print(f"VSL Length: {len(vsl_text)} caracteres")
    print("-" * 60)

    try:
        print("Enviando VSL para análise...")

        response = requests.post(
            webhook_url,
            json=payload,
            headers=headers,
            timeout=60
        )

        print(f"Status: {response.status_code}")

        if response.status_code == 200:
            print("SUCESSO!")
            print("-" * 40)

            try:
                result = response.json()

                # Exibir resultado formatado
                print("ANALISE EUGENE SCHWARTZ:")
                print("-" * 40)

                if 'consciousness_level' in result:
                    cl = result['consciousness_level']
                    print(f"Nivel Consciencia: {cl.get('level', 'N/A')}")
                    print(f"Confianca: {cl.get('confidence', 'N/A')}%")
                    print(f"Justificativa: {cl.get('justification', 'N/A')[:100]}...")

                if 'copywriting_framework' in result:
                    fw = result['copywriting_framework']
                    print(f"Framework: {fw.get('main_framework', 'N/A')}")

                if 'identified_problems' in result:
                    problems = result['identified_problems']
                    print(f"Problemas Identificados: {len(problems.get('problems_list', []))}")

                if 'suggested_improvements' in result:
                    improvements = result['suggested_improvements']
                    print(f"Melhorias Sugeridas: {len(improvements.get('detailed_improvements', []))}")

                print("\n" + "=" * 60)
                print("RESPOSTA COMPLETA (JSON):")
                print("=" * 60)
                print(json.dumps(result, indent=2, ensure_ascii=False))

            except json.JSONDecodeError:
                print("RESPOSTA (TEXTO):")
                print(response.text)

        elif response.status_code == 404:
            print("ERRO: Webhook não encontrado")
            print("Verifique se o workflow está importado e ativo no N8N")
        else:
            print(f"ERRO: {response.status_code}")
            print(f"Resposta: {response.text}")

    except requests.exceptions.ConnectionError:
        print("ERRO: Não foi possível conectar ao N8N")
        print("Verifique se N8N está rodando em localhost:5678")
    except requests.exceptions.Timeout:
        print("ERRO: Timeout - análise demorou mais que 60s")
    except Exception as e:
        print(f"ERRO: {e}")

    print("=" * 60)

if __name__ == "__main__":
    test_vsl_analysis()
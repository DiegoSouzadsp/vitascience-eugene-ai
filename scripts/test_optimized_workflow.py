#!/usr/bin/env python3
"""
Teste do workflow otimizado Eugene VSL (Haiku + Sonnet)
"""

import requests
import json
from datetime import datetime

def test_optimized_workflow():
    """Testa o workflow otimizado com VSL da Vitascience"""

    webhook_url = "http://localhost:5678/webhook/analyze-vsl-optimized"

    # VSL da Vitascience (Lead do teste)
    vsl_text = """
Na noite do ano de 1785, Antoine Lavoisier, um químico brilhante e famoso, descobriu o caminho para emagrecer sem sacrifícios.

Essa descoberta, que ficou escondida até hoje, é a chave para toda mulher perder a gordura da barriga, culote e papada… dizendo ADEUS ao efeito sanfona.

Independente se já passou dos 40 anos ou se precisa eliminar 5, 10 ou mais quilos.

Por trás dessa descoberta, está a verdadeira razão:

1 — Da atividade física não emagrecer por si só.
2 — O porquê a maioria das pessoas que fazem bariátrica engordam tudo de novo.
3 — E por que tomar remédios pra emagrecer acaba em efeito sanfona e aumentam o risco de desenvolver diabete.

Lavoisier descobriu que, pra perder peso, não adianta fazer horas de atividade física…

Se submeter a dietas altamente restritivas, cortando carboidratos, gorduras e açúcar da sua alimentação…

Colocar a sua vida em risco entrando na faca pra fazer cirurgias e procedimentos estéticos caros e perigosos, como, por exemplo, a bariátrica e a lipoaspiração…

Ou prejudicar a sua saúde tomando pílulas com propaganda milagrosa para emagrecer.

Na verdade, o que ele descobriu é que existe um processo no seu corpo capaz de transformar a sua gordura em gás.

É isso mesmo.

Você pode simplesmente fazer sua gordura evaporar e perder 5, 10 ou mais quilos.

E o melhor de tudo: você pode fazer isso simplesmente ao tomar esse poderoso suco que fica pronto em 15 segundinhos.

Já imaginou isso?

Você podendo:

Ao se olhar no espelho, gostar de verdade do seu corpo…

Se sentir mais bonita e feliz por ser magra…

Colocar qualquer roupa sem nem passar pela sua cabeça preocupações como: será que meu braço está muito gordo ou minha barriga está marcando muito?

E o melhor: poder vestir as roupas que mais gosta, mas que estavam guardadas em um cantinho do guarda-roupa.
    """.strip()

    payload = {
        "vsl_text": vsl_text,
        "analysis_id": f"vitascience_optimized_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
        "timestamp": datetime.now().isoformat()
    }

    headers = {
        'Content-Type': 'application/json',
        'User-Agent': 'VitascienceOptimizedTest/1.0'
    }

    print("=" * 60)
    print("TESTE WORKFLOW OTIMIZADO - HAIKU + SONNET")
    print("=" * 60)
    print(f"URL: {webhook_url}")
    print(f"VSL: {len(vsl_text)} caracteres")
    print(f"Estrategia: Haiku classificacao + Sonnet analise profunda")
    print("-" * 60)

    try:
        print("Iniciando analise (Haiku -> Sonnet)...")

        response = requests.post(
            webhook_url,
            json=payload,
            headers=headers,
            timeout=90  # Tempo maior para pipeline duplo
        )

        print(f"Status: {response.status_code}")

        if response.status_code == 200:
            print("SUCESSO - PIPELINE OTIMIZADO FUNCIONANDO!")
            print("-" * 40)

            try:
                result = response.json()

                # Exibir resultado estruturado
                print("RESULTADO DA ANALISE EUGENE SCHWARTZ:")
                print("-" * 40)

                # Metadados
                if 'analysis_metadata' in result.get('final_analysis', {}):
                    meta = result['final_analysis']['analysis_metadata']
                    print(f"Metodo: {meta.get('analysis_method', 'N/A')}")
                    print(f"Timestamp: {meta.get('timestamp', 'N/A')}")

                # Análise de consciência
                if 'consciousness_level' in result.get('final_analysis', {}):
                    cl = result['final_analysis']['consciousness_level']
                    print(f"Nivel Consciencia: {cl.get('level', 'N/A')}")
                    print(f"Confianca: {cl.get('confidence', 'N/A')}%")
                    print(f"Justificativa: {cl.get('justification', 'N/A')[:150]}...")

                # Framework
                if 'copywriting_framework' in result.get('final_analysis', {}):
                    fw = result['final_analysis']['copywriting_framework']
                    print(f"Framework: {fw.get('main_framework', 'N/A')}")
                    print(f"Efetividade: {fw.get('framework_effectiveness', 'N/A')}")

                # Problemas
                if 'identified_problems' in result.get('final_analysis', {}):
                    problems = result['final_analysis']['identified_problems']
                    critical = problems.get('critical_issues', [])
                    print(f"Problemas Criticos: {len(critical)}")
                    print(f"Problema Principal: {problems.get('main_problem', 'N/A')[:100]}...")

                # Melhorias
                if 'suggested_improvements' in result.get('final_analysis', {}):
                    improvements = result['final_analysis']['suggested_improvements']
                    quick_wins = improvements.get('quick_wins', [])
                    strategic = improvements.get('strategic_changes', [])
                    print(f"Quick Wins: {len(quick_wins)}")
                    print(f"Mudancas Estrategicas: {len(strategic)}")

                # Classificação rápida (Haiku)
                if 'quick_classification' in result.get('final_analysis', {}):
                    quick = result['final_analysis']['quick_classification']
                    print(f"Classificacao Haiku: Nivel {quick.get('consciousness_level', 'N/A')} ({quick.get('confidence', 'N/A')}%)")

                print("\n" + "=" * 60)
                print("RESPOSTA JSON COMPLETA:")
                print("=" * 60)
                print(json.dumps(result, indent=2, ensure_ascii=False))

                # Salvar resultado
                output_file = f"tests/optimized_test_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
                with open(output_file, 'w', encoding='utf-8') as f:
                    json.dump(result, f, indent=2, ensure_ascii=False)
                print(f"\nResultado salvo: {output_file}")

            except json.JSONDecodeError:
                print("RESPOSTA NAO-JSON:")
                print(response.text)

        elif response.status_code == 404:
            print("ERRO: Webhook nao encontrado")
            print("1. Verifique se o workflow foi importado")
            print("2. Ative o workflow no N8N")
            print("3. Configure as credenciais Anthropic")
        else:
            print(f"ERRO: {response.status_code}")
            print(f"Resposta: {response.text}")

    except requests.exceptions.ConnectionError:
        print("ERRO: N8N nao esta acessivel em localhost:5678")
    except requests.exceptions.Timeout:
        print("ERRO: Timeout - pipeline demorou mais que 90s")
    except Exception as e:
        print(f"ERRO: {e}")

    print("=" * 60)

if __name__ == "__main__":
    test_optimized_workflow()
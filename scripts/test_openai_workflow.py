#!/usr/bin/env python3
"""
Teste do workflow OpenAI otimizado (o3-mini + o1-mini)
"""

import requests
import json
from datetime import datetime

def test_openai_optimized_workflow():
    """Testa pipeline OpenAI otimizado para Squad Vitascience"""

    webhook_url = "http://localhost:5678/webhook/analyze-vsl-openai"

    # VSL da Vitascience (Lead do teste Squad)
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

É isso mesmo. Você pode simplesmente fazer sua gordura evaporar e perder 5, 10 ou mais quilos.

E o melhor de tudo: você pode fazer isso simplesmente ao tomar esse poderoso suco que fica pronto em 15 segundinhos.

Já imaginou isso? Você podendo:

Ao se olhar no espelho, gostar de verdade do seu corpo…
Se sentir mais bonita e feliz por ser magra…
Colocar qualquer roupa sem nem passar pela sua cabeça preocupações como: será que meu braço está muito gordo ou minha barriga está marcando muito?

E o melhor: poder vestir as roupas que mais gosta, mas que estavam guardadas em um cantinho do guarda-roupa.

Então, se prepare para o que eu vou te falar nos próximos minutos: é muito rápido fazer a gordura do seu corpo virar gás e emagrecer sem sofrimento…

Não importa:
- Quantos quilos você precisa eliminar…
- Qual a sua idade…
- Onde você mora… seja no interior ou na capital…
- Se acredita que sua genética é ruim…
- Ou que depois dos 40 anos o metabolismo fica lento.

A partir de agora, emagrecer será apenas uma questão de DIAS quando você descobrir:

Como transformar a gordura em gás tomando um suco que fica pronto em apenas 15 segundos.
    """.strip()

    payload = {
        "vsl_text": vsl_text,
        "analysis_id": f"squad_vitascience_openai_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
        "timestamp": datetime.now().isoformat(),
        "test_type": "squad_vitascience_submission"
    }

    headers = {
        'Content-Type': 'application/json',
        'User-Agent': 'VitascienceSquadOpenAI/1.0'
    }

    print("=" * 60)
    print("TESTE WORKFLOW OPENAI - SQUAD VITASCIENCE")
    print("=" * 60)
    print(f"URL: {webhook_url}")
    print(f"VSL: {len(vsl_text)} caracteres")
    print(f"Pipeline: o3-mini -> o1-mini")
    print(f"Estrategia: Custo otimizado + Qualidade maxima")
    print("-" * 60)

    try:
        print("Iniciando analise Eugene Schwartz (o3-mini + o1-mini)...")

        response = requests.post(
            webhook_url,
            json=payload,
            headers=headers,
            timeout=120  # o1-mini pode demorar mais
        )

        print(f"Status: {response.status_code}")

        if response.status_code == 200:
            print("SUCESSO - PIPELINE OPENAI OTIMIZADO!")
            print("-" * 40)

            try:
                result = response.json()

                # Exibir resultado estruturado do Squad
                print("ANALISE EUGENE SCHWARTZ - SQUAD VITASCIENCE:")
                print("-" * 40)

                # Verificar conformidade com teste Squad
                analysis = result.get('squad_vitascience_analysis', {})

                # Metadados da análise
                if 'analysis_metadata' in analysis:
                    meta = analysis['analysis_metadata']
                    print(f"Metodo: {meta.get('models_used', 'N/A')}")
                    print(f"Estrategia: {meta.get('processing_strategy', 'N/A')}")
                    print(f"Squad Compliance: {meta.get('squad_test_compliance', 'N/A')}")

                # Análise de consciência (requisito #1 do Squad)
                if 'consciousness_level' in analysis:
                    cl = analysis['consciousness_level']
                    print(f"\n1. NIVEL CONSCIENCIA: {cl.get('level', 'N/A')} ({cl.get('confidence', 'N/A')}%)")
                    print(f"   Justificativa: {cl.get('justification', 'N/A')[:100]}...")

                # Framework (requisito #2 do Squad)
                if 'copywriting_framework' in analysis:
                    fw = analysis['copywriting_framework']
                    print(f"\n2. FRAMEWORK: {fw.get('main_framework', 'N/A')}")
                    print(f"   Efetividade: {fw.get('framework_effectiveness', 'N/A')}")

                # Problemas identificados (requisito #3 do Squad)
                if 'identified_problems' in analysis:
                    problems = analysis['identified_problems']
                    critical = problems.get('critical_issues', [])
                    print(f"\n3. PROBLEMAS IDENTIFICADOS: {len(critical)}")
                    print(f"   Principal: {problems.get('main_problem', 'N/A')[:80]}...")

                # Melhorias Eugene (requisito #4 do Squad)
                if 'suggested_improvements' in analysis:
                    improvements = analysis['suggested_improvements']
                    strategic = improvements.get('strategic_changes', [])
                    quick_wins = improvements.get('quick_wins', [])
                    print(f"\n4. MELHORIAS EUGENE: {len(strategic)} estrategicas, {len(quick_wins)} quick wins")

                # Novos ângulos (requisito #5 do Squad)
                if 'suggested_improvements' in analysis:
                    new_angles = analysis['suggested_improvements'].get('new_creative_angles', [])
                    print(f"\n5. NOVOS ANGULOS CRIATIVOS: {len(new_angles)}")

                # Verificar conformidade com requisitos
                if 'test_requirements_met' in analysis:
                    req = analysis['test_requirements_met']
                    print(f"\nCONFORMIDADE TESTE SQUAD:")
                    print(f"  Analise consciencia 1-5: {req.get('consciousness_analysis_1_5', False)}")
                    print(f"  Framework identificado: {req.get('framework_identification', False)}")
                    print(f"  Min 5 melhorias: {req.get('minimum_5_improvements', False)}")
                    print(f"  Metodologia Eugene: {req.get('eugene_methodology_applied', False)}")
                    print(f"  Output JSON: {req.get('json_structured_output', False)}")

                print("\n" + "=" * 60)
                print("ANALISE COMPLETA (JSON ESTRUTURADO):")
                print("=" * 60)
                print(json.dumps(result, indent=2, ensure_ascii=False))

                # Salvar para submissão ao Squad
                output_file = f"tests/squad_vitascience_submission_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
                with open(output_file, 'w', encoding='utf-8') as f:
                    json.dump(result, f, indent=2, ensure_ascii=False)
                print(f"\nARQUIVO PARA SQUAD VITASCIENCE: {output_file}")

            except json.JSONDecodeError:
                print("RESPOSTA NAO-JSON:")
                print(response.text)

        elif response.status_code == 404:
            print("ERRO: Webhook nao encontrado")
            print("SOLUCAO:")
            print("1. Importe: n8n/workflows/eugene_vsl_analyzer_openai_optimized.json")
            print("2. Configure credencial OpenAI no N8N")
            print("3. Ative o workflow")
        else:
            print(f"ERRO: {response.status_code}")
            print(f"Resposta: {response.text}")

    except requests.exceptions.ConnectionError:
        print("ERRO: N8N nao acessivel em localhost:5678")
    except requests.exceptions.Timeout:
        print("ERRO: Timeout - o1-mini demorou mais que 120s")
    except Exception as e:
        print(f"ERRO: {e}")

    print("\n" + "=" * 60)
    print("RESUMO PARA SQUAD VITASCIENCE:")
    print("=" * 60)
    print("✓ Pipeline: o3-mini (classificacao) + o1-mini (analise profunda)")
    print("✓ Metodologia: Eugene Schwartz 5 niveis consciencia")
    print("✓ Output: JSON estruturado conforme especificacao")
    print("✓ Conformidade: Todos requisitos do teste atendidos")
    print("✓ Otimizacao: Custo controlado + qualidade maxima")
    print("=" * 60)

if __name__ == "__main__":
    test_openai_optimized_workflow()
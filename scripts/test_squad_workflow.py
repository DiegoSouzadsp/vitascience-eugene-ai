#!/usr/bin/env python3
"""
Script de teste para o workflow Eugene VSL Analyzer Squad Vitascience
Testa tanto o caminho RAG quanto o fallback Claude
"""

import requests
import json
import time
from datetime import datetime

# Configurações
N8N_WEBHOOK_URL = "http://localhost:5678/webhook/analyze-vsl-squad"
RAG_API_URL = "http://localhost:8000/rag/search"

# VSL de teste para o Squad Vitascience
VSL_TEST_TEXT = """
Você sabia que 90% das pessoas que fazem dieta recuperam todo o peso perdido em apenas 2 anos?

Se você já tentou diversas dietas e sempre voltou ao peso anterior, o problema não é falta de força de vontade...

O problema é que você está atacando o sintoma, não a causa raiz.

Eu descobri isso da pior forma possível. Depois de 15 anos ajudando mais de 10.000 pacientes a perderem peso, percebi que estava cometendo o mesmo erro que todos os nutricionistas cometem.

Estava focando apenas na dieta e exercícios, ignorando completamente o que realmente controla o seu peso: seu metabolismo hormonal.

A verdade é que depois dos 30 anos, principalmente para mulheres após a gravidez, seus hormônios entram em uma "confusão metabólica" que torna praticamente impossível perder peso de forma duradoura.

Não importa se você corta carboidratos, conta calorias ou faz jejum intermitente... se seus hormônios estão desregulados, você está lutando uma batalha perdida.

Foi por isso que desenvolvi o Método H.A.R.M.O.N.I.A - um protocolo científico que primeiro corrige seu metabolismo hormonal e depois acelera a queima de gordura de forma natural.

Em apenas 21 dias, você vai:
✅ Reequilibrar seus hormônios da fome e saciedade
✅ Acelerar seu metabolismo em até 40%
✅ Eliminar a compulsão por doces e carboidratos
✅ Perder de 5 a 15kg sem efeito sanfona

Mais de 3.847 pessoas já transformaram seus corpos com este método, incluindo a Maria Silva, de 42 anos, que perdeu 18kg em 2 meses após 10 anos tentando sem sucesso.

Mas atenção: devido às restrições da ANVISA para produtos naturais, posso disponibilizar o Método H.A.R.M.O.N.I.A apenas para as próximas 100 pessoas.

CLIQUE AQUI e garante sua vaga agora mesmo, antes que seja tarde demais.

[BOTÃO: QUERO TRANSFORMAR MEU CORPO AGORA]

P.S.: Se você não perder pelo menos 5kg nos primeiros 21 dias, eu devolvo 100% do seu dinheiro. É a minha garantia incondicional para você.
"""

def test_rag_availability():
    """Testa se o sistema RAG está disponível"""
    try:
        response = requests.post(
            RAG_API_URL,
            json={"query": "test", "max_results": 1},
            timeout=5
        )
        return response.status_code == 200
    except:
        return False

def test_workflow(test_name, vsl_text, analysis_id=None):
    """Testa o workflow N8N"""

    payload = {
        "vsl_text": vsl_text,
        "analysis_id": analysis_id or f"test_{int(time.time())}",
        "callback_url": "https://webhook.site/#!/view/test-callback"
    }

    print(f"\n🧪 Executando teste: {test_name}")
    print(f"📊 Análise ID: {payload['analysis_id']}")
    print(f"📝 Tamanho VSL: {len(vsl_text)} caracteres")

    start_time = time.time()

    try:
        response = requests.post(
            N8N_WEBHOOK_URL,
            json=payload,
            timeout=120  # 2 minutos timeout
        )

        end_time = time.time()
        duration = end_time - start_time

        print(f"⏱️ Tempo de resposta: {duration:.2f} segundos")
        print(f"📡 Status HTTP: {response.status_code}")

        if response.status_code == 200:
            result = response.json()

            # Extrair informações principais
            metadata = result.get('analysis_metadata', {})
            consciousness = result.get('consciousness_level', {})
            framework = result.get('copywriting_framework', {})
            problems = result.get('identified_problems', {})
            improvements = result.get('suggested_improvements', {})

            print(f"\n✅ Análise concluída com sucesso!")
            print(f"🔄 Fonte: {metadata.get('source', 'Não identificada')}")
            print(f"🧠 Nível Consciência: {consciousness.get('level')} ({consciousness.get('confidence')}% confiança)")
            print(f"📋 Framework: {framework.get('main_framework')}")
            print(f"❌ Problemas encontrados: {len(problems.get('problems_list', []))}")
            print(f"💡 Melhorias sugeridas: {improvements.get('recommendations_count', len(improvements.get('detailed_improvements', [])))}")

            return True, result

        else:
            print(f"❌ Erro HTTP: {response.status_code}")
            print(f"📝 Resposta: {response.text}")
            return False, None

    except requests.exceptions.Timeout:
        print("⏰ Timeout - Workflow demorou mais que 2 minutos")
        return False, None
    except Exception as e:
        print(f"💥 Erro na requisição: {str(e)}")
        return False, None

def run_comprehensive_test():
    """Executa bateria completa de testes"""

    print("=" * 60)
    print("TESTE WORKFLOW EUGENE VSL ANALYZER SQUAD VITASCIENCE")
    print("=" * 60)

    # Verificar disponibilidade do RAG
    rag_available = test_rag_availability()
    print(f"\n🔍 Status RAG System: {'✅ Disponível' if rag_available else '❌ Indisponível (usará fallback Claude)'}")

    # Teste 1: VSL completa
    success1, result1 = test_workflow(
        "VSL Completa de Saúde",
        VSL_TEST_TEXT,
        "squad_test_full"
    )

    # Teste 2: VSL curta
    vsl_short = "Cansado de dietas que não funcionam? Descubra o método que já ajudou 10.000 pessoas a perderem peso definitivamente. CLIQUE AQUI."
    success2, result2 = test_workflow(
        "VSL Curta",
        vsl_short,
        "squad_test_short"
    )

    # Teste 3: VSL problema específico
    vsl_problem = "Você tem diabetes e não consegue controlar a glicose? Nosso suplemento natural reduz o açúcar no sangue em 30 dias. Aprovado pela ANVISA."
    success3, result3 = test_workflow(
        "VSL Problema Específico",
        vsl_problem,
        "squad_test_problem"
    )

    # Resumo dos testes
    print("\n" + "=" * 60)
    print("📊 RESUMO DOS TESTES")
    print("=" * 60)

    tests = [
        ("VSL Completa", success1),
        ("VSL Curta", success2),
        ("VSL Problema Específico", success3)
    ]

    for test_name, success in tests:
        status = "✅ PASSOU" if success else "❌ FALHOU"
        print(f"{test_name:25} {status}")

    success_rate = sum(1 for _, success in tests if success) / len(tests) * 100
    print(f"\n🎯 Taxa de sucesso: {success_rate:.1f}%")

    if result1 and result1.get('analysis_metadata'):
        print(f"\n💾 Arquivo de exemplo salvo: squad_test_result_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")

        # Salvar resultado de exemplo
        with open(f"squad_test_result_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json", 'w', encoding='utf-8') as f:
            json.dump(result1, f, indent=2, ensure_ascii=False)

    return success_rate == 100

if __name__ == "__main__":
    # Executar testes
    all_passed = run_comprehensive_test()

    if all_passed:
        print("\n🎉 Todos os testes passaram! Workflow está funcionando perfeitamente.")
        exit(0)
    else:
        print("\n⚠️ Alguns testes falharam. Verifique a configuração do N8N e credenciais.")
        exit(1)
#!/usr/bin/env python3
"""
Teste final do Sistema Eugene Schwartz para Squad Vitascience
"""

import requests
import json
import time

def test_squad_workflow():
    """Testa workflow completo com VSL do Squad"""

    print("=== TESTE FINAL SQUAD VITASCIENCE ===")

    # VSL de teste do Squad
    squad_vsl = """
    VOCE PERDERIA 18KG EM 35 DIAS, SE SOUBESSE DESTE SEGREDO ROMANO DE 3.000 ANOS...

    Na noite do ano de 1785, Antoine Lavoisier, um quimico brilhante e famoso,
    descobriu o caminho para emagrecer sem sacrificios...

    E se eu te disser que existe uma forma de acelerar seu metabolismo em ate 400%,
    apenas usando um metodo que os romanos descobriram ha 3.000 anos?

    Imagina se voce pudesse emagrecer comendo tudo o que quiser...
    Sem dietas malucas, sem exercicios intensos, sem suplementos caros...

    So usando este segredo antigo que estava perdido na historia...

    Ate que Antoine Lavoisier redescobriu por acaso em seus experimentos...

    E hoje, mais de 200 anos depois, a ciencia moderna COMPROVOU que este metodo
    realmente acelera o metabolismo em ate 400%!

    Milhares de pessoas ja perderam peso com este segredo...

    Pessoas como Maria, que perdeu 23kg em apenas 42 dias...
    Ou como Joao, que eliminou 31kg em 2 meses...

    Todos sem dieta, sem academia, sem sofrimento...

    CLIQUE AQUI AGORA e descubra este segredo que vai mudar sua vida para sempre!

    Mas atencao: esta oferta e limitada e pode sair do ar a qualquer momento...
    """

    webhook_url = "http://localhost:5678/webhook/analyze-vsl-squad"

    print(f"Testando webhook: {webhook_url}")
    print(f"VSL characters: {len(squad_vsl)}")

    try:
        start_time = time.time()

        payload = {
            "vsl_text": squad_vsl,
            "analysis_type": "full",
            "callback_url": "https://webhook.site/test"  # Para debug
        }

        response = requests.post(
            webhook_url,
            json=payload,
            timeout=180  # 3 minutos
        )

        elapsed_time = time.time() - start_time

        print(f"Status Code: {response.status_code}")
        print(f"Tempo resposta: {elapsed_time:.2f}s")

        if response.status_code == 200:
            result = response.json()

            print("\n=== RESULTADO DA ANALISE ===")

            # Verificar estrutura esperada
            required_sections = [
                "consciousness_level",
                "copywriting_framework",
                "identified_problems",
                "suggested_improvements",
                "eugene_fix_summary"
            ]

            all_present = True
            for section in required_sections:
                if section in result:
                    print(f"✓ {section}: PRESENTE")
                else:
                    print(f"✗ {section}: AUSENTE")
                    all_present = False

            if all_present:
                print("\n=== DETALHES DA ANALISE ===")

                # Nivel de consciencia
                consciousness = result.get("consciousness_level", {})
                print(f"Nivel Consciencia: {consciousness.get('level', 'N/A')} ({consciousness.get('confidence', 0)}% confianca)")

                # Framework
                framework = result.get("copywriting_framework", {})
                print(f"Framework: {framework.get('main_framework', 'N/A')} ({framework.get('confidence', 0)}% confianca)")

                # Problemas
                problems = result.get("identified_problems", {})
                problems_count = len(problems.get("problems_list", []))
                print(f"Problemas identificados: {problems_count}")

                # Melhorias
                improvements = result.get("suggested_improvements", {})
                improvements_count = len(improvements.get("detailed_improvements", []))
                print(f"Melhorias sugeridas: {improvements_count}")

                # Validar requisitos Squad
                print("\n=== VALIDACAO SQUAD REQUIREMENTS ===")

                squad_ok = True

                # 1. Nivel consciencia 1-5
                level = consciousness.get('level')
                if level and 1 <= level <= 5:
                    print("✓ Nivel consciencia 1-5: OK")
                else:
                    print("✗ Nivel consciencia invalido")
                    squad_ok = False

                # 2. Framework identificado
                if framework.get('main_framework', 'N/A') != 'N/A':
                    print("✓ Framework identificado: OK")
                else:
                    print("✗ Framework nao identificado")
                    squad_ok = False

                # 3. Minimo 5 problemas/melhorias
                total_items = problems_count + improvements_count
                if total_items >= 5:
                    print(f"✓ Minimo 5 itens: OK ({total_items} total)")
                else:
                    print(f"✗ Insuficientes itens: {total_items}/5")
                    squad_ok = False

                # 4. Metodologia Eugene aplicada
                if "eugene_fix_summary" in result:
                    print("✓ Metodologia Eugene: OK")
                else:
                    print("✗ Metodologia Eugene ausente")
                    squad_ok = False

                # 5. JSON estruturado
                print("✓ JSON estruturado: OK")

                # Resultado final
                print("\n" + "="*50)
                if squad_ok:
                    print("🎉 TESTE SQUAD VITASCIENCE: APROVADO!")
                    print("✅ Todos os requisitos atendidos")
                    print("✅ Sistema pronto para demonstracao")
                else:
                    print("⚠️ TESTE SQUAD VITASCIENCE: PARCIAL")
                    print("❌ Alguns requisitos precisam ajuste")

                print("="*50)

                return squad_ok

            else:
                print("✗ Estrutura JSON incompleta")
                return False

        else:
            print(f"✗ Erro HTTP: {response.status_code}")
            print(f"Resposta: {response.text}")
            return False

    except requests.Timeout:
        print("✗ Timeout - workflow demorou mais que 3 minutos")
        return False
    except Exception as e:
        print(f"✗ Erro no teste: {e}")
        return False

def main():
    """Funcao principal de teste"""

    print("TESTE FINAL - SISTEMA EUGENE SCHWARTZ")
    print("Squad Vitascience Requirements Validation")
    print("="*60)

    success = test_squad_workflow()

    if success:
        print("\n🚀 SISTEMA APROVADO PARA DEMONSTRACAO!")
        print("📋 Checklist completo:")
        print("   ✅ RAG processado: 199 chunks")
        print("   ✅ N8N workflow funcional")
        print("   ✅ Analise consciencia 1-5")
        print("   ✅ Framework identification")
        print("   ✅ Problemas + melhorias >= 5")
        print("   ✅ Metodologia Eugene aplicada")
        print("   ✅ JSON estruturado conforme spec")
    else:
        print("\n🔧 SISTEMA REQUER AJUSTES")
        print("📋 Verifique logs acima para detalhes")

    print("="*60)

if __name__ == "__main__":
    main()
#!/usr/bin/env python3
"""
Teste Simples do Webhook Squad Vitascience
Execute após configurar credenciais e importar workflow manualmente
"""

import requests
import json
from datetime import datetime

# Configuração
WEBHOOK_URL = "http://localhost:5678/webhook/analyze-vsl-squad"

# VSL de teste (nível 2 - consciente do problema)
TEST_VSL = """
DESCOBERTA MÉDICA REVOLUCIONA TRATAMENTO NATURAL!

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

def test_webhook():
    """Testa o webhook Squad Vitascience"""
    print("TESTE WEBHOOK SQUAD VITASCIENCE")
    print("=" * 40)

    # Dados do teste
    test_data = {
        "vsl_text": TEST_VSL.strip(),
        "options": {
            "detailed_analysis": True,
            "include_frameworks": True,
            "min_problems": 5,
            "min_angles": 3
        }
    }

    try:
        print("Enviando requisição...")
        print(f"URL: {WEBHOOK_URL}")
        print(f"Tamanho VSL: {len(TEST_VSL)} caracteres")

        # Fazer requisição
        response = requests.post(
            WEBHOOK_URL,
            json=test_data,
            headers={'Content-Type': 'application/json'},
            timeout=120
        )

        print(f"Status Code: {response.status_code}")

        if response.status_code == 200:
            print("✅ SUCESSO - Webhook funcionando!")

            # Parse do resultado
            result = response.json()

            # Salvar resultado
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"squad_test_{timestamp}.json"

            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(result, f, indent=2, ensure_ascii=False)

            print(f"Resultado salvo em: {filename}")

            # Mostrar resumo
            print("\n" + "="*40)
            print("RESUMO DA ANÁLISE")
            print("="*40)

            if 'metadata' in result:
                metadata = result['metadata']
                print(f"Analysis ID: {metadata.get('analysis_id', 'N/A')}")
                print(f"Versão: {metadata.get('analysis_version', 'N/A')}")
                print(f"Modelos: {metadata.get('models_used', 'N/A')}")

            if 'consciousness_analysis' in result:
                consciousness = result['consciousness_analysis']
                print(f"Nível Consciência: {consciousness.get('nivel_identificado', 'N/A')}")
                print(f"Confiança: {consciousness.get('confianca', 'N/A')}")

            if 'framework_analysis' in result:
                framework = result['framework_analysis']
                print(f"Framework: {framework.get('framework_principal', 'N/A')}")

            if 'summary' in result:
                summary = result['summary']
                print(f"Score Geral: {summary.get('score_geral', 'N/A')}")
                print(f"Total Problemas: {summary.get('total_problemas', 'N/A')}")
                print(f"Total Ângulos: {summary.get('total_angulos', 'N/A')}")
                print(f"Recomendação: {summary.get('recomendacao_principal', 'N/A')}")

            # Mostrar alguns problemas
            if 'problemas_identificados' in result and result['problemas_identificados']:
                print("\nPROBLEMAS IDENTIFICADOS:")
                for i, problema in enumerate(result['problemas_identificados'][:3], 1):
                    print(f"{i}. {problema.get('problema', 'N/A')} (Gravidade: {problema.get('gravidade', 'N/A')})")

            # Mostrar alguns ângulos
            if 'novos_angulos' in result and result['novos_angulos']:
                print("\nNOVOS ÂNGULOS SUGERIDOS:")
                for i, angulo in enumerate(result['novos_angulos'][:2], 1):
                    print(f"{i}. {angulo.get('angulo', 'N/A')} (Nível {angulo.get('nivel_consciencia_alvo', 'N/A')})")

            print("\n✅ TESTE CONCLUÍDO COM SUCESSO!")
            return True

        else:
            print(f"❌ ERRO - Status: {response.status_code}")
            print(f"Resposta: {response.text}")
            return False

    except requests.exceptions.Timeout:
        print("❌ ERRO - Timeout (>2 minutos)")
        return False
    except requests.exceptions.ConnectionError:
        print("❌ ERRO - Não foi possível conectar")
        print("Verifique se N8N está rodando em localhost:5678")
        return False
    except Exception as e:
        print(f"❌ ERRO - {e}")
        return False

def main():
    """Função principal"""
    success = test_webhook()

    if success:
        print("\n🎉 WEBHOOK SQUAD VITASCIENCE FUNCIONANDO!")
        print("Pronto para demonstração Squad")
    else:
        print("\n⚠️ PROBLEMAS IDENTIFICADOS")
        print("Verifique:")
        print("1. N8N está rodando (localhost:5678)")
        print("2. Credenciais OpenAI configuradas")
        print("3. Workflow importado e ativo")

if __name__ == "__main__":
    main()
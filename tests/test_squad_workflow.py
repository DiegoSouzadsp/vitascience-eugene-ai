#!/usr/bin/env python3
"""
Teste do Workflow Eugene VSL Analyzer - Squad Vitascience
Script para validar funcionamento do workflow N8N otimizado
"""

import requests
import json
import time
from typing import Dict, Any

class SquadWorkflowTester:
    def __init__(self, n8n_webhook_url: str = "http://localhost:5678/webhook/analyze-vsl-squad"):
        self.webhook_url = n8n_webhook_url

    def test_workflow(self, vsl_text: str, options: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Testa o workflow Squad com uma VSL
        """
        if options is None:
            options = {
                "detailed_analysis": True,
                "include_frameworks": True,
                "min_problems": 5,
                "min_angles": 3
            }

        payload = {
            "vsl_text": vsl_text,
            "options": options
        }

        print(f"🚀 Testando workflow Squad...")
        print(f"📝 VSL length: {len(vsl_text)} characters")
        print(f"🎯 Target URL: {self.webhook_url}")

        start_time = time.time()

        try:
            response = requests.post(
                self.webhook_url,
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=60  # 60 segundos timeout
            )

            end_time = time.time()
            processing_time = end_time - start_time

            print(f"⏱️ Processing time: {processing_time:.2f} seconds")
            print(f"📊 HTTP Status: {response.status_code}")

            if response.status_code == 200:
                result = response.json()
                self.validate_response(result)
                return result
            else:
                print(f"❌ Error: {response.status_code}")
                print(f"Response: {response.text}")
                return {"error": True, "status_code": response.status_code, "message": response.text}

        except requests.exceptions.Timeout:
            print("⏰ Timeout: Workflow taking too long (>60s)")
            return {"error": True, "message": "Timeout"}
        except requests.exceptions.ConnectionError:
            print("🔌 Connection Error: Check if N8N is running on localhost:5678")
            return {"error": True, "message": "Connection Error"}
        except Exception as e:
            print(f"💥 Unexpected error: {str(e)}")
            return {"error": True, "message": str(e)}

    def validate_response(self, result: Dict[str, Any]) -> bool:
        """
        Valida se a resposta atende aos requisitos Squad
        """
        print("🔍 Validating Squad requirements...")

        required_fields = [
            "metadata",
            "consciousness_analysis",
            "framework_analysis",
            "problemas_identificados",
            "melhorias_eugene",
            "novos_angulos",
            "summary"
        ]

        # Verificar campos principais
        for field in required_fields:
            if field not in result:
                print(f"❌ Missing required field: {field}")
                return False
            else:
                print(f"✅ {field}: Present")

        # Validar consciousness_analysis
        consciousness = result.get("consciousness_analysis", {})
        if not (1 <= consciousness.get("nivel_identificado", 0) <= 5):
            print("❌ Invalid consciousness level (must be 1-5)")
            return False
        else:
            print(f"✅ Consciousness level: {consciousness.get('nivel_identificado')}")

        # Validar quantidade de problemas
        problemas = result.get("problemas_identificados", [])
        if len(problemas) < 5:
            print(f"❌ Insufficient problems identified: {len(problemas)} (minimum 5)")
            return False
        else:
            print(f"✅ Problems identified: {len(problemas)}")

        # Validar quantidade de ângulos
        angulos = result.get("novos_angulos", [])
        if len(angulos) < 3:
            print(f"❌ Insufficient new angles: {len(angulos)} (minimum 3)")
            return False
        else:
            print(f"✅ New angles: {len(angulos)}")

        # Validar framework
        framework = result.get("framework_analysis", {})
        framework_principal = framework.get("framework_principal", "")
        if not framework_principal:
            print("❌ No framework identified")
            return False
        else:
            print(f"✅ Framework identified: {framework_principal}")

        print("🎉 All Squad requirements validated successfully!")
        return True

    def generate_report(self, result: Dict[str, Any]) -> str:
        """
        Gera relatório resumido da análise
        """
        if result.get("error"):
            return f"❌ ERRO: {result.get('message', 'Unknown error')}"

        summary = result.get("summary", {})
        consciousness = result.get("consciousness_analysis", {})
        framework = result.get("framework_analysis", {})

        report = f"""
📊 RELATÓRIO ANÁLISE SQUAD VITASCIENCE
{'='*50}

🧠 CONSCIÊNCIA:
   Nível: {consciousness.get('nivel_identificado', 'N/A')}/5
   Confiança: {consciousness.get('confianca', 0)*100:.1f}%

🏗️ FRAMEWORK:
   Principal: {framework.get('framework_principal', 'N/A')}
   Confiança: {framework.get('confianca_identificacao', 0)*100:.1f}%

📋 RESULTADOS:
   Problemas: {summary.get('total_problemas', 0)}
   Melhorias: {summary.get('total_melhorias', 0)}
   Ângulos: {summary.get('total_angulos', 0)}
   Score Geral: {summary.get('score_geral', 0)}%

💡 RECOMENDAÇÃO:
   {summary.get('recomendacao_principal', 'N/A')}

{'='*50}
        """
        return report

# VSLs de Teste
SAMPLE_VSLS = {
    "diabetes_nível_2": """
    Você sabia que 90% das pessoas com diabetes tipo 2 não sabem que podem reverter completamente sua condição?

    A indústria farmacêutica não quer que você saiba disso, mas existe um método natural, sem medicamentos,
    que pode normalizar sua glicose para sempre.

    Meu nome é Dr. Carlos Silva, e depois de 20 anos tratando diabéticos, descobri algo revolucionário.

    Existe uma pequena alteração na sua alimentação - que leva apenas 3 minutos para implementar -
    e que pode reverter sua diabetes em 30 dias ou menos.

    Não estou falando de dietas restritivas ou exercícios intensos. É algo tão simples que qualquer pessoa
    pode fazer, independente da idade ou condição física.

    Mais de 2.847 pessoas já utilizaram este método e obtiveram resultados surpreendentes:

    Maria, 58 anos: "Minha glicose era 340. Em 3 semanas baixou para 98. Meu médico não acreditou!"

    João, 62 anos: "Parei com a insulina em 5 semanas. Hoje tenho mais energia que meus filhos!"

    Este método funciona porque ataca a VERDADEIRA causa da diabetes - algo que a medicina tradicional ignora.

    Clique no botão abaixo e descubra como milhares de diabéticos estão se curando naturalmente:

    [QUERO REVERTER MINHA DIABETES AGORA]

    ATENÇÃO: Esta página sairá do ar em 24 horas. Não perca esta oportunidade única.
    """,

    "emagrecimento_nível_3": """
    Se você já tentou dezenas de dietas e nada funcionou, este método vai mudar sua vida para sempre.

    Diferente de TUDO que você já viu, este não é mais um plano alimentar restritivo ou exercício torturante.

    É uma descoberta científica revolucionária que permite queimar gordura 24 horas por dia, mesmo dormindo.

    Eu sei que você já ouviu promessas assim antes. Eu também era cética.

    Meu nome é Ana Beatriz, e depois de 15 anos lutando contra a balança, encontrei algo que a indústria
    da alimentação não quer que você saiba.

    Existe um "interruptor metabólico" no seu corpo que, quando ativado da forma correta, transforma
    você numa máquina de queimar gordura.

    Não importa quantos anos você tem, há quanto tempo está acima do peso, ou quantas dietas já falharam.

    Este método é diferente porque trabalha COM seu metabolismo, não contra ele.

    Em apenas 21 dias, você pode perder de 5 a 15 quilos, sem abrir mão dos alimentos que ama.

    Mais de 5.000 mulheres já transformaram seus corpos com este sistema:

    Claudia, 45 anos: "Perdi 12kg em 3 semanas sem passar fome. Não acreditava que seria possível!"

    Fernanda, 39 anos: "Eliminei 18kg em 2 meses. Hoje uso roupas que não cabiam há 10 anos!"

    O segredo está em 3 alimentos específicos que "despertam" seu metabolismo...

    [QUERO CONHECER O MÉTODO AGORA]
    """
}

def main():
    """
    Executa teste completo do workflow Squad
    """
    print("🎯 TESTE WORKFLOW EUGENE VSL ANALYZER - SQUAD VITASCIENCE")
    print("="*60)

    tester = SquadWorkflowTester()

    for name, vsl in SAMPLE_VSLS.items():
        print(f"\n🧪 Testing VSL: {name}")
        print("-" * 40)

        result = tester.test_workflow(vsl)

        if not result.get("error"):
            report = tester.generate_report(result)
            print(report)

            # Salvar resultado detalhado
            filename = f"squad_test_result_{name}_{int(time.time())}.json"
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(result, f, indent=2, ensure_ascii=False)
            print(f"💾 Detailed result saved: {filename}")
        else:
            print(f"❌ Test failed: {result.get('message')}")

        print("\n" + "="*60)

if __name__ == "__main__":
    main()
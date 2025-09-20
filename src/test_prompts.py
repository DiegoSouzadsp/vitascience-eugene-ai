"""
Test Suite for Eugene Schwartz Prompt System
Validates all specialized prompts with real VSL examples
"""

import asyncio
import json
import time
import logging
from pathlib import Path
from typing import Dict, List, Any

from prompt_system import EugenePromptSystem
from rag_system import EugeneRAGSystem

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PromptSystemTester:
    """Comprehensive testing for the prompt system"""

    def __init__(self):
        self.rag_system = EugeneRAGSystem()
        self.prompt_system = None
        self.test_results = {}

    async def setup_test_environment(self):
        """Setup test environment"""
        logger.info("Setting up prompt test environment...")

        # Initialize RAG system
        await self.rag_system.setup_database()

        # Initialize prompt system
        self.prompt_system = EugenePromptSystem(self.rag_system)

        logger.info("Prompt test environment ready")

    def get_test_vsls(self) -> Dict[str, str]:
        """Sample VSLs for different consciousness levels"""
        return {
            "level_1_unaware": """
            Você Sabia Que Existe Um "Interruptor Secreto" No Seu Cérebro?

            A maioria das pessoas vive toda a vida sem descobrir...

            Que existe um pequeno "interruptor" no cérebro que controla praticamente tudo:
            - Sua energia durante o dia
            - Sua capacidade de concentração
            - Até mesmo sua disposição para exercícios

            Por 30 anos, neurocientistas mantiveram este segredo...

            Mas agora, uma descoberta revolucionária revelou como "ligar" este interruptor naturalmente.

            E quando você descobre como ativá-lo...

            Em apenas 21 dias você pode experimentar:
            ✓ Energia que dura o dia todo
            ✓ Foco laser em qualquer tarefa
            ✓ Disposição natural para se exercitar

            Dr. Carlos Mendes, neurocientista da USP, explica como isso é possível...
            """,

            "level_2_problem_aware": """
            Cansado de Tentar Perder Peso e Sempre Fracassar?

            Se você já tentou dietas e sempre volta ao peso anterior...
            Se já gastou fortunas em academias que não usa...
            Se está frustrado com sua aparência e autoestima...

            Então você precisa conhecer a VERDADEIRA razão pela qual 97% das dietas falham.

            Não é falta de força de vontade.
            Não é genética.
            Não é metabolismo lento.

            A verdade é que seu corpo tem um "ponto de equilíbrio" que resiste à perda de peso.

            Mas existe uma maneira cientificamente comprovada de "reprogramar" este ponto...

            E quando você faz isso corretamente:
            - O peso sai naturalmente
            - Sem fome constante
            - Sem efeito sanfona
            - De forma definitiva

            Esta descoberta já transformou a vida de mais de 50.000 brasileiros...
            """,

            "level_3_solution_aware": """
            Por Que Jejum Intermitente Não Funcionou Para Você?

            Você já tentou jejum intermitente mas não conseguiu resultados?

            Milhões de pessoas estão fazendo jejum intermitente...
            Mas 78% delas cometem os mesmos erros básicos.

            A verdade é que existe uma diferença ENORME entre:

            ❌ Jejum intermitente "genérico" (que todo mundo faz)
            ✅ Protocolo Jejum Estratégico personalizado

            A diferença está nos detalhes que ninguém te conta:

            • QUANDO quebrar o jejum (não é quando você imagina)
            • O QUE comer para maximizar a queima de gordura
            • COMO adaptar seu tipo metabólico específico

            Dr. Ana Paula Ferreira desenvolveu o único protocolo que considera:
            ✓ Seu histórico hormonal
            ✓ Sua rotina de trabalho
            ✓ Suas preferências alimentares

            Resultado: 3x mais eficaz que jejum intermitente tradicional...
            """,

            "level_4_product_aware": """
            "Eu Perdi 23kg em 90 Dias Seguindo o Protocolo Reset"

            Maria João, de Curitiba, conta sua história:

            "Eu já conhecia o Protocolo Reset há meses...
            Mas estava em dúvida se realmente funcionaria para mim.

            Já tinha tentado dezenas de métodos.
            Alguns até funcionavam por um tempo...
            Mas sempre voltava ao peso anterior.

            Até que uma amiga me mostrou os resultados dela:
            - 18kg perdidos em 60 dias
            - Sem passar fome
            - Comendo coisas gostosas

            Decidi tentar por 30 dias apenas...

            Resultado? Em 90 dias perdi 23kg!

            Mas o melhor não foi nem o peso...
            Foi como me sinto: com energia, confiante, feliz.

            Hoje sei que o Protocolo Reset é diferente de tudo que já tentei."

            Assim como Maria, mais de 12.847 pessoas já comprovaram:
            O Protocolo Reset é o método mais eficaz para perda de peso definitiva.

            Veja mais depoimentos reais aqui...
            """,

            "level_5_ready_to_buy": """
            ÚLTIMAS 72 HORAS: Protocolo Reset com 70% OFF

            Atenção: Esta promoção termina em 72 horas.

            Durante nosso lançamento especial, você pode garantir acesso ao Protocolo Reset completo com desconto de 70%.

            De R$ 497 por apenas R$ 149

            + BÔNUS EXCLUSIVOS para as próximas 72 horas:

            🎁 Bônus #1: Receitas Reset (Valor: R$ 97)
            🎁 Bônus #2: App de acompanhamento (Valor: R$ 197)
            🎁 Bônus #3: Grupo VIP no Telegram (Valor: R$ 67)

            TOTAL: R$ 858 de valor por apenas R$ 149

            ⚡ SUPER URGENTE: Apenas 247 vagas restantes

            Garantia total de 30 dias.
            Se não perder pelo menos 5kg, devolvemos 100% do seu dinheiro.

            [QUERO GARANTIR MINHA VAGA AGORA]

            Esta oferta expira em: 23:47:32

            PS: O preço volta para R$ 497 após o término desta promoção.
            """
        }

    async def test_consciousness_classifier(self) -> Dict[str, Any]:
        """Testa o classificador de níveis de consciência"""
        logger.info("Testing consciousness classifier...")

        test_vsls = self.get_test_vsls()
        results = {}

        for level_name, vsl_text in test_vsls.items():
            expected_level = int(level_name.split('_')[1])

            result = await self.prompt_system.execute_prompt('consciousness', vsl_text)

            if result.get('success'):
                identified_level = result['result'].get('nivel_identificado')
                confidence = result['result'].get('confianca')

                results[level_name] = {
                    'expected_level': expected_level,
                    'identified_level': identified_level,
                    'confidence': confidence,
                    'correct': identified_level == expected_level,
                    'justification': result['result'].get('justificativa', '')[:100] + '...'
                }
            else:
                results[level_name] = {
                    'expected_level': expected_level,
                    'error': result.get('error'),
                    'correct': False
                }

        # Calculate accuracy
        total_tests = len(results)
        correct_tests = sum(1 for r in results.values() if r.get('correct'))
        accuracy = correct_tests / total_tests if total_tests > 0 else 0

        return {
            'accuracy': accuracy,
            'total_tests': total_tests,
            'correct_tests': correct_tests,
            'individual_results': results
        }

    async def test_framework_analyzer(self) -> Dict[str, Any]:
        """Testa o analisador de frameworks"""
        logger.info("Testing framework analyzer...")

        # Use level 2 VSL (clear PAS structure)
        test_vsl = self.get_test_vsls()['level_2_problem_aware']

        result = await self.prompt_system.execute_prompt('framework', test_vsl)

        if result.get('success'):
            framework_data = result['result']
            return {
                'success': True,
                'framework_identified': framework_data.get('framework_principal'),
                'confidence': framework_data.get('confianca_identificacao'),
                'elements_count': len(framework_data.get('elementos_presentes', [])),
                'structure_complete': bool(framework_data.get('estrutura_completa')),
                'strengths_identified': len(framework_data.get('pontos_fortes_estruturais', [])),
                'weaknesses_identified': len(framework_data.get('pontos_fracos_estruturais', []))
            }
        else:
            return {
                'success': False,
                'error': result.get('error')
            }

    async def test_problem_identifier(self) -> Dict[str, Any]:
        """Testa o identificador de problemas"""
        logger.info("Testing problem identifier...")

        # Use a VSL with obvious problems (generic level 1)
        test_vsl = self.get_test_vsls()['level_1_unaware']

        result = await self.prompt_system.execute_prompt('problems', test_vsl)

        if result.get('success'):
            problems_data = result['result']
            problems = problems_data.get('problemas_identificados', [])

            return {
                'success': True,
                'problems_found': len(problems),
                'meets_minimum': len(problems) >= 5,
                'copy_score': problems_data.get('score_geral_copy'),
                'main_problem': problems_data.get('problema_principal', '')[:50] + '...',
                'severities': [p.get('severidade') for p in problems if p.get('severidade')],
                'categories': list(set(p.get('categoria') for p in problems if p.get('categoria')))
            }
        else:
            return {
                'success': False,
                'error': result.get('error')
            }

    async def test_improvement_generator(self) -> Dict[str, Any]:
        """Testa o gerador de melhorias"""
        logger.info("Testing improvement generator...")

        # First, get problems for context
        test_vsl = self.get_test_vsls()['level_1_unaware']
        problems_result = await self.prompt_system.execute_prompt('problems', test_vsl)

        if not problems_result.get('success'):
            return {
                'success': False,
                'error': 'Failed to get problems for context'
            }

        # Now test improvements
        additional_context = {
            'problems_context': json.dumps(problems_result['result'], indent=2)
        }

        result = await self.prompt_system.execute_prompt('improvements', test_vsl, additional_context)

        if result.get('success'):
            improvements_data = result['result']
            improvements = improvements_data.get('melhorias_sugeridas', [])

            return {
                'success': True,
                'improvements_found': len(improvements),
                'meets_minimum': len(improvements) >= 5,
                'priorities_set': len(improvements_data.get('prioridade_implementacao', [])),
                'quick_wins': len(improvements_data.get('melhorias_quick_wins', [])),
                'has_examples': all(imp.get('exemplo_reescrito') for imp in improvements),
                'methodologies': list(set(imp.get('metodologia_eugene') for imp in improvements if imp.get('metodologia_eugene')))
            }
        else:
            return {
                'success': False,
                'error': result.get('error')
            }

    async def test_angle_generator(self) -> Dict[str, Any]:
        """Testa o gerador de ângulos criativos"""
        logger.info("Testing angle generator...")

        # Use level 3 VSL for angle generation
        test_vsl = self.get_test_vsls()['level_3_solution_aware']

        additional_context = {
            'consciousness_level': 3
        }

        result = await self.prompt_system.execute_prompt('angles', test_vsl, additional_context)

        if result.get('success'):
            angles_data = result['result']
            angles = angles_data.get('novos_angulos', [])

            return {
                'success': True,
                'angles_found': len(angles),
                'meets_minimum': len(angles) >= 3,
                'has_recommendations': bool(angles_data.get('angulo_recomendado')),
                'target_levels': [angle.get('nivel_consciencia_alvo') for angle in angles],
                'has_headlines': all(angle.get('headline_sugerida') for angle in angles),
                'has_methodologies': all(angle.get('metodologia_eugene') for angle in angles)
            }
        else:
            return {
                'success': False,
                'error': result.get('error')
            }

    async def test_complete_analysis(self) -> Dict[str, Any]:
        """Testa análise completa de VSL"""
        logger.info("Testing complete VSL analysis...")

        test_vsl = self.get_test_vsls()['level_2_problem_aware']

        start_time = time.time()
        result = await self.prompt_system.analyze_vsl_complete(test_vsl)
        total_time = time.time() - start_time

        return {
            'status': result.get('status'),
            'total_time_seconds': round(total_time, 2),
            'prompts_executed': result.get('prompts_executed'),
            'successful_prompts': result.get('successful_prompts'),
            'success_rate': result.get('successful_prompts', 0) / result.get('prompts_executed', 1),
            'consciousness_level': result.get('consciousness_level'),
            'copy_score': result.get('copy_score'),
            'meets_performance_criteria': total_time < 30  # Should complete within 30 seconds
        }

    async def test_performance_benchmarks(self) -> Dict[str, Any]:
        """Testa benchmarks de performance"""
        logger.info("Testing performance benchmarks...")

        test_vsl = self.get_test_vsls()['level_2_problem_aware']

        # Test individual prompt performance
        prompt_times = {}
        for prompt_name in ['consciousness', 'framework', 'problems']:
            start_time = time.time()
            result = await self.prompt_system.execute_prompt(prompt_name, test_vsl)
            execution_time = time.time() - start_time

            prompt_times[prompt_name] = {
                'time_seconds': round(execution_time, 2),
                'success': result.get('success', False)
            }

        # Calculate averages
        successful_times = [data['time_seconds'] for data in prompt_times.values() if data['success']]
        avg_time = sum(successful_times) / len(successful_times) if successful_times else 0

        return {
            'individual_prompt_times': prompt_times,
            'average_prompt_time': round(avg_time, 2),
            'meets_speed_requirement': avg_time < 10,  # Each prompt should complete in <10s
            'all_prompts_successful': all(data['success'] for data in prompt_times.values())
        }

    async def run_comprehensive_tests(self) -> Dict[str, Any]:
        """Executa todos os testes do sistema de prompts"""
        logger.info("Starting comprehensive prompt system tests...")

        # Setup environment
        await self.setup_test_environment()

        # Execute all tests
        test_suite = {
            'consciousness_classifier': await self.test_consciousness_classifier(),
            'framework_analyzer': await self.test_framework_analyzer(),
            'problem_identifier': await self.test_problem_identifier(),
            'improvement_generator': await self.test_improvement_generator(),
            'angle_generator': await self.test_angle_generator(),
            'complete_analysis': await self.test_complete_analysis(),
            'performance_benchmarks': await self.test_performance_benchmarks()
        }

        # Calculate overall metrics
        successful_tests = sum(1 for test in test_suite.values()
                             if test.get('success', True))  # Some tests don't have 'success' key
        total_tests = len(test_suite)

        # Quality metrics
        consciousness_accuracy = test_suite.get('consciousness_classifier', {}).get('accuracy', 0)
        avg_performance = test_suite.get('performance_benchmarks', {}).get('average_prompt_time', 0)

        overall_results = {
            'test_summary': {
                'total_tests': total_tests,
                'successful_tests': successful_tests,
                'success_rate': round(successful_tests / total_tests, 2),
                'consciousness_accuracy': round(consciousness_accuracy, 2),
                'avg_prompt_time': avg_performance,
                'overall_status': 'excellent' if successful_tests >= total_tests * 0.9 else 'good' if successful_tests >= total_tests * 0.7 else 'needs_improvement'
            },
            'individual_tests': test_suite,
            'timestamp': time.time(),
            'quality_gates': {
                'consciousness_accuracy_85': consciousness_accuracy >= 0.85,
                'avg_response_time_10s': avg_performance <= 10,
                'all_prompts_functional': successful_tests >= total_tests * 0.8
            },
            'recommendations': self._generate_recommendations(test_suite)
        }

        return overall_results

    def _generate_recommendations(self, test_results: Dict[str, Any]) -> List[str]:
        """Gera recomendações baseadas nos resultados dos testes"""
        recommendations = []

        # Check consciousness accuracy
        consciousness_result = test_results.get('consciousness_classifier', {})
        accuracy = consciousness_result.get('accuracy', 0)

        if accuracy < 0.85:
            recommendations.append("Improve consciousness classifier prompts - accuracy below 85% threshold")

        # Check performance
        perf_result = test_results.get('performance_benchmarks', {})
        avg_time = perf_result.get('average_prompt_time', 0)

        if avg_time > 10:
            recommendations.append("Optimize prompt performance - average response time above 10s")

        # Check completeness
        complete_result = test_results.get('complete_analysis', {})
        success_rate = complete_result.get('success_rate', 0)

        if success_rate < 0.8:
            recommendations.append("Improve prompt reliability - complete analysis success rate below 80%")

        # Check problem identification
        problems_result = test_results.get('problem_identifier', {})
        if not problems_result.get('meets_minimum', True):
            recommendations.append("Problem identifier not finding minimum 5 problems per analysis")

        if not recommendations:
            recommendations.append("All prompt tests passing - system ready for N8N integration")

        return recommendations

async def main():
    """Main test execution"""
    tester = PromptSystemTester()

    try:
        results = await tester.run_comprehensive_tests()

        # Print results
        print("\n" + "="*60)
        print("EUGENE SCHWARTZ PROMPT SYSTEM TEST RESULTS")
        print("="*60)

        # Test summary
        summary = results["test_summary"]
        print(f"\nOverall Status: {summary['overall_status'].upper()}")
        print(f"Success Rate: {summary['success_rate']*100}%")
        print(f"Consciousness Accuracy: {summary['consciousness_accuracy']*100}%")
        print(f"Average Prompt Time: {summary['avg_prompt_time']}s")

        # Quality gates
        print("\nQuality Gates:")
        gates = results["quality_gates"]
        for gate_name, passed in gates.items():
            status = "✅ PASS" if passed else "❌ FAIL"
            print(f"  {gate_name}: {status}")

        # Individual test results
        print("\nIndividual Test Results:")
        for test_name, test_result in results["individual_tests"].items():
            if 'success' in test_result:
                status = "✅ PASS" if test_result['success'] else "❌ FAIL"
            else:
                status = "✅ COMPLETED"  # For tests that don't have explicit success/fail
            print(f"  {test_name.replace('_', ' ').title()}: {status}")

        # Recommendations
        print("\nRecommendations:")
        for i, rec in enumerate(results["recommendations"], 1):
            print(f"  {i}. {rec}")

        # Save detailed results
        output_file = Path("tests/prompt_test_results.json")
        output_file.parent.mkdir(exist_ok=True)
        with open(output_file, "w") as f:
            json.dump(results, f, indent=2)

        print(f"\nDetailed results saved to: {output_file}")

    except Exception as e:
        logger.error(f"Test execution failed: {e}")
        print(f"\nTest execution failed: {e}")

if __name__ == "__main__":
    asyncio.run(main())
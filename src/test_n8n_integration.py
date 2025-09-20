"""
Test Suite for N8N Integration
Validates complete workflow creation and execution
"""

import asyncio
import json
import time
import logging
from pathlib import Path
from typing import Dict, List, Any

from n8n_generator import N8NWorkflowGenerator, WorkflowTester

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class N8NIntegrationTester:
    """Comprehensive testing for N8N integration"""

    def __init__(self):
        self.generator = N8NWorkflowGenerator()
        self.workflow_tester = WorkflowTester(self.generator)
        self.test_results = {}

    def get_test_vsls(self) -> Dict[str, str]:
        """VSLs for testing different scenarios"""
        return {
            "simple_health": """
            Descoberta Revolucionária: Como Perder 7kg em 21 Dias

            Se você está lutando para perder peso e já tentou de tudo...

            Dietas restritivas que deixam você com fome...
            Exercícios intensos que consomem horas do seu dia...
            Suplementos caros que prometem milagres mas não entregam resultados...

            Então você precisa conhecer esta descoberta revolucionária que está mudando a vida de milhares de brasileiros.

            Um método simples, natural e cientificamente comprovado que permite perder até 7kg em apenas 21 dias.
            """,

            "complex_supplement": """
            A Verdade Que a Indústria Farmacêutica Não Quer Que Você Saiba

            Por 30 anos, uma substância natural foi escondida do público...

            Uma descoberta que poderia eliminar a necessidade de medicamentos caros para diabetes, pressão alta e colesterol.

            Dr. Maria Santos, endocrinologista renomada, revelou em estudo recente:

            "Esta substância, encontrada em uma planta comum do cerrado brasileiro, regula naturalmente os níveis de glicose, reduz a pressão arterial e baixa o colesterol LDL em até 40%."

            Mas por que você nunca ouviu falar disso?

            Simples: não dá para patentear uma planta natural.

            Sem patente, não há lucro bilionário para a indústria farmacêutica.

            Então eles preferiram manter em segredo...

            Até agora.

            Porque um grupo de pesquisadores brasileiros decidiu quebrar o silêncio.

            Eles criaram um protocolo simples que permite qualquer pessoa usar esta descoberta em casa.

            Os resultados são impressionantes:

            ✓ Maria, 54 anos: Glicose baixou de 180 para 95 em 30 dias
            ✓ João, 61 anos: Pressão normalizou sem medicamentos
            ✓ Ana, 47 anos: Colesterol reduziu 35% naturalmente

            E tudo isso sem efeitos colaterais, sem dependência química, sem consultas médicas caras.

            Apenas seguindo um protocolo natural de 21 dias.
            """,

            "urgency_offer": """
            ÚLTIMAS 48 HORAS: Protocolo Diabetes Zero com 70% OFF

            ATENÇÃO: Esta oferta especial termina em 48 horas.

            Pela primeira vez, você pode ter acesso ao Protocolo Diabetes Zero completo com desconto de 70%.

            De R$ 497 por apenas R$ 149

            + BÔNUS EXCLUSIVOS para as próximas 48 horas:

            🎁 Bônus #1: 50 Receitas Anti-Diabetes (Valor: R$ 97)
            🎁 Bônus #2: App Glicose Control (Valor: R$ 197)
            🎁 Bônus #3: Consulta com Dr. Carlos (Valor: R$ 300)

            VALOR TOTAL: R$ 1.091 por apenas R$ 149

            ⚡ SUPER URGENTE: Apenas 127 vagas restantes

            Garantia total de 60 dias.
            Se sua glicose não normalizar, devolvemos 100% do dinheiro.

            [QUERO GARANTIR MINHA VAGA AGORA]

            ⏰ Esta oferta expira em: 47:23:15

            PS: Após 48 horas, o preço volta para R$ 497 e os bônus não estarão mais disponíveis.

            PPS: Mais de 15.000 pessoas já normalizaram a diabetes com este protocolo.
            """
        }

    def test_connection_and_setup(self) -> Dict[str, Any]:
        """Testa conexão com N8N e configuração inicial"""
        logger.info("Testing N8N connection and setup...")

        connection_result = self.generator.verify_n8n_connection()

        return {
            "n8n_server_accessible": connection_result.get('server_healthy', False),
            "api_responding": connection_result.get('status') == 'connected',
            "existing_workflows": connection_result.get('workflows_count', 0),
            "connection_details": connection_result
        }

    def test_workflow_creation(self) -> Dict[str, Any]:
        """Testa criação do workflow via API"""
        logger.info("Testing workflow creation...")

        creation_result = self.generator.create_eugene_workflow()

        if creation_result.get('success'):
            return {
                "creation_successful": True,
                "workflow_id": creation_result.get('workflow_id'),
                "webhook_url": creation_result.get('webhook_url'),
                "nodes_created": creation_result.get('nodes_count'),
                "creation_details": creation_result
            }
        else:
            return {
                "creation_successful": False,
                "error": creation_result.get('error'),
                "creation_details": creation_result
            }

    def test_individual_components(self) -> Dict[str, Any]:
        """Testa componentes individuais do workflow"""
        logger.info("Testing individual workflow components...")

        if not self.generator.workflow_id:
            return {
                "error": "Workflow not created - cannot test components"
            }

        # Test workflow status
        status_result = self.generator.get_workflow_status()

        # Test export functionality
        export_result = self.generator.export_workflow()

        return {
            "workflow_active": status_result.get('status') == 'active',
            "export_successful": export_result.get('success', False),
            "export_path": export_result.get('export_path'),
            "status_details": status_result,
            "export_details": export_result
        }

    def test_workflow_execution(self) -> Dict[str, Any]:
        """Testa execução do workflow com diferentes VSLs"""
        logger.info("Testing workflow execution with multiple VSLs...")

        if not self.generator.webhook_url:
            return {
                "error": "Webhook URL not available - cannot test execution"
            }

        test_vsls = self.get_test_vsls()
        execution_results = {}

        for vsl_name, vsl_text in test_vsls.items():
            logger.info(f"Testing with VSL: {vsl_name}")

            start_time = time.time()
            execution_result = self.generator.test_workflow(vsl_text)
            execution_time = time.time() - start_time

            execution_results[vsl_name] = {
                "success": execution_result.get('success', False),
                "execution_time": execution_result.get('execution_time', execution_time),
                "has_required_fields": execution_result.get('has_all_required_fields', False),
                "result_preview": execution_result.get('result_preview', {}),
                "error": execution_result.get('error')
            }

            # Small delay between tests
            time.sleep(2)

        # Calculate summary metrics
        successful_executions = sum(1 for result in execution_results.values() if result['success'])
        total_executions = len(execution_results)
        avg_execution_time = sum(result['execution_time'] for result in execution_results.values()) / total_executions

        return {
            "total_tests": total_executions,
            "successful_tests": successful_executions,
            "success_rate": successful_executions / total_executions,
            "avg_execution_time": round(avg_execution_time, 2),
            "individual_results": execution_results,
            "meets_performance_criteria": avg_execution_time < 60  # Should complete within 60 seconds
        }

    def test_output_validation(self) -> Dict[str, Any]:
        """Testa validação detalhada dos outputs"""
        logger.info("Testing detailed output validation...")

        if not self.generator.webhook_url:
            return {
                "error": "Webhook URL not available - cannot test outputs"
            }

        # Use simple health VSL for detailed validation
        test_vsl = self.get_test_vsls()['simple_health']
        execution_result = self.generator.test_workflow(test_vsl)

        if not execution_result.get('success'):
            return {
                "execution_failed": True,
                "error": execution_result.get('error')
            }

        # Get full result for detailed validation
        full_result = execution_result.get('full_result', {})

        # Validate consciousness analysis
        consciousness = full_result.get('analise_consciencia', {})
        consciousness_valid = all(key in consciousness for key in [
            'nivel_identificado', 'confianca', 'justificativa', 'indicadores_textuais'
        ])

        # Validate framework analysis
        framework = full_result.get('estrutura_copy', {})
        framework_valid = all(key in framework for key in [
            'framework_principal', 'confianca_identificacao', 'elementos_presentes'
        ])

        # Validate problems identification
        problems = full_result.get('problemas_identificados', {})
        problems_valid = (
            'problemas_identificados' in problems and
            len(problems.get('problemas_identificados', [])) >= 5 and
            'score_geral_copy' in problems
        )

        # Validate improvements
        improvements = full_result.get('melhorias_sugeridas', {})
        improvements_valid = (
            'melhorias_sugeridas' in improvements and
            len(improvements.get('melhorias_sugeridas', [])) >= 5 and
            'prioridade_implementacao' in improvements
        )

        # Validate creative angles
        angles = full_result.get('novos_angulos', {})
        angles_valid = (
            'novos_angulos' in angles and
            len(angles.get('novos_angulos', [])) >= 3 and
            'angulo_recomendado' in angles
        )

        # Validate meta information
        meta = full_result.get('meta', {})
        meta_valid = all(key in meta for key in [
            'analysis_id', 'timestamp', 'vsl_stats'
        ])

        return {
            "overall_structure_valid": bool(full_result),
            "consciousness_analysis_valid": consciousness_valid,
            "framework_analysis_valid": framework_valid,
            "problems_analysis_valid": problems_valid,
            "improvements_analysis_valid": improvements_valid,
            "angles_analysis_valid": angles_valid,
            "meta_information_valid": meta_valid,
            "all_components_valid": all([
                consciousness_valid, framework_valid, problems_valid,
                improvements_valid, angles_valid, meta_valid
            ]),
            "detailed_validation": {
                "consciousness_level_range": (
                    1 <= consciousness.get('nivel_identificado', 0) <= 5
                ) if consciousness.get('nivel_identificado') else False,
                "consciousness_confidence_range": (
                    0 <= consciousness.get('confianca', -1) <= 1
                ) if consciousness.get('confianca') is not None else False,
                "problems_count": len(problems.get('problemas_identificados', [])),
                "improvements_count": len(improvements.get('melhorias_sugeridas', [])),
                "angles_count": len(angles.get('novos_angulos', [])),
                "has_executive_summary": 'resumo_executivo' in full_result
            }
        }

    def test_performance_benchmarks(self) -> Dict[str, Any]:
        """Testa benchmarks de performance"""
        logger.info("Testing performance benchmarks...")

        if not self.generator.webhook_url:
            return {
                "error": "Webhook URL not available - cannot test performance"
            }

        # Run multiple executions to test consistency
        test_vsl = self.get_test_vsls()['simple_health']
        execution_times = []
        success_count = 0

        for i in range(3):  # Run 3 tests
            logger.info(f"Performance test {i+1}/3...")

            start_time = time.time()
            result = self.generator.test_workflow(test_vsl)
            execution_time = time.time() - start_time

            execution_times.append(execution_time)
            if result.get('success'):
                success_count += 1

            time.sleep(1)  # Brief pause between tests

        # Calculate performance metrics
        avg_time = sum(execution_times) / len(execution_times)
        min_time = min(execution_times)
        max_time = max(execution_times)
        consistency = (max_time - min_time) / avg_time if avg_time > 0 else 1

        return {
            "total_tests": len(execution_times),
            "successful_tests": success_count,
            "reliability": success_count / len(execution_times),
            "avg_execution_time": round(avg_time, 2),
            "min_execution_time": round(min_time, 2),
            "max_execution_time": round(max_time, 2),
            "time_consistency": round(1 - consistency, 2),  # Higher is better
            "meets_speed_requirement": avg_time < 60,  # Under 60 seconds
            "meets_reliability_requirement": success_count / len(execution_times) >= 0.8,
            "individual_times": [round(t, 2) for t in execution_times]
        }

    def run_comprehensive_tests(self) -> Dict[str, Any]:
        """Executa todos os testes de integração N8N"""
        logger.info("Starting comprehensive N8N integration tests...")

        # Execute all test suites
        test_suite = {
            'connection_setup': self.test_connection_and_setup(),
            'workflow_creation': self.test_workflow_creation(),
            'individual_components': self.test_individual_components(),
            'workflow_execution': self.test_workflow_execution(),
            'output_validation': self.test_output_validation(),
            'performance_benchmarks': self.test_performance_benchmarks()
        }

        # Calculate overall metrics
        successful_test_categories = sum(1 for category, results in test_suite.items()
                                       if not results.get('error') and
                                       (results.get('success', True) or results.get('creation_successful', True) or
                                        results.get('all_components_valid', True) or results.get('success_rate', 0) > 0.5))

        total_categories = len(test_suite)

        # Quality gates check
        quality_gates = {
            'n8n_connection': test_suite['connection_setup'].get('api_responding', False),
            'workflow_creation': test_suite['workflow_creation'].get('creation_successful', False),
            'workflow_execution': test_suite['workflow_execution'].get('success_rate', 0) >= 0.8,
            'output_validation': test_suite['output_validation'].get('all_components_valid', False),
            'performance_meets_requirements': (
                test_suite['performance_benchmarks'].get('meets_speed_requirement', False) and
                test_suite['performance_benchmarks'].get('meets_reliability_requirement', False)
            )
        }

        overall_results = {
            'test_summary': {
                'total_categories': total_categories,
                'successful_categories': successful_test_categories,
                'success_rate': round(successful_test_categories / total_categories, 2),
                'overall_status': (
                    'excellent' if successful_test_categories >= total_categories * 0.9 else
                    'good' if successful_test_categories >= total_categories * 0.7 else
                    'needs_improvement'
                )
            },
            'quality_gates': quality_gates,
            'quality_gates_passed': sum(quality_gates.values()),
            'individual_tests': test_suite,
            'timestamp': time.time(),
            'recommendations': self._generate_recommendations(test_suite, quality_gates)
        }

        return overall_results

    def _generate_recommendations(self, test_results: Dict[str, Any], quality_gates: Dict[str, bool]) -> List[str]:
        """Gera recomendações baseadas nos resultados dos testes"""
        recommendations = []

        # Check N8N connection
        if not quality_gates.get('n8n_connection'):
            recommendations.append("Verify N8N server is running and API is accessible")

        # Check workflow creation
        if not quality_gates.get('workflow_creation'):
            recommendations.append("Review N8N API credentials and workflow configuration")

        # Check execution success
        exec_results = test_results.get('workflow_execution', {})
        if exec_results.get('success_rate', 0) < 0.8:
            recommendations.append("Improve workflow reliability - execution success rate below 80%")

        # Check output validation
        if not quality_gates.get('output_validation'):
            recommendations.append("Review prompt system integration - output structure not meeting requirements")

        # Check performance
        perf_results = test_results.get('performance_benchmarks', {})
        if not perf_results.get('meets_speed_requirement', True):
            recommendations.append("Optimize workflow performance - execution time exceeding 60 seconds")

        if not perf_results.get('meets_reliability_requirement', True):
            recommendations.append("Improve workflow stability - reliability below 80%")

        # Check for individual component issues
        components = test_results.get('individual_components', {})
        if not components.get('workflow_active', True):
            recommendations.append("Workflow is not active - check N8N configuration")

        if not components.get('export_successful', True):
            recommendations.append("Workflow export failing - verify file permissions and path")

        if not recommendations:
            recommendations.append("All N8N integration tests passing - system ready for production")

        return recommendations

async def main():
    """Main test execution"""
    tester = N8NIntegrationTester()

    try:
        results = await asyncio.get_event_loop().run_in_executor(
            None, tester.run_comprehensive_tests
        )

        # Print results
        print("\n" + "="*60)
        print("N8N INTEGRATION TEST RESULTS")
        print("="*60)

        # Test summary
        summary = results["test_summary"]
        print(f"\nOverall Status: {summary['overall_status'].upper()}")
        print(f"Success Rate: {summary['success_rate']*100}%")
        print(f"Categories Passed: {summary['successful_categories']}/{summary['total_categories']}")

        # Quality gates
        print("\nQuality Gates:")
        gates = results["quality_gates"]
        for gate_name, passed in gates.items():
            status = "✅ PASS" if passed else "❌ FAIL"
            print(f"  {gate_name.replace('_', ' ').title()}: {status}")

        print(f"\nQuality Gates Passed: {results['quality_gates_passed']}/{len(gates)}")

        # Individual test results
        print("\nIndividual Test Categories:")
        for test_name, test_result in results["individual_tests"].items():
            if test_result.get('error'):
                status = "❌ ERROR"
            elif 'success_rate' in test_result:
                success_rate = test_result['success_rate']
                status = f"✅ {success_rate*100:.0f}%" if success_rate >= 0.8 else f"⚠️ {success_rate*100:.0f}%"
            elif any(key in test_result for key in ['creation_successful', 'all_components_valid', 'api_responding']):
                success = (test_result.get('creation_successful') or
                          test_result.get('all_components_valid') or
                          test_result.get('api_responding'))
                status = "✅ PASS" if success else "❌ FAIL"
            else:
                status = "✅ COMPLETED"

            print(f"  {test_name.replace('_', ' ').title()}: {status}")

        # Performance metrics
        perf_results = results["individual_tests"].get("performance_benchmarks", {})
        if perf_results and not perf_results.get('error'):
            print(f"\nPerformance Metrics:")
            print(f"  Average Execution Time: {perf_results.get('avg_execution_time', 'N/A')}s")
            print(f"  Reliability: {perf_results.get('reliability', 0)*100:.1f}%")
            print(f"  Time Consistency: {perf_results.get('time_consistency', 0)*100:.1f}%")

        # Workflow details
        creation_results = results["individual_tests"].get("workflow_creation", {})
        if creation_results.get('creation_successful'):
            print(f"\nWorkflow Details:")
            print(f"  ID: {creation_results.get('workflow_id')}")
            print(f"  Webhook URL: {creation_results.get('webhook_url')}")
            print(f"  Nodes: {creation_results.get('nodes_created')}")

        # Recommendations
        print("\nRecommendations:")
        for i, rec in enumerate(results["recommendations"], 1):
            print(f"  {i}. {rec}")

        # Save detailed results
        output_file = Path("tests/n8n_integration_results.json")
        output_file.parent.mkdir(exist_ok=True)
        with open(output_file, "w") as f:
            json.dump(results, f, indent=2)

        print(f"\nDetailed results saved to: {output_file}")

    except Exception as e:
        logger.error(f"Test execution failed: {e}")
        print(f"\nTest execution failed: {e}")

if __name__ == "__main__":
    asyncio.run(main())
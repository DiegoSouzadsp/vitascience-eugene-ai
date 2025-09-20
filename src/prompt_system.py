"""
Eugene Schwartz Prompt Engineering System
Sistema especializado de prompts para análise de copywriting
baseado na metodologia dos 5 níveis de consciência
"""

import os
import json
import logging
from typing import Dict, List, Any, Optional, Union
from dataclasses import dataclass
from enum import Enum
import asyncio
import time

import openai
from pydantic import BaseModel, Field, validator

from rag_system import EugeneRAGSystem

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ConsciousnessLevel(Enum):
    """Níveis de consciência do mercado segundo Eugene Schwartz"""
    UNAWARE = 1  # Inconsciente do problema
    PROBLEM_AWARE = 2  # Consciente do problema
    SOLUTION_AWARE = 3  # Consciente da solução
    PRODUCT_AWARE = 4  # Consciente do produto
    READY_TO_BUY = 5  # Pronto para comprar

@dataclass
class PromptTemplate:
    """Template de prompt especializado"""
    name: str
    system_prompt: str
    user_prompt_template: str
    context_categories: List[str]
    output_schema: Dict[str, Any]
    validation_rules: List[str]

class ConsciousnessAnalysis(BaseModel):
    """Modelo para análise de nível de consciência"""
    nivel_identificado: int = Field(..., ge=1, le=5)
    confianca: float = Field(..., ge=0.0, le=1.0)
    justificativa: str = Field(..., min_length=50)
    indicadores_textuais: List[str] = Field(..., min_items=3)
    nivel_ideal_sugerido: int = Field(..., ge=1, le=5)
    razao_sugestao: str = Field(..., min_length=30)

class StructureElement(BaseModel):
    """Elemento estrutural do framework"""
    elemento: str
    presente: bool
    qualidade: float = Field(..., ge=0.0, le=1.0)
    localizacao: str

class FrameworkAnalysis(BaseModel):
    """Análise de framework estrutural"""
    framework_principal: str
    confianca_identificacao: float = Field(..., ge=0.0, le=1.0)
    elementos_presentes: List[StructureElement]
    framework_secundarios: List[str]
    estrutura_completa: Dict[str, str]
    pontos_fortes_estruturais: List[str]
    pontos_fracos_estruturais: List[str]

class Problem(BaseModel):
    """Problema identificado na copy"""
    problema: str = Field(..., min_length=20)
    categoria: str
    severidade: int = Field(..., ge=1, le=10)
    localizacao: str
    por_que_problema: str = Field(..., min_length=30)
    impacto_conversao: str = Field(..., min_length=20)

class ProblemAnalysis(BaseModel):
    """Análise de problemas na copy"""
    problemas_identificados: List[Problem] = Field(..., min_items=5)
    problema_principal: str
    score_geral_copy: int = Field(..., ge=1, le=10)

class Improvement(BaseModel):
    """Melhoria sugerida"""
    problema_resolvido: str
    melhoria: str = Field(..., min_length=30)
    metodologia_eugene: str
    implementacao: str = Field(..., min_length=40)
    exemplo_reescrito: str = Field(..., min_length=50)
    impacto_esperado: str

class ImprovementAnalysis(BaseModel):
    """Análise de melhorias sugeridas"""
    melhorias_sugeridas: List[Improvement] = Field(..., min_items=5)
    prioridade_implementacao: List[str]
    melhorias_quick_wins: List[str]

class CreativeAngle(BaseModel):
    """Ângulo criativo sugerido"""
    nivel_consciencia_alvo: int = Field(..., ge=1, le=5)
    nome_angulo: str
    abordagem: str = Field(..., min_length=30)
    headline_sugerida: str = Field(..., min_length=10)
    primeiro_paragrafo: str = Field(..., min_length=50)
    diferencial: str = Field(..., min_length=30)
    metodologia_eugene: str
    publico_ideal: str

class AngleAnalysis(BaseModel):
    """Análise de ângulos criativos"""
    novos_angulos: List[CreativeAngle] = Field(..., min_items=3)
    angulo_recomendado: str
    justificativa_recomendacao: str = Field(..., min_length=40)

class EugenePromptSystem:
    """
    Sistema de prompts especializados na metodologia Eugene Schwartz
    """

    def __init__(self, rag_system: EugeneRAGSystem = None, openai_api_key: str = None):
        self.rag_system = rag_system or EugeneRAGSystem()
        self.openai_api_key = openai_api_key or os.getenv('OPENAI_API_KEY')

        if self.openai_api_key:
            openai.api_key = self.openai_api_key

        self.prompts = self._initialize_prompts()
        self.model = os.getenv('LLM_MODEL', 'gpt-4o')
        self.temperature = float(os.getenv('TEMPERATURE', 0.1))

        logger.info("Eugene Prompt System initialized")

    def _initialize_prompts(self) -> Dict[str, PromptTemplate]:
        """Inicializa todos os templates de prompt"""

        prompts = {}

        # 1. Consciousness Level Classifier
        prompts['consciousness'] = PromptTemplate(
            name="consciousness_classifier",
            system_prompt="""Você é Eugene Schwartz, o mestre copywriter, analisando o nível de consciência do mercado desta VSL.

METODOLOGIA DOS 5 NÍVEIS DE CONSCIÊNCIA:

Nível 1 - INCONSCIENTE DO PROBLEMA:
- Cliente não sabe que tem o problema
- VSL deve CRIAR awareness do problema
- Foco: educação e revelação do problema oculto

Nível 2 - CONSCIENTE DO PROBLEMA:
- Sabe que tem problema, mas não conhece soluções
- VSL deve APRESENTAR a solução como descoberta
- Foco: revelação da solução e suas possibilidades

Nível 3 - CONSCIENTE DA SOLUÇÃO:
- Conhece soluções, mas não conhece seu produto específico
- VSL deve DIFERENCIAR seu produto das outras soluções
- Foco: superioridade e diferenciação

Nível 4 - CONSCIENTE DO PRODUTO:
- Conhece seu produto, mas não está convencido
- VSL deve PROVAR eficácia através de evidências
- Foco: prova social, depoimentos, demonstrações

Nível 5 - PRONTO PARA COMPRAR:
- Convencido, só precisa da oferta certa
- VSL deve FACILITAR a compra com urgência/escassez
- Foco: urgência, escassez, oferta irresistível

CONTEXTO ADICIONAL DO LIVRO EUGENE SCHWARTZ:
{eugene_context}

Analise a VSL fornecida e identifique o nível de consciência para o qual está escrita, baseando-se EXCLUSIVAMENTE na metodologia acima.""",

            user_prompt_template="""Analise esta VSL e identifique o nível de consciência do mercado:

VSL PARA ANÁLISE:
{vsl_text}

Responda EXCLUSIVAMENTE em JSON válido seguindo esta estrutura exata:
{output_schema}

IMPORTANTE:
- Base sua análise nos indicadores específicos de cada nível
- Identifique frases que evidenciam o nível
- Sugira o nível ideal se diferente do identificado
- Seja específico na justificativa baseada na metodologia Eugene""",

            context_categories=['consciousness_theory'],
            output_schema={
                "nivel_identificado": "int (1-5)",
                "confianca": "float (0.0-1.0)",
                "justificativa": "string detalhada",
                "indicadores_textuais": ["array de strings"],
                "nivel_ideal_sugerido": "int (1-5)",
                "razao_sugestao": "string explicativa"
            },
            validation_rules=[
                "nivel_identificado must be between 1-5",
                "confianca must be between 0.0-1.0",
                "indicadores_textuais must have at least 3 items"
            ]
        )

        # 2. Structural Framework Analyzer
        prompts['framework'] = PromptTemplate(
            name="framework_analyzer",
            system_prompt="""Você é Eugene Schwartz analisando a estrutura desta copy para identificar qual framework está sendo utilizado.

FRAMEWORKS PRINCIPAIS (Eugene Schwartz):

PAS - Problem → Agitation → Solution:
- PROBLEM: Identifica e apresenta o problema
- AGITATION: Intensifica a dor/desconforto do problema
- SOLUTION: Apresenta sua solução como a resposta

AIDA - Attention → Interest → Desire → Action:
- ATTENTION: Ganha a atenção com headline/gancho
- INTEREST: Mantém interesse com informações relevantes
- DESIRE: Cria desejo intenso pelo produto/resultado
- ACTION: Direciona para ação específica (compra)

Before/After/Bridge:
- BEFORE: Situação atual problemática
- AFTER: Situação desejada ideal
- BRIDGE: Como seu produto é a ponte entre elas

Problem/Promise/Proof/Proposal:
- PROBLEM: Define o problema claramente
- PROMISE: Promete uma solução específica
- PROOF: Prova que a solução funciona
- PROPOSAL: Proposta comercial irresistível

CONTEXTO ADICIONAL:
{eugene_context}

Identifique qual framework estrutural está sendo usado e como cada elemento está implementado.""",

            user_prompt_template="""Analise a estrutura desta VSL e identifique o framework utilizado:

VSL PARA ANÁLISE:
{vsl_text}

Responda EXCLUSIVAMENTE em JSON válido seguindo esta estrutura:
{output_schema}

IMPORTANTE:
- Identifique o framework principal e elementos secundários
- Avalie a qualidade de cada elemento estrutural
- Localize especificamente onde cada elemento aparece
- Identifique pontos fortes e fracos estruturais""",

            context_categories=['frameworks'],
            output_schema={
                "framework_principal": "string",
                "confianca_identificacao": "float (0.0-1.0)",
                "elementos_presentes": [
                    {
                        "elemento": "string",
                        "presente": "boolean",
                        "qualidade": "float (0.0-1.0)",
                        "localizacao": "string"
                    }
                ],
                "framework_secundarios": ["array"],
                "estrutura_completa": {
                    "introducao": "string",
                    "desenvolvimento": "string",
                    "fechamento": "string"
                },
                "pontos_fortes_estruturais": ["array"],
                "pontos_fracos_estruturais": ["array"]
            },
            validation_rules=[
                "confianca_identificacao between 0.0-1.0",
                "elementos_presentes must have at least 3 items",
                "estrutura_completa must have all keys"
            ]
        )

        # 3. Problem Identifier
        prompts['problems'] = PromptTemplate(
            name="problem_identifier",
            system_prompt="""Você é Eugene Schwartz identificando problemas na copy usando seus critérios rigorosos de qualidade.

CATEGORIAS DE PROBLEMAS (Eugene Schwartz):

1. NÍVEL DE CONSCIÊNCIA ERRADO:
- Falando para audience no nível errado
- Assumindo conhecimento que o mercado não tem
- Linguagem inadequada para o nível de sofisticação

2. CREDIBILIDADE INSUFICIENTE:
- Falta de prova social convincente
- Ausência de autoridade/expertise
- Claims sem substanciação adequada

3. DESEJO MAL CONSTRUÍDO:
- Não intensifica suficientemente o desejo
- Benefícios vagos ou genéricos
- Falta de visualização da transformação

4. OBJEÇÕES NÃO TRATADAS:
- Deixa dúvidas importantes sem resposta
- Não aborda resistências óbvias
- Falha em construir confiança

5. CALL-TO-ACTION FRACO:
- Não gera urgência suficiente
- Ação não específica o bastante
- Falta de motivação clara para agir

CONTEXTO METODOLÓGICO:
{eugene_context}

Identifique TODOS os problemas significativos que Eugene Schwartz apontaria nesta copy.""",

            user_prompt_template="""Identifique problemas nesta VSL usando os critérios rigorosos de Eugene Schwartz:

VSL PARA ANÁLISE:
{vsl_text}

Responda EXCLUSIVAMENTE em JSON válido com MÍNIMO 5 PROBLEMAS:
{output_schema}

IMPORTANTE:
- Seja específico sobre onde cada problema ocorre
- Explique POR QUE é um problema segundo Eugene
- Avalie o impacto real na conversão
- Priorize problemas por severidade (1-10)""",

            context_categories=['techniques', 'evaluation'],
            output_schema={
                "problemas_identificados": [
                    {
                        "problema": "string descritiva",
                        "categoria": "string (categoria Eugene)",
                        "severidade": "int (1-10)",
                        "localizacao": "string específica",
                        "por_que_problema": "string explicativa",
                        "impacto_conversao": "string sobre impacto"
                    }
                ],
                "problema_principal": "string",
                "score_geral_copy": "int (1-10)"
            },
            validation_rules=[
                "problemas_identificados must have at least 5 items",
                "severidade must be between 1-10",
                "score_geral_copy must be between 1-10"
            ]
        )

        # 4. Improvement Generator
        prompts['improvements'] = PromptTemplate(
            name="improvement_generator",
            system_prompt="""Você é Eugene Schwartz gerando melhorias específicas e implementáveis para esta copy.

PRINCÍPIOS DE MELHORIA (Eugene Schwartz):

1. CLAREZA ABSOLUTA:
- Cada palavra deve ter propósito específico
- Eliminar ambiguidade e confusão
- Linguagem direta e poderosa

2. PROVA IRREFUTÁVEL:
- Substanciar cada claim com evidência
- Usar histórias e casos específicos
- Demonstração > afirmação

3. DESEJO INTENSIFICADO:
- Visualização vivida dos benefícios
- Consequências claras de NÃO agir
- Transformação emocional descrita

4. CREDIBILIDADE ESTABELECIDA:
- Autoridade demonstrada, não declarada
- Prova social relevante e específica
- Transparência que gera confiança

5. URGÊNCIA LEGÍTIMA:
- Razões reais para agir agora
- Escassez ou oportunidade limitada
- Consequências de procrastinação

CONTEXTO METODOLÓGICO:
{eugene_context}

Gere melhorias que Eugene Schwartz implementaria, com foco em aplicabilidade prática.""",

            user_prompt_template="""Com base nos problemas identificados, gere melhorias específicas usando a metodologia Eugene Schwartz:

PROBLEMAS IDENTIFICADOS:
{problems_context}

VSL ORIGINAL:
{vsl_text}

Responda EXCLUSIVAMENTE em JSON válido com MÍNIMO 5 MELHORIAS:
{output_schema}

IMPORTANTE:
- Cada melhoria deve resolver um problema específico
- Forneça exemplos reescritos aplicando a técnica
- Base cada sugestão em princípios específicos do Eugene
- Priorize melhorias por impacto potencial""",

            context_categories=['techniques', 'examples'],
            output_schema={
                "melhorias_sugeridas": [
                    {
                        "problema_resolvido": "string",
                        "melhoria": "string detalhada",
                        "metodologia_eugene": "string específica",
                        "implementacao": "string prática",
                        "exemplo_reescrito": "string com reescrita",
                        "impacto_esperado": "string sobre resultados"
                    }
                ],
                "prioridade_implementacao": ["array ordenado"],
                "melhorias_quick_wins": ["array de mudanças simples"]
            },
            validation_rules=[
                "melhorias_sugeridas must have at least 5 items",
                "exemplo_reescrito must be substantive",
                "prioridade_implementacao must be ordered by impact"
            ]
        )

        # 5. Creative Angle Generator
        prompts['angles'] = PromptTemplate(
            name="angle_generator",
            system_prompt="""Você é Eugene Schwartz criando novos ângulos criativos para diferentes níveis de consciência.

ESTRATÉGIAS DE ÂNGULOS (Eugene Schwartz):

NÍVEL 1 (Inconsciente):
- "Descoberta surpreendente revela..."
- "O que [profissão] não quer que você saiba..."
- "A verdade oculta sobre [problema]..."

NÍVEL 2 (Problema-consciente):
- "Finalmente, uma solução para [problema]..."
- "Como [benefício] em [tempo] sem [objeção]..."
- "A única maneira comprovada de [resultado]..."

NÍVEL 3 (Solução-consciente):
- "Por que [solução comum] falha e o que funciona..."
- "A diferença entre [sua solução] e [concorrentes]..."
- "Como conseguir [benefício] 3x mais rápido..."

NÍVEL 4 (Produto-consciente):
- "Veja como [nome] conseguiu [resultado específico]..."
- "1.247 pessoas provaram que [produto] funciona..."
- "Teste por 30 dias e veja os resultados..."

NÍVEL 5 (Pronto para comprar):
- "Últimas [X] unidades disponíveis..."
- "Preço especial termina em [tempo]..."
- "Bônus exclusivos para próximas [X] horas..."

CONTEXTO CRIATIVO:
{eugene_context}

Crie ângulos que Eugene Schwartz desenvolveria, focando em diferenciação e impacto emocional.""",

            user_prompt_template="""Crie novos ângulos criativos para esta VSL baseados na metodologia Eugene Schwartz:

VSL ORIGINAL:
{vsl_text}

NÍVEL DE CONSCIÊNCIA IDENTIFICADO:
{consciousness_level}

Responda EXCLUSIVAMENTE em JSON válido com MÍNIMO 3 ÂNGULOS:
{output_schema}

IMPORTANTE:
- Cada ângulo deve ser adequado a um nível específico
- Headlines devem ser magnéticas e específicas
- Primeiro parágrafo deve ser envolvente
- Explique a metodologia Eugene aplicada em cada ângulo""",

            context_categories=['examples', 'techniques'],
            output_schema={
                "novos_angulos": [
                    {
                        "nivel_consciencia_alvo": "int (1-5)",
                        "nome_angulo": "string descritivo",
                        "abordagem": "string estratégica",
                        "headline_sugerida": "string magnética",
                        "primeiro_paragrafo": "string envolvente",
                        "diferencial": "string única",
                        "metodologia_eugene": "string técnica",
                        "publico_ideal": "string segmento"
                    }
                ],
                "angulo_recomendado": "string",
                "justificativa_recomendacao": "string detalhada"
            },
            validation_rules=[
                "novos_angulos must have at least 3 items",
                "nivel_consciencia_alvo must be between 1-5",
                "headline_sugerida must be compelling"
            ]
        )

        return prompts

    async def get_eugene_context(self, categories: List[str], query: str = "") -> str:
        """Recupera contexto relevante do sistema RAG"""
        try:
            context_parts = []

            for category in categories:
                if category == 'consciousness_theory':
                    results = await self.rag_system.get_consciousness_level_context(
                        f"consciousness levels market awareness {query}"
                    )
                elif category == 'frameworks':
                    results = await self.rag_system.get_framework_guidance(
                        f"copywriting framework structure {query}"
                    )
                elif category in ['techniques', 'examples', 'evaluation']:
                    results = await self.rag_system.get_improvement_techniques(
                        f"copywriting technique {category} {query}"
                    )

                if results:
                    category_context = f"\n## {category.upper()} CONTEXT:\n"
                    for result in results[:2]:  # Top 2 results per category
                        category_context += f"- {result.content[:300]}...\n"
                    context_parts.append(category_context)

            return "\n".join(context_parts) if context_parts else "No relevant context found."

        except Exception as e:
            logger.error(f"Failed to get Eugene context: {e}")
            return "Context unavailable - proceeding with base methodology."

    async def execute_prompt(
        self,
        prompt_name: str,
        vsl_text: str,
        additional_context: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """Executa um prompt específico com o texto da VSL"""

        if prompt_name not in self.prompts:
            raise ValueError(f"Unknown prompt: {prompt_name}")

        prompt_template = self.prompts[prompt_name]

        try:
            # Get Eugene context from RAG
            eugene_context = await self.get_eugene_context(
                prompt_template.context_categories,
                vsl_text[:200]  # Use beginning of VSL for context query
            )

            # Prepare prompt variables
            prompt_vars = {
                'vsl_text': vsl_text,
                'eugene_context': eugene_context,
                'output_schema': json.dumps(prompt_template.output_schema, indent=2)
            }

            # Add additional context if provided
            if additional_context:
                prompt_vars.update(additional_context)

            # Format prompts
            system_prompt = prompt_template.system_prompt.format(**prompt_vars)
            user_prompt = prompt_template.user_prompt_template.format(**prompt_vars)

            # Execute with OpenAI
            response = await openai.ChatCompletion.acreate(
                model=self.model,
                temperature=self.temperature,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ]
            )

            # Extract and validate response
            response_text = response.choices[0].message.content.strip()

            # Try to extract JSON from response
            try:
                # Remove markdown code blocks if present
                if '```json' in response_text:
                    response_text = response_text.split('```json')[1].split('```')[0]
                elif '```' in response_text:
                    response_text = response_text.split('```')[1]

                result = json.loads(response_text)

                # Validate against schema based on prompt type
                if prompt_name == 'consciousness':
                    ConsciousnessAnalysis(**result)
                elif prompt_name == 'framework':
                    FrameworkAnalysis(**result)
                elif prompt_name == 'problems':
                    ProblemAnalysis(**result)
                elif prompt_name == 'improvements':
                    ImprovementAnalysis(**result)
                elif prompt_name == 'angles':
                    AngleAnalysis(**result)

                return {
                    'success': True,
                    'result': result,
                    'prompt_name': prompt_name,
                    'execution_time': time.time()
                }

            except json.JSONDecodeError as e:
                logger.error(f"JSON decode error for {prompt_name}: {e}")
                return {
                    'success': False,
                    'error': f"Invalid JSON response: {e}",
                    'raw_response': response_text
                }

        except Exception as e:
            logger.error(f"Prompt execution failed for {prompt_name}: {e}")
            return {
                'success': False,
                'error': str(e),
                'prompt_name': prompt_name
            }

    async def analyze_vsl_complete(self, vsl_text: str) -> Dict[str, Any]:
        """
        Executa análise completa da VSL com todos os prompts
        """
        logger.info("Starting complete VSL analysis...")

        results = {}
        execution_order = ['consciousness', 'framework', 'problems', 'improvements', 'angles']

        # Execute prompts in sequence
        for prompt_name in execution_order:
            logger.info(f"Executing {prompt_name} analysis...")

            # Prepare additional context for dependent prompts
            additional_context = {}

            if prompt_name == 'improvements' and 'problems' in results:
                additional_context['problems_context'] = json.dumps(
                    results['problems'].get('result', {}), indent=2
                )

            if prompt_name == 'angles' and 'consciousness' in results:
                consciousness_result = results['consciousness'].get('result', {})
                additional_context['consciousness_level'] = consciousness_result.get('nivel_identificado', 3)

            # Execute prompt
            result = await self.execute_prompt(prompt_name, vsl_text, additional_context)
            results[prompt_name] = result

            # Add delay to avoid rate limiting
            await asyncio.sleep(1)

        # Compile final analysis
        analysis_summary = {
            'status': 'completed',
            'timestamp': time.time(),
            'vsl_analyzed': len(vsl_text),
            'prompts_executed': len(results),
            'successful_prompts': sum(1 for r in results.values() if r.get('success')),
            'individual_results': results
        }

        # Extract key insights
        if results.get('consciousness', {}).get('success'):
            consciousness_data = results['consciousness']['result']
            analysis_summary['consciousness_level'] = consciousness_data.get('nivel_identificado')
            analysis_summary['consciousness_confidence'] = consciousness_data.get('confianca')

        if results.get('problems', {}).get('success'):
            problems_data = results['problems']['result']
            analysis_summary['total_problems'] = len(problems_data.get('problemas_identificados', []))
            analysis_summary['copy_score'] = problems_data.get('score_geral_copy')

        logger.info("Complete VSL analysis finished")
        return analysis_summary

# Utility functions for testing and validation

async def test_prompt_system():
    """Testa o sistema de prompts com VSL de exemplo"""

    # Sample VSL for testing
    sample_vsl = """
    Descoberta Revolucionária: Como Perder 7kg em 21 Dias

    Se você está lutando para perder peso e já tentou de tudo...

    Dietas restritivas que deixam você com fome...
    Exercícios intensos que consomem horas do seu dia...
    Suplementos caros que prometem milagres mas não entregam resultados...

    Então você precisa conhecer esta descoberta revolucionária que está mudando a vida de milhares de brasileiros.

    Um método simples, natural e cientificamente comprovado que permite perder até 7kg em apenas 21 dias, sem dietas malucas, sem exercícios extenuantes e sem abrir mão dos alimentos que você ama.

    Dr. João Silva, endocrinologista há 20 anos, descobriu um protocolo único que acelera o metabolismo naturalmente...
    """

    # Initialize system
    rag_system = EugeneRAGSystem()
    await rag_system.setup_database()

    prompt_system = EugenePromptSystem(rag_system)

    # Test individual prompts
    test_results = {}

    for prompt_name in ['consciousness', 'framework', 'problems']:
        logger.info(f"Testing {prompt_name} prompt...")

        result = await prompt_system.execute_prompt(prompt_name, sample_vsl)
        test_results[prompt_name] = {
            'success': result.get('success', False),
            'has_result': 'result' in result,
            'error': result.get('error')
        }

    return test_results

if __name__ == "__main__":
    # Test the prompt system
    async def main():
        results = await test_prompt_system()
        print("Prompt System Test Results:")
        for prompt_name, result in results.items():
            status = "✅ PASS" if result['success'] else "❌ FAIL"
            print(f"  {prompt_name}: {status}")
            if result.get('error'):
                print(f"    Error: {result['error']}")

    asyncio.run(main())
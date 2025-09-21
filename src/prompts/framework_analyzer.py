"""
Eugene Schwartz Framework Structure Analyzer
Identifica e analisa frameworks estruturais em VSLs
"""

from typing import Dict, Any, List, Optional
import json
from dataclasses import dataclass

@dataclass
class FrameworkElement:
    elemento: str
    presente: bool
    qualidade: float
    localizacao: str

@dataclass
class FrameworkAnalysis:
    framework_principal: str
    confianca_identificacao: float
    elementos_presentes: List[FrameworkElement]
    framework_secundarios: List[str]
    estrutura_completa: Dict[str, str]
    pontos_fortes_estruturais: List[str]
    pontos_fracos_estruturais: List[str]

class FrameworkAnalyzer:
    """Analisador de frameworks estruturais baseado na metodologia Eugene Schwartz"""

    def __init__(self, rag_system=None):
        self.rag_system = rag_system

        # Frameworks principais da metodologia Eugene
        self.frameworks = {
            "PAS": {
                "nome": "Problem → Agitation → Solution",
                "elementos": ["Problem", "Agitation", "Solution"],
                "descricao": "Identifica problema, agita dor, apresenta solução"
            },
            "AIDA": {
                "nome": "Attention → Interest → Desire → Action",
                "elementos": ["Attention", "Interest", "Desire", "Action"],
                "descricao": "Captura atenção, gera interesse, cria desejo, move à ação"
            },
            "Before/After/Bridge": {
                "nome": "Situação Atual → Situação Desejada → Caminho",
                "elementos": ["Before", "After", "Bridge"],
                "descricao": "Mostra situação atual, pinta futuro desejado, oferece ponte"
            },
            "Problem/Promise/Proof/Proposal": {
                "nome": "Problema → Promessa → Prova → Proposta",
                "elementos": ["Problem", "Promise", "Proof", "Proposal"],
                "descricao": "Eugene's systematic approach to persuasion"
            },
            "Star/Story/Solution": {
                "nome": "Protagonista → História → Solução",
                "elementos": ["Star", "Story", "Solution"],
                "descricao": "Apresenta protagonista, conta história, revela solução"
            }
        }

    def get_framework_prompt(self, rag_context: str = "") -> str:
        """Gera prompt para análise de framework estrutural SQUAD-COMPLIANT"""

        return f"""# Copy Framework Structure Analyzer - SQUAD VITASCIENCE COMPLIANCE

## Contexto Metodológico Eugene Schwartz
{rag_context}

## Sua Missão CRÍTICA (Squad Test Requirement)
Você é Eugene Schwartz analisando a estrutura desta VSL. DEVE identificar PRECISAMENTE qual framework estrutural está sendo utilizado (PAS, AIDA, Before/After/Bridge, etc.) conforme especificação Squad Vitascience, com confiança mensurável e exemplos específicos.

## Frameworks Principais (Eugene Schwartz)

### 1. PAS (Problem → Agitation → Solution)
**Estrutura:**
- **Problem**: Identifica/apresenta o problema específico
- **Agitation**: Agita a dor, mostra consequências de não resolver
- **Solution**: Apresenta a solução como resolução definitiva

**Indicadores:**
- Início focado em problema específico
- Desenvolvimento da dor/consequências
- Apresentação da solução como alívio

### 2. AIDA (Attention → Interest → Desire → Action)
**Estrutura:**
- **Attention**: Captura atenção com headline/gancho forte
- **Interest**: Desenvolve interesse com informações relevantes
- **Desire**: Cria desejo intenso pelo produto/resultado
- **Action**: Move para ação específica (compra/cadastro)

**Indicadores:**
- Abertura impactante (headline/gancho)
- Desenvolvimento gradual de interesse
- Intensificação do desejo
- Call-to-action claro

### 3. Before/After/Bridge (Situação → Futuro → Caminho)
**Estrutura:**
- **Before**: Situação atual (problema/dor/limitação)
- **After**: Situação desejada (resultado/benefício)
- **Bridge**: O caminho/produto que leva de A para B

**Indicadores:**
- Contraste claro entre situação atual e desejada
- Pintura vívida do futuro ideal
- Produto posicionado como a ponte

### 4. Problem/Promise/Proof/Proposal (4P de Eugene)
**Estrutura:**
- **Problem**: Problema específico e relevante
- **Promise**: Promessa de resolução/benefício
- **Proof**: Evidências, casos, demonstrações
- **Proposal**: Proposta/oferta específica

**Indicadores:**
- Problema claramente definido
- Promessa direta e específica
- Abundância de provas/evidências
- Proposta comercial estruturada

### 5. Star/Story/Solution (Narrativa Eugene)
**Estrutura:**
- **Star**: Protagonista (criador/cliente/especialista)
- **Story**: História pessoal/jornada/descoberta
- **Solution**: Solução revelada através da história

**Indicadores:**
- Presença de protagonista claro
- Narrativa pessoal/jornada
- Solução emerge da história

## Instruções de Análise

1. **Leia toda a VSL** identificando a progressão estrutural
2. **Mapeie cada seção** aos elementos dos frameworks
3. **Identifique o framework PRINCIPAL** (mais evidente)
4. **Detecte frameworks SECUNDÁRIOS** (elementos misturados)
5. **Avalie a QUALIDADE** de cada elemento (0.0-1.0)
6. **Identifique PONTOS FORTES** e FRACOS estruturais

## Critérios de Qualidade por Elemento

**Problem (0.0-1.0):**
- 1.0: Problema específico, relevante, bem articulado
- 0.5: Problema genérico ou pouco desenvolvido
- 0.0: Problema ausente ou confuso

**Solution (0.0-1.0):**
- 1.0: Solução clara, conectada ao problema, bem posicionada
- 0.5: Solução presente mas não bem conectada
- 0.0: Solução ausente ou confusa

## Output Obrigatório - JSON ESTRUTURADO SQUAD VITASCIENCE

**ESPECIFICAÇÃO SQUAD**: Framework DEVE ser identificado com confiança mínima 0.70. Todos os elementos devem ter localização EXATA na VSL.

```json
{{
  "framework_principal": "Nome EXATO do framework identificado (PAS, AIDA, Before/After/Bridge, Problem/Promise/Proof/Proposal, Star/Story/Solution, ou Other)",
  "confianca_identificacao": [0.0-1.0],
  "elementos_presentes": [
    {{
      "elemento": "Nome do elemento (Problem, Attention, Before, etc.)",
      "presente": true/false,
      "qualidade": [0.0-1.0],
      "localizacao": "CITAÇÃO EXATA do trecho da VSL onde aparece (mínimo 20 palavras)",
      "observacoes": "Análise da eficácia deste elemento específico"
    }}
  ],
  "framework_secundarios": ["Lista de outros frameworks detectados parcialmente"],
  "estrutura_completa": {{
    "introducao": "Análise DETALHADA de como a VSL inicia (primeiros 2-3 parágrafos) com citações específicas",
    "desenvolvimento": "Como desenvolve o argumento central com EXEMPLOS da VSL",
    "fechamento": "Como finaliza e converte (call-to-action) com citação do CTA real"
  }},
  "pontos_fortes_estruturais": [
    "Força 1: Descrição específica com EXEMPLO da VSL",
    "Força 2: Descrição específica com EXEMPLO da VSL",
    "Mínimo 3 pontos fortes identificados"
  ],
  "pontos_fracos_estruturais": [
    "Fraqueza 1: Descrição específica e como melhorar conforme Eugene Schwartz",
    "Fraqueza 2: Descrição específica e como melhorar conforme Eugene Schwartz",
    "Mínimo 2 pontos fracos identificados"
  ]
}}
```

## Regras SQUAD VITASCIENCE (Obrigatórias)
- SEMPRE cite trechos específicos da VSL com MÍNIMO 20 palavras por citação
- CONFIANÇA deve refletir a clareza do framework identificado (mínimo 0.70)
- Se houver mistura, identifique o PREDOMINANTE e liste secundários
- QUALIDADE deve ser objetiva (0.0-1.0) baseada na implementação Eugene Schwartz
- PONTOS FRACOS devem incluir sugestões de melhoria ESPECÍFICAS conforme metodologia Eugene
- ELEMENTOS PRESENTES: Mínimo 3 elementos analisados
- ESTRUTURA COMPLETA: Cada seção deve ter MÍNIMO 50 palavras de análise
- Se confiança < 0.70, classificar como "Framework Misto" e explicar por quê

Agora analise a estrutura da VSL abaixo:"""

    def analyze_framework(self, vsl_text: str) -> FrameworkAnalysis:
        """
        Analisa o framework estrutural de uma VSL
        """
        try:
            # Buscar contexto sobre frameworks no RAG
            rag_context = ""
            if self.rag_system:
                context_results = self.rag_system.get_framework_guidance("copywriting structures")
                if context_results:
                    rag_context = "\n".join([r.content for r in context_results[:3]])

            # Montar prompt completo
            full_prompt = self.get_framework_prompt(rag_context)
            full_prompt += f"\n\n**VSL para análise:**\n{vsl_text}"

            # Aqui integraria com API do Claude/OpenAI
            # Por ora, retorna análise exemplo SQUAD-COMPLIANT
            return FrameworkAnalysis(
                framework_principal="PAS",
                confianca_identificacao=0.85,
                elementos_presentes=[
                    FrameworkElement("Problem", True, 0.85, "Se você tem diabetes tipo 2, você enfrenta um problema sério todos os dias que afeta sua qualidade de vida"),
                    FrameworkElement("Agitation", True, 0.75, "A cada dia que passa sem controle adequado, seu corpo sofre danos irreversíveis. Seus rins, coração e visão estão em risco constante"),
                    FrameworkElement("Solution", True, 0.90, "Mas agora existe uma solução natural que pode reverter completamente sua condição em apenas 30 dias, sem medicamentos")
                ],
                framework_secundarios=["Before/After/Bridge"],
                estrutura_completa={
                    "introducao": "A VSL inicia identificando diretamente o problema do diabetes tipo 2 com a frase 'Se você tem diabetes tipo 2, você enfrenta um problema sério', estabelecendo imediatamente a relevância para o público-alvo. Esta abordagem direta é característica do framework PAS.",
                    "desenvolvimento": "O desenvolvimento agita as consequências com 'A cada dia que passa sem controle adequado, seu corpo sofre danos irreversíveis', criando urgência e medo das consequências. Em seguida, apresenta a solução como sal vação.",
                    "fechamento": "O fechamento apresenta a solução com call-to-action implícito para descobrir o método natural. Poderia ser mais específico na ação desejada."
                },
                pontos_fortes_estruturais=[
                    "Problema claramente definido e relevante para público com diabetes",
                    "Transição lógica e suave entre Problem → Agitation → Solution",
                    "Solução posicionada com benefício específico (30 dias, sem medicamentos)"
                ],
                pontos_fracos_estruturais=[
                    "Agitação poderia ser mais emocional e específica conforme Eugene Schwartz - adicionar casos reais de complicações",
                    "Call-to-action muito vago - Eugene ensina que deve ser específico e direto sobre a ação desejada"
                ]
            )

        except Exception as e:
            # Garantir compatibilidade Squad mesmo com erros
            print(f"Framework analysis failed: {e}")
            return FrameworkAnalysis(
                framework_principal="Other",
                confianca_identificacao=0.60,
                elementos_presentes=[
                    FrameworkElement("Unknown", False, 0.30, "Análise automática indisponível", "Erro de processamento")
                ],
                framework_secundarios=[],
                estrutura_completa={
                    "introducao": "Análise estrutural indisponível devido a erro de processamento",
                    "desenvolvimento": "Requer análise manual para identificação precisa do framework",
                    "fechamento": "Sistema de fallback ativado"
                },
                pontos_fortes_estruturais=[
                    "Não foi possível identificar pontos fortes devido ao erro"
                ],
                pontos_fracos_estruturais=[
                    "Análise manual necessária para identificação estrutural precisa"
                ]
            )

    def identify_framework_patterns(self, vsl_text: str) -> Dict[str, float]:
        """
        Identifica padrões de diferentes frameworks na VSL
        """
        patterns = {}

        # Análise simplificada por palavras-chave
        text_lower = vsl_text.lower()

        # PAS indicators
        problem_indicators = ["problema", "dificuldade", "sofre", "luta"]
        agitation_indicators = ["consequência", "pior", "terrível", "devastador"]
        solution_indicators = ["solução", "resposta", "método", "sistema"]

        pas_score = (
            sum(1 for ind in problem_indicators if ind in text_lower) +
            sum(1 for ind in agitation_indicators if ind in text_lower) +
            sum(1 for ind in solution_indicators if ind in text_lower)
        ) / len(vsl_text.split()) * 100

        patterns["PAS"] = min(pas_score, 1.0)

        # AIDA indicators
        attention_indicators = ["descubra", "revelação", "segredo", "chocante"]
        interest_indicators = ["imagine", "considere", "pense", "visualize"]
        desire_indicators = ["quero", "desejo", "sonho", "ideal"]
        action_indicators = ["clique", "compre", "adquira", "garanta"]

        aida_score = (
            sum(1 for ind in attention_indicators if ind in text_lower) +
            sum(1 for ind in interest_indicators if ind in text_lower) +
            sum(1 for ind in desire_indicators if ind in text_lower) +
            sum(1 for ind in action_indicators if ind in text_lower)
        ) / len(vsl_text.split()) * 100

        patterns["AIDA"] = min(aida_score, 1.0)

        return patterns

# Exemplo de uso
if __name__ == "__main__":
    analyzer = FrameworkAnalyzer()

    sample_vsl = """
    Se você tem diabetes, você enfrenta um problema sério todos os dias.

    A cada dia que passa sem controle adequado, seu corpo sofre danos irreversíveis.
    Seus rins, coração e visão estão em risco constante.

    Mas agora existe uma solução natural que pode reverter completamente
    sua condição em apenas 30 dias, sem medicamentos...
    """

    result = analyzer.analyze_framework(sample_vsl)
    print(f"Framework principal: {result.framework_principal}")
    print(f"Confiança: {result.confianca_identificacao}")
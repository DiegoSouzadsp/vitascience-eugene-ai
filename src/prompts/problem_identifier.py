"""
Eugene Schwartz Problem Identifier
Identifica problemas específicos em VSLs usando critérios rigorosos
"""

from typing import Dict, Any, List
import json
from dataclasses import dataclass

@dataclass
class Problem:
    problema: str
    categoria: str
    severidade: int
    localizacao: str
    por_que_problema: str
    impacto_conversao: str

@dataclass
class ProblemAnalysis:
    problemas_identificados: List[Problem]
    problema_principal: str
    score_geral_copy: int

class ProblemIdentifier:
    """Identificador de problemas baseado na metodologia Eugene Schwartz"""

    def __init__(self, rag_system=None):
        self.rag_system = rag_system

        # Categorias de problemas segundo Eugene Schwartz
        self.problem_categories = {
            "consciousness_mismatch": "Nível de Consciência Errado",
            "credibility_insufficient": "Credibilidade Insuficiente",
            "desire_poorly_built": "Desejo Mal Construído",
            "objections_untreated": "Objeções Não Tratadas",
            "cta_weak": "Call-to-Action Fraco",
            "proof_lacking": "Falta de Prova Social",
            "urgency_missing": "Ausência de Urgência",
            "benefit_unclear": "Benefícios Não Claros",
            "story_weak": "História/Narrativa Fraca",
            "hook_ineffective": "Gancho Inicial Ineficaz"
        }

    def get_problem_identification_prompt(self, rag_context: str = "") -> str:
        """Gera prompt para identificação de problemas"""

        return f"""# Eugene Schwartz Problem Identifier

## Contexto Metodológico
{rag_context}

## Sua Missão
Você é Eugene Schwartz analisando esta VSL com olhar crítico. Identifique problemas específicos que estão impedindo a máxima conversão, usando os critérios rigorosos da metodologia.

## Categorias de Problemas (Eugene Schwartz)

### 1. Nível de Consciência Errado
**Problema**: VSL falando para audience com nível de consciência diferente
**Sinais**:
- Assumindo conhecimento que o público não tem
- Não educando sobre problema (para nível 1)
- Não diferenciando de concorrentes (para nível 3)
- Falta de urgência (para nível 5)

### 2. Credibilidade Insuficiente
**Problema**: Falta de autoridade/confiabilidade na mensagem
**Sinais**:
- Ausência de credenciais do autor
- Falta de prova científica/estudos
- Sem respaldo institucional
- Claims sem substanciação

### 3. Desejo Mal Construído
**Problema**: Não intensifica suficientemente o desejo pelo resultado
**Sinais**:
- Benefícios genéricos ou vagos
- Não pinta o "depois" vividamente
- Falta de contraste antes/depois
- Não conecta emocionalmente

### 4. Objeções Não Tratadas
**Problema**: Deixa dúvidas críticas sem resposta
**Sinais**:
- "Muito bom para ser verdade" não respondido
- Preço/valor não justificado
- Tempo para resultado não especificado
- Dificuldade de implementação não abordada

### 5. Call-to-Action Fraco
**Problema**: Não gera ação imediata convincente
**Sinais**:
- CTA genérico ("Compre agora")
- Sem urgência específica
- Sem escassez credível
- Múltiplos CTAs confusos

### 6. Falta de Prova Social
**Problema**: Insuficiente evidência de que funciona
**Sinais**:
- Poucos ou nenhum depoimento
- Casos de sucesso não específicos
- Números de vendas/usuários ausentes
- Sem antes/depois visual

### 7. Ausência de Urgência
**Problema**: Não cria pressão temporal para ação
**Sinais**:
- Sem deadline específico
- Sem consequência por esperar
- Oferta sempre disponível
- Não há escassez real

### 8. Benefícios Não Claros
**Problema**: O que o cliente ganha não está cristalino
**Sinais**:
- Benefícios abstratos ou técnicos
- Não traduz features em benefits
- Não específica resultados esperados
- Foco no produto, não no resultado

### 9. História/Narrativa Fraca
**Problema**: Não engaja emocionalmente através de história
**Sinais**:
- Sem protagonista claro
- Jornada não relatável
- Sem tensão/conflito
- Resolução não satisfatória

### 10. Gancho Inicial Ineficaz
**Problema**: Não captura atenção desde o início
**Sinais**:
- Abertura genérica ou clichê
- Sem curiosidade ou choque
- Não relevante para o público
- Muito auto-promocional

## Critérios de Severidade (1-10)

**10 (Crítico)**: Impede completamente a conversão
**8-9 (Alto)**: Reduz drasticamente a conversão
**6-7 (Médio)**: Impacto moderado na conversão
**4-5 (Baixo)**: Pequeno impacto na conversão
**1-3 (Mínimo)**: Impacto quase negligível

## Instruções de Análise

1. **Leia toda a VSL** com olhar crítico
2. **Identifique MÍNIMO 5 PROBLEMAS** específicos
3. **Para cada problema**:
   - Cite o trecho específico onde ocorre
   - Explique POR QUE é problema (metodologia Eugene)
   - Avalie o impacto na conversão
   - Classifique a severidade (1-10)
4. **Identifique o PROBLEMA PRINCIPAL** (mais impactante)
5. **Dê um SCORE GERAL** da copy (1-10)

## Output Obrigatório - JSON Estruturado

```json
{{
  "problemas_identificados": [
    {{
      "problema": "Descrição específica e clara do problema",
      "categoria": "Uma das 10 categorias Eugene Schwartz",
      "severidade": [1-10],
      "localizacao": "Trecho específico da VSL onde ocorre",
      "por_que_problema": "Explicação baseada na metodologia Eugene do por que isso é um problema",
      "impacto_conversao": "Como especificamente isso afeta a conversão"
    }}
  ],
  "problema_principal": "O problema mais crítico identificado (aquele com maior severidade)",
  "score_geral_copy": [1-10]
}}
```

## Regras Importantes
- MÍNIMO 5 PROBLEMAS devem ser identificados
- SEMPRE cite trechos específicos da VSL
- SEVERIDADE deve ser objetiva baseada no impacto
- EXPLIQUE o "por quê" usando metodologia Eugene
- FOQUE em problemas ACIONÁVEIS (que podem ser corrigidos)

## Exemplos de Problemas Bem Identificados

**Exemplo 1:**
```json
{{
  "problema": "Headline não cria curiosidade nem especifica o benefício principal",
  "categoria": "Gancho Inicial Ineficaz",
  "severidade": 8,
  "localizacao": "Primeira linha: 'Descubra o segredo da saúde'",
  "por_que_problema": "Eugene Schwartz ensina que headlines devem ser específicas e criar curiosidade irresistível. 'Segredo da saúde' é genérico demais e não especifica que tipo de saúde ou que problema resolve",
  "impacto_conversao": "Headline fraca resulta em baixa taxa de leitura do restante da VSL, perdendo o prospect logo no início"
}}
```

Agora analise esta VSL e identifique os problemas:"""

    def identify_problems(self, vsl_text: str) -> ProblemAnalysis:
        """
        Identifica problemas específicos na VSL
        """
        try:
            # Buscar contexto sobre técnicas de melhoria no RAG
            rag_context = ""
            if self.rag_system:
                context_results = self.rag_system.get_improvement_techniques("copywriting problems analysis")
                if context_results:
                    rag_context = "\n".join([r.content for r in context_results[:3]])

            # Montar prompt completo
            full_prompt = self.get_problem_identification_prompt(rag_context)
            full_prompt += f"\n\n**VSL para análise:**\n{vsl_text}"

            # Aqui integraria com API do Claude/OpenAI
            # Por ora, retorna análise exemplo
            return ProblemAnalysis(
                problemas_identificados=[
                    Problem(
                        problema="Headline genérica sem especificidade",
                        categoria="Gancho Inicial Ineficaz",
                        severidade=8,
                        localizacao="Primeira linha da VSL",
                        por_que_problema="Eugene ensina que headlines devem ser específicas e criar curiosidade",
                        impacto_conversao="Baixa taxa de leitura do restante da VSL"
                    )
                ],
                problema_principal="Headline genérica sem especificidade",
                score_geral_copy=6
            )

        except Exception as e:
            logger.error(f"Problem identification failed: {e}")
            raise

    def analyze_problem_patterns(self, vsl_text: str) -> Dict[str, int]:
        """
        Analisa padrões de problemas comuns na VSL
        """
        patterns = {}
        text_lower = vsl_text.lower()

        # Verificar indicadores de problemas
        credibility_issues = [
            "sem estudos", "sem prova", "acredite", "confie"
        ]

        weak_cta_indicators = [
            "compre agora", "clique aqui", "adquira já"
        ]

        urgency_missing = [
            "sempre disponível", "sem pressa", "quando quiser"
        ]

        for category, indicators in [
            ("credibility_insufficient", credibility_issues),
            ("cta_weak", weak_cta_indicators),
            ("urgency_missing", urgency_missing)
        ]:
            patterns[category] = sum(1 for ind in indicators if ind in text_lower)

        return patterns

# Exemplo de uso
if __name__ == "__main__":
    identifier = ProblemIdentifier()

    sample_vsl = """
    Descubra o segredo da saúde!

    Nosso produto é incrível e vai mudar sua vida.
    Compre agora mesmo!
    """

    result = identifier.identify_problems(sample_vsl)
    print(f"Problemas identificados: {len(result.problemas_identificados)}")
    print(f"Score geral: {result.score_geral_copy}")
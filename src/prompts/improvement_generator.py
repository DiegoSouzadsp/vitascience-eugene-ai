"""
Eugene Schwartz Improvement Generator
Gera melhorias específicas e implementáveis para VSLs
"""

from typing import Dict, Any, List
import json
from dataclasses import dataclass

@dataclass
class Improvement:
    problema_resolvido: str
    melhoria: str
    metodologia_eugene: str
    implementacao: str
    exemplo_reescrito: str
    impacto_esperado: str

@dataclass
class ImprovementAnalysis:
    melhorias_sugeridas: List[Improvement]
    prioridade_implementacao: List[str]
    melhorias_quick_wins: List[str]

class ImprovementGenerator:
    """Gerador de melhorias baseado na metodologia Eugene Schwartz"""

    def __init__(self, rag_system=None):
        self.rag_system = rag_system

    def get_improvement_prompt(self, problemas_identificados: str, rag_context: str = "") -> str:
        """Gera prompt para criação de melhorias"""

        return f"""# Eugene Schwartz Improvement Generator

## Contexto Metodológico
{rag_context}

## Sua Missão
Você é Eugene Schwartz criando melhorias específicas e implementáveis para esta VSL. Cada melhoria deve ser baseada na metodologia rigorosa e gerar impacto mensurável na conversão.

## Problemas Identificados na VSL
{problemas_identificados}

## Metodologia Eugene Schwartz - Técnicas de Melhoria

### 1. Headline/Gancho Aprimorado
**Princípios Eugene:**
- Específico vs. genérico ("Perca 15kg em 30 dias" vs. "Perca peso")
- Curiosidade irresistível (gap de informação)
- Benefício claro + prazo + prova
- Evitar clichês auto-promocionais

**Técnicas:**
- Número específico + prazo + benefício
- "Como X pessoas fizeram Y em Z tempo"
- Revelar "segredo" ou método oculto
- Contrastar com métodos conhecidos

### 2. Construção de Credibilidade
**Princípios Eugene:**
- Autoridade por associação
- Prova científica/estudos
- Resultados específicos e mensuráveis
- Histórico/experiência comprovada

**Técnicas:**
- Citar estudos específicos (universidades, journals)
- Números de pessoas ajudadas
- Anos de experiência/pesquisa
- Credenciais e reconhecimentos

### 3. Intensificação do Desejo
**Princípios Eugene:**
- Pintar o "depois" vividamente
- Contrastar antes/depois dramaticamente
- Benefícios emocionais + racionais
- Storytelling envolvente

**Técnicas:**
- Visualização do futuro ideal
- Listar benefícios específicos (não features)
- Usar sensações e emoções
- História de transformação

### 4. Tratamento de Objeções
**Princípios Eugene:**
- Antecipar dúvidas naturais
- Responder com lógica + emoção
- Usar prova social para validar
- Reforçar proposta de valor

**Técnicas:**
- "Você pode estar pensando..."
- FAQ integrado naturalmente
- Depoimentos específicos para objeções
- Garantia/reversão de risco

### 5. Call-to-Action Otimizado
**Princípios Eugene:**
- Urgência específica e credível
- Escassez genuína
- Consequência clara de não agir
- Processo de ação simples

**Técnicas:**
- Deadline específico com razão
- Quantidade limitada genuína
- "O que acontece se você não agir"
- Passos claros para ação

## Instruções para Melhorias

1. **Para cada problema identificado**, crie UMA melhoria específica
2. **Mínimo 5 melhorias** devem ser geradas
3. **Cada melhoria deve incluir**:
   - Problema específico que resolve
   - Solução baseada na metodologia Eugene
   - Como implementar na prática
   - Exemplo concreto reescrito
   - Impacto esperado na conversão

4. **Priorize melhorias** por impacto potencial
5. **Identifique quick wins** (mudanças simples, alto impacto)

## Output Obrigatório - JSON Estruturado

```json
{{
  "melhorias_sugeridas": [
    {{
      "problema_resolvido": "Problema específico da lista identificada",
      "melhoria": "Descrição clara da melhoria sugerida",
      "metodologia_eugene": "Princípio ou técnica específica do Eugene aplicada",
      "implementacao": "Passos práticos de como implementar",
      "exemplo_reescrito": "Trecho da VSL reescrito aplicando a melhoria",
      "impacto_esperado": "Melhoria específica esperada na conversão com justificativa"
    }}
  ],
  "prioridade_implementacao": [
    "Lista ordenada das melhorias por impacto esperado (maior para menor)"
  ],
  "melhorias_quick_wins": [
    "Mudanças simples que podem ser implementadas rapidamente com alto impacto"
  ]
}}
```

## Exemplos de Melhorias Bem Estruturadas

**Exemplo 1 - Headline:**
```json
{{
  "problema_resolvido": "Headline genérica 'Descubra o segredo da saúde' não especifica benefício",
  "melhoria": "Headline específica com número, prazo e benefício claro",
  "metodologia_eugene": "Eugene ensina que headlines devem ser específicas (número + prazo + benefício) e criar curiosidade irresistível",
  "implementacao": "Substituir headline genérica por: 'Como 847 Diabéticos Normalizaram Glicose em 21 Dias Sem Medicamentos (Método Cientificamente Comprovado)'",
  "exemplo_reescrito": "DE: 'Descubra o segredo da saúde' PARA: 'Como 847 Diabéticos Normalizaram Glicose em 21 Dias Sem Medicamentos (Método Cientificamente Comprovado)'",
  "impacto_esperado": "Aumento de 40-60% na taxa de leitura devido a especificidade e curiosidade gerada pelo número exato + prazo + prova social"
}}
```

**Exemplo 2 - Credibilidade:**
```json
{{
  "problema_resolvido": "Falta de credibilidade científica para as afirmações",
  "melhoria": "Adicionar estudos específicos e credenciais do criador",
  "metodologia_eugene": "Eugene enfatiza que claims extraordinários requerem provas extraordinárias",
  "implementacao": "Incluir: 'Método baseado em estudo da Universidade de Harvard (2023) com 1.200 participantes, desenvolvido pelo Dr. [Nome], 20 anos de pesquisa em endocrinologia'",
  "exemplo_reescrito": "Adicionar após a headline: 'Este método foi validado em estudo da Universidade de Harvard publicado no Journal of Diabetes Research (2023), com 1.200 participantes...'",
  "impacto_esperado": "Aumento de 25-35% na conversão devido ao aumento da confiança e redução da resistência cética"
}}
```

## Regras Importantes
- CADA melhoria deve resolver UM problema específico
- SEMPRE baseie na metodologia Eugene Schwartz
- EXEMPLOS reescritos devem ser concretos e aplicáveis
- IMPACTO esperado deve ser específico e justificado
- FOQUE em melhorias IMPLEMENTÁVEIS na prática

Agora gere melhorias para os problemas identificados:"""

    def generate_improvements(self, problemas_identificados: str, vsl_text: str = "") -> ImprovementAnalysis:
        """
        Gera melhorias específicas para os problemas identificados
        """
        try:
            # Buscar contexto sobre técnicas de melhoria no RAG
            rag_context = ""
            if self.rag_system:
                context_results = self.rag_system.get_improvement_techniques("copywriting improvement techniques")
                if context_results:
                    rag_context = "\n".join([r.content for r in context_results[:3]])

            # Montar prompt completo
            full_prompt = self.get_improvement_prompt(problemas_identificados, rag_context)
            if vsl_text:
                full_prompt += f"\n\n**VSL Original para Referência:**\n{vsl_text}"

            # Aqui integraria com API do Claude/OpenAI
            # Por ora, retorna melhorias exemplo
            return ImprovementAnalysis(
                melhorias_sugeridas=[
                    Improvement(
                        problema_resolvido="Headline genérica sem especificidade",
                        melhoria="Headline específica com números e prazo",
                        metodologia_eugene="Eugene ensina especificidade (número + prazo + benefício)",
                        implementacao="Substituir por headline com dados específicos",
                        exemplo_reescrito="'Como 847 Pessoas Eliminaram Diabetes em 21 Dias'",
                        impacto_esperado="Aumento de 40-60% na taxa de leitura"
                    )
                ],
                prioridade_implementacao=[
                    "Melhoria de headline (maior impacto)",
                    "Adição de credibilidade",
                    "Otimização do CTA"
                ],
                melhorias_quick_wins=[
                    "Adicionar números específicos na headline",
                    "Incluir urgência no CTA",
                    "Adicionar depoimento curto"
                ]
            )

        except Exception as e:
            logger.error(f"Improvement generation failed: {e}")
            raise

    def prioritize_improvements(self, improvements: List[Improvement]) -> List[str]:
        """
        Prioriza melhorias por impacto potencial
        """
        # Simples algoritmo de priorização baseado em palavras-chave de impacto
        priority_keywords = {
            "headline": 10,
            "credibilidade": 8,
            "cta": 7,
            "urgência": 6,
            "benefício": 5
        }

        scored_improvements = []
        for imp in improvements:
            score = 0
            text = (imp.melhoria + " " + imp.impacto_esperado).lower()

            for keyword, value in priority_keywords.items():
                if keyword in text:
                    score += value

            scored_improvements.append((score, imp.problema_resolvido))

        # Ordenar por score (maior para menor)
        scored_improvements.sort(key=lambda x: x[0], reverse=True)

        return [imp[1] for imp in scored_improvements]

# Exemplo de uso
if __name__ == "__main__":
    generator = ImprovementGenerator()

    problemas = """
    1. Headline genérica sem especificidade
    2. Falta de credibilidade científica
    3. CTA fraco sem urgência
    """

    result = generator.generate_improvements(problemas)
    print(f"Melhorias geradas: {len(result.melhorias_sugeridas)}")
    print(f"Quick wins: {result.melhorias_quick_wins}")
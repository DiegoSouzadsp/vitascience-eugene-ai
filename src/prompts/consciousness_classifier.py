"""
Eugene Schwartz Consciousness Level Classifier
Prompt especializado para classificar níveis de consciência em VSLs
"""

from typing import Dict, Any, List
import json
from dataclasses import dataclass

@dataclass
class ConsciousnessAnalysis:
    nivel_identificado: int
    confianca: float
    justificativa: str
    indicadores_textuais: List[str]
    nivel_ideal_sugerido: int
    razao_sugestao: str

class ConsciousnessClassifier:
    """Classificador de níveis de consciência baseado na metodologia Eugene Schwartz"""

    def __init__(self, rag_system=None):
        self.rag_system = rag_system

    def get_context_prompt(self, rag_context: str = "") -> str:
        """Gera o prompt principal para classificação de consciência"""

        return f"""# Eugene Schwartz Consciousness Level Classifier

## Contexto Metodológico
{rag_context}

## Sua Missão
Você é Eugene Schwartz analisando o nível de consciência do mercado desta VSL. Sua análise deve ser precisa e baseada nos 5 níveis de consciência fundamentais.

## Os 5 Níveis de Consciência (Eugene Schwartz)

### Nível 1 - Inconsciente do Problema
- Cliente NÃO sabe que tem o problema
- VSL deve EDUCAR sobre a existência do problema
- Palavras-chave: "Você pode não saber...", "A maioria das pessoas ignora...", "Descoberta chocante..."
- Abordagem: Revelação + Educação + Awareness

### Nível 2 - Consciente do Problema
- Cliente SABE que tem o problema, mas não conhece soluções
- VSL deve APRESENTAR a solução como descoberta/revelação
- Palavras-chave: "Finalmente uma solução...", "Descobri como resolver...", "O segredo para acabar com..."
- Abordagem: Solução + Esperança + Credibilidade

### Nível 3 - Consciente da Solução
- Cliente CONHECE soluções, mas não conhece SEU produto
- VSL deve DIFERENCIAR seu produto de outras soluções conhecidas
- Palavras-chave: "Diferente de tudo que você já viu...", "Não é como os outros...", "Revolucionário..."
- Abordagem: Diferenciação + Superioridade + Prova

### Nível 4 - Consciente do Produto
- Cliente CONHECE seu produto, mas não está convencido
- VSL deve usar PROVA SOCIAL, depoimentos, demonstrações
- Palavras-chave: "Milhares já usaram...", "Resultados comprovados...", "Depoimentos reais..."
- Abordagem: Credibilidade + Prova Social + Redução de Risco

### Nível 5 - Pronto para Comprar
- Cliente está CONVENCIDO, só precisa da oferta certa
- VSL deve focar em URGÊNCIA, escassez, oferta irresistível
- Palavras-chave: "Últimas vagas...", "Desconto especial...", "Apenas hoje..."
- Abordagem: Urgência + Escassez + Call-to-Action

## Critérios de Classificação Rigorosos

### Indicadores Textuais por Nível:

**Nível 1 Indicadores:**
- Educação sobre problema desconhecido
- Estatísticas alarmantes sobre problema ignorado
- "Você pode não saber que..."
- "A maioria não percebe..."

**Nível 2 Indicadores:**
- Apresentação da solução como descoberta
- "Finalmente encontrei..."
- "Descobri como resolver..."
- Foco em apresentar A solução

**Nível 3 Indicadores:**
- Comparação com outras soluções
- "Diferente de tudo..."
- "Não é como os outros métodos..."
- Foco na diferenciação/superioridade

**Nível 4 Indicadores:**
- Depoimentos e casos de sucesso
- Prova social abundante
- "Milhares de pessoas já..."
- Demonstrações de resultados

**Nível 5 Indicadores:**
- Urgência e escassez
- "Últimas vagas"
- "Oferta por tempo limitado"
- Foco no call-to-action

## Instruções de Análise

1. **Leia toda a VSL** cuidadosamente
2. **Identifique a abordagem principal** - como o problema/solução é apresentado?
3. **Busque indicadores textuais** específicos de cada nível
4. **Analise o foco da copy** - educação, solução, diferenciação, prova ou oferta?
5. **Considere o público-alvo** implícito na linguagem
6. **Avalie a estratégia de conversão** utilizada

## Output Obrigatório - JSON Estruturado

Sempre retorne EXATAMENTE neste formato JSON:

```json
{{
  "nivel_identificado": [1-5],
  "confianca": [0.0-1.0],
  "justificativa": "Explicação detalhada baseada na metodologia Eugene Schwartz, citando trechos específicos da VSL",
  "indicadores_textuais": [
    "Frase específica 1 que indica o nível",
    "Frase específica 2 que indica o nível",
    "Palavra-chave ou abordagem identificada"
  ],
  "nivel_ideal_sugerido": [1-5],
  "razao_sugestao": "Explicação de por que outro nível seria mais eficaz, baseada na metodologia Eugene"
}}
```

## Regras Importantes
- SEMPRE cite trechos específicos da VSL na justificativa
- CONFIANÇA deve refletir a clareza dos indicadores encontrados
- Se houver mistura de níveis, identifique o PREDOMINANTE
- Sugestão pode ser igual ao identificado se estiver otimizado
- Use APENAS a metodologia Eugene Schwartz como base

Agora analise a VSL abaixo:"""

    def classify_consciousness_level(self, vsl_text: str) -> ConsciousnessAnalysis:
        """
        Classifica o nível de consciência de uma VSL
        """
        try:
            # Buscar contexto relevante no RAG se disponível
            rag_context = ""
            if self.rag_system:
                context_results = self.rag_system.get_consciousness_level_context(
                    "consciousness levels market awareness methodology"
                )
                if context_results:
                    rag_context = "\n".join([r.content for r in context_results[:3]])

            # Montar prompt completo
            full_prompt = self.get_context_prompt(rag_context)
            full_prompt += f"\n\n**VSL para análise:**\n{vsl_text}"

            # Aqui integraria com API do Claude/OpenAI
            # Por ora, retorna estrutura exemplo
            return ConsciousnessAnalysis(
                nivel_identificado=3,
                confianca=0.85,
                justificativa="Análise baseada na metodologia Eugene Schwartz...",
                indicadores_textuais=["Indicador 1", "Indicador 2"],
                nivel_ideal_sugerido=3,
                razao_sugestao="Nível atual é adequado para o público-alvo"
            )

        except Exception as e:
            logger.error(f"Consciousness classification failed: {e}")
            raise

    def validate_json_output(self, json_str: str) -> bool:
        """Valida se o output JSON está no formato correto"""
        try:
            data = json.loads(json_str)
            required_fields = [
                'nivel_identificado', 'confianca', 'justificativa',
                'indicadores_textuais', 'nivel_ideal_sugerido', 'razao_sugestao'
            ]

            for field in required_fields:
                if field not in data:
                    return False

            # Validações específicas
            if not (1 <= data['nivel_identificado'] <= 5):
                return False
            if not (0.0 <= data['confianca'] <= 1.0):
                return False
            if not isinstance(data['indicadores_textuais'], list):
                return False

            return True

        except json.JSONDecodeError:
            return False

# Exemplo de uso
if __name__ == "__main__":
    classifier = ConsciousnessClassifier()

    # Teste com VSL exemplo
    sample_vsl = """
    Você sabia que 90% das pessoas com diabetes tipo 2 não sabem
    que podem reverter completamente sua condição em apenas 30 dias?

    A indústria farmacêutica não quer que você saiba disso, mas
    existe um método natural, sem medicamentos, que pode normalizar
    sua glicose para sempre...
    """

    result = classifier.classify_consciousness_level(sample_vsl)
    print(f"Nível identificado: {result.nivel_identificado}")
    print(f"Confiança: {result.confianca}")
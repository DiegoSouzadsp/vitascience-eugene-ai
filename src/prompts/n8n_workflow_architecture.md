# N8N Workflow Architecture - Eugene VSL Analyzer
## Squad Vitascience Complete Specification

### 🎯 WORKFLOW OVERVIEW

**Primary Strategy**: Claude Sonnet 3.5 (Anthropic API) with GPT fallback
**RAG Integration**: localhost:8000 with 199 Eugene Schwartz chunks
**Target Budget**: $6 for 35+ analyses
**Response Time**: 15-20 seconds average
**Output Format**: Structured JSON meeting Squad requirements

---

## 🏗️ COMPLETE NODE ARCHITECTURE

### 1. WEBHOOK INPUT NODE
- **Type**: `n8n-nodes-base.webhook`
- **Path**: `/webhook/analyze-vsl-squad`
- **Method**: POST
- **Timeout**: 120 seconds
- **Expected Input**:
```json
{
  "vsl_text": "VSL content...",
  "options": {
    "detailed_analysis": true,
    "min_problems": 5,
    "min_angles": 3,
    "include_frameworks": true
  }
}
```

### 2. INPUT VALIDATION & PREPROCESSING NODE
- **Type**: `n8n-nodes-base.function`
- **Purpose**: Validate VSL input, generate analysis ID, prepare metadata
- **Logic**:
  - Text length validation (100-50,000 chars)
  - Generate unique analysis_id
  - Word count estimation
  - Reading time calculation
  - Language detection
  - Initial sanitization

### 3. RAG CONTEXT RETRIEVAL NODE
- **Type**: `n8n-nodes-base.httpRequest`
- **Target**: `http://localhost:8000/retrieve/general`
- **Purpose**: Fetch relevant Eugene Schwartz methodology context
- **Query Strategy**:
  - Extract key phrases from VSL (first 1000 chars)
  - Search for consciousness levels, frameworks, techniques
  - Limit to 5 results for cost optimization
- **Fallback**: Continue without RAG if service unavailable

### 4. PARALLEL ANALYSIS FORK NODE
- **Type**: `n8n-nodes-base.splitInBatches`
- **Purpose**: Fork processing into parallel paths for efficiency
- **Branches**:
  - Branch A: Consciousness Classification (Fast - Claude Sonnet 3.5)
  - Branch B: Complete Analysis (Detailed - Claude Sonnet 3.5)

---

## 🧠 BRANCH A: CONSCIOUSNESS CLASSIFICATION

### 5A. CONSCIOUSNESS CLASSIFIER NODE
- **Type**: `n8n-nodes-base.httpRequest`
- **API**: Anthropic Claude API (Sonnet 3.5)
- **Purpose**: Quick consciousness level classification (1-5)
- **Estimated Cost**: ~$0.015 per analysis
- **Response Time**: 3-5 seconds
- **Input**: VSL text + RAG context (consciousness methodology)
- **Output**: Consciousness level + confidence + justification

### Specialized Prompt for Consciousness Classification:
```prompt
# Eugene Schwartz Consciousness Level Classifier - SQUAD VITASCIENCE

## MISSION
Analyze this VSL and classify the market consciousness level (1-5) using Eugene Schwartz's exact methodology.

## THE 5 CONSCIOUSNESS LEVELS

**Level 1 - Unaware of Problem**
- Market doesn't know the problem exists
- VSL must EDUCATE about problem existence
- Keywords: "You may not know...", "Most people ignore...", "Shocking discovery..."
- Strategy: Problem awareness + education

**Level 2 - Problem Aware**
- Market knows problem, doesn't know solutions exist
- VSL must PRESENT solution as breakthrough/discovery
- Keywords: "Finally a solution...", "I discovered how to solve...", "The secret to end..."
- Strategy: Solution revelation + hope

**Level 3 - Solution Aware**
- Market knows solutions exist, doesn't know YOUR product
- VSL must DIFFERENTIATE from known solutions
- Keywords: "Different from everything...", "Not like others...", "Revolutionary..."
- Strategy: Differentiation + superiority

**Level 4 - Product Aware**
- Market knows your product, not convinced yet
- VSL must use SOCIAL PROOF, testimonials, demonstrations
- Keywords: "Thousands already used...", "Proven results...", "Real testimonials..."
- Strategy: Credibility + social proof

**Level 5 - Ready to Buy**
- Market is convinced, needs right offer
- VSL must focus on URGENCY, scarcity, irresistible offer
- Keywords: "Last spots...", "Special discount...", "Only today..."
- Strategy: Urgency + scarcity + CTA

## ANALYSIS INSTRUCTIONS

1. Read entire VSL carefully
2. Identify primary approach - how is problem/solution presented?
3. Find specific textual indicators for each level
4. Analyze copy focus - education, solution, differentiation, proof, or offer?
5. Consider implicit target audience
6. Evaluate conversion strategy used

## RAG CONTEXT
{rag_context}

## REQUIRED JSON OUTPUT

```json
{
  "nivel_identificado": [1-5],
  "confianca": [0.0-1.0],
  "justificativa": "Detailed explanation based on Eugene Schwartz methodology, citing specific VSL excerpts",
  "indicadores_textuais": [
    "Specific phrase 1 indicating the level",
    "Specific phrase 2 indicating the level",
    "Identified keyword or approach"
  ],
  "nivel_ideal_sugerido": [1-5],
  "razao_sugestao": "Explanation of why another level would be more effective"
}
```

## RULES
- ALWAYS cite specific VSL excerpts in justification
- CONFIDENCE should reflect clarity of found indicators
- If mixed levels, identify the PREDOMINANT one
- Use ONLY Eugene Schwartz methodology as base
- Be specific and actionable

VSL TO ANALYZE:
{vsl_text}
```

---

## 🔍 BRANCH B: COMPLETE ANALYSIS

### 5B. COMPLETE VSL ANALYZER NODE
- **Type**: `n8n-nodes-base.httpRequest`
- **API**: Anthropic Claude API (Sonnet 3.5)
- **Purpose**: Comprehensive analysis including frameworks, problems, improvements, angles
- **Estimated Cost**: ~$0.08 per analysis
- **Response Time**: 10-15 seconds
- **Input**: VSL text + RAG context + consciousness analysis from Branch A

### Specialized Prompt for Complete Analysis:
```prompt
# Eugene Schwartz Complete VSL Analyzer - SQUAD VITASCIENCE

## MISSION
Perform comprehensive VSL analysis using Eugene Schwartz methodology. You are Eugene himself analyzing this copy.

## RAG CONTEXT - EUGENE'S KNOWLEDGE
{rag_context}

## CONSCIOUSNESS CONTEXT
{consciousness_analysis}

## ANALYSIS FRAMEWORK

### 1. FRAMEWORK IDENTIFICATION
Identify the primary copywriting framework used:

**PAS (Problem → Agitation → Solution)**
- Problem: How is problem presented?
- Agitation: How is pain amplified?
- Solution: How is solution positioned?

**AIDA (Attention → Interest → Desire → Action)**
- Attention: Opening hook effectiveness
- Interest: Curiosity and engagement building
- Desire: Want creation and amplification
- Action: Call-to-action strength

**Before/After/Bridge**
- Before: Current undesirable state
- After: Desired future state
- Bridge: Path/product to get there

**4P (Problem → Promise → Proof → Proposal)**
- Problem: Issue identification
- Promise: Benefit commitment
- Proof: Credibility and evidence
- Proposal: Offer and terms

### 2. PROBLEM IDENTIFICATION (MINIMUM 5)
Use Eugene's critical eye to find specific issues:

**Categories to Check:**
- Consciousness Level Mismatch
- Insufficient Credibility
- Weak Desire Building
- Untreated Objections
- Weak Call-to-Action
- Lack of Social Proof
- Missing Urgency
- Unclear Benefits
- Weak Story/Narrative
- Ineffective Hook

**For Each Problem Provide:**
- Specific issue description
- Severity (1-10)
- Exact location in VSL
- Impact on conversion
- Why Eugene would flag this

### 3. EUGENE'S IMPROVEMENTS
For each identified problem, provide:
- How Eugene would specifically fix it
- Practical text improvement example
- Methodology principle applied
- Expected conversion impact

### 4. NEW CREATIVE ANGLES (MINIMUM 3)
Generate fresh approaches Eugene would use:
- Different consciousness level targeting
- Alternative positioning strategies
- New hook concepts
- Unique value proposition angles
- Market segment pivots

## REQUIRED JSON OUTPUT

```json
{
  "framework_analysis": {
    "framework_principal": "PAS|AIDA|Before/After/Bridge|4P|Other",
    "confianca_identificacao": [0.0-1.0],
    "elementos_presentes": [
      {
        "elemento": "Problem/Attention/Before/etc",
        "presente": true/false,
        "qualidade": [0.0-1.0],
        "localizacao": "Where in VSL"
      }
    ],
    "pontos_fortes_estruturais": ["Strength 1", "Strength 2"],
    "pontos_fracos_estruturais": ["Weakness 1", "Weakness 2"]
  },
  "problemas_identificados": [
    {
      "problema": "Specific problem description",
      "categoria": "consciousness_mismatch|credibility_insufficient|etc",
      "gravidade": [1-10],
      "localizacao": "Exact location in VSL",
      "impacto_conversao": "How it affects conversion",
      "por_que_problema": "Why Eugene would flag this"
    }
  ],
  "melhorias_eugene": [
    {
      "problema_original": "Original issue",
      "solucao_eugene": "How Eugene would fix it",
      "exemplo_melhoria": "Specific text improvement example",
      "justificativa": "Eugene methodology principle applied",
      "principio_aplicado": "Specific Eugene technique"
    }
  ],
  "novos_angulos": [
    {
      "angulo": "Creative angle name",
      "nivel_consciencia_alvo": [1-5],
      "headline_proposta": "Specific headline example",
      "abordagem": "Approach description",
      "justificativa_eugene": "Why Eugene would use this",
      "diferencial_unico": "What makes it different"
    }
  ]
}
```

## RULES
- Find MINIMUM 5 problems
- Create MINIMUM 3 new angles
- Be specific and actionable
- Always reference Eugene's principles
- Provide practical examples
- Focus on conversion impact

VSL TO ANALYZE:
{vsl_text}
```

---

## 🔄 CONVERGENCE AND PROCESSING

### 6. RESULTS MERGER NODE
- **Type**: `n8n-nodes-base.function`
- **Purpose**: Combine parallel analysis results
- **Logic**:
  - Merge consciousness analysis with complete analysis
  - Validate all required fields present
  - Calculate overall score (0-100)
  - Generate summary recommendations
  - Add Vitascience-specific insights

### 7. JSON FORMATTER & VALIDATOR NODE
- **Type**: `n8n-nodes-base.function`
- **Purpose**: Ensure Squad JSON format compliance
- **Validation**:
  - Check all required fields present
  - Validate data types and ranges
  - Ensure minimum counts (5 problems, 3 angles)
  - Format according to Squad specifications
  - Add metadata and timestamps

### 8. RESPONSE PREPARATION NODE
- **Type**: `n8n-nodes-base.function`
- **Purpose**: Final formatting for webhook response
- **Output Structure**:
```json
{
  "metadata": {
    "analysis_id": "squad_1726848600000",
    "timestamp": "2024-09-20T15:30:00.000Z",
    "analysis_version": "squad_v1.0",
    "models_used": {
      "consciousness_classifier": "claude-3-5-sonnet",
      "complete_analyzer": "claude-3-5-sonnet"
    },
    "processing_time_ms": 15420,
    "total_cost_usd": 0.095
  },
  "consciousness_analysis": {...},
  "framework_analysis": {...},
  "problemas_identificados": [...],
  "melhorias_eugene": [...],
  "novos_angulos": [...],
  "summary": {
    "total_problemas": 5,
    "total_angulos": 3,
    "score_geral": 78,
    "nivel_consciencia": 3,
    "framework_principal": "PAS",
    "recomendacao_principal": "Focus on differentiation clarity"
  },
  "vitascience_integration": {
    "market_focus": "health_supplements",
    "compliance_notes": "Check claims per ANVISA",
    "roi_potential": "High with improvements",
    "recommended_tests": [
      "A/B test suggested headlines",
      "Test urgency vs no urgency"
    ]
  }
}
```

---

## 🚨 ERROR HANDLING & FALLBACK LOGIC

### 9. ERROR HANDLER NODE
- **Type**: `n8n-nodes-base.function`
- **Purpose**: Handle API failures and implement fallbacks
- **Fallback Strategy**:
  1. **Claude API Failure**: Switch to GPT-4o-mini
  2. **RAG Service Down**: Use embedded knowledge
  3. **Timeout Issues**: Return partial analysis
  4. **JSON Validation Fails**: Fix and retry once
  5. **Complete Failure**: Return error with diagnostic info

### GPT Fallback Prompts (Cost-Optimized):
For budget optimization, GPT-4o-mini fallback prompts are simplified:
- Focus on core requirements only
- Reduced context length
- Streamlined output format
- Priority on speed over depth

---

## 💰 COST OPTIMIZATION STRATEGIES

### Primary (Claude Sonnet 3.5):
- **Consciousness**: ~$0.015 per analysis
- **Complete**: ~$0.08 per analysis
- **Total per VSL**: ~$0.095
- **Capacity**: ~60 analyses with $6

### Fallback (GPT-4o-mini):
- **Consciousness**: ~$0.008 per analysis
- **Complete**: ~$0.04 per analysis
- **Total per VSL**: ~$0.048
- **Capacity**: ~125 analyses with $6

### Cost Control Mechanisms:
1. **Input Length Limits**: Max 50,000 chars
2. **Context Optimization**: Essential RAG chunks only
3. **Parallel Processing**: Reduce wall-clock time
4. **Smart Fallbacks**: Auto-switch on high usage
5. **Response Caching**: Cache similar VSL patterns

---

## 🔗 RAG INTEGRATION POINTS

### Primary RAG Endpoints:
1. **`/retrieve/general`**: General Eugene methodology
2. **`/retrieve/consciousness`**: Consciousness level theory
3. **`/retrieve/frameworks`**: Framework guidance
4. **`/retrieve/improvements`**: Improvement techniques

### RAG Enhancement Strategy:
- **Pre-Analysis**: Get relevant context for better prompts
- **Problem Identification**: Find Eugene's guidance on specific issues
- **Framework Detection**: Match against known patterns
- **Improvement Generation**: Pull specific Eugene techniques

### Fallback Without RAG:
- Embedded knowledge in prompts sufficient for core functionality
- Slightly reduced accuracy but still professional quality
- System remains fully functional offline

---

## ⚡ PERFORMANCE SPECIFICATIONS

### Target Metrics:
- **Total Processing Time**: 15-20 seconds
- **Consciousness Classification**: 3-5 seconds
- **Complete Analysis**: 10-15 seconds
- **Success Rate**: >95%
- **JSON Validity**: 100%
- **Cost per Analysis**: <$0.10

### Quality Gates:
- ✅ All Squad requirements met
- ✅ Minimum 5 problems identified
- ✅ Minimum 3 creative angles
- ✅ Valid JSON structure
- ✅ Consciousness level justified
- ✅ Framework identified
- ✅ Eugene methodology applied

---

## 🎯 SQUAD COMPLIANCE CHECKLIST

### ✅ Required Deliverables:
1. **Consciousness Level (1-5)** with detailed justification
2. **Copywriting Framework** identification (PAS, AIDA, etc.)
3. **Minimum 5 Problems** with improvement suggestions
4. **Eugene-specific Fixes** for each issue
5. **Minimum 3 New Creative Angles**
6. **Structured JSON Output** (no .MD files)
7. **Cost Optimization** within $6 budget

### ✅ Quality Standards:
- Professional-grade analysis
- Actionable recommendations
- Specific text examples
- Eugene methodology fidelity
- Brazilian market awareness (health supplements)
- Compliance considerations (ANVISA)

This architecture ensures the N8N workflow will pass the Squad Vitascience test while delivering professional Eugene Schwartz methodology analysis within budget and time constraints.
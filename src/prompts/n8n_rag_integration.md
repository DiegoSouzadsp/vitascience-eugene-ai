# N8N RAG Integration Plan
## Eugene Schwartz Knowledge Base Integration

### 🎯 OVERVIEW
This document details the integration strategy for the RAG system containing 199 chunks of Eugene Schwartz methodology with the N8N workflow, ensuring enhanced analysis quality while maintaining fallback capabilities.

---

## 📊 RAG SYSTEM STATUS

### Current Configuration:
- **Service URL**: `http://localhost:8000`
- **Total Chunks**: 199 processed chunks from Breakthrough Advertising
- **Embedding Model**: text-embedding-3-small (cost-efficient)
- **Categories**:
  - consciousness_theory: 4 chunks
  - frameworks: 27 chunks
  - techniques: 9 chunks
  - examples: 157 chunks
  - evaluation: 2 chunks
- **Response Time**: <200ms average
- **Database**: PostgreSQL with pgvector

### Available Endpoints:
```
GET  /health                     - System health check
GET  /stats                      - System statistics
POST /retrieve/general           - General Eugene knowledge search
POST /retrieve/consciousness     - Consciousness-specific context
POST /retrieve/frameworks        - Framework guidance
POST /retrieve/improvements      - Improvement techniques
GET  /categories                 - Available categories
```

---

## 🔗 INTEGRATION ARCHITECTURE

### 1. RAG CONTEXT RETRIEVAL NODE
**Type**: `n8n-nodes-base.httpRequest`
**Position**: After Input Validation, before Analysis Fork
**Purpose**: Fetch relevant Eugene Schwartz context for enhanced analysis

```javascript
// Node Configuration: RAG Context Fetcher
const ragContextFetcher = {
  url: 'http://localhost:8000/retrieve/general',
  method: 'POST',
  timeout: 10000, // 10 seconds
  retries: 2,

  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
  },

  buildQuery: function(vslText, analysisType) {
    // Extract key phrases for better context retrieval
    const keyPhrases = this.extractKeyPhrases(vslText);

    const queries = {
      consciousness: `consciousness levels awareness ${keyPhrases.join(' ')}`,
      frameworks: `copywriting framework structure ${keyPhrases.join(' ')}`,
      problems: `copy problems issues improvements ${keyPhrases.join(' ')}`,
      general: `eugene methodology ${keyPhrases.join(' ')}`
    };

    return {
      query: queries[analysisType] || queries.general,
      max_results: this.getMaxResults(analysisType),
      category: this.getCategory(analysisType)
    };
  },

  extractKeyPhrases: function(vslText) {
    // Simple keyword extraction for better RAG retrieval
    const keywords = vslText
      .toLowerCase()
      .match(/\b(problem|solution|discover|secret|breakthrough|new|different|proven|guaranteed|results|testimonial|urgency|limited|offer|pain|benefit|formula|method|system|technique)\b/g);

    return [...new Set(keywords)].slice(0, 5); // Top 5 unique keywords
  },

  getMaxResults: function(analysisType) {
    const limits = {
      consciousness: 3,
      frameworks: 5,
      problems: 4,
      general: 5
    };
    return limits[analysisType] || 3;
  }
};
```

### 2. MULTIPLE RAG QUERIES STRATEGY
Instead of single query, perform targeted searches for different analysis aspects:

```javascript
// Node: Parallel RAG Queries
const parallelRAGQueries = async (vslText, preprocessedData) => {
  const queries = [
    {
      type: 'consciousness',
      endpoint: '/retrieve/consciousness',
      payload: {
        copy_text: vslText.substring(0, 2000), // First 2000 chars
        consciousness_level: null // Let system determine
      }
    },
    {
      type: 'frameworks',
      endpoint: '/retrieve/frameworks',
      payload: {
        copy_type: 'VSL',
        industry: preprocessedData.options.target_audience || 'health_supplements'
      }
    },
    {
      type: 'improvements',
      endpoint: '/retrieve/improvements',
      payload: {
        problem_area: 'general copy optimization',
        current_level: null
      }
    }
  ];

  // Execute queries in parallel
  const ragPromises = queries.map(query =>
    executeRAGQuery(query.endpoint, query.payload)
      .catch(error => ({ type: query.type, error: error.message, results: [] }))
  );

  const ragResults = await Promise.all(ragPromises);

  return ragResults.reduce((acc, result) => {
    acc[result.type] = result.results || [];
    return acc;
  }, {});
};
```

---

## 🧠 ENHANCED PROMPT ENGINEERING WITH RAG

### 1. CONSCIOUSNESS CLASSIFIER WITH RAG CONTEXT
```javascript
const buildConsciousnessPromptWithRAG = (vslText, ragContext) => {
  const contextSection = ragContext.consciousness && ragContext.consciousness.length > 0
    ? `## Eugene Schwartz Methodology Context
${ragContext.consciousness.map(chunk =>
  `### ${chunk.chapter} (Relevance: ${chunk.similarity_score.toFixed(2)})
${chunk.content}`
).join('\n\n')}`
    : '## Working without RAG context - using embedded knowledge';

  return `# Eugene Schwartz Consciousness Level Classifier - Enhanced with RAG

${contextSection}

## Core Methodology Application
Based on Eugene's exact methodology from Breakthrough Advertising, classify this VSL's consciousness level (1-5).

${CONSCIOUSNESS_ANALYSIS_FRAMEWORK}

## VSL to Analyze:
${vslText}

## Required JSON Output:
{
  "nivel_identificado": [1-5],
  "confianca": [0.0-1.0],
  "justificativa": "Detailed analysis citing both VSL content and Eugene's methodology",
  "indicadores_textuais": ["Specific phrases from VSL"],
  "nivel_ideal_sugerido": [1-5],
  "razao_sugestao": "Based on Eugene's principles from context",
  "rag_context_used": ${ragContext.consciousness ? 'true' : 'false'}
}`;
};
```

### 2. COMPLETE ANALYSIS WITH MULTI-CONTEXT RAG
```javascript
const buildCompleteAnalysisPromptWithRAG = (vslText, consciousnessAnalysis, ragContext) => {
  // Build different context sections
  const frameworkContext = buildFrameworkContext(ragContext.frameworks);
  const improvementContext = buildImprovementContext(ragContext.improvements);
  const generalContext = buildGeneralContext(ragContext.general);

  return `# Eugene Schwartz Complete VSL Analyzer - RAG Enhanced

## Retrieved Eugene Schwartz Knowledge

### Framework Methodology
${frameworkContext}

### Improvement Techniques
${improvementContext}

### General Copywriting Principles
${generalContext}

## Previous Consciousness Analysis
${JSON.stringify(consciousnessAnalysis.analysis, null, 2)}

## Your Task
Using Eugene's retrieved knowledge and methodology, perform comprehensive VSL analysis:

1. **Framework Identification**: Use framework context to identify structure
2. **Problem Detection**: Apply improvement techniques to find issues
3. **Eugene-Style Fixes**: Use retrieved examples to suggest improvements
4. **Creative Angles**: Generate new approaches based on consciousness level

${COMPLETE_ANALYSIS_FRAMEWORK}

## VSL for Analysis:
${vslText}

## Required Comprehensive JSON Output:
${COMPLETE_ANALYSIS_JSON_SCHEMA}`;
};
```

---

## 🔄 RAG HEALTH & FALLBACK LOGIC

### 1. RAG SERVICE HEALTH MONITORING
```javascript
// Node: RAG Health Checker
const ragHealthChecker = {
  async checkRAGHealth() {
    try {
      const startTime = Date.now();
      const response = await fetch('http://localhost:8000/health', {
        timeout: 5000
      });

      const responseTime = Date.now() - startTime;

      if (response.ok) {
        const data = await response.json();
        return {
          status: 'healthy',
          chunks: data.total_chunks,
          responseTime: responseTime,
          categories: data.category_distribution
        };
      } else {
        return {
          status: 'unhealthy',
          error: `HTTP ${response.status}`,
          responseTime: responseTime
        };
      }
    } catch (error) {
      return {
        status: 'unavailable',
        error: error.message,
        fallbackRequired: true
      };
    }
  },

  async performHealthCheck() {
    const health = await this.checkRAGHealth();

    // Log health status
    console.log(`RAG Health: ${health.status}`, health);

    // Set workflow variable for downstream nodes
    return {
      rag_available: health.status === 'healthy',
      rag_performance: health.responseTime || 0,
      rag_chunks: health.chunks || 0,
      fallback_mode: health.status !== 'healthy'
    };
  }
};
```

### 2. FALLBACK STRATEGY IMPLEMENTATION
```javascript
// Node: RAG Fallback Handler
const ragFallbackHandler = {
  // Embedded essential Eugene knowledge for offline operation
  embeddedKnowledge: {
    consciousness_principles: [
      "Level 1: Market unaware of problem - educate about problem existence",
      "Level 2: Problem aware - present solution as breakthrough discovery",
      "Level 3: Solution aware - differentiate from known solutions",
      "Level 4: Product aware - use social proof and testimonials",
      "Level 5: Ready to buy - focus on urgency and irresistible offer"
    ],

    frameworks: {
      "PAS": "Problem identification → Agitation of pain → Solution presentation",
      "AIDA": "Attention grabbing → Interest building → Desire creation → Action trigger",
      "Before/After/Bridge": "Current state → Desired future → Path to get there"
    },

    common_problems: [
      "Headline lacks specificity and curiosity",
      "Insufficient social proof and credibility",
      "Weak or unclear value proposition",
      "Missing urgency and scarcity elements",
      "Poor call-to-action positioning"
    ],

    improvement_templates: [
      "Add specific numbers and timeframes",
      "Include customer testimonials and results",
      "Clarify unique selling proposition",
      "Create genuine urgency with deadlines",
      "Strengthen call-to-action with clear benefits"
    ]
  },

  buildFallbackContext: function(analysisType) {
    switch(analysisType) {
      case 'consciousness':
        return this.embeddedKnowledge.consciousness_principles.join('\n');

      case 'frameworks':
        return Object.entries(this.embeddedKnowledge.frameworks)
          .map(([name, desc]) => `${name}: ${desc}`)
          .join('\n');

      case 'problems':
        return this.embeddedKnowledge.common_problems.join('\n');

      default:
        return Object.values(this.embeddedKnowledge).flat().join('\n');
    }
  }
};
```

---

## 📈 RAG PERFORMANCE OPTIMIZATION

### 1. SMART CACHING STRATEGY
```javascript
// Node: RAG Cache Manager
const ragCacheManager = {
  cache: new Map(),
  maxCacheSize: 100,
  cacheExpiry: 3600000, // 1 hour

  getCacheKey: function(query, category) {
    return `${category}_${this.hashString(query)}`;
  },

  async getCachedResult(query, category) {
    const key = this.getCacheKey(query, category);
    const cached = this.cache.get(key);

    if (cached && (Date.now() - cached.timestamp) < this.cacheExpiry) {
      console.log('RAG cache hit:', key);
      return { ...cached.data, fromCache: true };
    }

    return null;
  },

  setCachedResult: function(query, category, data) {
    const key = this.getCacheKey(query, category);

    // Manage cache size
    if (this.cache.size >= this.maxCacheSize) {
      const oldestKey = this.cache.keys().next().value;
      this.cache.delete(oldestKey);
    }

    this.cache.set(key, {
      data: data,
      timestamp: Date.now()
    });
  }
};
```

### 2. QUERY OPTIMIZATION
```javascript
// Optimize RAG queries for better results
const optimizeRAGQuery = {
  improveQuery: function(vslText, analysisType) {
    // Extract relevant context based on analysis type
    const strategies = {
      consciousness: this.extractConsciousnessIndicators(vslText),
      frameworks: this.extractStructuralElements(vslText),
      problems: this.extractPotentialIssues(vslText)
    };

    return strategies[analysisType] || this.extractGeneralKeywords(vslText);
  },

  extractConsciousnessIndicators: function(text) {
    const indicators = {
      level1: ['não sabia', 'descoberta', 'revelação', 'você pode não saber'],
      level2: ['problema', 'solução', 'finalmente', 'descobri como'],
      level3: ['diferente', 'único', 'revolucionário', 'não é como'],
      level4: ['comprovado', 'testemunhos', 'resultados', 'milhares'],
      level5: ['urgente', 'limitado', 'últimas vagas', 'apenas hoje']
    };

    const foundIndicators = [];
    Object.entries(indicators).forEach(([level, keywords]) => {
      keywords.forEach(keyword => {
        if (text.toLowerCase().includes(keyword)) {
          foundIndicators.push(`${level}: ${keyword}`);
        }
      });
    });

    return foundIndicators.join(' ');
  }
};
```

---

## 🎯 INTEGRATION TESTING & VALIDATION

### 1. RAG INTEGRATION TEST SUITE
```javascript
// Node: RAG Integration Validator
const ragIntegrationTests = {
  async runValidationSuite() {
    const tests = [
      this.testHealthEndpoint(),
      this.testConsciousnessRetrieval(),
      this.testFrameworkRetrieval(),
      this.testImprovementRetrieval(),
      this.testFallbackBehavior()
    ];

    const results = await Promise.all(tests);

    return {
      allPassed: results.every(test => test.passed),
      results: results,
      recommendations: this.generateRecommendations(results)
    };
  },

  async testHealthEndpoint() {
    try {
      const response = await fetch('http://localhost:8000/health');
      const data = await response.json();

      return {
        test: 'health_endpoint',
        passed: response.ok && data.total_chunks > 0,
        data: data
      };
    } catch (error) {
      return {
        test: 'health_endpoint',
        passed: false,
        error: error.message
      };
    }
  },

  async testConsciousnessRetrieval() {
    try {
      const response = await fetch('http://localhost:8000/retrieve/consciousness', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          copy_text: "Você sabia que 90% das pessoas não conhecem este segredo...",
          consciousness_level: null
        })
      });

      const data = await response.json();

      return {
        test: 'consciousness_retrieval',
        passed: response.ok && Array.isArray(data) && data.length > 0,
        resultCount: data.length
      };
    } catch (error) {
      return {
        test: 'consciousness_retrieval',
        passed: false,
        error: error.message
      };
    }
  }
};
```

### 2. QUALITY METRICS FOR RAG-ENHANCED ANALYSIS
```javascript
const ragQualityMetrics = {
  measureEnhancement: function(withRAG, withoutRAG) {
    return {
      accuracy_improvement: this.calculateAccuracyGain(withRAG, withoutRAG),
      detail_increase: this.measureDetailIncrease(withRAG, withoutRAG),
      relevance_score: this.calculateRelevanceScore(withRAG),
      context_utilization: this.measureContextUsage(withRAG)
    };
  },

  calculateRelevanceScore: function(analysis) {
    // Check if RAG context is meaningfully used in analysis
    const contextUsed = analysis.rag_context_used || false;
    const qualityIndicators = [
      analysis.justificativa.length > 200,
      analysis.indicadores_textuais.length >= 3,
      analysis.confianca > 0.8
    ];

    return {
      rag_utilized: contextUsed,
      quality_score: qualityIndicators.filter(Boolean).length / qualityIndicators.length,
      enhancement_detected: contextUsed && qualityIndicators.filter(Boolean).length >= 2
    };
  }
};
```

---

## 📋 SQUAD VITASCIENCE RAG REQUIREMENTS

### Implementation Checklist:
- ✅ **RAG Health Monitoring**: Continuous service availability check
- ✅ **Multi-Endpoint Utilization**: Use specialized endpoints for different analysis types
- ✅ **Fallback Capability**: Function without RAG when service unavailable
- ✅ **Context Optimization**: Smart query building for better retrieval
- ✅ **Caching Strategy**: Reduce redundant API calls for similar queries
- ✅ **Quality Enhancement**: Measurable improvement in analysis depth with RAG
- ✅ **Error Handling**: Graceful degradation when RAG fails
- ✅ **Cost Awareness**: RAG calls don't significantly impact budget

### Integration Success Metrics:
- **Response Time**: RAG queries add <3 seconds to total analysis time
- **Enhancement Rate**: 80%+ of analyses show improvement with RAG context
- **Availability**: 99%+ uptime with seamless fallback when needed
- **Relevance**: 85%+ of retrieved context is relevant to analysis
- **Cost Impact**: RAG integration adds <$0.01 per analysis in processing

This RAG integration strategy ensures the Eugene VSL Analyzer leverages the full 199-chunk knowledge base while maintaining robust fallback capabilities and meeting all Squad Vitascience requirements.
# N8N Error Handling & Fallback Logic
## Robust System Design for Eugene VSL Analyzer

### 🎯 OVERVIEW
This document defines comprehensive error handling strategies, fallback mechanisms, and recovery procedures for the Eugene VSL Analyzer N8N workflow to ensure 99%+ uptime and graceful degradation.

---

## 🛡️ ERROR CATEGORIES & STRATEGIES

### 1. API FAILURES
**Primary Concern**: Claude/GPT API unavailable or rate-limited

#### Claude API Failure Handling:
```javascript
// Node: API Error Handler Function
const handleClaudeAPIFailure = (error, context) => {
  const errorType = determineErrorType(error);

  switch(errorType) {
    case 'rate_limit':
      return {
        strategy: 'retry_with_delay',
        delay_ms: 60000,  // 1 minute
        fallback_to: 'gpt_api'
      };

    case 'quota_exceeded':
      return {
        strategy: 'immediate_fallback',
        fallback_to: 'gpt_api',
        alert_admin: true
      };

    case 'service_unavailable':
      return {
        strategy: 'retry_then_fallback',
        max_retries: 2,
        retry_delay_ms: 30000,
        fallback_to: 'gpt_api'
      };

    case 'invalid_request':
      return {
        strategy: 'validate_and_retry',
        max_retries: 1,
        fallback_to: 'simplified_prompt'
      };

    default:
      return {
        strategy: 'immediate_fallback',
        fallback_to: 'offline_analysis'
      };
  }
};
```

#### GPT Fallback Implementation:
```javascript
// Simplified prompts for GPT fallback
const getGPTFallbackPrompt = (analysisType, vslText) => {
  if (analysisType === 'consciousness') {
    return `Analyze this VSL and classify consciousness level (1-5):

${vslText}

Return JSON:
{
  "nivel_identificado": [1-5],
  "confianca": [0.0-1.0],
  "justificativa": "Brief explanation",
  "indicadores_textuais": ["key phrase 1", "key phrase 2"],
  "nivel_ideal_sugerido": [1-5],
  "razao_sugestao": "Why this level would be better"
}`;
  }

  // Simplified complete analysis for cost optimization
  return `Analyze this VSL for problems and improvements:

${vslText}

Find 5+ problems and suggest 3+ new angles. Return JSON format.`;
};
```

### 2. TIMEOUT HANDLING
**Primary Concern**: Long-running API calls exceeding N8N timeout limits

#### Timeout Prevention Strategy:
```javascript
// Node: Timeout Manager
const timeoutConfig = {
  consciousness_analysis: {
    timeout_ms: 30000,      // 30 seconds
    warning_threshold: 20000, // 20 seconds
    action_on_timeout: 'return_partial'
  },
  complete_analysis: {
    timeout_ms: 90000,      // 90 seconds
    warning_threshold: 60000, // 60 seconds
    action_on_timeout: 'simplify_and_retry'
  },
  total_workflow: {
    timeout_ms: 120000,     // 2 minutes
    warning_threshold: 90000, // 90 seconds
    action_on_timeout: 'emergency_fallback'
  }
};

const handleTimeout = (nodeType, elapsedTime) => {
  const config = timeoutConfig[nodeType];

  if (elapsedTime > config.warning_threshold) {
    // Start preparing fallback
    prepareTimeoutFallback(nodeType);
  }

  if (elapsedTime > config.timeout_ms) {
    return executeTimeoutAction(config.action_on_timeout);
  }

  return { continue: true };
};
```

### 3. RAG SERVICE FAILURES
**Primary Concern**: PostgreSQL/RAG API unavailable

#### RAG Fallback Logic:
```javascript
// Node: RAG Health Check
const checkRAGAvailability = async () => {
  try {
    const response = await fetch('http://localhost:8000/health', {
      timeout: 5000
    });

    if (response.ok) {
      const data = await response.json();
      return {
        available: true,
        chunk_count: data.total_chunks,
        response_time: data.response_time_ms
      };
    }
  } catch (error) {
    return {
      available: false,
      error: error.message,
      fallback_strategy: 'embedded_knowledge'
    };
  }
};

// Embedded Eugene knowledge for offline operation
const embeddedEugeneKnowledge = {
  consciousness_levels: {
    1: "Unaware - educate about problem existence",
    2: "Problem aware - present solution as discovery",
    3: "Solution aware - differentiate from competitors",
    4: "Product aware - use social proof and testimonials",
    5: "Ready to buy - focus on urgency and offer"
  },

  frameworks: {
    PAS: "Problem → Agitation → Solution",
    AIDA: "Attention → Interest → Desire → Action",
    "Before/After/Bridge": "Current state → Desired state → Path"
  },

  common_problems: [
    "Weak headline lacking specificity",
    "Insufficient social proof",
    "Unclear value proposition",
    "Missing urgency elements",
    "Poor call-to-action"
  ]
};
```

### 4. JSON VALIDATION FAILURES
**Primary Concern**: Malformed API responses breaking the pipeline

#### JSON Recovery System:
```javascript
// Node: JSON Validator & Fixer
const validateAndFixJSON = (jsonString, expectedSchema) => {
  try {
    const parsed = JSON.parse(jsonString);

    // Validate against schema
    const validation = validateSchema(parsed, expectedSchema);

    if (validation.valid) {
      return { success: true, data: parsed };
    } else {
      // Attempt to fix common issues
      const fixed = attemptJSONFix(jsonString, validation.errors);
      return { success: true, data: fixed, warning: 'JSON was repaired' };
    }
  } catch (error) {
    // JSON is completely malformed - attempt parsing strategies
    const recovered = attemptJSONRecovery(jsonString, expectedSchema);

    if (recovered) {
      return {
        success: true,
        data: recovered,
        warning: 'JSON was reconstructed'
      };
    } else {
      return {
        success: false,
        error: 'JSON unrecoverable',
        fallback_needed: true
      };
    }
  }
};

const attemptJSONFix = (jsonString, errors) => {
  let fixed = jsonString;

  // Common fixes
  fixed = fixed.replace(/,\s*}/g, '}');  // Remove trailing commas
  fixed = fixed.replace(/,\s*]/g, ']');  // Remove trailing commas in arrays
  fixed = fixed.replace(/'/g, '"');      // Replace single quotes
  fixed = fixed.replace(/(\w+):/g, '"$1":'); // Quote unquoted keys

  // Try to parse again
  try {
    return JSON.parse(fixed);
  } catch (e) {
    return null;
  }
};
```

### 5. COST LIMIT ENFORCEMENT
**Primary Concern**: Exceeding $6 budget allocation

#### Cost Tracking & Protection:
```javascript
// Node: Cost Controller
const costController = {
  budget_total: 6.00,
  budget_used: 0.00,
  analysis_count: 0,

  // Model costs (USD per 1K tokens)
  model_costs: {
    'claude-3-5-sonnet': { input: 0.003, output: 0.015 },
    'gpt-4o-mini': { input: 0.00015, output: 0.0006 },
    'gpt-3.5-turbo': { input: 0.0005, output: 0.0015 }
  },

  estimateAnalysisCost: function(vslLength, model) {
    const tokens = Math.ceil(vslLength / 4); // Rough token estimation
    const promptTokens = tokens + 2000; // Include prompt overhead
    const responseTokens = 1500; // Estimated response length

    const cost = (promptTokens * this.model_costs[model].input / 1000) +
                 (responseTokens * this.model_costs[model].output / 1000);

    return cost;
  },

  checkBudget: function(estimatedCost) {
    const remaining = this.budget_total - this.budget_used;

    if (estimatedCost > remaining) {
      return {
        allowed: false,
        reason: 'budget_exceeded',
        remaining_budget: remaining,
        suggested_action: 'use_cheaper_model'
      };
    }

    if (remaining < 1.00 && estimatedCost > 0.50) {
      return {
        allowed: true,
        warning: 'budget_low',
        suggested_model: 'gpt-4o-mini'
      };
    }

    return { allowed: true };
  },

  recordCost: function(actualCost) {
    this.budget_used += actualCost;
    this.analysis_count += 1;

    // Log for monitoring
    console.log(`Cost tracking: ${this.budget_used.toFixed(4)}/${this.budget_total} used (${this.analysis_count} analyses)`);
  }
};
```

---

## 🔄 FALLBACK HIERARCHY

### Level 1: Primary System
- **Claude Sonnet 3.5** for all analysis
- **Full RAG integration** with 199 chunks
- **Complete prompt templates** with rich context
- **Target cost**: ~$0.095 per analysis

### Level 2: Cost-Optimized Fallback
- **GPT-4o-mini** for analysis
- **Simplified prompts** without extensive context
- **RAG integration** maintained
- **Target cost**: ~$0.048 per analysis

### Level 3: Emergency Fallback
- **GPT-3.5-turbo** for basic analysis
- **Minimal prompts** focused on core requirements
- **No RAG dependency** (embedded knowledge)
- **Target cost**: ~$0.025 per analysis

### Level 4: Offline Fallback
- **Rule-based analysis** using embedded Eugene knowledge
- **Template-based responses** with placeholder values
- **No API calls** required
- **Target cost**: $0.00 per analysis

---

## 🚨 SPECIFIC ERROR SCENARIOS

### Scenario 1: Claude API Rate Limit
```javascript
// Detection
if (error.status === 429) {
  // Wait and retry once
  await sleep(60000);
  const retryResult = await retryClaudeAPI();

  if (retryResult.success) {
    return retryResult;
  } else {
    // Switch to GPT fallback
    return switchToGPTAnalysis();
  }
}
```

### Scenario 2: Complete API Failure
```javascript
// All APIs down - use offline fallback
const offlineAnalysis = {
  metadata: {
    analysis_id: generateID(),
    timestamp: new Date().toISOString(),
    analysis_version: "offline_fallback_v1.0",
    models_used: { fallback: "rule_based_analysis" }
  },

  consciousness_analysis: generateOfflineConsciousness(vslText),
  framework_analysis: detectFrameworkOffline(vslText),
  problemas_identificados: getCommonProblems(),
  melhorias_eugene: getStandardImprovements(),
  novos_angulos: generateBasicAngles(),

  summary: {
    total_problemas: 5,
    total_angulos: 3,
    score_geral: 65, // Conservative estimate
    recomendacao_principal: "Professional analysis recommended when services available"
  }
};
```

### Scenario 3: Partial Failure Recovery
```javascript
// One branch fails, use the other to estimate missing data
const recoverFromPartialFailure = (successfulBranch, failedBranch) => {
  if (successfulBranch === 'consciousness' && failedBranch === 'complete') {
    // Use consciousness analysis to estimate framework and problems
    return {
      ...consciousnessResult,
      framework_analysis: estimateFrameworkFromConsciousness(consciousnessResult),
      problemas_identificados: getProblemsForLevel(consciousnessResult.nivel_identificado),
      melhorias_eugene: getImprovementsForLevel(consciousnessResult.nivel_identificado),
      novos_angulos: getAnglesForLevel(consciousnessResult.nivel_identificado)
    };
  }

  // Similar logic for opposite scenario
};
```

---

## 📊 MONITORING & ALERTING

### Real-Time Monitoring:
```javascript
const monitoringSystem = {
  metrics: {
    total_requests: 0,
    successful_analyses: 0,
    failed_analyses: 0,
    fallback_usage: {},
    average_response_time: 0,
    cost_tracking: {}
  },

  logEvent: function(eventType, data) {
    const timestamp = new Date().toISOString();

    console.log(`[${timestamp}] ${eventType}:`, data);

    // Update metrics
    this.updateMetrics(eventType, data);

    // Check for alerting conditions
    this.checkAlerts(eventType, data);
  },

  checkAlerts: function(eventType, data) {
    // High failure rate
    const failureRate = this.metrics.failed_analyses / this.metrics.total_requests;
    if (failureRate > 0.1) { // 10% failure rate
      this.sendAlert('high_failure_rate', { rate: failureRate });
    }

    // Budget usage alert
    if (costController.budget_used / costController.budget_total > 0.8) {
      this.sendAlert('budget_warning', {
        used: costController.budget_used,
        total: costController.budget_total
      });
    }

    // API health alerts
    if (eventType === 'api_failure') {
      this.sendAlert('api_health_issue', data);
    }
  }
};
```

### Health Check Endpoint:
```javascript
// Node: System Health Reporter
const generateHealthReport = () => {
  return {
    timestamp: new Date().toISOString(),
    overall_status: determineOverallHealth(),

    services: {
      claude_api: testClaudeAPI(),
      gpt_api: testGPTAPI(),
      rag_service: testRAGService(),
      n8n_workflow: 'operational'
    },

    performance: {
      average_response_time: monitoringSystem.metrics.average_response_time,
      success_rate: calculateSuccessRate(),
      fallback_usage_rate: calculateFallbackUsage()
    },

    budget: {
      total_budget: costController.budget_total,
      used_budget: costController.budget_used,
      remaining_budget: costController.budget_total - costController.budget_used,
      analyses_completed: costController.analysis_count
    },

    recommendations: generateHealthRecommendations()
  };
};
```

---

## 🔧 RECOVERY PROCEDURES

### Automatic Recovery Actions:
1. **Retry Logic**: Exponential backoff for transient failures
2. **Circuit Breaker**: Temporary disable failing services
3. **Graceful Degradation**: Reduce analysis depth if needed
4. **Load Balancing**: Switch between available models
5. **Cache Utilization**: Use cached results for similar VSLs

### Manual Recovery Triggers:
1. **Admin Override**: Force specific fallback mode
2. **Budget Reset**: Reset cost tracking if needed
3. **Service Restart**: Restart specific N8N nodes
4. **Emergency Mode**: Switch to offline-only operation

### Recovery Validation:
```javascript
const validateRecovery = async (recoveryAction) => {
  // Test the recovery action
  const testResult = await runRecoveryTest(recoveryAction);

  if (testResult.success) {
    console.log(`Recovery successful: ${recoveryAction}`);
    return { recovered: true, action: recoveryAction };
  } else {
    console.log(`Recovery failed: ${recoveryAction}, trying next option`);
    return { recovered: false, nextAction: getNextRecoveryOption() };
  }
};
```

This comprehensive error handling system ensures the Eugene VSL Analyzer maintains high availability and provides meaningful responses even under adverse conditions, meeting the Squad Vitascience reliability requirements.
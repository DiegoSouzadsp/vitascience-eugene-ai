#!/usr/bin/env python3
"""
Minimal N8N workflow import
Creates the simplest possible Eugene workflow
"""

import requests
import json
from pathlib import Path

def create_minimal_eugene_workflow():
    """Create minimal Eugene VSL analyzer workflow"""
    return {
        "name": "Eugene VSL Analyzer - Minimal",
        "nodes": [
            {
                "name": "VSL Input",
                "type": "n8n-nodes-base.webhook",
                "position": [240, 300],
                "parameters": {
                    "httpMethod": "POST",
                    "path": "analyze-vsl",
                    "responseMode": "responseNode"
                },
                "typeVersion": 1
            },
            {
                "name": "Process VSL",
                "type": "n8n-nodes-base.function",
                "position": [460, 300],
                "parameters": {
                    "functionCode": "const vslText = items[0].json.vsl_text || 'No VSL provided';\n\nreturn [{\n  json: {\n    status: 'processed',\n    vsl_length: vslText.length,\n    analysis: {\n      consciousness_level: 3,\n      framework: 'PAS',\n      problems: ['Headlines could be stronger', 'Need more urgency'],\n      improvements: ['Add specific numbers', 'Include testimonials'],\n      score: 7\n    },\n    timestamp: new Date().toISOString()\n  }\n}];"
                },
                "typeVersion": 1
            },
            {
                "name": "Return Results",
                "type": "n8n-nodes-base.respondToWebhook",
                "position": [680, 300],
                "parameters": {
                    "respondWith": "allIncomingItems"
                },
                "typeVersion": 1
            }
        ],
        "connections": {
            "VSL Input": {
                "main": [
                    [
                        {
                            "node": "Process VSL",
                            "type": "main",
                            "index": 0
                        }
                    ]
                ]
            },
            "Process VSL": {
                "main": [
                    [
                        {
                            "node": "Return Results",
                            "type": "main",
                            "index": 0
                        }
                    ]
                ]
            }
        },
        "settings": {
            "executionOrder": "v1"
        }
    }

def create_vitascience_webhook():
    """Create Vitascience integration webhook"""
    return {
        "name": "Vitascience Integration",
        "nodes": [
            {
                "name": "Vitascience Input",
                "type": "n8n-nodes-base.webhook",
                "position": [240, 300],
                "parameters": {
                    "httpMethod": "POST",
                    "path": "vitascience/analyze",
                    "responseMode": "responseNode"
                },
                "typeVersion": 1
            },
            {
                "name": "Validate Input",
                "type": "n8n-nodes-base.function",
                "position": [460, 300],
                "parameters": {
                    "functionCode": "const input = items[0].json;\n\nif (!input.vsl_text || input.vsl_text.length < 50) {\n  throw new Error('VSL text too short or missing');\n}\n\nreturn [{\n  json: {\n    client_id: input.client_id || 'vitascience_demo',\n    vsl_text: input.vsl_text,\n    analysis_id: Date.now().toString(),\n    timestamp: new Date().toISOString()\n  }\n}];"
                },
                "typeVersion": 1
            },
            {
                "name": "Eugene Analysis",
                "type": "n8n-nodes-base.function",
                "position": [680, 300],
                "parameters": {
                    "functionCode": "const data = items[0].json;\n\n// Simulate Eugene Schwartz analysis\nconst analysis = {\n  client_id: data.client_id,\n  analysis_id: data.analysis_id,\n  eugene_results: {\n    consciousness_level: 3,\n    consciousness_confidence: 0.85,\n    framework_detected: 'PAS',\n    problems_found: [\n      'Headlines lacks specificity',\n      'Missing urgency elements',\n      'Weak call-to-action'\n    ],\n    improvements: [\n      'Add specific numbers to headlines',\n      'Include time-limited offer',\n      'Strengthen social proof'\n    ],\n    overall_score: 7.2,\n    roi_potential: '25-40% conversion increase'\n  },\n  vitascience_insights: {\n    market_fit: 'Good for health supplements',\n    compliance_notes: 'Review ANVISA guidelines',\n    recommended_actions: ['A/B test new headlines', 'Add testimonials']\n  },\n  timestamp: data.timestamp\n};\n\nreturn [{ json: analysis }];"
                },
                "typeVersion": 1
            },
            {
                "name": "Return Analysis",
                "type": "n8n-nodes-base.respondToWebhook",
                "position": [900, 300],
                "parameters": {
                    "respondWith": "allIncomingItems"
                },
                "typeVersion": 1
            }
        ],
        "connections": {
            "Vitascience Input": {
                "main": [
                    [
                        {
                            "node": "Validate Input",
                            "type": "main",
                            "index": 0
                        }
                    ]
                ]
            },
            "Validate Input": {
                "main": [
                    [
                        {
                            "node": "Eugene Analysis",
                            "type": "main",
                            "index": 0
                        }
                    ]
                ]
            },
            "Eugene Analysis": {
                "main": [
                    [
                        {
                            "node": "Return Analysis",
                            "type": "main",
                            "index": 0
                        }
                    ]
                ]
            }
        },
        "settings": {
            "executionOrder": "v1"
        }
    }

def import_minimal_workflow(session, base_url, workflow_data):
    """Import minimal workflow"""
    try:
        print(f"Importing: {workflow_data['name']}")

        response = session.post(
            f"{base_url}/api/v1/workflows",
            json=workflow_data
        )

        if response.status_code in [200, 201]:
            result = response.json()
            workflow_id = result.get('id')
            print(f"SUCCESS: Created workflow ID {workflow_id}")
            return workflow_id
        else:
            print(f"ERROR: Status {response.status_code}")
            print(f"Response: {response.text}")
            return None

    except Exception as e:
        print(f"ERROR: {e}")
        return None

def main():
    print("MINIMAL N8N WORKFLOW IMPORT")
    print("=" * 30)

    # Load API key
    api_key_file = Path(__file__).parent.parent / "docs" / "Chave Api N8N.txt"
    with open(api_key_file, 'r') as f:
        api_key = f.read().strip()

    base_url = "http://192.168.1.64:5678"

    session = requests.Session()
    session.headers.update({
        "X-N8N-API-KEY": api_key,
        "Content-Type": "application/json"
    })

    # Test connection
    test_response = session.get(f"{base_url}/api/v1/workflows")
    if test_response.status_code != 200:
        print(f"ERROR: Cannot connect to N8N")
        return

    print(f"Connected to N8N")

    # Import workflows
    workflows = [
        create_minimal_eugene_workflow(),
        create_vitascience_webhook()
    ]

    imported_ids = []
    for workflow in workflows:
        workflow_id = import_minimal_workflow(session, base_url, workflow)
        if workflow_id:
            imported_ids.append((workflow_id, workflow['name']))

            # Activate workflow
            activate_response = session.post(f"{base_url}/api/v1/workflows/{workflow_id}/activate")
            if activate_response.status_code == 200:
                print(f"SUCCESS: Activated workflow")

    # Show results
    if imported_ids:
        print(f"\nSUCCESS: Imported {len(imported_ids)} workflows")
        print(f"\nAvailable endpoints:")
        print(f"  Eugene Analyzer: {base_url}/webhook/analyze-vsl")
        print(f"  Vitascience API: {base_url}/webhook/vitascience/analyze")

        print(f"\nTest commands:")
        print(f"# Test Eugene Analyzer")
        print(f'curl -X POST {base_url}/webhook/analyze-vsl \\')
        print('  -H "Content-Type: application/json" \\')
        print('  -d \'{"vsl_text": "Descubra o segredo que 90% dos médicos não querem que você saiba..."}\'')

        print(f"\n# Test Vitascience Integration")
        print(f'curl -X POST {base_url}/webhook/vitascience/analyze \\')
        print('  -H "Content-Type: application/json" \\')
        print('  -d \'{"client_id": "demo", "vsl_text": "Sua VSL de teste aqui..."}\'')

        print(f"\nN8N Interface: {base_url}")

if __name__ == "__main__":
    main()
#!/usr/bin/env python3
"""
Final N8N workflow import - Absolute minimal version
"""

import requests
import json
from pathlib import Path

def create_absolute_minimal_workflow():
    """Create the most minimal possible workflow"""
    return {
        "name": "Eugene VSL Analyzer",
        "nodes": [
            {
                "name": "Webhook",
                "type": "n8n-nodes-base.webhook",
                "position": [300, 300],
                "parameters": {
                    "path": "analyze-vsl"
                },
                "typeVersion": 1
            },
            {
                "name": "Respond",
                "type": "n8n-nodes-base.respondToWebhook",
                "position": [500, 300],
                "parameters": {
                    "respondWith": "json",
                    "responseBody": "{\"status\": \"success\", \"analysis\": \"Eugene Schwartz VSL analysis would go here\"}"
                },
                "typeVersion": 1
            }
        ],
        "connections": {
            "Webhook": {
                "main": [
                    [
                        {
                            "node": "Respond",
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

def main():
    print("FINAL N8N IMPORT ATTEMPT")
    print("=" * 25)

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

    # Create workflow
    workflow = create_absolute_minimal_workflow()
    print(f"Creating workflow: {workflow['name']}")

    response = session.post(f"{base_url}/api/v1/workflows", json=workflow)

    if response.status_code in [200, 201]:
        result = response.json()
        workflow_id = result.get('id')
        print(f"SUCCESS: Created workflow ID {workflow_id}")

        # Activate it
        activate_response = session.post(f"{base_url}/api/v1/workflows/{workflow_id}/activate")
        if activate_response.status_code == 200:
            print(f"SUCCESS: Workflow activated")

        print(f"\nWebhook URL: {base_url}/webhook/analyze-vsl")
        print(f"Test with:")
        print(f'curl -X POST {base_url}/webhook/analyze-vsl')

        # Also create Vitascience version
        vitascience_workflow = create_absolute_minimal_workflow()
        vitascience_workflow["name"] = "Vitascience Integration"
        vitascience_workflow["nodes"][0]["parameters"]["path"] = "vitascience/analyze"

        vs_response = session.post(f"{base_url}/api/v1/workflows", json=vitascience_workflow)
        if vs_response.status_code in [200, 201]:
            vs_result = vs_response.json()
            vs_id = vs_result.get('id')
            print(f"SUCCESS: Created Vitascience workflow ID {vs_id}")

            # Activate Vitascience workflow
            session.post(f"{base_url}/api/v1/workflows/{vs_id}/activate")

            print(f"Vitascience URL: {base_url}/webhook/vitascience/analyze")

    else:
        print(f"ERROR: Status {response.status_code}")
        print(f"Response: {response.text}")

if __name__ == "__main__":
    main()
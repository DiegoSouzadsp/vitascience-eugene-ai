#!/usr/bin/env python3
"""
Clean and import N8N workflows
Remove extra properties that cause API errors
"""

import requests
import json
from pathlib import Path

def load_n8n_config():
    """Load N8N configuration"""
    config = {"host": "192.168.1.64", "port": "5678"}

    api_key_file = Path(__file__).parent.parent / "docs" / "Chave Api N8N.txt"
    with open(api_key_file, 'r') as f:
        config["api_key"] = f.read().strip()

    return config

def clean_workflow_json(workflow_data):
    """Clean workflow JSON for API import"""
    # Keep only essential properties for import
    cleaned = {
        "name": workflow_data.get("name", "Imported Workflow"),
        "nodes": workflow_data.get("nodes", []),
        "connections": workflow_data.get("connections", {}),
        "active": False,  # Import as inactive first
        "settings": workflow_data.get("settings", {}),
        "staticData": workflow_data.get("staticData", {})
    }

    # Clean nodes - remove IDs and unnecessary properties
    for node in cleaned["nodes"]:
        # Remove ID (will be auto-generated)
        if "id" in node:
            del node["id"]

        # Keep essential node properties
        essential_props = ["name", "type", "position", "parameters", "typeVersion"]
        cleaned_node = {k: v for k, v in node.items() if k in essential_props}
        node.clear()
        node.update(cleaned_node)

    return cleaned

def create_simple_test_workflow():
    """Create a simple test workflow"""
    return {
        "name": "Eugene Test Workflow",
        "nodes": [
            {
                "name": "Start",
                "type": "n8n-nodes-base.start",
                "position": [300, 300],
                "parameters": {},
                "typeVersion": 1
            },
            {
                "name": "Webhook",
                "type": "n8n-nodes-base.webhook",
                "position": [500, 300],
                "parameters": {
                    "httpMethod": "POST",
                    "path": "test-eugene",
                    "responseMode": "responseNode"
                },
                "typeVersion": 1
            },
            {
                "name": "Respond to Webhook",
                "type": "n8n-nodes-base.respondToWebhook",
                "position": [700, 300],
                "parameters": {
                    "respondWith": "json",
                    "responseBody": "={\"status\": \"success\", \"message\": \"Eugene workflow test\"}"
                },
                "typeVersion": 1
            }
        ],
        "connections": {
            "Start": {
                "main": [
                    [
                        {
                            "node": "Webhook",
                            "type": "main",
                            "index": 0
                        }
                    ]
                ]
            },
            "Webhook": {
                "main": [
                    [
                        {
                            "node": "Respond to Webhook",
                            "type": "main",
                            "index": 0
                        }
                    ]
                ]
            }
        },
        "active": False,
        "settings": {}
    }

def import_workflow(session, base_url, workflow_data, name):
    """Import cleaned workflow"""
    try:
        print(f"Importing: {name}")

        response = session.post(
            f"{base_url}/api/v1/workflows",
            json=workflow_data
        )

        if response.status_code == 201:
            result = response.json()
            workflow_id = result.get('id')
            print(f"SUCCESS: Created workflow ID {workflow_id}")

            # Activate workflow
            activate_response = session.post(f"{base_url}/api/v1/workflows/{workflow_id}/activate")
            if activate_response.status_code == 200:
                print(f"SUCCESS: Activated workflow")

            return workflow_id
        else:
            print(f"ERROR: Status {response.status_code}")
            print(f"Response: {response.text}")
            return None

    except Exception as e:
        print(f"ERROR: {e}")
        return None

def main():
    print("N8N WORKFLOW CLEANER AND IMPORTER")
    print("=" * 40)

    # Setup
    config = load_n8n_config()
    base_url = f"http://{config['host']}:{config['port']}"

    session = requests.Session()
    session.headers.update({
        "X-N8N-API-KEY": config["api_key"],
        "Content-Type": "application/json"
    })

    # Test connection
    test_response = session.get(f"{base_url}/api/v1/workflows")
    if test_response.status_code != 200:
        print(f"ERROR: Cannot connect to N8N API")
        return

    print(f"Connected to N8N at {base_url}")

    # Create simple test workflow first
    print("\nCreating simple test workflow...")
    test_workflow = create_simple_test_workflow()
    test_id = import_workflow(session, base_url, test_workflow, "Eugene Test")

    if test_id:
        print(f"\nTest webhook URL: {base_url}/webhook/test-eugene")
        print("Test with: curl -X POST http://192.168.1.64:5678/webhook/test-eugene")

    # Try to clean and import original workflows
    workflows_dir = Path(__file__).parent.parent / "n8n" / "workflows"

    for workflow_file in ["eugene_vsl_analyzer.json", "vitascience_integration.json"]:
        file_path = workflows_dir / workflow_file

        if file_path.exists():
            print(f"\nProcessing: {workflow_file}")

            with open(file_path, 'r', encoding='utf-8') as f:
                original_data = json.load(f)

            cleaned_data = clean_workflow_json(original_data)
            workflow_id = import_workflow(session, base_url, cleaned_data, cleaned_data["name"])

            if workflow_id:
                # Save cleaned version
                cleaned_file = workflows_dir / f"cleaned_{workflow_file}"
                with open(cleaned_file, 'w', encoding='utf-8') as f:
                    json.dump(cleaned_data, f, indent=2)
                print(f"Saved cleaned version: {cleaned_file}")

    print("\nDone! Check N8N interface at: http://192.168.1.64:5678")

if __name__ == "__main__":
    main()
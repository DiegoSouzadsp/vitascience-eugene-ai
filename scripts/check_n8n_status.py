#!/usr/bin/env python3
"""
Check N8N workflow status and manually activate
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

def main():
    print("N8N STATUS CHECK")
    print("=" * 20)

    config = load_n8n_config()
    base_url = f"http://{config['host']}:{config['port']}"

    session = requests.Session()
    session.headers.update({
        "X-N8N-API-KEY": config["api_key"],
        "Content-Type": "application/json"
    })

    # List all workflows
    response = session.get(f"{base_url}/api/v1/workflows")
    if response.status_code == 200:
        workflows = response.json().get('data', [])
        print(f"Found {len(workflows)} workflows:")

        for wf in workflows:
            name = wf.get('name', 'Unknown')
            wf_id = wf.get('id', 'Unknown')
            active = wf.get('active', False)
            status = "ACTIVE" if active else "INACTIVE"

            print(f"  - {name} (ID: {wf_id}) [{status}]")

            # If inactive, try to activate
            if not active:
                print(f"    Activating {name}...")
                activate_response = session.post(f"{base_url}/api/v1/workflows/{wf_id}/activate")
                if activate_response.status_code == 200:
                    print(f"    SUCCESS: Activated {name}")
                else:
                    print(f"    ERROR: Could not activate {name} - {activate_response.status_code}")

            # Show webhook details
            details_response = session.get(f"{base_url}/api/v1/workflows/{wf_id}")
            if details_response.status_code == 200:
                workflow_details = details_response.json()
                webhook_paths = []

                for node in workflow_details.get('nodes', []):
                    if node.get('type') == 'n8n-nodes-base.webhook':
                        path = node.get('parameters', {}).get('path', '')
                        if path:
                            webhook_paths.append(path)

                if webhook_paths:
                    print(f"    Webhook paths: {', '.join(webhook_paths)}")
                else:
                    print(f"    No webhooks found")

    print(f"\nN8N Interface: {base_url}")

if __name__ == "__main__":
    main()
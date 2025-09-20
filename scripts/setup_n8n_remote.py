#!/usr/bin/env python3
"""
Setup N8N workflows no servidor remoto 192.168.1.64
"""

import requests
import json
from pathlib import Path
import time

# N8N Server Configuration
N8N_HOST = "192.168.1.64"
N8N_PORT = "5678"
N8N_BASE_URL = f"http://{N8N_HOST}:{N8N_PORT}"
N8N_USERNAME = "admin"
N8N_PASSWORD = "password"

def check_n8n_remote():
    """Check remote N8N connection"""
    try:
        print(f"Checking N8N at {N8N_BASE_URL}...")
        response = requests.get(
            f"{N8N_BASE_URL}/api/v1/workflows",
            auth=(N8N_USERNAME, N8N_PASSWORD),
            timeout=10
        )
        if response.status_code == 200:
            print("SUCCESS: N8N remote connection established")
            return True
        else:
            print(f"ERROR: N8N responded with status {response.status_code}")
            return False
    except Exception as e:
        print(f"ERROR: Cannot connect to N8N - {e}")
        return False

def list_existing_workflows():
    """List existing workflows in N8N"""
    try:
        response = requests.get(
            f"{N8N_BASE_URL}/api/v1/workflows",
            auth=(N8N_USERNAME, N8N_PASSWORD)
        )
        if response.status_code == 200:
            workflows = response.json().get('data', [])
            print(f"\nExisting workflows ({len(workflows)}):")
            for wf in workflows:
                print(f"  - {wf.get('name', 'Unnamed')} (ID: {wf.get('id')})")
            return workflows
        return []
    except Exception as e:
        print(f"ERROR listing workflows: {e}")
        return []

def delete_workflow_by_name(name):
    """Delete existing workflow by name"""
    try:
        workflows = list_existing_workflows()
        for wf in workflows:
            if wf.get('name') == name:
                delete_response = requests.delete(
                    f"{N8N_BASE_URL}/api/v1/workflows/{wf['id']}",
                    auth=(N8N_USERNAME, N8N_PASSWORD)
                )
                if delete_response.status_code == 200:
                    print(f"DELETED: Existing workflow '{name}'")
                    return True
        return False
    except Exception as e:
        print(f"ERROR deleting workflow: {e}")
        return False

def import_workflow_remote(workflow_file, name):
    """Import workflow to remote N8N"""
    try:
        print(f"\nImporting: {name}")
        print(f"File: {workflow_file}")

        # Read workflow JSON
        with open(workflow_file, 'r', encoding='utf-8') as f:
            workflow_data = json.load(f)

        # Update workflow for remote URLs (if needed)
        workflow_data = update_workflow_urls(workflow_data)

        # Delete existing workflow with same name
        delete_workflow_by_name(name)

        # Create new workflow
        response = requests.post(
            f"{N8N_BASE_URL}/api/v1/workflows",
            json=workflow_data,
            auth=(N8N_USERNAME, N8N_PASSWORD),
            headers={'Content-Type': 'application/json'}
        )

        if response.status_code == 201:
            workflow_id = response.json().get('id')
            print(f"SUCCESS: Created workflow '{name}' (ID: {workflow_id})")

            # Activate workflow
            time.sleep(1)
            activate_response = requests.post(
                f"{N8N_BASE_URL}/api/v1/workflows/{workflow_id}/activate",
                auth=(N8N_USERNAME, N8N_PASSWORD)
            )

            if activate_response.status_code == 200:
                print(f"SUCCESS: Activated workflow '{name}'")
            else:
                print(f"WARNING: Could not activate workflow (Status: {activate_response.status_code})")

            return True
        else:
            print(f"ERROR: Failed to create workflow (Status: {response.status_code})")
            print(f"Response: {response.text[:200]}...")
            return False

    except Exception as e:
        print(f"ERROR importing {name}: {e}")
        return False

def update_workflow_urls(workflow_data):
    """Update URLs in workflow to point to correct RAG API"""
    # Update RAG API URLs to point to local or accessible endpoint
    # For now, keep localhost assuming RAG API is accessible from N8N server
    return workflow_data

def main():
    print("N8N REMOTE WORKFLOWS SETUP")
    print("=" * 35)
    print(f"Target N8N: {N8N_BASE_URL}")
    print(f"Credentials: {N8N_USERNAME}/{N8N_PASSWORD}")

    # Check connection
    if not check_n8n_remote():
        print("\nFAILED: Cannot connect to remote N8N")
        print("Please check:")
        print("1. N8N is running on 192.168.1.64:5678")
        print("2. Network connectivity")
        print("3. Credentials (admin/password)")
        return

    # List existing workflows
    existing = list_existing_workflows()

    # Find workflow files
    workflows_dir = Path(__file__).parent.parent / "n8n" / "workflows"
    print(f"\nLooking for workflows in: {workflows_dir}")

    if not workflows_dir.exists():
        print("ERROR: Workflows directory not found")
        return

    workflows_to_import = [
        {
            "file": "eugene_vsl_analyzer.json",
            "name": "Eugene VSL Analyzer - Complete Pipeline"
        },
        {
            "file": "vitascience_integration.json",
            "name": "Vitascience Integration - Eugene Analysis"
        }
    ]

    success_count = 0
    total_workflows = len(workflows_to_import)

    for workflow_info in workflows_to_import:
        workflow_file = workflows_dir / workflow_info["file"]

        if not workflow_file.exists():
            print(f"ERROR: File not found - {workflow_file}")
            continue

        if import_workflow_remote(workflow_file, workflow_info["name"]):
            success_count += 1

    # Final summary
    print(f"\n" + "=" * 40)
    print(f"IMPORT SUMMARY: {success_count}/{total_workflows} workflows")

    if success_count > 0:
        print(f"\nSUCCESS: Workflows imported to N8N!")
        print(f"Access: {N8N_BASE_URL}")
        print(f"Login: {N8N_USERNAME} / {N8N_PASSWORD}")

        print(f"\nAvailable webhooks:")
        print(f"  Complete Analysis: {N8N_BASE_URL}/webhook/analyze-vsl")
        print(f"  Vitascience API: {N8N_BASE_URL}/webhook/vitascience/analyze")

        print(f"\nTest with curl:")
        print(f'curl -X POST {N8N_BASE_URL}/webhook/analyze-vsl \\')
        print('  -H "Content-Type: application/json" \\')
        print('  -d \'{"vsl_text": "Sua VSL aqui..."}\'')

        # List final workflows
        print("\nFinal workflows:")
        list_existing_workflows()

    else:
        print("ERROR: No workflows were imported successfully")

if __name__ == "__main__":
    main()
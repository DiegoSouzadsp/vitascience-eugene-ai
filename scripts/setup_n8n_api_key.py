#!/usr/bin/env python3
"""
Setup N8N workflows using API Key authentication
Uses the proper N8N API key instead of basic auth
"""

import requests
import json
from pathlib import Path
import time

def load_n8n_config():
    """Load N8N configuration from files"""
    config = {
        "host": "192.168.1.64",
        "port": "5678",
        "api_key": None,
        "username": None,
        "password": None
    }

    # Try to load API key
    api_key_file = Path(__file__).parent.parent / "docs" / "Chave Api N8N.txt"
    if api_key_file.exists():
        with open(api_key_file, 'r') as f:
            config["api_key"] = f.read().strip()
        print(f"API Key loaded from: {api_key_file}")

    # Fallback to username/password if no API key
    if not config["api_key"]:
        user_pass_file = Path(__file__).parent.parent / "docs" / "usuario senha N8N.txt"
        if user_pass_file.exists():
            with open(user_pass_file, 'r') as f:
                lines = f.read().strip().split('\n')
                if len(lines) >= 2:
                    config["username"] = lines[0].strip()
                    config["password"] = lines[1].strip()
            print(f"Username/Password loaded from: {user_pass_file}")

    return config

def create_n8n_session(config):
    """Create requests session with proper authentication"""
    session = requests.Session()
    base_url = f"http://{config['host']}:{config['port']}"

    if config["api_key"]:
        # Use API Key authentication (preferred)
        session.headers.update({
            "X-N8N-API-KEY": config["api_key"],
            "Content-Type": "application/json",
            "Accept": "application/json"
        })
        print("Using API Key authentication")
    elif config["username"] and config["password"]:
        # Fallback to basic auth
        session.auth = (config["username"], config["password"])
        session.headers.update({
            "Content-Type": "application/json",
            "Accept": "application/json"
        })
        print("Using Basic authentication")
    else:
        print("ERROR: No authentication method available")
        return None, None

    return session, base_url

def test_n8n_connection(session, base_url):
    """Test N8N API connection"""
    try:
        print(f"Testing connection to: {base_url}")
        response = session.get(f"{base_url}/api/v1/workflows")

        if response.status_code == 200:
            workflows = response.json()
            print(f"SUCCESS: Connected to N8N")
            print(f"Found {len(workflows.get('data', []))} existing workflows")
            return True
        else:
            print(f"ERROR: N8N API returned status {response.status_code}")
            print(f"Response: {response.text[:200]}")
            return False

    except Exception as e:
        print(f"ERROR: Connection failed - {e}")
        return False

def list_workflows(session, base_url):
    """List existing workflows"""
    try:
        response = session.get(f"{base_url}/api/v1/workflows")
        if response.status_code == 200:
            workflows = response.json().get('data', [])
            print(f"\nExisting workflows ({len(workflows)}):")
            for wf in workflows:
                active_status = "ACTIVE" if wf.get('active') else "INACTIVE"
                print(f"  - {wf.get('name')} (ID: {wf.get('id')}) [{active_status}]")
            return workflows
        return []
    except Exception as e:
        print(f"ERROR listing workflows: {e}")
        return []

def import_workflow(session, base_url, workflow_file, workflow_name):
    """Import workflow to N8N using API"""
    try:
        print(f"\nImporting workflow: {workflow_name}")

        # Read workflow JSON
        with open(workflow_file, 'r', encoding='utf-8') as f:
            workflow_data = json.load(f)

        # Remove ID if present (for new workflow)
        if 'id' in workflow_data:
            del workflow_data['id']

        # Set active to true
        workflow_data['active'] = True

        # Create workflow
        response = session.post(
            f"{base_url}/api/v1/workflows",
            json=workflow_data
        )

        if response.status_code == 201:
            workflow_info = response.json()
            workflow_id = workflow_info.get('id')
            print(f"SUCCESS: Created workflow '{workflow_name}' (ID: {workflow_id})")
            return workflow_id
        else:
            print(f"ERROR: Failed to create workflow")
            print(f"Status: {response.status_code}")
            print(f"Response: {response.text[:300]}")
            return None

    except Exception as e:
        print(f"ERROR importing workflow: {e}")
        return None

def activate_workflow(session, base_url, workflow_id, workflow_name):
    """Activate workflow"""
    try:
        response = session.post(f"{base_url}/api/v1/workflows/{workflow_id}/activate")
        if response.status_code == 200:
            print(f"SUCCESS: Activated workflow '{workflow_name}'")
            return True
        else:
            print(f"WARNING: Could not activate workflow (Status: {response.status_code})")
            return False
    except Exception as e:
        print(f"ERROR activating workflow: {e}")
        return False

def get_webhook_urls(session, base_url, workflow_id):
    """Get webhook URLs for workflow"""
    try:
        response = session.get(f"{base_url}/api/v1/workflows/{workflow_id}")
        if response.status_code == 200:
            workflow = response.json()
            webhook_urls = []

            # Look for webhook nodes
            for node in workflow.get('nodes', []):
                if node.get('type') == 'n8n-nodes-base.webhook':
                    path = node.get('parameters', {}).get('path', '')
                    if path:
                        webhook_url = f"{base_url}/webhook/{path}"
                        webhook_urls.append(webhook_url)

            return webhook_urls
        return []
    except Exception as e:
        print(f"ERROR getting webhook URLs: {e}")
        return []

def main():
    print("N8N WORKFLOW SETUP - API KEY AUTHENTICATION")
    print("=" * 50)

    # Load configuration
    config = load_n8n_config()
    print(f"Target: {config['host']}:{config['port']}")

    # Create session
    session, base_url = create_n8n_session(config)
    if not session:
        return

    # Test connection
    if not test_n8n_connection(session, base_url):
        return

    # List existing workflows
    existing_workflows = list_workflows(session, base_url)

    # Find workflow files to import
    workflows_dir = Path(__file__).parent.parent / "n8n" / "workflows"

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

    imported_workflows = []

    for workflow_info in workflows_to_import:
        workflow_file = workflows_dir / workflow_info["file"]

        if not workflow_file.exists():
            print(f"ERROR: File not found - {workflow_file}")
            continue

        # Check if workflow already exists
        existing_id = None
        for existing in existing_workflows:
            if existing.get('name') == workflow_info["name"]:
                existing_id = existing.get('id')
                print(f"Workflow '{workflow_info['name']}' already exists (ID: {existing_id})")
                break

        if existing_id:
            # Update existing workflow
            print(f"Updating existing workflow...")
            # For now, skip update and use existing
            imported_workflows.append({
                "id": existing_id,
                "name": workflow_info["name"]
            })
        else:
            # Import new workflow
            workflow_id = import_workflow(session, base_url, workflow_file, workflow_info["name"])
            if workflow_id:
                activate_workflow(session, base_url, workflow_id, workflow_info["name"])
                imported_workflows.append({
                    "id": workflow_id,
                    "name": workflow_info["name"]
                })

    # Show results
    print(f"\n{'='*50}")
    print(f"IMPORT COMPLETE: {len(imported_workflows)} workflows")

    if imported_workflows:
        print(f"\nACCESS N8N: {base_url}")
        print(f"Available workflows:")

        for wf in imported_workflows:
            webhook_urls = get_webhook_urls(session, base_url, wf["id"])
            print(f"\n  {wf['name']}:")
            if webhook_urls:
                for url in webhook_urls:
                    print(f"    Webhook: {url}")
            else:
                print(f"    No webhooks found")

        print(f"\nTest with curl:")
        if imported_workflows:
            first_wf_id = imported_workflows[0]["id"]
            webhook_urls = get_webhook_urls(session, base_url, first_wf_id)
            if webhook_urls:
                print(f"curl -X POST {webhook_urls[0]} \\")
                print('  -H "Content-Type: application/json" \\')
                print('  -d \'{"vsl_text": "Sua VSL de teste aqui..."}\'')

if __name__ == "__main__":
    main()
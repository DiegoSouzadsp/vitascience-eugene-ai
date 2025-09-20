#!/usr/bin/env python3
"""
Clean up duplicate N8N workflows
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
    print("N8N WORKFLOW CLEANUP")
    print("=" * 25)

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
        print(f"Found {len(workflows)} workflows")

        # Group by name
        workflow_groups = {}
        for wf in workflows:
            name = wf.get('name', 'Unknown')
            if name not in workflow_groups:
                workflow_groups[name] = []
            workflow_groups[name].append(wf)

        # Keep newest workflow for each name, delete the rest
        for name, group in workflow_groups.items():
            if len(group) > 1:
                print(f"\nFound {len(group)} workflows named '{name}'")

                # Sort by creation date, keep the newest
                group.sort(key=lambda x: x.get('createdAt', ''), reverse=True)
                newest = group[0]
                duplicates = group[1:]

                print(f"Keeping newest: {newest.get('id')} (created {newest.get('createdAt', 'unknown')})")

                for duplicate in duplicates:
                    dup_id = duplicate.get('id')
                    created = duplicate.get('createdAt', 'unknown')
                    print(f"Deleting duplicate: {dup_id} (created {created})")

                    # Delete duplicate
                    delete_response = session.delete(f"{base_url}/api/v1/workflows/{dup_id}")
                    if delete_response.status_code == 200:
                        print(f"  SUCCESS: Deleted {dup_id}")
                    else:
                        print(f"  ERROR: Could not delete {dup_id} - {delete_response.status_code}")

                # Ensure the kept workflow is active
                if not newest.get('active', False):
                    print(f"Activating {name}...")
                    activate_response = session.post(f"{base_url}/api/v1/workflows/{newest.get('id')}/activate")
                    if activate_response.status_code == 200:
                        print(f"  SUCCESS: Activated {name}")
                    else:
                        print(f"  ERROR: Could not activate - {activate_response.status_code}")

        print(f"\nCleanup completed. Checking final status...")

        # List final workflows
        final_response = session.get(f"{base_url}/api/v1/workflows")
        if final_response.status_code == 200:
            final_workflows = final_response.json().get('data', [])
            print(f"\nFinal workflow count: {len(final_workflows)}")

            for wf in final_workflows:
                name = wf.get('name', 'Unknown')
                wf_id = wf.get('id', 'Unknown')
                active = wf.get('active', False)
                status = "ACTIVE" if active else "INACTIVE"
                print(f"  - {name} (ID: {wf_id}) [{status}]")

        print(f"\nN8N Interface: {base_url}")
        print(f"Try restarting N8N if webhooks still don't work")

if __name__ == "__main__":
    main()
#!/usr/bin/env python3
"""
Setup N8N workflows - Simple version
"""

import requests
import json
from pathlib import Path
import time

def check_n8n():
    """Check N8N connection"""
    try:
        response = requests.get(
            "http://localhost:5678/api/v1/workflows",
            auth=("admin", "password"),
            timeout=10
        )
        return response.status_code == 200
    except:
        return False

def wait_for_n8n():
    """Wait for N8N to be ready"""
    print("Waiting for N8N to start...")
    for i in range(30):  # Wait up to 30 seconds
        if check_n8n():
            print("N8N is ready!")
            return True
        print(f"Waiting... ({i+1}/30)")
        time.sleep(1)
    return False

def import_workflow(workflow_file, name):
    """Import workflow to N8N"""
    try:
        with open(workflow_file, 'r', encoding='utf-8') as f:
            workflow_data = json.load(f)

        response = requests.post(
            "http://localhost:5678/api/v1/workflows",
            json=workflow_data,
            auth=("admin", "password")
        )

        if response.status_code == 201:
            print(f"SUCCESS: Imported {name}")
            return True
        else:
            print(f"FAILED: {name} - Status: {response.status_code}")
            return False
    except Exception as e:
        print(f"ERROR importing {name}: {e}")
        return False

def main():
    print("N8N WORKFLOWS SETUP")
    print("=" * 30)

    # Wait for N8N
    if not wait_for_n8n():
        print("ERROR: N8N not accessible")
        print("Try: docker-compose up -d n8n")
        return

    # Import workflows
    workflows_dir = Path(__file__).parent.parent / "n8n" / "workflows"

    workflows = [
        ("eugene_vsl_analyzer.json", "Eugene VSL Analyzer"),
        ("vitascience_integration.json", "Vitascience Integration")
    ]

    success = 0
    for file, name in workflows:
        workflow_path = workflows_dir / file
        if workflow_path.exists():
            if import_workflow(workflow_path, name):
                success += 1
        else:
            print(f"NOT FOUND: {file}")

    print(f"\nRESULT: {success}/{len(workflows)} workflows imported")

    if success > 0:
        print("\nACCESS: http://localhost:5678 (admin/password)")
        print("WEBHOOK: http://localhost:5678/webhook/analyze-vsl")

if __name__ == "__main__":
    main()
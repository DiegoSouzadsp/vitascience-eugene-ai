#!/usr/bin/env python3
"""
Setup N8N workflows automatically via API
Creates Eugene Schwartz VSL analyzer workflows in N8N
"""

import requests
import json
from pathlib import Path
import time

def check_n8n_connection():
    """Check if N8N is accessible"""
    try:
        response = requests.get(
            "http://localhost:5678/api/v1/workflows",
            auth=("admin", "password"),
            timeout=10
        )
        if response.status_code == 200:
            print("✅ N8N API connection successful")
            return True
        else:
            print(f"❌ N8N API error: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ N8N connection failed: {e}")
        return False

def import_workflow(workflow_file_path, workflow_name):
    """Import a workflow JSON file to N8N"""
    try:
        # Read workflow JSON
        with open(workflow_file_path, 'r', encoding='utf-8') as f:
            workflow_data = json.load(f)

        # Check if workflow already exists
        existing_response = requests.get(
            "http://localhost:5678/api/v1/workflows",
            auth=("admin", "password")
        )

        if existing_response.status_code == 200:
            existing_workflows = existing_response.json()
            for workflow in existing_workflows.get('data', []):
                if workflow.get('name') == workflow_name:
                    print(f"⚠️  Workflow '{workflow_name}' already exists")
                    # Update existing workflow
                    update_response = requests.put(
                        f"http://localhost:5678/api/v1/workflows/{workflow['id']}",
                        json=workflow_data,
                        auth=("admin", "password")
                    )
                    if update_response.status_code == 200:
                        print(f"✅ Updated workflow: {workflow_name}")
                        return True
                    else:
                        print(f"❌ Failed to update workflow: {update_response.status_code}")
                        return False

        # Create new workflow
        response = requests.post(
            "http://localhost:5678/api/v1/workflows",
            json=workflow_data,
            auth=("admin", "password")
        )

        if response.status_code == 201:
            print(f"✅ Created workflow: {workflow_name}")
            return True
        else:
            print(f"❌ Failed to create workflow: {response.status_code}")
            print(f"Response: {response.text}")
            return False

    except Exception as e:
        print(f"❌ Error importing workflow {workflow_name}: {e}")
        return False

def activate_workflow(workflow_name):
    """Activate a workflow in N8N"""
    try:
        # Get workflow ID by name
        response = requests.get(
            "http://localhost:5678/api/v1/workflows",
            auth=("admin", "password")
        )

        if response.status_code != 200:
            print(f"❌ Failed to get workflows: {response.status_code}")
            return False

        workflows = response.json()
        workflow_id = None

        for workflow in workflows.get('data', []):
            if workflow.get('name') == workflow_name:
                workflow_id = workflow.get('id')
                break

        if not workflow_id:
            print(f"❌ Workflow '{workflow_name}' not found")
            return False

        # Activate workflow
        activation_response = requests.post(
            f"http://localhost:5678/api/v1/workflows/{workflow_id}/activate",
            auth=("admin", "password")
        )

        if activation_response.status_code == 200:
            print(f"✅ Activated workflow: {workflow_name}")
            return True
        else:
            print(f"❌ Failed to activate workflow: {activation_response.status_code}")
            return False

    except Exception as e:
        print(f"❌ Error activating workflow {workflow_name}: {e}")
        return False

def main():
    """Main setup function"""
    print("🔧 N8N WORKFLOWS SETUP - EUGENE SCHWARTZ VSL ANALYZER")
    print("=" * 60)

    # Check N8N connection
    if not check_n8n_connection():
        print("\n❌ N8N is not accessible. Please ensure:")
        print("1. N8N is running: docker-compose up -d")
        print("2. N8N is accessible at: http://localhost:5678")
        print("3. Credentials: admin/password")
        return

    # Define workflows to import
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

    print(f"\n📁 Looking for workflows in: {workflows_dir}")

    if not workflows_dir.exists():
        print(f"❌ Workflows directory not found: {workflows_dir}")
        return

    success_count = 0
    total_workflows = len(workflows_to_import)

    # Import each workflow
    for workflow_info in workflows_to_import:
        workflow_file = workflows_dir / workflow_info["file"]

        if not workflow_file.exists():
            print(f"❌ Workflow file not found: {workflow_file}")
            continue

        print(f"\n🔄 Importing: {workflow_info['name']}")
        print(f"   File: {workflow_info['file']}")

        if import_workflow(workflow_file, workflow_info["name"]):
            # Wait a moment then activate
            time.sleep(1)
            if activate_workflow(workflow_info["name"]):
                success_count += 1

    # Final summary
    print(f"\n📊 IMPORT SUMMARY")
    print(f"Successful imports: {success_count}/{total_workflows}")

    if success_count == total_workflows:
        print("\n🎉 ALL WORKFLOWS IMPORTED SUCCESSFULLY!")
        print("\n🔗 Access your workflows:")
        print("   N8N Interface: http://localhost:5678")
        print("   Login: admin / password")

        print("\n🚀 Available endpoints:")
        print("   Complete Analysis: POST http://localhost:5678/webhook/analyze-vsl")
        print("   Vitascience API: POST http://localhost:5678/webhook/vitascience/analyze")

        print("\n💡 Test with curl:")
        print('   curl -X POST http://localhost:5678/webhook/analyze-vsl \\')
        print('   -H "Content-Type: application/json" \\')
        print('   -d \'{"vsl_text": "Your VSL text here..."}\'')

    else:
        print(f"\n⚠️  {total_workflows - success_count} workflows failed to import")
        print("Check the errors above and try again")

if __name__ == "__main__":
    main()
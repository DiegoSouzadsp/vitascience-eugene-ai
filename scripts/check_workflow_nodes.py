#!/usr/bin/env python3
"""
Check N8N workflow node details
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
    print("VERIFICACAO DE NOS DOS WORKFLOWS N8N")
    print("=" * 40)

    config = load_n8n_config()
    base_url = f"http://{config['host']}:{config['port']}"

    session = requests.Session()
    session.headers.update({
        "X-N8N-API-KEY": config["api_key"],
        "Content-Type": "application/json"
    })

    # List all workflows
    response = session.get(f"{base_url}/api/v1/workflows")
    if response.status_code != 200:
        print(f"ERRO: Nao foi possivel conectar - Status {response.status_code}")
        return

    workflows = response.json().get('data', [])

    for wf in workflows:
        if 'eugene' in wf.get('name', '').lower() or 'vitascience' in wf.get('name', '').lower():
            name = wf.get('name')
            wf_id = wf.get('id')

            print(f"\nWorkflow: {name}")
            print(f"ID: {wf_id}")

            # Get detailed workflow info
            details_response = session.get(f"{base_url}/api/v1/workflows/{wf_id}")
            if details_response.status_code == 200:
                workflow_details = details_response.json()
                nodes = workflow_details.get('nodes', [])

                print(f"Quantidade de nos: {len(nodes)}")
                print("Nos:")

                for i, node in enumerate(nodes, 1):
                    node_name = node.get('name', 'Sem nome')
                    node_type = node.get('type', 'Tipo desconhecido')
                    print(f"  {i}. {node_name} ({node_type})")

                    # Special info for webhook nodes
                    if 'webhook' in node_type:
                        path = node.get('parameters', {}).get('path', '')
                        method = node.get('parameters', {}).get('httpMethod', 'GET')
                        if path:
                            print(f"     Webhook: {method} /{path}")

                # Show connections
                connections = workflow_details.get('connections', {})
                print("Conexoes:")
                for source_node, connections_data in connections.items():
                    if 'main' in connections_data:
                        for connection_group in connections_data['main']:
                            for connection in connection_group:
                                target_node = connection.get('node', '')
                                print(f"  {source_node} -> {target_node}")
            print("-" * 40)

if __name__ == "__main__":
    main()
#!/usr/bin/env python3
"""
Script para configurar credenciais no N8N localhost
"""

import requests
import json

# Chaves das APIs (dos arquivos docs/)
ANTHROPIC_API_KEY = "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"
OPENAI_API_KEY = "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"
N8N_API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJmMWFkN2I5MS00ZWZiLTQzMjAtOGE2Yy1jZjQ5NDQxYjIwY2UiLCJpc3MiOiJuOG4iLCJhdWQiOiJwdWJsaWMtYXBpIiwiaWF0IjoxNzU4Mzg0NTQ0LCJleHAiOjE3NjA5MzI4MDB9.w_V_Zi2OuFOLz1CEr6eGpjtpfQZ8AZeZdOX48p2h_6E"

def setup_n8n_credentials():
    """Configura as credenciais necessárias no N8N"""

    print("=" * 60)
    print("CONFIGURACAO CREDENCIAIS N8N LOCALHOST")
    print("=" * 60)

    # Credencial Anthropic
    anthropic_cred = {
        "name": "Anthropic API",
        "type": "anthropicApi",
        "data": {
            "apiKey": ANTHROPIC_API_KEY
        }
    }

    # Credencial OpenAI
    openai_cred = {
        "name": "OpenAI API",
        "type": "openAiApi",
        "data": {
            "apiKey": OPENAI_API_KEY
        }
    }

    print("Chaves carregadas dos arquivos docs/:")
    print(f"Anthropic: ...{ANTHROPIC_API_KEY[-20:]}")
    print(f"OpenAI: ...{OPENAI_API_KEY[-20:]}")
    print(f"N8N: ...{N8N_API_KEY[-20:]}")

    print("\n" + "=" * 60)
    print("INSTRUCOES MANUAIS (N8N nao permite API para credenciais)")
    print("=" * 60)

    print("1. Acesse: http://localhost:5678")
    print("2. Vá em: Settings > Credentials")
    print("3. Clique: 'Add Credential'")
    print("4. Crie as seguintes credenciais:")

    print("\n" + "-" * 40)
    print("CREDENCIAL 1: ANTHROPIC")
    print("-" * 40)
    print("Tipo: Anthropic")
    print("Nome: 'Anthropic API'")
    print(f"API Key: {ANTHROPIC_API_KEY}")

    print("\n" + "-" * 40)
    print("CREDENCIAL 2: OPENAI (Opcional)")
    print("-" * 40)
    print("Tipo: OpenAI")
    print("Nome: 'OpenAI API'")
    print(f"API Key: {OPENAI_API_KEY}")

    print("\n" + "=" * 60)
    print("DEPOIS DE CONFIGURAR:")
    print("=" * 60)
    print("1. Importe o workflow otimizado:")
    print("   n8n/workflows/eugene_vsl_analyzer_optimized.json")
    print("2. Configure as credenciais nos nodes Anthropic")
    print("3. Ative o workflow")
    print("4. Teste com: python scripts/test_optimized_workflow.py")

if __name__ == "__main__":
    setup_n8n_credentials()
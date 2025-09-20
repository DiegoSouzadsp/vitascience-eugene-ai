#!/usr/bin/env python3
"""
Configuração e Teste do Workflow Squad Vitascience
Script para configurar credenciais OpenAI e testar o workflow N8N final
"""

import requests
import json
import os
import sys
from datetime import datetime

# Configurações
N8N_BASE_URL = "http://localhost:5678"
WEBHOOK_PATH = "/webhook/analyze-vsl-squad"
WORKFLOW_FILE = "n8n/workflows/eugene_vsl_analyzer_squad_final.json"

# Chave OpenAI do Squad
OPENAI_API_KEY = "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"

def check_n8n_status():
    """Verifica se N8N está rodando"""
    try:
        response = requests.get(f"{N8N_BASE_URL}/healthz", timeout=5)
        if response.status_code == 200:
            print("OK - N8N está rodando")
            return True
        else:
            print(f"ERRO - N8N não está respondendo (status: {response.status_code})")
            return False
    except Exception as e:
        print(f"ERRO - ao conectar com N8N: {e}")
        return False

def configure_openai_credentials():
    """Configura credenciais OpenAI no N8N"""
    print("\nConfigurando credenciais OpenAI...")

    # Dados da credencial
    credential_data = {
        "name": "OpenAI Squad Credentials",
        "type": "openAiApi",
        "data": {
            "apiKey": OPENAI_API_KEY
        }
    }

    try:
        # Login básico (N8N padrão)
        auth = ('admin', 'password')

        # Criar/atualizar credencial
        response = requests.post(
            f"{N8N_BASE_URL}/rest/credentials",
            json=credential_data,
            auth=auth,
            headers={'Content-Type': 'application/json'}
        )

        if response.status_code in [200, 201]:
            print("OK - Credenciais OpenAI configuradas com sucesso")
            return True
        else:
            print(f"ERRO - ao configurar credenciais: {response.status_code}")
            print(f"Resposta: {response.text}")
            return False

    except Exception as e:
        print(f"ERRO - ao configurar credenciais: {e}")
        return False

def import_workflow():
    """Importa o workflow final para o N8N"""
    print("\nImportando workflow Squad Vitascience...")

    try:
        # Carregar workflow JSON
        with open(WORKFLOW_FILE, 'r', encoding='utf-8') as f:
            workflow_data = json.load(f)

        # Login básico
        auth = ('admin', 'password')

        # Importar workflow
        response = requests.post(
            f"{N8N_BASE_URL}/rest/workflows",
            json=workflow_data,
            auth=auth,
            headers={'Content-Type': 'application/json'}
        )

        if response.status_code in [200, 201]:
            print("OK - Workflow importado com sucesso")
            workflow_id = response.json().get('id')
            print(f"Workflow ID: {workflow_id}")

            # Ativar workflow
            activate_response = requests.patch(
                f"{N8N_BASE_URL}/rest/workflows/{workflow_id}",
                json={"active": True},
                auth=auth,
                headers={'Content-Type': 'application/json'}
            )

            if activate_response.status_code == 200:
                print("OK - Workflow ativado com sucesso")
                return workflow_id
            else:
                print("AVISO - Workflow importado mas não ativado")
                return workflow_id

        else:
            print(f"ERRO - ao importar workflow: {response.status_code}")
            print(f"Resposta: {response.text}")
            return None

    except Exception as e:
        print(f"ERRO - ao importar workflow: {e}")
        return None

def test_webhook():
    """Testa o webhook com dados de exemplo"""
    print("\nTestando webhook com VSL de exemplo...")

    # VSL de teste
    test_vsl = """
    DESCOBERTA MÉDICA REVOLUCIONA TRATAMENTO NATURAL!

    Se você sofre com dores nas articulações, fadiga crônica ou inflamação,
    esta descoberta científica vai mudar sua vida para sempre.

    Depois de 15 anos de pesquisa, cientistas da Universidade de Harvard
    descobriram um composto natural que elimina a inflamação em apenas 30 dias.

    Diferente de todos os tratamentos que você já tentou, este método ataca
    a causa raiz do problema, não apenas os sintomas.

    Mais de 47.000 pessoas já experimentaram resultados extraordinários:
    - 89% relataram redução significativa da dor
    - 94% sentiram mais energia e disposição
    - 76% eliminaram completamente a inflamação

    Mas atenção: devido à alta demanda, temos apenas 500 unidades disponíveis
    neste mês. Depois disso, você terá que entrar na lista de espera.

    Clique agora e garante sua transformação ainda hoje!
    """

    test_data = {
        "vsl_text": test_vsl,
        "options": {
            "detailed_analysis": True,
            "include_frameworks": True,
            "min_problems": 5,
            "min_angles": 3
        }
    }

    try:
        print("Enviando requisição para webhook...")
        response = requests.post(
            f"{N8N_BASE_URL}{WEBHOOK_PATH}",
            json=test_data,
            headers={'Content-Type': 'application/json'},
            timeout=120  # 2 minutos timeout
        )

        if response.status_code == 200:
            print("OK - Teste do webhook executado com sucesso!")

            # Salvar resultado
            result = response.json()
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            result_file = f"tests/squad_test_result_{timestamp}.json"

            os.makedirs("tests", exist_ok=True)
            with open(result_file, 'w', encoding='utf-8') as f:
                json.dump(result, f, indent=2, ensure_ascii=False)

            print(f"Resultado salvo em: {result_file}")

            # Mostrar resumo
            if 'summary' in result:
                summary = result['summary']
                print(f"Score Geral: {summary.get('score_geral', 'N/A')}")
                print(f"Nível Consciência: {summary.get('nivel_consciencia', 'N/A')}")
                print(f"Framework: {summary.get('framework_principal', 'N/A')}")
                print(f"Problemas Identificados: {summary.get('total_problemas', 'N/A')}")
                print(f"Ângulos Sugeridos: {summary.get('total_angulos', 'N/A')}")

            return True

        else:
            print(f"ERRO - Teste falhou com status: {response.status_code}")
            print(f"Resposta: {response.text}")
            return False

    except Exception as e:
        print(f"ERRO - no teste: {e}")
        return False

def main():
    """Função principal de configuração"""
    print("CONFIGURACAO WORKFLOW SQUAD VITASCIENCE")
    print("=" * 50)

    # 1. Verificar N8N
    print("\n1. Verificando N8N...")
    if not check_n8n_status():
        print("\nERRO - N8N não está acessível. Verifique se está rodando em localhost:5678")
        print("Para iniciar: docker-compose up -d")
        sys.exit(1)

    # 2. Configurar credenciais
    print("\n2. Configurando credenciais...")
    if not configure_openai_credentials():
        print("\nAVISO - Não foi possível configurar credenciais automaticamente.")
        print("Configure manualmente no N8N:")
        print("1. Acesse Settings > Credentials")
        print("2. Crie nova credencial 'OpenAI'")
        print("3. Nome: 'OpenAI Squad Credentials'")
        print(f"4. API Key: {OPENAI_API_KEY[:20]}...")

    # 3. Importar workflow
    print("\n3. Importando workflow...")
    workflow_id = import_workflow()
    if not workflow_id:
        print("\nERRO - Não foi possível importar o workflow")
        sys.exit(1)

    # 4. Testar webhook
    print("\n4. Testando funcionamento...")
    if test_webhook():
        print("\n" + "="*50)
        print("CONFIGURACAO CONCLUIDA COM SUCESSO!")
        print(f"Webhook URL: {N8N_BASE_URL}{WEBHOOK_PATH}")
        print("Para usar, envie POST com:")
        print('   {"vsl_text": "sua VSL aqui"}')
        print("="*50)
    else:
        print("\nAVISO - Configuração completa, mas teste falhou")
        print("Verifique as credenciais OpenAI no N8N")

if __name__ == "__main__":
    main()
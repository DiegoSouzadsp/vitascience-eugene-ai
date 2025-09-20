#!/usr/bin/env python3
"""
Script para testar o webhook N8N com VSL real
Converte arquivo VSL para JSON e envia para o webhook
"""

import json
import requests
import sys
from pathlib import Path
from datetime import datetime

def load_vsl_content(file_path: str) -> str:
    """Carrega conteúdo do VSL do arquivo"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Remove marcações markdown se necessário
        content = content.replace('# **', '').replace('**', '')
        content = content.replace('![][image', '[IMAGE')
        content = content.replace('---', '')

        # Limpa conteúdo extra
        lines = [line.strip() for line in content.split('\n') if line.strip()]
        clean_content = '\n'.join(lines)

        return clean_content
    except Exception as e:
        print(f"Erro ao carregar VSL: {e}")
        return ""

def send_to_n8n_webhook(vsl_content: str, webhook_url: str) -> dict:
    """Envia VSL para webhook N8N"""

    payload = {
        "vsl_text": vsl_content,
        "analysis_type": "complete",
        "timestamp": datetime.now().isoformat(),
        "source": "vitascience_test",
        "metadata": {
            "content_length": len(vsl_content),
            "analysis_requested": "eugene_schwartz_5_levels"
        }
    }

    headers = {
        'Content-Type': 'application/json',
        'User-Agent': 'VitascienceTest/1.0'
    }

    try:
        print(f"Enviando VSL para: {webhook_url}")
        print(f"Tamanho do conteúdo: {len(vsl_content)} caracteres")

        response = requests.post(
            webhook_url,
            json=payload,
            headers=headers,
            timeout=120  # 2 minutos timeout
        )

        print(f"Status: {response.status_code}")

        if response.status_code == 200:
            return response.json()
        else:
            print(f"Erro na resposta: {response.text}")
            return {"error": f"HTTP {response.status_code}", "details": response.text}

    except requests.exceptions.Timeout:
        return {"error": "Timeout", "details": "Webhook demorou mais que 2 minutos"}
    except Exception as e:
        return {"error": "Request failed", "details": str(e)}

def main():
    """Função principal"""

    # Configurações
    VSL_FILE = "docs/[Vitascience] Material para Teste Prático.md"
    N8N_WEBHOOK = "http://192.168.1.64:5678/webhook-test/vitascience/analyze"

    # Permite override via argumentos
    if len(sys.argv) > 1:
        VSL_FILE = sys.argv[1]
    if len(sys.argv) > 2:
        N8N_WEBHOOK = sys.argv[2]

    print("=" * 60)
    print("TESTE VSL WEBHOOK N8N - VITASCIENCE EUGENE AI")
    print("=" * 60)
    print(f"Arquivo VSL: {VSL_FILE}")
    print(f"Webhook N8N: {N8N_WEBHOOK}")
    print("-" * 60)

    # Verifica se arquivo existe
    if not Path(VSL_FILE).exists():
        print(f"ERRO: Arquivo não encontrado: {VSL_FILE}")
        return

    # Carrega VSL
    print("Carregando conteúdo do VSL...")
    vsl_content = load_vsl_content(VSL_FILE)

    if not vsl_content:
        print("ERRO: Falha ao carregar VSL")
        return

    # Preview do conteúdo
    preview = vsl_content[:200] + "..." if len(vsl_content) > 200 else vsl_content
    print(f"Preview: {preview}")
    print("-" * 60)

    # Envia para N8N
    print("Enviando para N8N...")
    result = send_to_n8n_webhook(vsl_content, N8N_WEBHOOK)

    # Exibe resultado
    print("=" * 60)
    print("RESULTADO:")
    print("=" * 60)

    if "error" in result:
        print(f"ERRO: {result['error']}")
        print(f"Detalhes: {result['details']}")
    else:
        print("SUCESSO!")
        print(json.dumps(result, indent=2, ensure_ascii=False))

    print("=" * 60)

    # Salva resultado
    output_file = f"tests/webhook_test_result_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    Path("tests").mkdir(exist_ok=True)

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump({
            "timestamp": datetime.now().isoformat(),
            "vsl_file": VSL_FILE,
            "webhook_url": N8N_WEBHOOK,
            "vsl_content_length": len(vsl_content),
            "result": result
        }, f, indent=2, ensure_ascii=False)

    print(f"Resultado salvo em: {output_file}")

if __name__ == "__main__":
    main()
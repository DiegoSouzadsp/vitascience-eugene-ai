#!/usr/bin/env python3
"""
Verificação de Setup - Squad Vitascience
Script para verificar se tudo está configurado corretamente
"""

import requests
import json
import os
import subprocess
import sys
from pathlib import Path

class SquadSetupVerifier:
    def __init__(self):
        self.base_path = Path(__file__).parent.parent
        self.n8n_url = "http://localhost:5678"
        self.webhook_url = f"{self.n8n_url}/webhook/analyze-vsl-squad"
        self.results = []

    def check_item(self, description: str, condition: bool, details: str = "") -> bool:
        """Verifica um item e adiciona ao relatório"""
        status = "✅" if condition else "❌"
        self.results.append({
            "description": description,
            "status": condition,
            "details": details
        })
        print(f"{status} {description}")
        if details and not condition:
            print(f"   📋 {details}")
        return condition

    def check_n8n_running(self) -> bool:
        """Verifica se N8N está rodando"""
        try:
            response = requests.get(f"{self.n8n_url}/api/v1/active", timeout=5)
            return response.status_code == 200
        except:
            return False

    def check_openai_key(self) -> bool:
        """Verifica se a chave OpenAI está configurada"""
        key_file = self.base_path / "docs" / "Chave OpenAi.txt"
        if not key_file.exists():
            return False

        try:
            with open(key_file, 'r') as f:
                key = f.read().strip()
            return key.startswith('sk-') and len(key) > 20
        except:
            return False

    def check_workflow_file(self) -> bool:
        """Verifica se o arquivo do workflow existe"""
        workflow_file = self.base_path / "n8n" / "workflows" / "eugene_vsl_analyzer_squad_optimized.json"
        return workflow_file.exists()

    def check_webhook_endpoint(self) -> bool:
        """Verifica se o webhook está ativo"""
        try:
            # Tenta fazer POST com dados mínimos
            test_data = {"vsl_text": "Test VSL content for verification"}
            response = requests.post(
                self.webhook_url,
                json=test_data,
                timeout=10
            )
            # Aceita qualquer resposta (erro de validação é OK, significa que está ativo)
            return response.status_code in [200, 400, 500]
        except:
            return False

    def check_required_directories(self) -> bool:
        """Verifica se os diretórios necessários existem"""
        required_dirs = [
            "n8n",
            "n8n/workflows",
            "tests",
            "scripts",
            "docs"
        ]

        all_exist = True
        for dir_name in required_dirs:
            dir_path = self.base_path / dir_name
            if not dir_path.exists():
                all_exist = False
                print(f"   📁 Missing directory: {dir_name}")

        return all_exist

    def check_python_dependencies(self) -> bool:
        """Verifica se as dependências Python estão instaladas"""
        try:
            import requests
            return True
        except ImportError:
            return False

    def check_docker_running(self) -> bool:
        """Verifica se Docker está rodando (opcional)"""
        try:
            result = subprocess.run(['docker', 'ps'],
                                  capture_output=True, text=True, timeout=5)
            return result.returncode == 0
        except:
            return False

    def run_verification(self) -> bool:
        """Executa verificação completa"""
        print("🔍 VERIFICAÇÃO SETUP SQUAD VITASCIENCE")
        print("=" * 50)

        all_ok = True

        # Verificações críticas
        print("\n📋 VERIFICAÇÕES CRÍTICAS:")
        all_ok &= self.check_item(
            "Diretórios necessários",
            self.check_required_directories(),
            "Execute: mkdir -p n8n/workflows tests scripts docs"
        )

        all_ok &= self.check_item(
            "Arquivo workflow Squad",
            self.check_workflow_file(),
            "Workflow não encontrado em n8n/workflows/"
        )

        all_ok &= self.check_item(
            "Chave OpenAI configurada",
            self.check_openai_key(),
            "Configure chave em docs/Chave OpenAi.txt"
        )

        all_ok &= self.check_item(
            "Python requests instalado",
            self.check_python_dependencies(),
            "Execute: pip install requests"
        )

        # Verificações N8N
        print("\n🔧 VERIFICAÇÕES N8N:")
        n8n_running = self.check_n8n_running()
        all_ok &= self.check_item(
            "N8N rodando (localhost:5678)",
            n8n_running,
            "Inicie N8N: npm run start ou docker-compose up"
        )

        if n8n_running:
            webhook_active = self.check_webhook_endpoint()
            all_ok &= self.check_item(
                "Webhook Squad ativo",
                webhook_active,
                "Importe workflow em N8N e ative"
            )
        else:
            self.check_item(
                "Webhook Squad ativo",
                False,
                "N8N não está rodando"
            )

        # Verificações opcionais
        print("\n⚙️ VERIFICAÇÕES OPCIONAIS:")
        self.check_item(
            "Docker disponível",
            self.check_docker_running(),
            "Docker não é obrigatório para este setup"
        )

        # Relatório final
        print("\n" + "=" * 50)
        if all_ok:
            print("🎉 SETUP SQUAD VITASCIENCE: PRONTO!")
            print("✅ Todos os componentes críticos estão funcionando")
            print(f"🚀 Webhook disponível: {self.webhook_url}")
        else:
            print("⚠️ SETUP INCOMPLETO - Resolva os problemas acima")
            print("📋 Execute os comandos sugeridos e execute novamente")

        return all_ok

    def generate_setup_commands(self):
        """Gera comandos para resolver problemas"""
        print("\n🛠️ COMANDOS PARA RESOLVER PROBLEMAS:")
        print("-" * 40)

        if not self.check_n8n_running():
            print("# Iniciar N8N:")
            print("cd n8n && npm run start")
            print("# OU usando Docker:")
            print("docker-compose up -d")

        if not self.check_openai_key():
            print("\n# Configurar chave OpenAI:")
            print("echo 'sua_chave_openai_aqui' > docs/Chave OpenAi.txt")

        if not self.check_python_dependencies():
            print("\n# Instalar dependências Python:")
            print("pip install requests")

        print("\n# Verificar novamente:")
        print("python scripts/verify_squad_setup.py")

def main():
    verifier = SquadSetupVerifier()

    success = verifier.run_verification()

    if not success:
        verifier.generate_setup_commands()
        sys.exit(1)
    else:
        print("\n🎯 Próximos passos:")
        print("1. Importe o workflow em N8N (se ainda não fez)")
        print("2. Configure credenciais OpenAI no N8N")
        print("3. Execute teste: python tests/test_squad_workflow.py")
        sys.exit(0)

if __name__ == "__main__":
    main()
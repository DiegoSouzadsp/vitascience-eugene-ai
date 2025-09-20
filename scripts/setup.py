#!/usr/bin/env python3
"""
Setup script for Eugene Schwartz VSL Analyzer
Initializes the complete system with database, RAG, and N8N workflows
"""

import os
import sys
import asyncio
import subprocess
import time
import requests
import json
from pathlib import Path

# Add src to Python path
sys.path.append(str(Path(__file__).parent.parent / "src"))

def print_step(step, message):
    """Print formatted setup step"""
    print(f"\n{'='*60}")
    print(f"STEP {step}: {message}")
    print(f"{'='*60}")

def run_command(command, cwd=None):
    """Run shell command and return result"""
    try:
        result = subprocess.run(
            command,
            shell=True,
            check=True,
            capture_output=True,
            text=True,
            cwd=cwd
        )
        return True, result.stdout
    except subprocess.CalledProcessError as e:
        return False, e.stderr

def wait_for_service(url, timeout=60, interval=5):
    """Wait for service to be available"""
    print(f"Waiting for service at {url}...")

    for i in range(0, timeout, interval):
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                print(f"✅ Service available at {url}")
                return True
        except requests.exceptions.RequestException:
            pass

        print(f"⏳ Waiting... ({i+interval}/{timeout}s)")
        time.sleep(interval)

    print(f"❌ Service at {url} not available after {timeout}s")
    return False

def setup_environment():
    """Setup environment variables"""
    print_step(1, "Setting up environment")

    env_file = Path(__file__).parent.parent / ".env"

    if not env_file.exists():
        print("❌ .env file not found. Please create it based on .env.example")
        return False

    print("✅ Environment file found")
    return True

def setup_docker():
    """Setup Docker containers"""
    print_step(2, "Setting up Docker containers")

    project_root = Path(__file__).parent.parent

    # Stop any existing containers
    print("Stopping existing containers...")
    run_command("docker-compose down", cwd=project_root)

    # Build and start containers
    print("Building and starting containers...")
    success, output = run_command("docker-compose up -d --build", cwd=project_root)

    if not success:
        print(f"❌ Failed to start Docker containers: {output}")
        return False

    print("✅ Docker containers started")
    return True

def verify_services():
    """Verify all services are running"""
    print_step(3, "Verifying services")

    services = [
        ("PostgreSQL", "http://localhost:5432", False),  # PostgreSQL doesn't have HTTP endpoint
        ("RAG API", "http://localhost:8000/health", True),
        ("N8N", "http://localhost:5678", True),
        ("Redis", "http://localhost:6379", False)  # Redis doesn't have HTTP endpoint
    ]

    all_good = True

    for service_name, url, check_http in services:
        if check_http:
            if not wait_for_service(url, timeout=120):
                all_good = False
        else:
            print(f"ℹ️  {service_name} - Manual verification required")

    return all_good

async def setup_database():
    """Setup database with RAG system"""
    print_step(4, "Setting up RAG database")

    try:
        from rag_system import EugeneRAGSystem

        # Initialize RAG system
        rag = EugeneRAGSystem()

        # Setup database
        setup_success = await rag.setup_database()
        if not setup_success:
            print("❌ Failed to setup RAG database")
            return False

        # Check health
        health = await rag.health_check()
        if health.get('status') == 'healthy':
            print("✅ RAG database setup completed")
            print(f"📊 Total chunks: {health.get('total_chunks', 0)}")
            return True
        else:
            print(f"❌ RAG system unhealthy: {health}")
            return False

    except Exception as e:
        print(f"❌ Error setting up database: {e}")
        return False

def setup_n8n_workflows():
    """Import N8N workflows"""
    print_step(5, "Setting up N8N workflows")

    # Wait for N8N to be ready
    if not wait_for_service("http://localhost:5678", timeout=60):
        print("❌ N8N service not available")
        return False

    # Import workflows
    workflows_dir = Path(__file__).parent.parent / "n8n" / "workflows"

    if not workflows_dir.exists():
        print("❌ N8N workflows directory not found")
        return False

    # List workflow files
    workflow_files = list(workflows_dir.glob("*.json"))

    if not workflow_files:
        print("❌ No workflow files found")
        return False

    print(f"📁 Found {len(workflow_files)} workflow files:")
    for wf in workflow_files:
        print(f"  - {wf.name}")

    print("ℹ️  To import workflows:")
    print("1. Open http://localhost:5678 (admin/password)")
    print("2. Go to Settings > Import from file")
    print("3. Import each workflow file from n8n/workflows/")

    return True

def verify_complete_system():
    """Run end-to-end system test"""
    print_step(6, "Running system verification")

    # Test RAG API
    try:
        response = requests.get("http://localhost:8000/health", timeout=10)
        if response.status_code == 200:
            print("✅ RAG API responding")
        else:
            print(f"❌ RAG API error: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ RAG API connection failed: {e}")
        return False

    # Test sample analysis
    try:
        sample_vsl = "Descubra o segredo que 95% dos médicos não querem que você saiba sobre diabetes..."

        analysis_data = {
            "vsl_text": sample_vsl,
            "analysis_type": "consciousness",
            "include_context": True
        }

        response = requests.post(
            "http://localhost:8000/analyze/consciousness",
            json=analysis_data,
            timeout=30
        )

        if response.status_code == 200:
            result = response.json()
            print(f"✅ Sample analysis completed")
            print(f"   Consciousness level: {result.get('nivel_identificado', 'N/A')}")
            print(f"   Confidence: {result.get('confianca', 'N/A')}")
        else:
            print(f"❌ Analysis failed: {response.status_code}")
            return False

    except Exception as e:
        print(f"❌ Analysis test failed: {e}")
        return False

    return True

def print_success_summary():
    """Print success summary with next steps"""
    print("\n" + "="*60)
    print("🎉 EUGENE SCHWARTZ VSL ANALYZER - SETUP COMPLETE!")
    print("="*60)

    print("\n📊 SERVICES RUNNING:")
    print("• PostgreSQL (pgvector): http://localhost:5432")
    print("• RAG API: http://localhost:8000")
    print("• N8N Workflows: http://localhost:5678")
    print("• Redis Cache: http://localhost:6379")

    print("\n🔗 ACCESS POINTS:")
    print("• API Documentation: http://localhost:8000/docs")
    print("• N8N Interface: http://localhost:5678 (admin/password)")
    print("• RAG Health Check: http://localhost:8000/health")

    print("\n🚀 NEXT STEPS:")
    print("1. Import N8N workflows from n8n/workflows/")
    print("2. Test VSL analysis: curl -X POST http://localhost:8000/analyze/consciousness \\")
    print("   -H 'Content-Type: application/json' \\")
    print("   -d '{\"vsl_text\":\"Your VSL text here\", \"analysis_type\":\"consciousness\"}'")
    print("3. Check documentation at http://localhost:8000/docs")

    print("\n💡 TROUBLESHOOTING:")
    print("• Logs: docker-compose logs -f")
    print("• Restart: docker-compose restart")
    print("• Health: curl http://localhost:8000/health")

async def main():
    """Main setup function"""
    print("🔧 EUGENE SCHWARTZ VSL ANALYZER - SETUP")
    print("Setting up complete system for Vitascience...")

    try:
        # Step 1: Environment
        if not setup_environment():
            sys.exit(1)

        # Step 2: Docker
        if not setup_docker():
            sys.exit(1)

        # Step 3: Verify services
        if not verify_services():
            print("⚠️  Some services may not be ready. Continuing...")

        # Wait a bit for services to fully start
        print("⏳ Waiting for services to fully initialize...")
        time.sleep(10)

        # Step 4: Database setup
        if not await setup_database():
            print("⚠️  Database setup issues. System may work with limited functionality.")

        # Step 5: N8N workflows
        if not setup_n8n_workflows():
            print("⚠️  N8N workflow setup incomplete. Manual import required.")

        # Step 6: System verification
        if not verify_complete_system():
            print("⚠️  System verification incomplete. Check logs for issues.")

        # Success summary
        print_success_summary()

    except KeyboardInterrupt:
        print("\n❌ Setup interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Setup failed with error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())
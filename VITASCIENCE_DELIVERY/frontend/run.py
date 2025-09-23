#!/usr/bin/env python3
"""
Production runner for Eugene Schwartz VSL Analyzer Frontend
"""

import os
import sys
from app import app

if __name__ == '__main__':
    # Environment configuration
    port = int(os.getenv('PORT', 8080))
    debug = os.getenv('DEBUG', 'False').lower() == 'true'
    host = os.getenv('HOST', '0.0.0.0')

    print("=" * 60)
    print("EUGENE SCHWARTZ VSL ANALYZER - FRONTEND")
    print("=" * 60)
    print(f"🚀 Starting server on {host}:{port}")
    print(f"🔧 Debug mode: {debug}")
    print(f"🌐 N8N Webhook: {os.getenv('N8N_WEBHOOK_URL', 'http://localhost:5678/webhook/analyze-vsl-squad')}")
    print("=" * 60)

    try:
        app.run(
            host=host,
            port=port,
            debug=debug,
            threaded=True
        )
    except KeyboardInterrupt:
        print("\n👋 Shutting down gracefully...")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        sys.exit(1)
#!/usr/bin/env python3
"""
Frontend Web Interface for Eugene Schwartz VSL Analyzer
Simple Flask-based interface that integrates with N8N workflow
"""

from flask import Flask, render_template, request, jsonify, flash, redirect, url_for
import requests
import json
import os
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'eugene-schwartz-vsl-analyzer-2024')

# Configuration
N8N_URL = os.getenv('N8N_URL', 'http://localhost:5678')
N8N_WEBHOOK_PATH = os.getenv('N8N_WEBHOOK_PATH', '/webhook/analyze-vsl-eugene-rag')
N8N_WEBHOOK_URL = f"{N8N_URL}{N8N_WEBHOOK_PATH}"
N8N_BASE_URL = N8N_URL

class VSLAnalyzer:
    """Interface for VSL analysis via N8N workflow"""

    def __init__(self):
        self.webhook_url = N8N_WEBHOOK_URL
        self.base_url = N8N_BASE_URL

    def analyze_vsl(self, vsl_text: str, analysis_type: str = 'complete') -> dict:
        """Send VSL to N8N workflow for analysis"""
        try:
            payload = {
                'vsl_text': vsl_text.strip(),
                'options': {
                    'detailed_analysis': True,
                    'dynamic_rag': True
                }
            }

            logger.info(f"Sending VSL analysis request to: {self.webhook_url}")

            response = requests.post(
                self.webhook_url,
                json=payload,
                timeout=120,
                headers={'Content-Type': 'application/json'}
            )

            response.raise_for_status()
            result = response.json()

            logger.info("VSL analysis completed successfully")
            return {
                'success': True,
                'data': result,
                'response_time': response.elapsed.total_seconds()
            }

        except requests.exceptions.Timeout:
            logger.error("Request timeout - analysis took too long")
            return {
                'success': False,
                'error': 'Análise demorou muito para completar. Tente novamente.',
                'error_type': 'timeout'
            }

        except requests.exceptions.ConnectionError:
            logger.error("Connection error - N8N workflow not available")
            return {
                'success': False,
                'error': 'Sistema de análise indisponível. Verifique se o N8N está rodando.',
                'error_type': 'connection'
            }

        except requests.exceptions.HTTPError as e:
            logger.error(f"HTTP error during analysis: {e}")
            return {
                'success': False,
                'error': f'Erro na análise: {e.response.status_code}',
                'error_type': 'http_error'
            }

        except Exception as e:
            logger.error(f"Unexpected error during analysis: {e}")
            return {
                'success': False,
                'error': f'Erro inesperado: {str(e)}',
                'error_type': 'unexpected'
            }

# Initialize analyzer
analyzer = VSLAnalyzer()

@app.route('/')
def index():
    """Main page with VSL input form"""
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    """Process VSL analysis request"""
    try:
        vsl_text = request.form.get('vsl_text', '').strip()
        analysis_type = request.form.get('analysis_type', 'complete')

        # Validation
        if not vsl_text:
            flash('Por favor, insira o texto do VSL para análise.', 'error')
            return redirect(url_for('index'))

        if len(vsl_text) < 100:
            flash('O texto do VSL deve ter pelo menos 100 caracteres.', 'error')
            return redirect(url_for('index'))

        # Perform analysis
        result = analyzer.analyze_vsl(vsl_text, analysis_type)

        if result['success']:
            return render_template('results.html',
                                 analysis=result['data'],
                                 response_time=result['response_time'],
                                 original_text=vsl_text)
        else:
            flash(f"Erro na análise: {result['error']}", 'error')
            return redirect(url_for('index'))

    except Exception as e:
        logger.error(f"Error in analyze route: {e}")
        flash(f"Erro interno: {str(e)}", 'error')
        return redirect(url_for('index'))

@app.route('/api/analyze', methods=['POST'])
def api_analyze():
    """API endpoint for VSL analysis"""
    try:
        data = request.get_json()

        if not data:
            return jsonify({
                'success': False,
                'error': 'JSON payload required'
            }), 400

        vsl_text = data.get('vsl_text', '').strip()
        analysis_type = data.get('analysis_type', 'complete')

        if not vsl_text:
            return jsonify({
                'success': False,
                'error': 'vsl_text field is required'
            }), 400

        if len(vsl_text) < 100:
            return jsonify({
                'success': False,
                'error': 'vsl_text must be at least 100 characters'
            }), 400

        # Perform analysis
        result = analyzer.analyze_vsl(vsl_text, analysis_type)

        if result['success']:
            return jsonify({
                'success': True,
                'data': result['data'],
                'response_time': result['response_time']
            })
        else:
            return jsonify({
                'success': False,
                'error': result['error'],
                'error_type': result.get('error_type', 'unknown')
            }), 500

    except Exception as e:
        logger.error(f"Error in API analyze: {e}")
        return jsonify({
            'success': False,
            'error': f'Internal server error: {str(e)}'
        }), 500

@app.route('/health')
def health():
    """Health check endpoint"""
    try:
        # Test N8N connectivity
        test_response = requests.get(f"{N8N_BASE_URL}/healthz", timeout=5)
        n8n_status = "healthy" if test_response.status_code == 200 else "unhealthy"
    except:
        n8n_status = "unreachable"

    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'n8n_status': n8n_status,
        'webhook_url': N8N_WEBHOOK_URL
    })

@app.route('/demo')
def demo():
    """Demo page with sample VSL"""
    try:
        # Carregar material de teste Vitascience
        with open('docs/[Vitascience] Material para Teste Prático.md', 'r', encoding='utf-8') as f:
            content = f.read()

        # Extrair apenas o texto da VSL (remover markdown e metadados)
        lines = content.split('\n')
        vsl_lines = []
        skip_line = False

        for line in lines:
            # Pular linhas de metadata, imagens e links
            if line.startswith('#') or line.startswith('![]') or line.startswith('Fonte:') or line.startswith('---'):
                continue
            if 'http' in line and line.strip().startswith('['):
                continue
            if line.strip().startswith('**[') and line.strip().endswith('.]**'):
                continue

            # Limpar formatação markdown
            clean_line = line.replace('**', '').replace('*', '').strip()
            if clean_line and len(clean_line) > 10:  # Filtrar linhas muito curtas
                vsl_lines.append(clean_line)

        sample_vsl = '\n\n'.join(vsl_lines[:50])  # Primeiros 50 parágrafos

    except Exception as e:
        logger.error(f"Error loading Vitascience material: {e}")
        # Fallback para VSL básica
        sample_vsl = """
        Na noite do ano de 1785, Antoine Lavoisier descobriu o caminho para emagrecer sem sacrifícios.

        Essa descoberta é a chave para toda mulher perder a gordura da barriga, culote e papada.

        Por trás dessa descoberta, está a verdadeira razão da atividade física não emagrecer por si só.

        Lavoisier descobriu que existe um processo no seu corpo capaz de transformar a sua gordura em gás.

        Você pode fazer sua gordura evaporar e perder 5, 10 ou mais quilos.
        """

    return render_template('demo.html', sample_vsl=sample_vsl)

@app.errorhandler(404)
def not_found(error):
    return render_template('error.html',
                         error_code=404,
                         error_message="Página não encontrada"), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('error.html',
                         error_code=500,
                         error_message="Erro interno do servidor"), 500

if __name__ == '__main__':
    # Create templates directory if it doesn't exist
    os.makedirs('templates', exist_ok=True)
    os.makedirs('static/css', exist_ok=True)
    os.makedirs('static/js', exist_ok=True)

    # Development mode
    app.run(
        debug=True,
        host='0.0.0.0',
        port=int(os.getenv('PORT', 8080))
    )
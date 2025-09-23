#!/bin/bash

echo "===================================="
echo "EUGENE SCHWARTZ VSL ANALYZER"
echo "Squad Vitascience Demo Setup"
echo "===================================="
echo

echo "[1/3] Checking Python installation..."
python3 --version
if [ $? -ne 0 ]; then
    echo "ERROR: Python3 not found. Please install Python 3.8+"
    exit 1
fi

echo
echo "[2/3] Installing dependencies..."
pip3 install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to install dependencies"
    exit 1
fi

echo
echo "[3/3] Starting frontend server..."
echo
echo "Frontend will be available at: http://localhost:8080"
echo "N8N webhook endpoint: http://localhost:5678/webhook/analyze-vsl-squad"
echo
echo "Press Ctrl+C to stop the server"
echo

python3 run.py
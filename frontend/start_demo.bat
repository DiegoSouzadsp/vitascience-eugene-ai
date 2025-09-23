@echo off
echo ====================================
echo EUGENE SCHWARTZ VSL ANALYZER
echo Squad Vitascience Demo Setup
echo ====================================
echo.

echo [1/3] Checking Python installation...
python --version
if %errorlevel% neq 0 (
    echo ERROR: Python not found. Please install Python 3.8+
    pause
    exit /b 1
)

echo.
echo [2/3] Installing dependencies...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)

echo.
echo [3/3] Starting frontend server...
echo.
echo Frontend will be available at: http://localhost:8080
echo N8N webhook endpoint: http://localhost:5678/webhook/analyze-vsl-squad
echo.
echo Press Ctrl+C to stop the server
echo.

python run.py
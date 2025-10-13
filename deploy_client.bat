@echo off
setlocal enabledelayedexpansion

echo HAL Client Deployment Script
echo ==========================

:: Check Python installation
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed
    exit /b 1
)

:: Create virtual environment if it doesn't exist
if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
)

:: Activate virtual environment
call venv\Scripts\activate

:: Install requirements
echo Installing dependencies...
pip install -r requirements.txt

:: Check for environment variables
if not defined PORCUPINE_ACCESS_KEY (
    echo WARNING: PORCUPINE_ACCESS_KEY is not set
    echo Please set PORCUPINE_ACCESS_KEY environment variable
)

if not defined HAL_SERVER_URL (
    echo Setting default HAL_SERVER_URL...
    set HAL_SERVER_URL=ws://ollama.lcs.ai:8765
)

:: Create necessary directories
if not exist logs mkdir logs

echo.
echo Client deployment complete!
echo To start the client, run: python voice_handler.py
echo.

@echo off
title HAL Client
cd /d C:\qmsys\hal\mac_deployment_package

REM Check if venv exists
if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate venv and install dependencies
call venv\Scripts\activate.bat
pip install -q websockets 2>nul

REM Run client
echo.
echo ================================================
echo Starting HAL Text Client
echo ================================================
echo.
python hal_text_client.py

pause

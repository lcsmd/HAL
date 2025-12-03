@echo off
title HAL Voice Assistant Client
cd /d %~dp0

echo ================================================
echo HAL Voice Assistant Client
echo ================================================
echo.
echo Starting client...
echo Server: 10.1.34.103:8768
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found!
    echo Install Python 3.x from: https://python.org
    pause
    exit /b 1
)

REM Install dependencies if needed
python -c "import websockets" >nul 2>&1
if errorlevel 1 (
    echo Installing websockets...
    python -m pip install websockets
)

python -c "import pygame" >nul 2>&1
if errorlevel 1 (
    echo Installing pygame...
    python -m pip install pygame
)

echo.
echo Starting HAL client...
echo.

REM Start the GUI client
python hal_voice_client_gui.py

pause

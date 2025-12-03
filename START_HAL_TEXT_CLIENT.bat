@echo off
title HAL Text Client
cd /d C:\qmsys\hal

echo ================================================
echo Starting HAL Text Client (Console)
echo ================================================
echo.
echo Simple text-only interface
echo Type your queries and press ENTER
echo.

REM Install dependencies if needed
python -m pip install -q websockets 2>nul

REM Start the text client
python hal_text_client_windows.py

pause

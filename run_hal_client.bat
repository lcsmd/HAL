@echo off
title HAL Text Client
cd /d C:\qmsys\hal

REM Install websockets if needed
python -m pip install -q websockets 2>nul

REM Run client
echo.
echo ================================================
echo Starting HAL Text Client for Windows
echo ================================================
echo.
python hal_text_client_windows.py

pause

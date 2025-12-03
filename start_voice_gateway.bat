@echo off
title HAL Voice Gateway
cd /d C:\qmsys\hal

echo ========================================
echo Starting HAL Voice Gateway
echo ========================================
echo.
echo Voice Gateway will listen on port 8768
echo AI.SERVER is on port 8745
echo.
echo Press Ctrl+C to stop
echo ========================================
echo.

python PY\voice_gateway.py

pause

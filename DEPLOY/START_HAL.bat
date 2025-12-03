@echo off
title HAL Voice Assistant Client

REM Check if websockets is installed
python -c "import websockets" 2>nul
if errorlevel 1 (
    echo ================================================
    echo FIRST TIME SETUP
    echo ================================================
    echo.
    echo Installing websockets library...
    echo.
    python -m pip install websockets
    echo.
    echo Setup complete!
    echo.
    pause
)

REM Run HAL client
cls
python hal_client_standalone.py

pause

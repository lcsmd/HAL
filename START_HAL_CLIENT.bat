@echo off
title HAL Voice Assistant Client
cd /d C:\qmsys\hal\voice_assistant_v2\client

echo ================================================
echo Starting HAL Voice Assistant Client (GUI)
echo ================================================
echo.
echo This will open a GUI window with:
echo   - Text input interface
echo   - Voice input (if microphone available)
echo   - Text-to-speech toggle
echo.

REM Install dependencies if needed
python -m pip install -q websockets pygame 2>nul

REM Start the GUI client
python hal_voice_client_gui.py

pause

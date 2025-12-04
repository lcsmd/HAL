@echo off
REM Start HAL Web Voice Client Servers
REM Run this on Windows Server (10.1.34.103)

echo Starting HAL Web Voice Client Servers...
echo.

REM Change to script directory
cd /d "%~dp0"

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found. Please install Python 3.7+.
    pause
    exit /b 1
)

REM Check if required Python packages are installed
echo Checking Python dependencies...
python -c "import websockets, aiohttp" >nul 2>&1
if errorlevel 1 (
    echo Installing required Python packages...
    python -m pip install websockets aiohttp
)

echo.
echo Starting services...
echo.

REM Create logs directory if it doesn't exist
if not exist logs mkdir logs

REM Start HTTP server for static files (port 8080)
echo [1/2] Starting HTTP server on port 8080...
cd voice_assistant_v2\web_client
start "HAL HTTP Server" /MIN python -m http.server 8080
cd ..\..
timeout /t 2 /nobreak >nul

REM Start Voice Gateway WebSocket server (port 8768)
echo [2/2] Starting Voice Gateway on port 8768...
cd PY
start "HAL Voice Gateway" /MIN python voice_gateway_web.py
cd ..

echo.
echo ======================================
echo HAL Web Voice Client is running!
echo ======================================
echo.
echo HTTP Server (static files): http://10.1.34.103:8080
echo Voice Gateway (WebSocket):  ws://10.1.34.103:8768
echo.
echo Public URL: https://hal2.lcs.ai
echo.
echo Servers are running in minimized windows.
echo Close the windows to stop the servers.
echo.
pause

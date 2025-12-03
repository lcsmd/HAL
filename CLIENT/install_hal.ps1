# HAL Client Installer - Unified (Voice + Text)
# One-line: Invoke-WebRequest -Uri http://10.1.34.103:8080/install_hal.ps1 -OutFile $env:TEMP\hal_install.ps1; $env:HAL_SERVER_URL="http://10.1.34.103:8768"; & $env:TEMP\hal_install.ps1

param(
    [string]$ServerUrl = $env:HAL_SERVER_URL,
    [string]$PorcupineKey = $env:PORCUPINE_ACCESS_KEY
)

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "HAL Client Installation (Voice + Text)" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""

# Prompt for server URL if not provided
if (-not $ServerUrl) {
    $ServerUrl = Read-Host "Enter HAL Server URL (e.g., http://10.1.34.103:8768)"
}

# Convert HTTP to WebSocket URL
$GatewayUrl = $ServerUrl -replace '^http://', 'ws://' -replace '^https://', 'wss://'

# Get installer server URL
$InstallerHost = ($ServerUrl -replace 'http://', '' -replace 'https://', '') -split ':' | Select-Object -First 1
$InstallerUrl = "http://${InstallerHost}:8080"

Write-Host "Configuration:" -ForegroundColor Yellow
Write-Host "  Server: $ServerUrl" -ForegroundColor White
Write-Host "  Gateway: $GatewayUrl" -ForegroundColor White
Write-Host ""

# Check Python
Write-Host "[1/7] Checking Python..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    if ($LASTEXITCODE -ne 0) { throw "Python not found" }
    Write-Host "  [OK] $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "  [ERROR] Python 3 required: https://www.python.org/downloads/" -ForegroundColor Red
    exit 1
}

# Install base dependencies
Write-Host ""
Write-Host "[2/7] Installing base dependencies..." -ForegroundColor Yellow
try {
    python -m pip install --user --quiet websockets 2>&1 | Out-Null
    Write-Host "  [OK] websockets installed" -ForegroundColor Green
} catch {
    Write-Host "  [WARNING] websockets installation may have failed" -ForegroundColor Yellow
}

# Install voice dependencies (optional)
Write-Host ""
Write-Host "[3/7] Installing voice dependencies..." -ForegroundColor Yellow
Write-Host "  (This may take a few minutes on first install)" -ForegroundColor Gray
$VoiceAvailable = $true
try {
    python -m pip install --user --quiet pyaudio openwakeword openai-whisper numpy 2>&1 | Out-Null
    Write-Host "  [OK] Voice dependencies installed (pyaudio, openwakeword, whisper)" -ForegroundColor Green
} catch {
    Write-Host "  [WARNING] Voice dependencies failed (text mode will still work)" -ForegroundColor Yellow
    Write-Host "    For PyAudio: https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio" -ForegroundColor Gray
    $VoiceAvailable = $false
}

# Create installation directory
Write-Host ""
Write-Host "[4/7] Setting up directories..." -ForegroundColor Yellow
$InstallDir = "$env:USERPROFILE\.hal-client"
New-Item -ItemType Directory -Path "$InstallDir\VOICE\SOUNDS" -Force | Out-Null
Write-Host "  [OK] $InstallDir" -ForegroundColor Green

# Create text client
Write-Host ""
Write-Host "[5/7] Creating text client..." -ForegroundColor Yellow
$TextClientCode = @'
#!/usr/bin/env python3
"""HAL Text Client"""
import asyncio
import websockets
import json
import sys
import os

GATEWAY_URL = os.getenv('HAL_GATEWAY_URL', 'ws://localhost:8768')

class HALClient:
    def __init__(self, gateway_url):
        self.gateway_url = gateway_url
        self.session_id = None
        self.websocket = None
        
    async def connect(self):
        try:
            self.websocket = await websockets.connect(self.gateway_url)
            response = await self.websocket.recv()
            data = json.loads(response)
            if data.get('type') == 'connected':
                self.session_id = data.get('session_id')
                return True
            return False
        except Exception as e:
            print(f"✗ Connection failed: {e}")
            return False
    
    async def send_text_query(self, text):
        if not self.websocket:
            return None
        try:
            message = {'type': 'text_input', 'text': text, 'session_id': self.session_id}
            await self.websocket.send(json.dumps(message))
            while True:
                response = await asyncio.wait_for(self.websocket.recv(), timeout=30.0)
                data = json.loads(response)
                if data.get('type') == 'response':
                    print(f"\n{data.get('text', '')}")
                    return data.get('text')
                elif data.get('type') == 'processing':
                    pass
        except Exception as e:
            print(f"✗ Error: {e}")
            return None
    
    async def interactive_mode(self):
        print("\nHAL Text Client - Interactive Mode")
        print("(Type 'quit' to exit)\n")
        while True:
            try:
                query = input("You: ").strip()
                if not query:
                    continue
                if query.lower() in ['quit', 'exit', 'q']:
                    break
                await self.send_text_query(query)
            except KeyboardInterrupt:
                break
    
    async def close(self):
        if self.websocket:
            await self.websocket.close()

async def main():
    import argparse
    parser = argparse.ArgumentParser(description='HAL Text Client')
    parser.add_argument('--url', default=GATEWAY_URL, help='Gateway URL')
    parser.add_argument('--query', help='Single query')
    args = parser.parse_args()
    
    client = HALClient(args.url)
    if not await client.connect():
        return 1
    try:
        if args.query:
            await client.send_text_query(args.query)
        else:
            await client.interactive_mode()
    finally:
        await client.close()
    return 0

if __name__ == '__main__':
    try:
        sys.exit(asyncio.run(main()))
    except KeyboardInterrupt:
        sys.exit(0)
'@

$TextClientCode | Out-File -FilePath "$InstallDir\hal_text_client.py" -Encoding UTF8
Write-Host "  [OK] Text client installed" -ForegroundColor Green

# Download voice client
Write-Host ""
Write-Host "[6/7] Downloading voice client..." -ForegroundColor Yellow
try {
    Invoke-WebRequest -Uri "$InstallerUrl/hal_voice_client.py" -OutFile "$InstallDir\hal_voice_client.py" -ErrorAction Stop
    Write-Host "  [OK] Voice client installed" -ForegroundColor Green
    
    # Download TNG sound
    try {
        Invoke-WebRequest -Uri "$InstallerUrl/ack.wav" -OutFile "$InstallDir\VOICE\SOUNDS\ack.wav" -ErrorAction Stop
        Write-Host "  [OK] TNG activation sound installed" -ForegroundColor Green
    } catch {
        Write-Host "  [WARNING] Could not download TNG sound (will use fallback)" -ForegroundColor Yellow
    }
} catch {
    Write-Host "  [WARNING] Could not download voice client (text mode will still work)" -ForegroundColor Yellow
    $VoiceAvailable = $false
}

# Create configuration
Write-Host ""
Write-Host "[7/7] Creating configuration..." -ForegroundColor Yellow

@"
HAL_GATEWAY_URL=$GatewayUrl
HAL_SERVER_URL=$ServerUrl
WAKE_WORD_MODEL=hey_jarvis
WHISPER_MODEL=base
"@ | Out-File -FilePath "$InstallDir\.env" -Encoding UTF8

# Create unified launcher
@"
@echo off
setlocal
cd /d "%USERPROFILE%\.hal-client"
for /f "tokens=*" %%i in ('type .env') do set %%i

set USE_VOICE=0
set ARGS=

:parse_args
if "%~1"=="" goto :done_parsing
if "%~1"=="--voice" (
    set USE_VOICE=1
) else if "%~1"=="-v" (
    set USE_VOICE=1
) else (
    set ARGS=%ARGS% %1
)
shift
goto :parse_args

:done_parsing
if %USE_VOICE%==1 (
    if exist "%USERPROFILE%\.hal-client\hal_voice_client.py" (
        python "%USERPROFILE%\.hal-client\hal_voice_client.py" %ARGS%
    ) else (
        echo ✗ Voice client not installed. Using text mode.
        python "%USERPROFILE%\.hal-client\hal_text_client.py" %ARGS%
    )
) else (
    python "%USERPROFILE%\.hal-client\hal_text_client.py" %ARGS%
)
"@ | Out-File -FilePath "$InstallDir\hal.bat" -Encoding ASCII

# Add to PATH
$UserPath = [Environment]::GetEnvironmentVariable("Path", "User")
if ($UserPath -notlike "*$InstallDir*") {
    [Environment]::SetEnvironmentVariable("Path", "$UserPath;$InstallDir", "User")
    Write-Host "  [OK] Added to PATH" -ForegroundColor Green
}

Write-Host "  [OK] Configuration saved" -ForegroundColor Green

Write-Host ""
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "Installation Complete!" -ForegroundColor Green
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "Installed Modes:" -ForegroundColor Yellow
Write-Host "  [OK] Text mode (always available)" -ForegroundColor Green
if ($VoiceAvailable -and (Test-Path "$InstallDir\hal_voice_client.py")) {
    Write-Host "  [OK] Voice mode (with wake word support)" -ForegroundColor Green
} else {
    Write-Host "  [X] Voice mode (not available)" -ForegroundColor Gray
}
Write-Host ""

if ($VoiceAvailable) {
    Write-Host "Wake Word: Free & Open Source (OpenWakeWord)" -ForegroundColor Green
    Write-Host "  No API key needed!" -ForegroundColor White
    Write-Host "  Say: 'Hey Jarvis' or 'Computer'" -ForegroundColor White
    Write-Host ""
}

Write-Host "Usage:" -ForegroundColor Yellow
Write-Host ""
Write-Host "Text Mode (default):" -ForegroundColor White
Write-Host "  hal --query `"What medications am I taking?`"" -ForegroundColor Gray
Write-Host "  hal  # Interactive mode" -ForegroundColor Gray
Write-Host ""
if ($VoiceAvailable) {
    Write-Host "Voice Mode:" -ForegroundColor White
    Write-Host "  hal --voice" -ForegroundColor Gray
    Write-Host "  Say 'Computer' then TNG beep plays then speak query" -ForegroundColor Gray
    Write-Host ""
}
Write-Host "Configuration: $InstallDir\.env" -ForegroundColor Gray
Write-Host ""
Write-Host "Restart your terminal, then type: hal" -ForegroundColor Yellow
Write-Host ""
Write-Host "Live long and prosper! 🖖" -ForegroundColor Cyan
Write-Host ""

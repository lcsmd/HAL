# HAL Voice Client - Windows Installer
# Usage: 
#   $env:HAL_SERVER_URL="http://10.1.34.103:8768"; iex (irm http://10.1.34.103:8080/install_hal_windows.ps1)

param(
    [string]$ServerUrl = $env:HAL_SERVER_URL
)

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "HAL Voice Client - Windows Installation" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""

# Prompt for server URL if not provided
if (-not $ServerUrl) {
    $ServerUrl = Read-Host "Enter HAL Server URL (e.g., http://10.1.34.103:8768)"
}

# Convert HTTP to WebSocket URL
$GatewayUrl = $ServerUrl -replace '^http://', 'ws://' -replace '^https://', 'wss://'

Write-Host "Configuration:" -ForegroundColor Yellow
Write-Host "  Server URL: $ServerUrl" -ForegroundColor White
Write-Host "  Gateway URL: $GatewayUrl" -ForegroundColor White
Write-Host ""

# Check Python
Write-Host "[1/5] Checking Python..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    if ($LASTEXITCODE -ne 0) {
        throw "Python not found"
    }
    Write-Host "  ✓ Found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "  ✗ Error: Python 3 is required but not installed." -ForegroundColor Red
    Write-Host "    Install from: https://www.python.org/downloads/" -ForegroundColor Yellow
    exit 1
}

# Install dependencies
Write-Host ""
Write-Host "[2/5] Installing Python dependencies..." -ForegroundColor Yellow
try {
    python -m pip install --user --quiet websockets 2>&1 | Out-Null
    Write-Host "  ✓ websockets installed" -ForegroundColor Green
} catch {
    Write-Host "  ⚠ Warning: Could not install websockets" -ForegroundColor Yellow
}

# Create installation directory
Write-Host ""
Write-Host "[3/5] Setting up installation directory..." -ForegroundColor Yellow
$InstallDir = "$env:USERPROFILE\.hal-client"
if (-not (Test-Path $InstallDir)) {
    New-Item -ItemType Directory -Path $InstallDir -Force | Out-Null
}
Write-Host "  ✓ Directory: $InstallDir" -ForegroundColor Green

# Download client
Write-Host ""
Write-Host "[4/5] Downloading HAL client..." -ForegroundColor Yellow
$ClientCode = @'
#!/usr/bin/env python3
"""HAL Voice Client for Windows"""
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
        print(f"Connecting to HAL at {self.gateway_url}...")
        try:
            self.websocket = await websockets.connect(self.gateway_url)
            print("✓ Connected to HAL")
            response = await self.websocket.recv()
            data = json.loads(response)
            if data.get('type') == 'connected':
                self.session_id = data.get('session_id')
                print(f"✓ Session: {self.session_id}")
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
            print("  Waiting for response...", flush=True)
            while True:
                response = await asyncio.wait_for(self.websocket.recv(), timeout=30.0)
                data = json.loads(response)
                msg_type = data.get('type')
                if msg_type == 'response':
                    response_text = data.get('text', '')
                    intent = data.get('intent', 'unknown')
                    action = data.get('action', 'unknown')
                    print(f"\n[HAL Response]")
                    print(f"Intent: {intent}")
                    print(f"Action: {action}")
                    print(f"Text: {response_text}")
                    return response_text
                elif msg_type == 'processing':
                    print("  (HAL is thinking...)")
        except asyncio.TimeoutError:
            print("✗ Timeout waiting for response")
            return None
        except Exception as e:
            print(f"✗ Error: {e}")
            return None
    
    async def interactive_mode(self):
        print("\n" + "="*60)
        print("HAL Voice Client - Type your queries")
        print("="*60)
        print("(Type 'quit' to exit)\n")
        while True:
            try:
                query = input("You: ").strip()
                if not query:
                    continue
                if query.lower() in ['quit', 'exit', 'q']:
                    print("Goodbye!")
                    break
                await self.send_text_query(query)
                print()
            except KeyboardInterrupt:
                print("\nGoodbye!")
                break
            except Exception as e:
                print(f"Error: {e}")
    
    async def close(self):
        if self.websocket:
            await self.websocket.close()

async def main():
    import argparse
    parser = argparse.ArgumentParser(description='HAL Voice Client')
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

$ClientCode | Out-File -FilePath "$InstallDir\hal_client.py" -Encoding UTF8
Write-Host "  ✓ Client created" -ForegroundColor Green

# Create configuration
Write-Host ""
Write-Host "[5/5] Creating configuration..." -ForegroundColor Yellow
@"
HAL_GATEWAY_URL=$GatewayUrl
HAL_SERVER_URL=$ServerUrl
"@ | Out-File -FilePath "$InstallDir\.env" -Encoding UTF8

# Create launcher batch file
@"
@echo off
setlocal
for /f "tokens=*" %%i in ('type "%USERPROFILE%\.hal-client\.env"') do set %%i
python "%USERPROFILE%\.hal-client\hal_client.py" %*
"@ | Out-File -FilePath "$InstallDir\hal.bat" -Encoding ASCII

# Add to PATH if not already there
$UserPath = [Environment]::GetEnvironmentVariable("Path", "User")
if ($UserPath -notlike "*$InstallDir*") {
    [Environment]::SetEnvironmentVariable("Path", "$UserPath;$InstallDir", "User")
    Write-Host "  ✓ Added to PATH" -ForegroundColor Green
    Write-Host "  ℹ You may need to restart your terminal" -ForegroundColor Yellow
}

Write-Host "  ✓ Configuration saved" -ForegroundColor Green

# Test connection
Write-Host ""
Write-Host "Testing connection to HAL..." -ForegroundColor Yellow
$env:HAL_GATEWAY_URL = $GatewayUrl
$TestOutput = python "$InstallDir\hal_client.py" --query "test" 2>&1
if ($TestOutput -match "Connected") {
    Write-Host "  ✓ Connection successful!" -ForegroundColor Green
} else {
    Write-Host "  ⚠ Could not connect to HAL server" -ForegroundColor Yellow
    Write-Host "    Make sure the Voice Gateway is running at $ServerUrl" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "Installation Complete!" -ForegroundColor Green
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "To start HAL client:" -ForegroundColor Yellow
Write-Host "  1. Restart your terminal (or open new window)" -ForegroundColor White
Write-Host "  2. Type: hal" -ForegroundColor White
Write-Host ""
Write-Host "Or run directly:" -ForegroundColor Yellow
Write-Host "  $InstallDir\hal.bat" -ForegroundColor White
Write-Host ""
Write-Host "Single query:" -ForegroundColor Yellow
Write-Host "  hal --query `"What medications am I taking?`"" -ForegroundColor White
Write-Host ""
Write-Host "Configuration: $InstallDir\.env" -ForegroundColor Gray
Write-Host ""

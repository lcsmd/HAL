# HAL Voice Client - Windows Installer
# One-line: Invoke-WebRequest -Uri http://10.1.34.103:8080/install_hal_voice_windows.ps1 -OutFile $env:TEMP\hal_voice_install.ps1; $env:HAL_SERVER_URL="http://10.1.34.103:8768"; & $env:TEMP\hal_voice_install.ps1

param(
    [string]$ServerUrl = $env:HAL_SERVER_URL,
    [string]$PorcupineKey = $env:PORCUPINE_ACCESS_KEY
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

# Get installer server URL
$InstallerHost = ($ServerUrl -replace 'http://', '' -replace 'https://', '') -split ':' | Select-Object -First 1
$InstallerUrl = "http://${InstallerHost}:8080"

Write-Host "Configuration:" -ForegroundColor Yellow
Write-Host "  Server URL: $ServerUrl" -ForegroundColor White
Write-Host "  Gateway URL: $GatewayUrl" -ForegroundColor White
Write-Host "  Installer: $InstallerUrl" -ForegroundColor White
Write-Host ""

# Check Python
Write-Host "[1/6] Checking Python..." -ForegroundColor Yellow
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
Write-Host "[2/6] Installing Python dependencies..." -ForegroundColor Yellow
Write-Host "  (This may take a few minutes on first install)" -ForegroundColor Gray
try {
    python -m pip install --user --quiet pyaudio pvporcupine openai-whisper 2>&1 | Out-Null
    Write-Host "  ✓ Dependencies installed (pyaudio, pvporcupine, whisper)" -ForegroundColor Green
} catch {
    Write-Host "  ⚠ Warning: Some packages may have failed to install" -ForegroundColor Yellow
    Write-Host "  For PyAudio issues, download from: https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio" -ForegroundColor Yellow
}

# Create installation directory
Write-Host ""
Write-Host "[3/6] Setting up installation directory..." -ForegroundColor Yellow
$InstallDir = "$env:USERPROFILE\.hal-voice"
if (-not (Test-Path $InstallDir)) {
    New-Item -ItemType Directory -Path $InstallDir -Force | Out-Null
}
New-Item -ItemType Directory -Path "$InstallDir\VOICE\SOUNDS" -Force | Out-Null
Write-Host "  ✓ Directory: $InstallDir" -ForegroundColor Green

# Download voice client
Write-Host ""
Write-Host "[4/6] Downloading HAL voice client..." -ForegroundColor Yellow
try {
    Invoke-WebRequest -Uri "$InstallerUrl/hal_voice_client.py" -OutFile "$InstallDir\hal_voice_client.py"
    Write-Host "  ✓ Voice client downloaded" -ForegroundColor Green
} catch {
    Write-Host "  ✗ Failed to download voice client from $InstallerUrl" -ForegroundColor Red
    Write-Host "  Make sure installer server is running: python serve_installer.py" -ForegroundColor Yellow
    exit 1
}

# Download TNG activation sound
Write-Host ""
Write-Host "[5/6] Downloading TNG activation sound..." -ForegroundColor Yellow
try {
    Invoke-WebRequest -Uri "$InstallerUrl/ack.wav" -OutFile "$InstallDir\VOICE\SOUNDS\ack.wav"
    Write-Host "  ✓ TNG sound installed (ack.wav)" -ForegroundColor Green
} catch {
    Write-Host "  ⚠ Warning: Could not download TNG sound (will use fallback beep)" -ForegroundColor Yellow
}

# Create configuration
Write-Host ""
Write-Host "[6/6] Creating configuration..." -ForegroundColor Yellow
@"
HAL_GATEWAY_URL=$GatewayUrl
HAL_SERVER_URL=$ServerUrl
PORCUPINE_ACCESS_KEY=$PorcupineKey
WHISPER_MODEL=base
"@ | Out-File -FilePath "$InstallDir\.env" -Encoding UTF8

# Create launcher batch file
@"
@echo off
setlocal
cd /d "%USERPROFILE%\.hal-voice"
for /f "tokens=*" %%i in ('type .env') do set %%i
python "%USERPROFILE%\.hal-voice\hal_voice_client.py" %*
"@ | Out-File -FilePath "$InstallDir\hal-voice.bat" -Encoding ASCII

# Add to PATH if not already there
$UserPath = [Environment]::GetEnvironmentVariable("Path", "User")
if ($UserPath -notlike "*$InstallDir*") {
    [Environment]::SetEnvironmentVariable("Path", "$UserPath;$InstallDir", "User")
    Write-Host "  ✓ Added to PATH" -ForegroundColor Green
    Write-Host "  ℹ You may need to restart your terminal" -ForegroundColor Yellow
}

Write-Host "  ✓ Configuration saved" -ForegroundColor Green

echo ""
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "Installation Complete!" -ForegroundColor Green
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""

# Check if Porcupine key is set
if (-not $PorcupineKey) {
    Write-Host "⚠ PORCUPINE_ACCESS_KEY not set" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "To enable wake word detection:" -ForegroundColor Yellow
    Write-Host "  1. Get free key: https://console.picovoice.ai/" -ForegroundColor White
    Write-Host "  2. Add to $InstallDir\.env:" -ForegroundColor White
    Write-Host "     PORCUPINE_ACCESS_KEY=your-key-here" -ForegroundColor Gray
    Write-Host ""
    Write-Host "Without this key, you'll use keyboard mode (press ENTER to record)" -ForegroundColor Gray
    Write-Host ""
}

Write-Host "To start HAL Voice Client:" -ForegroundColor Yellow
Write-Host "  1. Restart your terminal (or open new window)" -ForegroundColor White
Write-Host "  2. Type: hal-voice" -ForegroundColor White
Write-Host ""
Write-Host "Or run directly:" -ForegroundColor Yellow
Write-Host "  $InstallDir\hal-voice.bat" -ForegroundColor White
Write-Host ""
Write-Host "Voice Mode:" -ForegroundColor Yellow
Write-Host "  - Say 'Computer' to activate" -ForegroundColor White
Write-Host "  - 🔊 Hear TNG activation sound" -ForegroundColor White
Write-Host "  - Speak your query" -ForegroundColor White
Write-Host "  - Get HAL's response" -ForegroundColor White
Write-Host ""
Write-Host "Text Mode (testing):" -ForegroundColor Yellow
Write-Host "  hal-voice --query `"What medications am I taking?`"" -ForegroundColor White
Write-Host ""
Write-Host "Configuration: $InstallDir\.env" -ForegroundColor Gray
Write-Host ""
Write-Host "Live long and prosper! 🖖" -ForegroundColor Cyan
Write-Host ""

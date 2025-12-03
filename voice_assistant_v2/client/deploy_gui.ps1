#
# HAL Voice Assistant - GUI Client Deployment
# One-command deployment for Windows/Mac/Linux
#

$ErrorActionPreference = "Stop"

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "HAL Voice Assistant GUI - Deploy" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Functions to print status
function Print-Status {
    param([string]$Message)
    Write-Host "checkmark $Message" -ForegroundColor Green
}

function Print-Error {
    param([string]$Message)
    Write-Host "X $Message" -ForegroundColor Red
}

function Print-Warning {
    param([string]$Message)
    Write-Host "! $Message" -ForegroundColor Yellow
}

# Step 1: Check Python 3
Write-Host "Checking Python 3..."
try {
    $pythonVersion = python --version 2>&1
    if ($pythonVersion -match "Python 3") {
        Print-Status "Found: $pythonVersion"
    } else {
        Print-Error "Python 3 not found!"
        Write-Host "Install from: https://www.python.org/downloads/"
        exit 1
    }
} catch {
    Print-Error "Python 3 not found!"
    Write-Host "Install from: https://www.python.org/downloads/"
    exit 1
}
Write-Host ""

# Step 2: Create virtual environment
Write-Host "Setting up virtual environment..."
if (Test-Path "venv") {
    Print-Status "Virtual environment exists"
} else {
    python -m venv venv
    Print-Status "Virtual environment created"
}
Write-Host ""

# Step 3: Install Python packages
Write-Host "Installing Python packages..."
& "venv\Scripts\Activate.ps1"
python -m pip install --upgrade pip --quiet
pip install -r requirements.txt
Print-Status "Python packages installed"
Write-Host ""

# Step 4: Check sound files
Write-Host "Checking sound files..."
if (Test-Path "sounds\activation.mp3") {
    Print-Status "Sound files found"
} else {
    Print-Warning "Sound files not found (optional for GUI)"
}
Write-Host ""

# Step 5: Display startup info
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "✓ Deployment Complete!" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Starting HAL Voice Assistant GUI..." -ForegroundColor Green
Write-Host ""
Write-Host "Features:" -ForegroundColor Yellow
Write-Host "  • Type messages and press Enter" -ForegroundColor White
Write-Host "  • Say wake word for voice input" -ForegroundColor White
Write-Host "  • Toggle TTS on/off (button)" -ForegroundColor White
Write-Host "  • Voice auto-enables TTS" -ForegroundColor White
Write-Host "  • Text keeps current TTS state" -ForegroundColor White
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Step 6: Start the GUI client
python hal_voice_client_gui.py

# If client exits, deactivate venv
deactivate

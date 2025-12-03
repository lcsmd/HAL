# HAL Voice Assistant - GUI Client Deployment
# One-command deployment for Windows

$ErrorActionPreference = "Stop"

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "HAL Voice Assistant GUI - Deploy" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Step 1: Check Python 3
Write-Host "Checking Python 3..."
try {
    $pythonVersion = python --version 2>&1
    if ($pythonVersion -match "Python 3") {
        Write-Host "[OK] Found: $pythonVersion" -ForegroundColor Green
    } else {
        Write-Host "[ERROR] Python 3 not found!" -ForegroundColor Red
        Write-Host "Install from: https://www.python.org/downloads/"
        exit 1
    }
} catch {
    Write-Host "[ERROR] Python 3 not found!" -ForegroundColor Red
    Write-Host "Install from: https://www.python.org/downloads/"
    exit 1
}
Write-Host ""

# Step 2: Create virtual environment
Write-Host "Setting up virtual environment..."
if (Test-Path "venv") {
    Write-Host "[OK] Virtual environment exists" -ForegroundColor Green
} else {
    python -m venv venv
    Write-Host "[OK] Virtual environment created" -ForegroundColor Green
}
Write-Host ""

# Step 3: Install Python packages
Write-Host "Installing Python packages..."
& "venv\Scripts\Activate.ps1"
python -m pip install --upgrade pip --quiet
pip install -r requirements.txt
Write-Host "[OK] Python packages installed" -ForegroundColor Green
Write-Host ""

# Step 4: Check sound files
Write-Host "Checking sound files..."
if (Test-Path "sounds\activation.mp3") {
    Write-Host "[OK] Sound files found" -ForegroundColor Green
} else {
    Write-Host "[WARN] Sound files not found (optional for GUI)" -ForegroundColor Yellow
}
Write-Host ""

# Step 5: Display startup info
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Deployment Complete!" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Starting HAL Voice Assistant GUI..." -ForegroundColor Green
Write-Host ""
Write-Host "Features:" -ForegroundColor Yellow
Write-Host "  - Type messages and press Enter" -ForegroundColor White
Write-Host "  - Say wake word for voice input" -ForegroundColor White
Write-Host "  - Toggle TTS on/off (button)" -ForegroundColor White
Write-Host "  - Voice auto-enables TTS" -ForegroundColor White
Write-Host "  - Text keeps current TTS state" -ForegroundColor White
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Step 6: Start the GUI client
python hal_voice_client_gui.py

# If client exits, deactivate venv
deactivate

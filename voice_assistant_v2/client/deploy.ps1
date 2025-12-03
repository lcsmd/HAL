#
# HAL Voice Client - One-Command Deployment (Windows)
#
# Usage:
#   .\deploy.ps1
#
# This script will:
# 1. Check for required tools (Python 3)
# 2. Create virtual environment
# 3. Install Python packages
# 4. Copy sound files from CLIENT\ directory
# 5. Start the voice client
#

$ErrorActionPreference = "Stop"

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "HAL Voice Client - One-Command Deploy" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Function to print status
function Print-Status {
    param([string]$Message)
    Write-Host "✓ $Message" -ForegroundColor Green
}

function Print-Error {
    param([string]$Message)
    Write-Host "✗ $Message" -ForegroundColor Red
}

function Print-Warning {
    param([string]$Message)
    Write-Host "⚠ $Message" -ForegroundColor Yellow
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

# Step 4: Copy sound files
Write-Host "Copying sound files..."

# Determine CLIENT directory location
$clientDir = $null
if (Test-Path "..\..\CLIENT") {
    $clientDir = "..\..\CLIENT"
} elseif (Test-Path "..\..\..\CLIENT") {
    $clientDir = "..\..\..\CLIENT"
} else {
    Print-Warning "CLIENT directory not found at ..\..\CLIENT"
    Print-Warning "Sound files must be copied manually"
}

if ($clientDir) {
    # Create sounds directory
    if (-not (Test-Path "sounds")) {
        New-Item -ItemType Directory -Path "sounds" | Out-Null
    }
    
    # Copy activation sound
    if (Test-Path "$clientDir\activation.mp3") {
        Copy-Item "$clientDir\activation.mp3" "sounds\" -Force
        Print-Status "Copied activation.mp3"
    } else {
        Print-Warning "activation.mp3 not found in $clientDir"
    }
    
    # Copy acknowledgement sound
    if (Test-Path "$clientDir\acknowledgement.wav") {
        Copy-Item "$clientDir\acknowledgement.wav" "sounds\" -Force
        Print-Status "Copied acknowledgement.wav"
    } elseif (Test-Path "$clientDir\ack.wav") {
        Copy-Item "$clientDir\ack.wav" "sounds\acknowledgement.wav" -Force
        Print-Status "Copied ack.wav -> acknowledgement.wav"
    } else {
        Print-Warning "acknowledgement.wav not found in $clientDir"
    }
}
Write-Host ""

# Step 5: Check configuration
Write-Host "Checking configuration..."
if (Test-Path "voice_client.config") {
    Print-Status "Configuration file found"
} else {
    Print-Warning "voice_client.config not found (will use defaults)"
}
Write-Host ""

# Step 6: Display startup info
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "✓ Deployment Complete!" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Voice Server: ws://10.1.10.20:8585"
Write-Host "Wake Word: HEY JARVIS"
Write-Host ""
Write-Host "Starting HAL Voice Client..."
Write-Host ""
Write-Host 'Say: "HEY JARVIS, what time is it?"'
Write-Host ""
Write-Host "Press Ctrl+C to exit"
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Step 7: Start the client
python hal_voice_client.py

# If client exits, deactivate venv
deactivate

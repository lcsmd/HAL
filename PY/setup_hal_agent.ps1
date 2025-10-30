<#
setup_hal_agent.ps1
Purpose:
  - Create Python virtual environment for HAL
  - Install dependencies
  - Set environment variables
  - Launch hal_agent.py

Usage:
  Run this script in PowerShell:
      PS C:\QMSYS\HAL\PY> .\setup_hal_agent.ps1
#>

# === Config ===
$HAL_ROOT = "C:\QMSYS\HAL"
$PY_PATH  = "$HAL_ROOT\PY"
$VENV     = "$PY_PATH\venv"
$TOKEN    = "CHANGEME-STRONG-TOKEN"   # Replace with your own secret

Write-Host "=== HAL Agent Setup ==="
Write-Host "HAL Root: $HAL_ROOT"
Write-Host "Python Path: $PY_PATH"
Write-Host "Virtual Env: $VENV"
Write-Host ""

# === Step 1: Create venv if missing ===
if (!(Test-Path "$VENV")) {
    Write-Host "Creating virtual environment..."
    py -m venv $VENV
} else {
    Write-Host "Virtual environment already exists."
}

# === Step 2: Activate and install dependencies ===
Write-Host "Activating environment..."
$activate = "$VENV\Scripts\Activate.ps1"
& $activate

Write-Host "Upgrading pip..."
pip install --upgrade pip

Write-Host "Installing FastAPI, uvicorn, pydantic, requests..."
pip install fastapi uvicorn pydantic requests

# === Step 3: Set environment variables ===
Write-Host "Setting environment variables..."
$env:HAL_ROOT = $HAL_ROOT
$env:HAL_AGENT_TOKEN = $TOKEN
$env:HAL_AGENT_HOST = "127.0.0.1"
$env:HAL_AGENT_PORT = "8766"

# Persist to user environment for reuse
[System.Environment]::SetEnvironmentVariable("HAL_ROOT", $HAL_ROOT, "User")
[System.Environment]::SetEnvironmentVariable("HAL_AGENT_TOKEN", $TOKEN, "User")
[System.Environment]::SetEnvironmentVariable("HAL_AGENT_HOST", "127.0.0.1", "User")
[System.Environment]::SetEnvironmentVariable("HAL_AGENT_PORT", "8766", "User")

# === Step 4: Start Agent ===
Write-Host ""
Write-Host "Starting HAL Agent..."
python "$PY_PATH\hal_agent.py"


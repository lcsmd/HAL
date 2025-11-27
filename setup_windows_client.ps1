# HAL Windows Client - Automated Setup Script
# This script automates the complete setup process

param(
    [switch]$IncludeVoice = $false,
    [string]$InstallPath = "$env:USERPROFILE\Documents\HAL"
)

$ErrorActionPreference = "Continue"

Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "HAL Windows Client - Automated Setup" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

# Check if running as admin (for execution policy)
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
if (-not $isAdmin) {
    Write-Host "Note: Not running as administrator. Will use CurrentUser scope for settings." -ForegroundColor Yellow
    Write-Host ""
}

# Step 1: Check Python
Write-Host "Step 1: Checking Python Installation" -ForegroundColor Green
Write-Host "-------------------------------------" -ForegroundColor Green
$pythonCmd = Get-Command python -ErrorAction SilentlyContinue
if (-not $pythonCmd) {
    Write-Host "✗ Python not found!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Please install Python 3.11+ from:" -ForegroundColor Yellow
    Write-Host "  https://www.python.org/downloads/" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "IMPORTANT: Check 'Add Python to PATH' during installation!" -ForegroundColor Yellow
    Write-Host ""
    
    $openBrowser = Read-Host "Open download page in browser? (Y/n)"
    if ($openBrowser -ne "n") {
        Start-Process "https://www.python.org/downloads/"
    }
    exit 1
}

$pythonVersion = python --version 2>&1
Write-Host "✓ Python found: $pythonVersion" -ForegroundColor Green
Write-Host ""

# Step 2: Check/Fix Execution Policy
Write-Host "Step 2: Checking PowerShell Execution Policy" -ForegroundColor Green
Write-Host "-------------------------------------" -ForegroundColor Green
$currentPolicy = Get-ExecutionPolicy -Scope CurrentUser
Write-Host "Current policy: $currentPolicy"

if ($currentPolicy -eq "Restricted" -or $currentPolicy -eq "Undefined") {
    Write-Host "Setting execution policy to RemoteSigned..." -ForegroundColor Yellow
    try {
        Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser -Force
        Write-Host "✓ Execution policy updated" -ForegroundColor Green
    } catch {
        Write-Host "⚠ Could not update execution policy. May need manual intervention." -ForegroundColor Yellow
    }
} else {
    Write-Host "✓ Execution policy is OK" -ForegroundColor Green
}
Write-Host ""

# Step 3: Check Git
Write-Host "Step 3: Checking Git Installation" -ForegroundColor Green
Write-Host "-------------------------------------" -ForegroundColor Green
$gitCmd = Get-Command git -ErrorAction SilentlyContinue
if (-not $gitCmd) {
    Write-Host "✗ Git not found!" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Options:" -ForegroundColor Yellow
    Write-Host "  1. Install Git: https://git-scm.com/download/win" -ForegroundColor Yellow
    Write-Host "  2. Or manually copy files from QM server" -ForegroundColor Yellow
    Write-Host ""
    
    $installGit = Read-Host "Open Git download page? (Y/n)"
    if ($installGit -ne "n") {
        Start-Process "https://git-scm.com/download/win"
    }
    
    Write-Host ""
    Write-Host "After installing Git, run this script again." -ForegroundColor Yellow
    exit 1
}

$gitVersion = git --version 2>&1
Write-Host "✓ Git found: $gitVersion" -ForegroundColor Green
Write-Host ""

# Step 4: Clone or Update Repository
Write-Host "Step 4: Getting HAL Client Files" -ForegroundColor Green
Write-Host "-------------------------------------" -ForegroundColor Green

if (Test-Path $InstallPath) {
    Write-Host "Directory exists: $InstallPath" -ForegroundColor Yellow
    $action = Read-Host "Update existing installation? (Y/n)"
    if ($action -ne "n") {
        Push-Location $InstallPath
        Write-Host "Updating from GitHub..." -ForegroundColor Cyan
        git pull
        Pop-Location
        Write-Host "✓ Updated" -ForegroundColor Green
    }
} else {
    Write-Host "Cloning from GitHub to: $InstallPath" -ForegroundColor Cyan
    New-Item -ItemType Directory -Path (Split-Path $InstallPath) -Force | Out-Null
    git clone https://github.com/lcsmd/HAL.git $InstallPath
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✓ Repository cloned" -ForegroundColor Green
    } else {
        Write-Host "✗ Failed to clone repository" -ForegroundColor Red
        Write-Host ""
        Write-Host "Manual alternative:" -ForegroundColor Yellow
        Write-Host "  Copy files from: \\10.1.34.103\qmsys\hal\mac_deployment_package\" -ForegroundColor Yellow
        Write-Host "  To: $InstallPath\mac_deployment_package\" -ForegroundColor Yellow
        exit 1
    }
}
Write-Host ""

# Step 5: Create Virtual Environment
$clientPath = Join-Path $InstallPath "mac_deployment_package"
Write-Host "Step 5: Setting Up Python Virtual Environment" -ForegroundColor Green
Write-Host "-------------------------------------" -ForegroundColor Green

if (-not (Test-Path $clientPath)) {
    Write-Host "✗ Client directory not found: $clientPath" -ForegroundColor Red
    exit 1
}

Push-Location $clientPath

$venvPath = "venv"
if (Test-Path $venvPath) {
    Write-Host "Virtual environment already exists" -ForegroundColor Yellow
    $recreate = Read-Host "Recreate virtual environment? (y/N)"
    if ($recreate -eq "y") {
        Remove-Item -Recurse -Force $venvPath
        python -m venv venv
        Write-Host "✓ Virtual environment recreated" -ForegroundColor Green
    }
} else {
    Write-Host "Creating virtual environment..." -ForegroundColor Cyan
    python -m venv venv
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✓ Virtual environment created" -ForegroundColor Green
    } else {
        Write-Host "✗ Failed to create virtual environment" -ForegroundColor Red
        Pop-Location
        exit 1
    }
}
Write-Host ""

# Step 6: Install Dependencies
Write-Host "Step 6: Installing Python Dependencies" -ForegroundColor Green
Write-Host "-------------------------------------" -ForegroundColor Green

Write-Host "Activating virtual environment..." -ForegroundColor Cyan
& ".\venv\Scripts\Activate.ps1"

Write-Host "Upgrading pip..." -ForegroundColor Cyan
python -m pip install --upgrade pip --quiet

Write-Host "Installing websockets (required for text client)..." -ForegroundColor Cyan
pip install websockets --quiet
Write-Host "✓ websockets installed" -ForegroundColor Green

if ($IncludeVoice) {
    Write-Host ""
    Write-Host "Installing voice client dependencies..." -ForegroundColor Cyan
    Write-Host "(This may take a few minutes)" -ForegroundColor Yellow
    
    # Install pipwin for PyAudio
    pip install pipwin --quiet
    Write-Host "  ✓ pipwin installed" -ForegroundColor Green
    
    # Install PyAudio via pipwin
    pipwin install pyaudio --quiet
    Write-Host "  ✓ pyaudio installed" -ForegroundColor Green
    
    # Install other voice dependencies
    pip install pvporcupine numpy simpleaudio --quiet
    Write-Host "  ✓ voice dependencies installed" -ForegroundColor Green
}

Write-Host "✓ All dependencies installed" -ForegroundColor Green
Write-Host ""

# Step 7: Test Connection
Write-Host "Step 7: Testing Connection to HAL Server" -ForegroundColor Green
Write-Host "-------------------------------------" -ForegroundColor Green

# Python test script will be created inline below to avoid parsing issues

Write-Host "Testing connection to QM server (10.1.34.103:8768)..." -ForegroundColor Cyan

# Create test script using separate lines to avoid parsing issues
$testLines = @(
    "import asyncio",
    "import websockets",
    "import sys",
    "",
    "async def test():",
    "    uri = 'ws://10.1.34.103:8768'",
    "    try:",
    "        async with websockets.connect(uri, ping_interval=None) as ws:",
    "            await ws.send('{`"command`":`"ping`"}')",
    "            response = await asyncio.wait_for(ws.recv(), timeout=5)",
    "            print('SUCCESS')",
    "            return True",
    "    except Exception as e:",
    "        print(f'FAILED: {e}')",
    "        return False",
    "",
    "result = asyncio.run(test())",
    "sys.exit(0 if result else 1)"
)

$testLines | Out-File -FilePath "test_connection_temp.py" -Encoding UTF8
$testOutput = python test_connection_temp.py 2>&1

if ($testOutput -match "SUCCESS") {
    Write-Host "✓ Connection successful!" -ForegroundColor Green
} else {
    Write-Host "⚠ Connection failed" -ForegroundColor Yellow
    Write-Host "  Error: $testOutput" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "  Possible causes:" -ForegroundColor Yellow
    Write-Host "    - QM server is offline" -ForegroundColor Yellow
    Write-Host "    - WebSocket listener not running on server" -ForegroundColor Yellow
    Write-Host "    - Firewall blocking connection" -ForegroundColor Yellow
    Write-Host "    - Not on same network" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "  You can still use the client, but it won't connect yet." -ForegroundColor Yellow
}

Remove-Item "test_connection_temp.py" -ErrorAction SilentlyContinue
Write-Host ""

# Step 8: Create Desktop Shortcuts
Write-Host "Step 8: Creating Desktop Shortcuts" -ForegroundColor Green
Write-Host "-------------------------------------" -ForegroundColor Green

$createShortcuts = Read-Host "Create desktop shortcuts? (Y/n)"
if ($createShortcuts -ne "n") {
    
    # Text Client Batch File
    $textBat = @"
@echo off
title HAL Text Client
cd /d "$clientPath"
call venv\Scripts\activate.bat
python hal_text_client.py
pause
"@
    $textBatPath = Join-Path $clientPath "HAL_Text_Client.bat"
    $textBat | Out-File -FilePath $textBatPath -Encoding ASCII
    
    # Create shortcut
    $WshShell = New-Object -ComObject WScript.Shell
    $Shortcut = $WshShell.CreateShortcut("$env:USERPROFILE\Desktop\HAL Text Client.lnk")
    $Shortcut.TargetPath = $textBatPath
    $Shortcut.WorkingDirectory = $clientPath
    $Shortcut.Description = "HAL Text Client"
    $Shortcut.Save()
    
    Write-Host "✓ Text client shortcut created" -ForegroundColor Green
    
    if ($IncludeVoice) {
        # Voice Client Batch File
        $voiceBat = @"
@echo off
title HAL Voice Client
cd /d "$clientPath"
call venv\Scripts\activate.bat
python hal_voice_client.py
pause
"@
        $voiceBatPath = Join-Path $clientPath "HAL_Voice_Client.bat"
        $voiceBat | Out-File -FilePath $voiceBatPath -Encoding ASCII
        
        # Create shortcut
        $Shortcut = $WshShell.CreateShortcut("$env:USERPROFILE\Desktop\HAL Voice Client.lnk")
        $Shortcut.TargetPath = $voiceBatPath
        $Shortcut.WorkingDirectory = $clientPath
        $Shortcut.Description = "HAL Voice Client"
        $Shortcut.Save()
        
        Write-Host "✓ Voice client shortcut created" -ForegroundColor Green
    }
}
Write-Host ""

# Step 9: Summary
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "Setup Complete!" -ForegroundColor Green
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Installation Directory:" -ForegroundColor Cyan
Write-Host "  $clientPath" -ForegroundColor White
Write-Host ""
Write-Host "To run HAL client:" -ForegroundColor Cyan
Write-Host ""
Write-Host "  Option 1 - Desktop Shortcut:" -ForegroundColor Yellow
Write-Host "    Double-click 'HAL Text Client' on your desktop" -ForegroundColor White
Write-Host ""
Write-Host "  Option 2 - Command Line:" -ForegroundColor Yellow
Write-Host "    cd `"$clientPath`"" -ForegroundColor White
Write-Host "    .\venv\Scripts\Activate.ps1" -ForegroundColor White
Write-Host "    python hal_text_client.py" -ForegroundColor White
Write-Host ""

if ($IncludeVoice) {
    Write-Host "  Option 3 - Voice Client:" -ForegroundColor Yellow
    Write-Host "    Double-click 'HAL Voice Client' on your desktop" -ForegroundColor White
    Write-Host "    Or: python hal_voice_client.py" -ForegroundColor White
    Write-Host ""
}

Write-Host "Example Queries:" -ForegroundColor Cyan
Write-Host "  - What medications am I taking?" -ForegroundColor White
Write-Host "  - Show my appointments" -ForegroundColor White
Write-Host "  - List my allergies" -ForegroundColor White
Write-Host ""

Write-Host "Documentation:" -ForegroundColor Cyan
Write-Host "  Local: $InstallPath\DOCS\DEPLOYMENT\" -ForegroundColor White
Write-Host "  GitHub: https://github.com/lcsmd/HAL" -ForegroundColor White
Write-Host ""

$runNow = Read-Host "Run text client now? (Y/n)"
if ($runNow -ne "n") {
    Write-Host ""
    Write-Host "Starting HAL Text Client..." -ForegroundColor Green
    Write-Host "(Type 'quit' to exit)" -ForegroundColor Yellow
    Write-Host ""
    & ".\venv\Scripts\Activate.ps1"
    python hal_text_client.py
}

Pop-Location

# Voice Assistant AI Server Setup Script (Windows/OpenQM)
# Run as Administrator in PowerShell
#
# This script:
# 1. Compiles and catalogs the AI.SERVER program
# 2. Creates required OpenQM files
# 3. Sets up firewall rules
# 4. Creates helper scripts
# 5. Optionally starts the phantom process

param(
    [switch]$AutoStart = $false
)

# Check if running as Administrator
$currentPrincipal = New-Object Security.Principal.WindowsPrincipal([Security.Principal.WindowsIdentity]::GetCurrent())
$isAdmin = $currentPrincipal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)

if (-not $isAdmin) {
    Write-Host "ERROR: This script must be run as Administrator" -ForegroundColor Red
    Write-Host "Right-click PowerShell and select 'Run as Administrator'" -ForegroundColor Yellow
    exit 1
}

Write-Host "============================================" -ForegroundColor Cyan
Write-Host "Voice Assistant AI Server Setup (Windows)" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

# Configuration
$QM_HOME = "C:\qmsys"
$HAL_ACCOUNT = "HAL"
$QM_BIN = "$QM_HOME\bin"
$AI_SERVER_DIR = "$PSScriptRoot"
$AI_SERVER_PROGRAM = "AI.SERVER"

# Check if OpenQM is installed
Write-Host "[1/7] Checking OpenQM installation..." -ForegroundColor Green
if (-not (Test-Path "$QM_BIN\qm.exe")) {
    Write-Host "ERROR: OpenQM not found at $QM_BIN" -ForegroundColor Red
    Write-Host "Please install OpenQM first" -ForegroundColor Yellow
    exit 1
}

Write-Host "Found OpenQM at $QM_BIN" -ForegroundColor White

# Check if HAL account exists
Write-Host ""
Write-Host "[2/7] Checking HAL account..." -ForegroundColor Green
$accountPath = "$QM_HOME\hal"
if (-not (Test-Path $accountPath)) {
    Write-Host "ERROR: HAL account not found at $accountPath" -ForegroundColor Red
    Write-Host "Please create the HAL account first" -ForegroundColor Yellow
    exit 1
}

Write-Host "HAL account found at $accountPath" -ForegroundColor White

# Copy AI.SERVER program to BP directory
Write-Host ""
Write-Host "[3/7] Installing AI.SERVER program..." -ForegroundColor Green
$bpDir = "$accountPath\BP"
if (-not (Test-Path $bpDir)) {
    New-Item -ItemType Directory -Path $bpDir | Out-Null
}

Copy-Item "$AI_SERVER_DIR\AI.SERVER" "$bpDir\AI.SERVER" -Force
Write-Host "Program copied to $bpDir\AI.SERVER" -ForegroundColor White

# Compile and catalog the program
Write-Host ""
Write-Host "[4/7] Compiling and cataloging AI.SERVER..." -ForegroundColor Green

$qmScript = @"
LOGTO HAL
BASIC BP AI.SERVER
CATALOG BP AI.SERVER
QUIT
"@

$qmScript | & "$QM_BIN\qm.exe" -aHAL

if ($LASTEXITCODE -eq 0) {
    Write-Host "Program compiled and cataloged successfully" -ForegroundColor White
} else {
    Write-Host "WARNING: Compilation may have had issues" -ForegroundColor Yellow
}

# Create required OpenQM files
Write-Host ""
Write-Host "[5/7] Creating required OpenQM files..." -ForegroundColor Green

$createFilesScript = @"
LOGTO HAL
CREATE.FILE VOICE.ASSISTANT.LOG 1
CREATE.FILE VOICE.SESSIONS 1
QUIT
"@

$createFilesScript | & "$QM_BIN\qm.exe" -aHAL

Write-Host "Files created: VOICE.ASSISTANT.LOG, VOICE.SESSIONS" -ForegroundColor White

# Configure Windows Firewall
Write-Host ""
Write-Host "[6/7] Configuring Windows Firewall..." -ForegroundColor Green

try {
    # Check if rule exists
    $existingRule = Get-NetFirewallRule -DisplayName "Voice Assistant AI Server" -ErrorAction SilentlyContinue
    
    if ($existingRule) {
        Write-Host "Firewall rule already exists" -ForegroundColor Yellow
    } else {
        New-NetFirewallRule `
            -DisplayName "Voice Assistant AI Server" `
            -Direction Inbound `
            -LocalPort 8745 `
            -Protocol TCP `
            -Action Allow `
            -Profile Any `
            -Description "Voice Assistant AI Server WebSocket Port"
        
        Write-Host "Firewall rule created for port 8745" -ForegroundColor White
    }
} catch {
    Write-Host "WARNING: Failed to configure firewall" -ForegroundColor Yellow
    Write-Host $_.Exception.Message -ForegroundColor Red
}

# Create helper scripts
Write-Host ""
Write-Host "[7/7] Creating helper scripts..." -ForegroundColor Green

# Start script
$startScript = @"
@echo off
REM Start AI Server Phantom Process
echo Starting AI Server...
cd /d C:\qmsys\bin
echo LOGTO HAL | qm.exe
echo PHANTOM BP AI.SERVER | qm.exe -aHAL
echo AI Server started
pause
"@

Set-Content -Path "$AI_SERVER_DIR\start_ai_server.bat" -Value $startScript
Write-Host "Created: start_ai_server.bat" -ForegroundColor White

# Stop script
$stopScript = @"
@echo off
REM Stop AI Server Phantom Process
echo Stopping AI Server...
cd /d C:\qmsys\bin
REM Find and kill the phantom process
tasklist | findstr qm.exe
echo.
echo Please manually stop the phantom process if running
pause
"@

Set-Content -Path "$AI_SERVER_DIR\stop_ai_server.bat" -Value $stopScript
Write-Host "Created: stop_ai_server.bat" -ForegroundColor White

# Status script
$statusScript = @"
@echo off
REM Check AI Server Status
echo Checking AI Server status...
cd /d C:\qmsys\bin
echo.
echo Active QM processes:
tasklist | findstr qm.exe
echo.
echo Listening on port 8745:
netstat -an | findstr 8745
pause
"@

Set-Content -Path "$AI_SERVER_DIR\status_ai_server.bat" -Value $statusScript
Write-Host "Created: status_ai_server.bat" -ForegroundColor White

# View logs script
$logsScript = @"
@echo off
REM View AI Server Logs
cd /d C:\qmsys\hal
echo.
echo Recent AI Server log entries:
echo.
C:\qmsys\bin\qm.exe -aHAL << EOF
LIST VOICE.ASSISTANT.LOG WITH DATE >= TODAY - 1 BY.DSND DATE BY.DSND TIME
QUIT
EOF
pause
"@

Set-Content -Path "$AI_SERVER_DIR\view_logs.bat" -Value $logsScript
Write-Host "Created: view_logs.bat" -ForegroundColor White

Write-Host ""
Write-Host "============================================" -ForegroundColor Cyan
Write-Host "Setup Complete!" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "AI Server installed in: $accountPath" -ForegroundColor White
Write-Host ""
Write-Host "Helper scripts created:" -ForegroundColor Yellow
Write-Host "  start_ai_server.bat    - Start the AI server phantom process" -ForegroundColor White
Write-Host "  stop_ai_server.bat     - Stop the AI server" -ForegroundColor White
Write-Host "  status_ai_server.bat   - Check server status" -ForegroundColor White
Write-Host "  view_logs.bat          - View server logs" -ForegroundColor White
Write-Host ""
Write-Host "Port 8745 is now open in Windows Firewall" -ForegroundColor White
Write-Host ""

# Option to start now
if ($AutoStart) {
    $startNow = "Y"
} else {
    $startNow = Read-Host "Start the AI server now? (Y/N)"
}

if ($startNow -eq "Y" -or $startNow -eq "y") {
    Write-Host ""
    Write-Host "Starting AI Server..." -ForegroundColor Green
    
    # Start phantom process
    $phantomScript = @"
LOGTO HAL
PHANTOM BP AI.SERVER
QUIT
"@
    
    $phantomScript | & "$QM_BIN\qm.exe" -aHAL
    
    Start-Sleep -Seconds 2
    
    # Check if running
    Write-Host ""
    Write-Host "Checking status..." -ForegroundColor Green
    netstat -an | Select-String "8745"
    
    Write-Host ""
    Write-Host "AI Server should now be running" -ForegroundColor Green
    Write-Host "Check logs with: view_logs.bat" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Setup complete!" -ForegroundColor Cyan
Write-Host ""

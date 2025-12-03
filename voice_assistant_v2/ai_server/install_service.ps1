#
# Install AI Server as Windows Scheduled Task (Auto-start on Boot)
# Run as Administrator
#

param(
    [switch]$Uninstall = $false
)

# Check if running as Administrator
$currentPrincipal = New-Object Security.Principal.WindowsPrincipal([Security.Principal.WindowsIdentity]::GetCurrent())
$isAdmin = $currentPrincipal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)

if (-not $isAdmin) {
    Write-Host "ERROR: This script must be run as Administrator" -ForegroundColor Red
    Write-Host "Right-click PowerShell and select 'Run as Administrator'" -ForegroundColor Yellow
    exit 1
}

$TASK_NAME = "HAL Voice Assistant AI Server"
$SCRIPT_PATH = "$PSScriptRoot\start_phantom.ps1"

Write-Host "============================================" -ForegroundColor Cyan
Write-Host "AI Server Auto-Start Setup" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

if ($Uninstall) {
    # Uninstall the scheduled task
    Write-Host "Uninstalling scheduled task..." -ForegroundColor Yellow
    
    $task = Get-ScheduledTask -TaskName $TASK_NAME -ErrorAction SilentlyContinue
    
    if ($task) {
        Unregister-ScheduledTask -TaskName $TASK_NAME -Confirm:$false
        Write-Host "Scheduled task removed successfully" -ForegroundColor Green
    } else {
        Write-Host "Scheduled task not found" -ForegroundColor Yellow
    }
    
    Write-Host ""
    Write-Host "Uninstall complete!" -ForegroundColor Cyan
    exit 0
}

# Install the scheduled task
Write-Host "Installing AI Server as auto-start service..." -ForegroundColor Green
Write-Host ""

# Check if script exists
if (-not (Test-Path $SCRIPT_PATH)) {
    Write-Host "ERROR: Script not found: $SCRIPT_PATH" -ForegroundColor Red
    exit 1
}

Write-Host "Script: $SCRIPT_PATH" -ForegroundColor White
Write-Host ""

# Remove existing task if it exists
$existingTask = Get-ScheduledTask -TaskName $TASK_NAME -ErrorAction SilentlyContinue
if ($existingTask) {
    Write-Host "Removing existing scheduled task..." -ForegroundColor Yellow
    Unregister-ScheduledTask -TaskName $TASK_NAME -Confirm:$false
}

# Create the scheduled task action
$action = New-ScheduledTaskAction `
    -Execute "PowerShell.exe" `
    -Argument "-NoProfile -WindowStyle Hidden -ExecutionPolicy Bypass -File `"$SCRIPT_PATH`" -Monitor"

# Create the trigger (at startup)
$trigger = New-ScheduledTaskTrigger -AtStartup

# Create additional trigger (at logon of any user) as backup
$triggerLogon = New-ScheduledTaskTrigger -AtLogOn

# Set to run as SYSTEM account with highest privileges
$principal = New-ScheduledTaskPrincipal `
    -UserId "SYSTEM" `
    -LogonType ServiceAccount `
    -RunLevel Highest

# Task settings
$settings = New-ScheduledTaskSettingsSet `
    -AllowStartIfOnBatteries `
    -DontStopIfGoingOnBatteries `
    -StartWhenAvailable `
    -RestartCount 3 `
    -RestartInterval (New-TimeSpan -Minutes 1) `
    -ExecutionTimeLimit (New-TimeSpan -Days 365)

# Register the scheduled task
try {
    Register-ScheduledTask `
        -TaskName $TASK_NAME `
        -Action $action `
        -Trigger @($trigger, $triggerLogon) `
        -Principal $principal `
        -Settings $settings `
        -Description "HAL Voice Assistant AI Server - Auto-starts on boot and monitors the phantom process"
    
    Write-Host "Scheduled task created successfully!" -ForegroundColor Green
    Write-Host ""
    
    # Display task info
    Write-Host "Task Details:" -ForegroundColor Cyan
    Write-Host "  Name: $TASK_NAME" -ForegroundColor White
    Write-Host "  Trigger: At system startup" -ForegroundColor White
    Write-Host "  Action: Start phantom and monitor" -ForegroundColor White
    Write-Host "  Auto-restart: Yes (on failure)" -ForegroundColor White
    Write-Host ""
    
    # Ask if user wants to start now
    $startNow = Read-Host "Start the AI Server now? (Y/N)"
    
    if ($startNow -eq "Y" -or $startNow -eq "y") {
        Write-Host ""
        Write-Host "Starting AI Server..." -ForegroundColor Green
        
        Start-ScheduledTask -TaskName $TASK_NAME
        
        Write-Host "Task started. Checking status in 5 seconds..." -ForegroundColor Yellow
        Start-Sleep -Seconds 5
        
        # Check if running
        $listening = Get-NetTCPConnection -LocalPort 8745 -ErrorAction SilentlyContinue
        if ($listening) {
            Write-Host "✓ AI Server is running on port 8745" -ForegroundColor Green
        } else {
            Write-Host "⚠ AI Server may still be starting..." -ForegroundColor Yellow
            Write-Host "  Check logs: $PSScriptRoot\phantom_monitor.log" -ForegroundColor White
        }
    }
    
    Write-Host ""
    Write-Host "============================================" -ForegroundColor Cyan
    Write-Host "Installation Complete!" -ForegroundColor Cyan
    Write-Host "============================================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "The AI Server will now:" -ForegroundColor White
    Write-Host "  ✓ Start automatically on system boot" -ForegroundColor Green
    Write-Host "  ✓ Restart automatically if it crashes" -ForegroundColor Green
    Write-Host "  ✓ Run continuously in the background" -ForegroundColor Green
    Write-Host ""
    Write-Host "Management Commands:" -ForegroundColor Yellow
    Write-Host "  Start:   Start-ScheduledTask -TaskName '$TASK_NAME'" -ForegroundColor White
    Write-Host "  Stop:    Stop-ScheduledTask -TaskName '$TASK_NAME'" -ForegroundColor White
    Write-Host "  Status:  Get-ScheduledTask -TaskName '$TASK_NAME'" -ForegroundColor White
    Write-Host "  Remove:  .\install_service.ps1 -Uninstall" -ForegroundColor White
    Write-Host ""
    Write-Host "Logs:" -ForegroundColor Yellow
    Write-Host "  Monitor: $PSScriptRoot\phantom_monitor.log" -ForegroundColor White
    Write-Host "  QM logs: .\view_logs.bat" -ForegroundColor White
    Write-Host ""
    
} catch {
    Write-Host "ERROR: Failed to create scheduled task" -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Red
    exit 1
}

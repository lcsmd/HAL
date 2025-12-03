#
# Check AI Server Phantom Status
#

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "AI Server Status" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check scheduled task
Write-Host "[1] Scheduled Task Status:" -ForegroundColor Yellow
$taskName = "HAL Voice Assistant AI Server"
$task = Get-ScheduledTask -TaskName $taskName -ErrorAction SilentlyContinue

if ($task) {
    Write-Host "  Task Name: $($task.TaskName)" -ForegroundColor White
    Write-Host "  State: $($task.State)" -ForegroundColor $(if ($task.State -eq "Running") { "Green" } else { "Yellow" })
    
    $taskInfo = Get-ScheduledTaskInfo -TaskName $taskName
    Write-Host "  Last Run: $($taskInfo.LastRunTime)" -ForegroundColor White
    Write-Host "  Last Result: $($taskInfo.LastTaskResult) $(if ($taskInfo.LastTaskResult -eq 0) { '(Success)' } else { '(Error)' })" -ForegroundColor White
    Write-Host "  Next Run: $($taskInfo.NextRunTime)" -ForegroundColor White
} else {
    Write-Host "  ✗ Scheduled task not installed" -ForegroundColor Red
    Write-Host "  Run: .\install_service.ps1" -ForegroundColor Yellow
}

Write-Host ""

# Check QM processes
Write-Host "[2] QM Processes:" -ForegroundColor Yellow
$qmProcesses = Get-Process -Name "qm" -ErrorAction SilentlyContinue

if ($qmProcesses) {
    Write-Host "  Found $($qmProcesses.Count) QM process(es)" -ForegroundColor Green
    foreach ($proc in $qmProcesses) {
        Write-Host "    PID: $($proc.Id), Memory: $([math]::Round($proc.WorkingSet64/1MB, 2)) MB, CPU: $($proc.CPU)s" -ForegroundColor White
    }
} else {
    Write-Host "  ✗ No QM processes running" -ForegroundColor Red
}

Write-Host ""

# Check port 8745
Write-Host "[3] Network Status:" -ForegroundColor Yellow
$listening = Get-NetTCPConnection -LocalPort 8745 -State Listen -ErrorAction SilentlyContinue

if ($listening) {
    Write-Host "  ✓ Port 8745 is LISTENING" -ForegroundColor Green
    Write-Host "    Local: $($listening.LocalAddress):$($listening.LocalPort)" -ForegroundColor White
    Write-Host "    PID: $($listening.OwningProcess)" -ForegroundColor White
} else {
    Write-Host "  ✗ Port 8745 NOT listening" -ForegroundColor Red
    Write-Host "    AI Server may not be running" -ForegroundColor Yellow
}

# Check for active connections
$connections = Get-NetTCPConnection -LocalPort 8745 -State Established -ErrorAction SilentlyContinue
if ($connections) {
    Write-Host ""
    Write-Host "  Active connections:" -ForegroundColor Green
    foreach ($conn in $connections) {
        Write-Host "    $($conn.RemoteAddress):$($conn.RemotePort) -> $($conn.LocalAddress):$($conn.LocalPort)" -ForegroundColor White
    }
}

Write-Host ""

# Check monitor log
Write-Host "[4] Monitor Log:" -ForegroundColor Yellow
$logFile = "$PSScriptRoot\phantom_monitor.log"

if (Test-Path $logFile) {
    Write-Host "  Log file: $logFile" -ForegroundColor White
    $lastLines = Get-Content $logFile -Tail 5 -ErrorAction SilentlyContinue
    if ($lastLines) {
        Write-Host "  Last 5 entries:" -ForegroundColor White
        foreach ($line in $lastLines) {
            Write-Host "    $line" -ForegroundColor Gray
        }
    }
} else {
    Write-Host "  No monitor log found" -ForegroundColor Yellow
}

Write-Host ""

# Overall status
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Overall Status:" -ForegroundColor Cyan

if ($listening -and $qmProcesses) {
    Write-Host "  ✓ AI SERVER IS RUNNING" -ForegroundColor Green
    Write-Host "  Port 8745 is accepting connections" -ForegroundColor White
} elseif ($qmProcesses -and -not $listening) {
    Write-Host "  ⚠ AI SERVER MAY BE STARTING" -ForegroundColor Yellow
    Write-Host "  QM process exists but port not ready" -ForegroundColor White
} else {
    Write-Host "  ✗ AI SERVER IS NOT RUNNING" -ForegroundColor Red
    Write-Host ""
    Write-Host "  To start:" -ForegroundColor Yellow
    if ($task) {
        Write-Host "    Start-ScheduledTask -TaskName '$taskName'" -ForegroundColor White
    } else {
        Write-Host "    .\start_phantom.ps1" -ForegroundColor White
    }
}

Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

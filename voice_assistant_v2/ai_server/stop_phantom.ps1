#
# Stop AI Server Phantom Process
#

Write-Host "Stopping AI Server..." -ForegroundColor Yellow

# Stop the scheduled task if it exists
$taskName = "HAL Voice Assistant AI Server"
$task = Get-ScheduledTask -TaskName $taskName -ErrorAction SilentlyContinue

if ($task) {
    Write-Host "Stopping scheduled task..." -ForegroundColor White
    Stop-ScheduledTask -TaskName $taskName -ErrorAction SilentlyContinue
}

# Find and stop QM phantom processes
$qmProcesses = Get-Process -Name "qm" -ErrorAction SilentlyContinue

if ($qmProcesses) {
    Write-Host "Found $($qmProcesses.Count) QM process(es)" -ForegroundColor White
    
    foreach ($proc in $qmProcesses) {
        try {
            Write-Host "  Stopping process ID: $($proc.Id)" -ForegroundColor White
            Stop-Process -Id $proc.Id -Force
            Write-Host "  ✓ Stopped" -ForegroundColor Green
        } catch {
            Write-Host "  ✗ Failed to stop process $($proc.Id)" -ForegroundColor Red
        }
    }
} else {
    Write-Host "No QM processes found" -ForegroundColor Yellow
}

# Verify port is no longer listening
Start-Sleep -Seconds 2
$listening = Get-NetTCPConnection -LocalPort 8745 -ErrorAction SilentlyContinue

if ($listening) {
    Write-Host ""
    Write-Host "WARNING: Port 8745 still in use" -ForegroundColor Yellow
    Write-Host "Process may not have stopped completely" -ForegroundColor Yellow
} else {
    Write-Host ""
    Write-Host "✓ AI Server stopped successfully" -ForegroundColor Green
}

Write-Host ""

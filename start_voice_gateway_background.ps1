# Start Voice Gateway in background
$processInfo = New-Object System.Diagnostics.ProcessStartInfo
$processInfo.FileName = "python"
$processInfo.Arguments = "PY\voice_gateway.py"
$processInfo.WorkingDirectory = "C:\qmsys\hal"
$processInfo.WindowStyle = [System.Diagnostics.ProcessWindowStyle]::Minimized
$processInfo.CreateNoWindow = $false

$process = [System.Diagnostics.Process]::Start($processInfo)

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "HAL Voice Gateway Started" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Process ID: $($process.Id)" -ForegroundColor Yellow
Write-Host "Port: 8768" -ForegroundColor Yellow  
Write-Host "AI.SERVER Port: 8745" -ForegroundColor Yellow
Write-Host ""
Write-Host "To stop: Stop-Process -Id $($process.Id)" -ForegroundColor Gray
Write-Host ""

# Wait a moment then check port
Start-Sleep -Seconds 3
$port = netstat -ano | findstr :8768
if ($port) {
    Write-Host "[OK] Port 8768 is listening" -ForegroundColor Green
    Write-Host ""
    Write-Host "Voice Gateway is ready for clients!" -ForegroundColor Green
} else {
    Write-Host "[ERROR] Port 8768 not listening" -ForegroundColor Red  
}

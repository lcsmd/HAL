# Start QM Voice Listener (Medium Version)
Write-Host "Starting QM Voice Listener (Medium Version)..." -ForegroundColor Cyan

# Start in background
$process = Start-Process -FilePath "C:\qmsys\bin\qm.exe" `
    -ArgumentList "HAL" `
    -WorkingDirectory "C:\qmsys\bin" `
    -WindowStyle Hidden `
    -PassThru

Start-Sleep -Seconds 2

# Check if listening
$listening = Get-NetTCPConnection -LocalPort 8767 -State Listen -ErrorAction SilentlyContinue

if ($listening) {
    Write-Host "[OK] Voice Listener is now running on port 8767" -ForegroundColor Green
} else {
    Write-Host "[WARNING] Port 8767 not yet listening - may still be starting" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Process ID: $($process.Id)"
Write-Host "You may need to manually run: PHANTOM BP VOICE.LISTENER in the QM session"

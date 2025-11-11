# Automated QM Voice Listener startup
Write-Host "Starting QM Voice Listener..." -ForegroundColor Cyan

# Create a temporary script file for QM to execute
$qmScript = @"
LOGTO HAL
BASIC BP VOICE.LISTENER
CATALOG BP VOICE.LISTENER
PHANTOM BP VOICE.LISTENER
"@

$scriptPath = "C:\qmsys\hal\temp_start_listener.qm"
$qmScript | Out-File -FilePath $scriptPath -Encoding ASCII

# Start QM with the script
Start-Process -FilePath "C:\qmsys\bin\qm.exe" -ArgumentList "HAL < `"$scriptPath`"" -NoNewWindow -Wait

# Clean up
Start-Sleep -Seconds 2
Remove-Item $scriptPath -ErrorAction SilentlyContinue

# Verify
$listening = Get-NetTCPConnection -LocalPort 8767 -State Listen -ErrorAction SilentlyContinue
if ($listening) {
    Write-Host "[SUCCESS] Voice Listener is running on port 8767!" -ForegroundColor Green
} else {
    Write-Host "[WARNING] Port 8767 not listening yet" -ForegroundColor Yellow
}

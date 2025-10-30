# Test stunnel setup
Write-Host "Stopping any existing stunnel..."
Stop-Process -Name stunnel -Force -ErrorAction SilentlyContinue
Start-Sleep 2

Write-Host "`nStarting stunnel in background..."
Start-Process -FilePath "C:\Program Files (x86)\stunnel\bin\stunnel.exe" `
              -ArgumentList "c:\QMSYS\HAL\stunnel.conf" `
              -WindowStyle Hidden

Start-Sleep 3

Write-Host "`nChecking if ports are listening..."
$ports = netstat -an | Select-String "LISTENING"
$port8443 = $ports | Select-String "127.0.0.1:8443"
$port8444 = $ports | Select-String "127.0.0.1:8444"

if ($port8443) {
    Write-Host "✓ Port 8443 (OpenAI) is listening"
} else {
    Write-Host "✗ Port 8443 (OpenAI) is NOT listening"
}

if ($port8444) {
    Write-Host "✓ Port 8444 (Anthropic) is listening"
} else {
    Write-Host "✗ Port 8444 (Anthropic) is NOT listening"
}

Write-Host "`nTesting OpenAI connection..."
try {
    $response = Invoke-WebRequest -Uri "http://127.0.0.1:8443/v1/models" `
                                   -Headers @{"Authorization"="Bearer test"} `
                                   -TimeoutSec 5 `
                                   -ErrorAction Stop
    Write-Host "✓ Connected to OpenAI (got response)"
} catch {
    if ($_.Exception.Response.StatusCode -eq 401 -or $_.Exception.Response.StatusCode -eq 403) {
        Write-Host "✓ Connected to OpenAI (got auth error - expected with fake key)"
    } else {
        Write-Host "✗ Failed to connect: $($_.Exception.Message)"
    }
}

Write-Host "`nStunnel process status:"
Get-Process stunnel -ErrorAction SilentlyContinue | Select-Object Id, ProcessName, CPU

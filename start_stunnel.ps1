# Start stunnel for OpenQM AI integration
# This version runs stunnel in foreground mode which works correctly

$stunnelPath = "C:\Program Files (x86)\stunnel\bin\stunnel.exe"
$configPath = "c:\QMSYS\HAL\stunnel-fg.conf"

# Kill any existing stunnel processes
Write-Host "Stopping any existing stunnel processes..."
Stop-Process -Name stunnel -Force -ErrorAction SilentlyContinue
Start-Sleep -Seconds 1

if (Test-Path $stunnelPath) {
    Write-Host "Starting stunnel in foreground mode..."
    
    # Start stunnel in a new hidden window
    Start-Process -FilePath $stunnelPath `
                  -ArgumentList $configPath `
                  -WindowStyle Hidden
    
    Start-Sleep -Seconds 3
    
    # Verify it's running
    $port8443 = netstat -an | Select-String "LISTENING" | Select-String "127.0.0.1:8443"
    $port8444 = netstat -an | Select-String "LISTENING" | Select-String "127.0.0.1:8444"
    
    if ($port8443 -and $port8444) {
        Write-Host "✓ Stunnel is running successfully!"
        Write-Host "  - OpenAI:    localhost:8443 -> api.openai.com:443"
        Write-Host "  - Anthropic: localhost:8444 -> api.anthropic.com:443"
        Write-Host "`nYou can now use :ask.b with gpt-4o or claude models!"
    } else {
        Write-Host "✗ Stunnel failed to start properly"
        if ($port8443) { Write-Host "  ✓ Port 8443 (OpenAI) is listening" }
        else { Write-Host "  ✗ Port 8443 (OpenAI) is NOT listening" }
        if ($port8444) { Write-Host "  ✓ Port 8444 (Anthropic) is listening" }
        else { Write-Host "  ✗ Port 8444 (Anthropic) is NOT listening" }
    }
} else {
    Write-Host "✗ Stunnel not found at: $stunnelPath"
}

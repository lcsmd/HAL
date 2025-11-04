# Deploy voice.lcs.ai backend to HAProxy from Windows
# This script will SSH to ubu6 and configure HAProxy

$ErrorActionPreference = "Stop"

Write-Host "=" * 60 -ForegroundColor Cyan
Write-Host "HAProxy voice.lcs.ai Backend Deployment" -ForegroundColor Cyan
Write-Host "=" * 60 -ForegroundColor Cyan
Write-Host ""

$ubu6Host = "ubu6"
$ubu6Port = "2222"
$username = "lawr"
$password = "apgar-66"
$mv1IP = "10.1.34.103"

Write-Host "Target: ${username}@${ubu6Host}:${ubu6Port}" -ForegroundColor Yellow
Write-Host "Backend: MV1 (${mv1IP}:8765)" -ForegroundColor Yellow
Write-Host ""

# Create the complete script to run on ubu6
$remoteScript = @'
#!/bin/bash
echo "=== Configuring HAProxy for voice.lcs.ai ==="
echo ""

# Check if already configured
if sudo grep -q "is_voice" /etc/haproxy/haproxy.cfg; then
    echo "✓ Voice backend already exists!"
    exit 0
fi

# Backup
echo "1. Creating backup..."
sudo cp /etc/haproxy/haproxy.cfg /etc/haproxy/haproxy.cfg.backup.$(date +%Y%m%d_%H%M%S)
echo "   Done"

# Add ACL
echo "2. Adding ACL..."
sudo sed -i '/acl is_/a \    acl is_voice hdr(host) -i voice.lcs.ai' /etc/haproxy/haproxy.cfg
echo "   Done"

# Add use_backend
echo "3. Adding use_backend..."
sudo sed -i '/use_backend.*if is_/a \    use_backend voice_gateway if is_voice' /etc/haproxy/haproxy.cfg
echo "   Done"

# Add backend
echo "4. Adding backend..."
cat << 'EOF' | sudo tee -a /etc/haproxy/haproxy.cfg > /dev/null

# Voice Gateway WebSocket
backend voice_gateway
    mode http
    option http-server-close
    option forwardfor
    timeout tunnel 3600s
    timeout client 3600s
    timeout server 3600s
    http-request set-header X-Forwarded-Proto https
    http-request set-header X-Forwarded-Host %[req.hdr(Host)]
    server voice1 10.1.34.103:8765 check
EOF
echo "   Done"

# Test
echo "5. Testing configuration..."
if sudo haproxy -c -f /etc/haproxy/haproxy.cfg; then
    echo "   ✓ Configuration valid"
    
    # Reload
    echo "6. Reloading HAProxy..."
    if sudo systemctl reload haproxy; then
        echo "   ✓ HAProxy reloaded"
        echo ""
        echo "=== SUCCESS! voice.lcs.ai is now active ==="
        exit 0
    else
        echo "   ✗ Failed to reload HAProxy"
        exit 1
    fi
else
    echo "   ✗ Configuration invalid, restoring backup"
    sudo cp /etc/haproxy/haproxy.cfg.backup.* /etc/haproxy/haproxy.cfg 2>/dev/null
    exit 1
fi
'@

# Save script to temp file
$tempScript = "$env:TEMP\deploy_voice_backend.sh"
$remoteScript | Out-File -FilePath $tempScript -Encoding ASCII -NoNewline

Write-Host "Step 1: Copying script to ubu6..." -ForegroundColor Green
$scpCmd = "scp -P $ubu6Port `"$tempScript`" ${username}@${ubu6Host}:/tmp/deploy_voice_backend.sh"
Write-Host "Running: $scpCmd" -ForegroundColor Gray

# Use echo to pipe password
$scpProcess = "echo $password | scp -P $ubu6Port `"$tempScript`" ${username}@${ubu6Host}:/tmp/deploy_voice_backend.sh 2>&1"
try {
    $result = cmd /c $scpProcess
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✓ Script copied" -ForegroundColor Green
    } else {
        Write-Host "Note: SCP may require interactive password entry" -ForegroundColor Yellow
    }
} catch {
    Write-Host "Note: Will try SSH with interactive authentication" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Step 2: Executing script on ubu6..." -ForegroundColor Green
Write-Host "You may be prompted for password: $password" -ForegroundColor Yellow
Write-Host ""

# Execute the script via SSH
$sshCmd = "ssh -p $ubu6Port ${username}@${ubu6Host} 'bash /tmp/deploy_voice_backend.sh'"
Write-Host "Running: $sshCmd" -ForegroundColor Gray
Write-Host ""

# Run SSH command
& ssh -p $ubu6Port "${username}@${ubu6Host}" 'bash /tmp/deploy_voice_backend.sh'

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "=" * 60 -ForegroundColor Green
    Write-Host "SUCCESS! voice.lcs.ai backend is configured!" -ForegroundColor Green
    Write-Host "=" * 60 -ForegroundColor Green
    Write-Host ""
    Write-Host "Next steps:" -ForegroundColor Cyan
    Write-Host "1. Test: wscat -c wss://voice.lcs.ai" -ForegroundColor White
    Write-Host "2. Start QM Voice Listener: PHANTOM VOICE.LISTENER" -ForegroundColor White
    Write-Host "3. Deploy Mac client and start talking to HAL!" -ForegroundColor White
} else {
    Write-Host ""
    Write-Host "=" * 60 -ForegroundColor Red
    Write-Host "Failed to configure HAProxy" -ForegroundColor Red
    Write-Host "=" * 60 -ForegroundColor Red
    Write-Host ""
    Write-Host "Troubleshooting:" -ForegroundColor Yellow
    Write-Host "1. Check if you can SSH manually: ssh -p 2222 lawr@ubu6" -ForegroundColor White
    Write-Host "2. Verify password: apgar-66" -ForegroundColor White
    Write-Host "3. Try manual method (see APPLY_HAPROXY_CONFIG.md)" -ForegroundColor White
}

# Cleanup
Remove-Item $tempScript -ErrorAction SilentlyContinue

Write-Host ""
Write-Host "Press any key to continue..."
$null = $Host.UI.RawUI.ReadKey('NoEcho,IncludeKeyDown')

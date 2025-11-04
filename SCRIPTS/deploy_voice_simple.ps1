# Simple HAProxy voice.lcs.ai deployment
Write-Host "Deploying voice.lcs.ai backend to HAProxy..." -ForegroundColor Cyan
Write-Host ""

$script = @"
sudo bash -c 'if grep -q is_voice /etc/haproxy/haproxy.cfg; then echo Already configured; exit 0; fi; cp /etc/haproxy/haproxy.cfg /etc/haproxy/haproxy.cfg.backup.\$(date +%Y%m%d_%H%M%S); sed -i "/acl is_/a \    acl is_voice hdr(host) -i voice.lcs.ai" /etc/haproxy/haproxy.cfg; sed -i "/use_backend.*if is_/a \    use_backend voice_gateway if is_voice" /etc/haproxy/haproxy.cfg; cat >> /etc/haproxy/haproxy.cfg << EOF

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
haproxy -c -f /etc/haproxy/haproxy.cfg && systemctl reload haproxy && echo SUCCESS || echo FAILED'
"@

Write-Host "Connecting to ubu6..." -ForegroundColor Yellow
Write-Host "You will be prompted for password: apgar-66" -ForegroundColor Yellow
Write-Host ""

ssh -p 2222 lawr@ubu6 $script

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "SUCCESS! voice.lcs.ai is configured!" -ForegroundColor Green
} else {
    Write-Host ""
    Write-Host "Failed. Try manual method (see APPLY_HAPROXY_CONFIG.md)" -ForegroundColor Red
}

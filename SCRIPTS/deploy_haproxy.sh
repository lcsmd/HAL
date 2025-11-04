#!/bin/bash
echo "Deploying voice.lcs.ai backend to HAProxy..."

# Backup
sudo cp /etc/haproxy/haproxy.cfg /etc/haproxy/haproxy.cfg.backup.$(date +%Y%m%d_%H%M%S)
echo "Config backed up"

# Check if already exists
if sudo grep -q "is_voice" /etc/haproxy/haproxy.cfg; then
    echo "Voice backend already configured!"
    exit 0
fi

# Add ACL
sudo sed -i '/acl is_/a \    acl is_voice hdr(host) -i voice.lcs.ai' /etc/haproxy/haproxy.cfg
echo "ACL added"

# Add use_backend
sudo sed -i '/use_backend.*if is_/a \    use_backend voice_gateway if is_voice' /etc/haproxy/haproxy.cfg
echo "Routing added"

# Add backend
sudo tee -a /etc/haproxy/haproxy.cfg > /dev/null << 'EOF'

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
echo "Backend added"

# Test and reload
echo "Testing configuration..."
if sudo haproxy -c -f /etc/haproxy/haproxy.cfg; then
    echo "Configuration valid, reloading..."
    sudo systemctl reload haproxy
    echo ""
    echo "SUCCESS! voice.lcs.ai is now active!"
else
    echo "ERROR: Invalid configuration, restoring backup"
    sudo cp /etc/haproxy/haproxy.cfg.backup.* /etc/haproxy/haproxy.cfg
    exit 1
fi

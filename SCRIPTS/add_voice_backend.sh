#!/bin/bash
# Add voice.lcs.ai backend to HAProxy

echo "=== Adding voice.lcs.ai Backend to HAProxy ==="
echo ""

# Backup current config
echo "1. Backing up current configuration..."
sudo cp /etc/haproxy/haproxy.cfg /etc/haproxy/haproxy.cfg.backup.$(date +%Y%m%d_%H%M%S)
echo "  Backup created"
echo ""

# Check if voice backend already exists
if sudo grep -q "is_voice" /etc/haproxy/haproxy.cfg; then
    echo "  Voice backend already exists!"
    exit 0
fi

# Add ACL for voice in frontend section
echo "2. Adding voice ACL to frontend..."
sudo sed -i '/acl is_/a \    acl is_voice hdr(host) -i voice.lcs.ai' /etc/haproxy/haproxy.cfg
echo "  ACL added"
echo ""

# Add use_backend for voice
echo "3. Adding use_backend for voice..."
sudo sed -i '/use_backend.*if is_/a \    use_backend voice_gateway if is_voice' /etc/haproxy/haproxy.cfg
echo "  use_backend added"
echo ""

# Add voice backend at the end
echo "4. Adding voice_gateway backend..."
cat << 'EOF' | sudo tee -a /etc/haproxy/haproxy.cfg

# Voice Gateway WebSocket
backend voice_gateway
    mode http
    option http-server-close
    option forwardfor
    # WebSocket support
    timeout tunnel 3600s
    timeout client 3600s
    timeout server 3600s
    http-request set-header X-Forwarded-Proto https
    http-request set-header X-Forwarded-Host %[req.hdr(Host)]
    server voice1 10.1.34.103:8765 check
EOF
echo "  Backend added"
echo ""

# Test configuration
echo "5. Testing HAProxy configuration..."
if sudo haproxy -c -f /etc/haproxy/haproxy.cfg; then
    echo "  Configuration is valid!"
    echo ""
    
    # Reload HAProxy
    echo "6. Reloading HAProxy..."
    sudo systemctl reload haproxy
    
    if [ $? -eq 0 ]; then
        echo "  HAProxy reloaded successfully!"
        echo ""
        echo "=== voice.lcs.ai is now active ==="
    else
        echo "  ERROR: Failed to reload HAProxy"
        exit 1
    fi
else
    echo "  ERROR: Configuration is invalid!"
    echo "  Restoring backup..."
    sudo cp /etc/haproxy/haproxy.cfg.backup.* /etc/haproxy/haproxy.cfg
    exit 1
fi

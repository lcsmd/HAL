# HAProxy Configuration for HAL Voice Gateway

## Overview
Configure HAProxy to route external WebSocket connections to the HAL Voice Gateway.

## HAProxy Configuration

Add to your `haproxy.cfg`:

```haproxy
#---------------------------------------------------------------------
# HAL Voice Gateway - WebSocket Support
#---------------------------------------------------------------------
frontend hal_voice_frontend
    bind *:443 ssl crt /path/to/certificate.pem
    bind *:80
    
    # Redirect HTTP to HTTPS
    redirect scheme https code 301 if !{ ssl_fc }
    
    # WebSocket upgrade headers
    acl is_websocket hdr(Upgrade) -i WebSocket
    acl is_websocket hdr_beg(Host) -i hal.
    
    # Route to HAL Voice Gateway
    use_backend hal_voice_backend if is_websocket
    
    # Default backend for other traffic
    default_backend hal_voice_backend

backend hal_voice_backend
    # WebSocket specific settings
    option http-server-close
    option forceclose
    
    # Timeout settings for WebSocket
    timeout connect 5s
    timeout client 1h
    timeout server 1h
    timeout tunnel 1h
    
    # Health check
    option httpchk GET / HTTP/1.1\r\nHost:\ localhost\r\nUpgrade:\ websocket
    
    # Route to Voice Gateway
    server voice_gateway localhost:8768 check

#---------------------------------------------------------------------
# Alternative: Use path-based routing
#---------------------------------------------------------------------
frontend hal_https_frontend
    bind *:443 ssl crt /path/to/certificate.pem
    
    # Route /voice or /ws to Voice Gateway
    acl is_voice path_beg /voice /ws
    use_backend hal_voice_backend if is_voice
    
    # Other paths can go elsewhere
    default_backend other_backend

# Stats page (optional)
listen stats
    bind *:8404
    stats enable
    stats uri /stats
    stats refresh 30s
    stats auth admin:password
```

## Simple Configuration (No SSL)

For testing or internal network only:

```haproxy
frontend hal_simple
    bind *:80
    
    acl is_websocket hdr(Upgrade) -i WebSocket
    use_backend hal_voice_backend if is_websocket
    default_backend hal_voice_backend

backend hal_voice_backend
    timeout tunnel 1h
    server voice_gateway localhost:8768 check
```

## DNS/Domain Setup

### Option 1: Subdomain
Point `hal.yourdomain.com` to your server IP:
```
hal.yourdomain.com.  A  123.45.67.89
```

Then use: `https://hal.yourdomain.com`

### Option 2: Path-based
Use existing domain with path:
```
https://yourdomain.com/voice
```

Configure HAProxy path routing (see Alternative config above).

### Option 3: IP-based (No DNS)
Direct to IP with SSL:
```
https://123.45.67.89
```

Requires valid SSL certificate for the IP.

## SSL Certificate

### Option 1: Let's Encrypt (Free)
```bash
# Install certbot
apt-get install certbot

# Get certificate for your domain
certbot certonly --standalone -d hal.yourdomain.com

# Combine cert and key for HAProxy
cat /etc/letsencrypt/live/hal.yourdomain.com/fullchain.pem \\
    /etc/letsencrypt/live/hal.yourdomain.com/privkey.pem \\
    > /etc/haproxy/certs/hal.yourdomain.com.pem

# Set permissions
chmod 600 /etc/haproxy/certs/hal.yourdomain.com.pem
```

### Option 2: Self-Signed (Testing Only)
```bash
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \\
    -keyout /etc/haproxy/certs/selfsigned.key \\
    -out /etc/haproxy/certs/selfsigned.crt

cat /etc/haproxy/certs/selfsigned.crt \\
    /etc/haproxy/certs/selfsigned.key \\
    > /etc/haproxy/certs/selfsigned.pem
```

## Firewall Rules

### Windows (Voice Gateway)
```powershell
# Allow HAProxy to connect to Voice Gateway
New-NetFirewallRule -DisplayName "HAL Voice Gateway" \\
    -Direction Inbound -LocalPort 8768 -Protocol TCP -Action Allow
```

### Linux (HAProxy Server)
```bash
# Allow HTTPS
ufw allow 443/tcp

# Allow HTTP (for redirect)
ufw allow 80/tcp

# If HAProxy on different machine, allow it to connect to Windows
# On Windows, allow the HAProxy server IP
```

## Testing

### Test HAProxy Config
```bash
haproxy -c -f /etc/haproxy/haproxy.cfg
```

### Reload HAProxy
```bash
systemctl reload haproxy
```

### Test Connection
```bash
# From Mac
curl -i -N -H "Connection: Upgrade" \\
     -H "Upgrade: websocket" \\
     -H "Host: hal.yourdomain.com" \\
     https://hal.yourdomain.com/
```

## Mac Client URLs

After HAProxy setup, Mac clients use:

**Local Network:**
```bash
HAL_SERVER_URL=http://192.168.1.100:8768
```

**External via HAProxy:**
```bash
HAL_SERVER_URL=https://hal.yourdomain.com
```

**Path-based routing:**
```bash
HAL_SERVER_URL=https://yourdomain.com/voice
```

## Troubleshooting

### Connection Refused
- Check HAProxy is running: `systemctl status haproxy`
- Check Voice Gateway is running on port 8768
- Check firewall allows connections

### WebSocket Upgrade Failed
- Verify `Upgrade: websocket` header is being passed
- Check HAProxy logs: `tail -f /var/log/haproxy.log`
- Ensure timeout tunnel is set (not timing out)

### SSL Certificate Errors
- Verify certificate is valid: `openssl s_client -connect hal.yourdomain.com:443`
- Check certificate permissions (should be 600)
- Ensure combined cert includes both cert and key

### HAProxy Can't Reach Voice Gateway
- If HAProxy on different machine, check network connectivity
- Verify Windows firewall allows connection from HAProxy server
- Test: `telnet windows_ip 8768` from HAProxy server

## Architecture

```
Internet/WAN
    ↓
HAProxy (Port 443/80) - SSL Termination
    ↓
Voice Gateway (Port 8768) - WebSocket
    ↓
QM Listener (Port 8767) - Native QM
    ↓
HAL QM Database
```

## Security Considerations

- Use SSL/TLS for external access
- Consider adding WebSocket authentication
- Use strong SSL certificates (not self-signed for production)
- Keep HAProxy updated
- Monitor logs for suspicious activity
- Consider rate limiting in HAProxy

# HAProxy Configuration for HAL Voice Interface

**Infrastructure**: HAProxy on ubu6 with wildcard SSL cert for *.lcs.ai

---

## Current Setup

### Existing Subdomains
- `ollama.lcs.ai` → ubuai:11434 (Ollama LLM server)
- `speech.lcs.ai` → ubuai:???? (Speech transcription + TTS)
- `hal.lcs.ai` → Open-WebUI
- `next.lcs.ai` → Nextcloud

### DNS
- Windows Server Domain Controller (q1)
- Wildcard DNS: *.lcs.ai → ubu6 (HAProxy)

---

## New Subdomains Needed for Voice Interface

### 1. `voice.lcs.ai` - Voice Gateway
**Backend**: Windows QM Server (this machine)  
**Port**: 8765 (WebSocket)  
**Protocol**: HTTPS/WSS (WebSocket Secure)

**HAProxy Backend Configuration**:
```haproxy
# Voice Gateway WebSocket
frontend https_in
    bind *:443 ssl crt /etc/haproxy/certs/lcs.ai.pem
    
    # Voice Gateway WebSocket
    acl is_voice hdr(host) -i voice.lcs.ai
    use_backend voice_gateway if is_voice

backend voice_gateway
    mode http
    option http-server-close
    option forwardfor
    # Enable WebSocket
    timeout tunnel 3600s
    timeout client 3600s
    timeout server 3600s
    http-request set-header X-Forwarded-Proto https
    server voice1 qm-server:8765 check
```

### 2. `speech.lcs.ai` - Already Configured ✓
**Backend**: ubuai (Speech transcription + TTS)  
**Endpoints Needed**:
- `POST /transcribe` - Faster-Whisper transcription
- `POST /tts` - Text-to-Speech generation
- `GET /health` - Health check

**Verify Configuration**:
```haproxy
backend speech_service
    mode http
    balance roundrobin
    option httpchk GET /health
    server speech1 ubuai:9000 check
```

### 3. `ollama.lcs.ai` - Already Configured ✓
**Backend**: ubuai:11434  
**Used For**: Local LLM inference

---

## Updated Voice Gateway Configuration

### New URLs (Using HAProxy)

```json
{
  "gateway": {
    "public_url": "wss://voice.lcs.ai",
    "local_url": "ws://localhost:8765"
  },
  "whisper": {
    "url": "https://speech.lcs.ai/transcribe"
  },
  "ollama": {
    "url": "https://ollama.lcs.ai"
  },
  "tts": {
    "url": "https://speech.lcs.ai/tts"
  }
}
```

### Benefits
- ✅ Single wildcard SSL certificate
- ✅ Centralized routing through HAProxy
- ✅ Easy to add/remove backends
- ✅ Load balancing capability
- ✅ Health checks
- ✅ Secure WebSocket (WSS)

---

## HAProxy Complete Configuration Example

```haproxy
global
    log /dev/log local0
    log /dev/log local1 notice
    chroot /var/lib/haproxy
    stats socket /run/haproxy/admin.sock mode 660 level admin
    stats timeout 30s
    user haproxy
    group haproxy
    daemon
    
    # SSL
    ssl-default-bind-ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256
    ssl-default-bind-options ssl-min-ver TLSv1.2 no-tls-tickets
    tune.ssl.default-dh-param 2048

defaults
    log global
    mode http
    option httplog
    option dontlognull
    timeout connect 5000
    timeout client 50000
    timeout server 50000

frontend http_in
    bind *:80
    # Redirect HTTP to HTTPS
    redirect scheme https code 301

frontend https_in
    bind *:443 ssl crt /etc/haproxy/certs/lcs.ai.pem
    
    # ACLs for subdomain routing
    acl is_ollama hdr(host) -i ollama.lcs.ai
    acl is_speech hdr(host) -i speech.lcs.ai
    acl is_hal hdr(host) -i hal.lcs.ai
    acl is_next hdr(host) -i next.lcs.ai
    acl is_voice hdr(host) -i voice.lcs.ai
    
    # WebSocket detection
    acl is_websocket hdr(Upgrade) -i WebSocket
    
    # Backend selection
    use_backend ollama_backend if is_ollama
    use_backend speech_backend if is_speech
    use_backend hal_backend if is_hal
    use_backend nextcloud_backend if is_next
    use_backend voice_gateway if is_voice is_websocket
    use_backend voice_gateway if is_voice

# Ollama LLM (Already configured)
backend ollama_backend
    mode http
    balance roundrobin
    option httpchk GET /api/tags
    timeout server 120s
    server ollama1 ubuai:11434 check

# Speech (Whisper + TTS) - Needs verification
backend speech_backend
    mode http
    balance roundrobin
    option httpchk GET /health
    timeout server 60s
    server speech1 ubuai:9000 check
    # If TTS is on different port:
    # server tts1 ubuai:5000 check backup

# HAL Open-WebUI (Already configured)
backend hal_backend
    mode http
    server hal1 hal-webui-server:port check

# Nextcloud (Already configured)
backend nextcloud_backend
    mode http
    server next1 nextcloud-server:port check

# Voice Gateway (NEW)
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
    server voice1 qm-server:8765 check
```

---

## Testing the Setup

### 1. Test Ollama (Should Already Work)
```bash
curl https://ollama.lcs.ai/api/tags
```

Expected: JSON list of models

### 2. Test Speech Service
```bash
# Test transcription endpoint
curl https://speech.lcs.ai/health

# Test transcription (with sample audio)
curl -X POST https://speech.lcs.ai/transcribe \
  -H "Content-Type: application/json" \
  -d '{"audio": "base64_audio_data", "language": "en"}'

# Test TTS
curl -X POST https://speech.lcs.ai/tts \
  -H "Content-Type: application/json" \
  -d '{"text": "Hello world", "voice": "en_US-lessac-medium"}'
```

### 3. Test Voice Gateway (Once Configured)
```bash
# From Mac or Windows
wscat -c wss://voice.lcs.ai

# Or use Python
python -c "
import asyncio
import websockets

async def test():
    async with websockets.connect('wss://voice.lcs.ai') as ws:
        msg = await ws.recv()
        print(f'Received: {msg}')

asyncio.run(test())
"
```

---

## Client Configuration Updates

### Mac Voice Client
```python
# Change from:
GATEWAY_URL = "ws://localhost:8765"

# To:
GATEWAY_URL = "wss://voice.lcs.ai"
```

### Windows Testing
```python
# Local testing (on QM server):
GATEWAY_URL = "ws://localhost:8765"

# Remote testing (from other machines):
GATEWAY_URL = "wss://voice.lcs.ai"
```

---

## Security Considerations

### 1. WebSocket Security
- ✅ WSS (WebSocket Secure) via HAProxy SSL
- ✅ Wildcard certificate for *.lcs.ai
- ⚠️ Consider adding authentication token in WebSocket handshake

### 2. API Security
- ⚠️ Speech API should have rate limiting
- ⚠️ Consider API keys for external access
- ✅ Internal network traffic can be HTTP (behind HAProxy)

### 3. Firewall Rules
**ubu6 (HAProxy)**:
- Port 80 (HTTP → HTTPS redirect)
- Port 443 (HTTPS/WSS)

**ubuai (AI Services)**:
- Port 11434 (Ollama) - Internal only
- Port 9000 (Whisper) - Internal only
- Port 5000 (TTS) - Internal only

**qm-server (Voice Gateway)**:
- Port 8765 (WebSocket) - Internal only
- Port 8767 (QM Listener) - Internal only

---

## Deployment Steps

### Step 1: Verify Existing Services
```bash
# SSH to ubu6 (HAProxy)
ssh ubu6

# Check current backends
sudo cat /etc/haproxy/haproxy.cfg | grep backend

# Test ollama
curl https://ollama.lcs.ai/api/tags

# Test speech
curl https://speech.lcs.ai/health
```

### Step 2: Add Voice Gateway Backend
```bash
# Edit HAProxy config
sudo nano /etc/haproxy/haproxy.cfg

# Add voice_gateway backend (see config above)

# Test configuration
sudo haproxy -c -f /etc/haproxy/haproxy.cfg

# Reload HAProxy (zero downtime)
sudo systemctl reload haproxy
```

### Step 3: Start Voice Gateway on QM Server
```powershell
cd C:\qmsys\hal\PY
python voice_gateway.py
```

### Step 4: Test from External Client
```bash
# From Mac or any machine
wscat -c wss://voice.lcs.ai
```

---

## Monitoring

### HAProxy Stats
```bash
# Enable stats page in haproxy.cfg
listen stats
    bind *:9000
    stats enable
    stats uri /stats
    stats refresh 30s
    stats auth admin:password

# Access at: http://ubu6:9000/stats
```

### Health Checks
```bash
# Check all backends
curl https://ollama.lcs.ai/api/tags
curl https://speech.lcs.ai/health
curl https://hal.lcs.ai/
curl https://voice.lcs.ai/ (should upgrade to WebSocket)
```

---

## Troubleshooting

### Voice Gateway Not Accessible
```bash
# On ubu6
sudo tail -f /var/log/haproxy.log

# Check if backend is down
echo "show servers state" | sudo socat stdio /var/run/haproxy/admin.sock

# Manual test
curl http://qm-server:8765
```

### Speech Service Issues
```bash
# SSH to ubuai
ssh ubuai

# Check if service is running
ps aux | grep whisper
ps aux | grep tts

# Check ports
netstat -tulpn | grep :9000
netstat -tulpn | grep :5000
```

### SSL Certificate Issues
```bash
# Check certificate
openssl s_client -connect voice.lcs.ai:443 -servername voice.lcs.ai

# Verify wildcard cert includes voice.lcs.ai
openssl x509 -in /etc/haproxy/certs/lcs.ai.pem -text -noout | grep DNS
```

---

## Next Steps

1. **Verify speech.lcs.ai endpoints**
   - What API does it expose?
   - Is it Faster-Whisper compatible?
   - Does it have TTS?

2. **Add voice.lcs.ai backend to HAProxy**
   - Configure WebSocket support
   - Add health checks
   - Test from external client

3. **Update Voice Gateway**
   - Use HTTPS URLs for speech and ollama
   - Handle SSL connections
   - Test transcription integration

4. **Deploy Mac Client**
   - Use wss://voice.lcs.ai
   - Test end-to-end flow

---

## Questions for You

1. **What API does speech.lcs.ai expose?**
   - Is it Faster-Whisper?
   - What are the endpoints?
   - POST /transcribe format?

2. **What's the QM server hostname for HAProxy?**
   - Is it `qm-server`, `q1`, or something else?
   - What's the internal IP?

3. **Do you want voice.lcs.ai subdomain?**
   - Or different name?
   - Should it be public or internal only?

Let me know these details and I can generate the exact HAProxy configuration!

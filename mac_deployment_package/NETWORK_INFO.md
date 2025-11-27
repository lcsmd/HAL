# HAL Network Configuration

## Your Network Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        HAL Network                              │
└─────────────────────────────────────────────────────────────────┘

┌──────────────────┐
│  MacBook Pro     │  ← Your client (this machine)
│  (Mac Client)    │     Text/Voice interface
└────────┬─────────┘
         │
         │ WebSocket (ws://10.1.34.103:8768)
         │
         ↓
┌──────────────────┐
│  QM Server       │  ← Windows Server
│  10.1.34.103     │     OpenQM Database
│                  │
│  Services:       │     ┌─────────────────────┐
│  - HAL Database  │────▶│ WebSocket Listener  │ (Phantom Process)
│  - Intent Engine │     │ Port 8768           │ Runs in QM
│  - Query Router  │     └─────────────────────┘ Auto-started
└────────┬─────────┘
         │
         │ HTTP/TCP
         │
         ↓
┌──────────────────┐
│  AI Server       │  ← Linux Server (Ubuntu)
│  10.1.10.20      │     Ollama (LLM models)
│                  │     Faster-Whisper (STT)
│  Services:       │
│  - Ollama:11434  │
│  - Whisper:9000  │
└──────────────────┘

         ↑
         │ Load Balancing (optional)
         │
┌──────────────────┐
│  HAProxy         │  ← Load Balancer
│  10.1.50.100     │     SSH access: port 2222
│                  │     Can route traffic
│  Access:         │
│  - SSH:2222      │
└──────────────────┘
```

---

## Server Details

### 1. QM Server (Windows)
- **IP**: `10.1.34.103`
- **Username**: `lawr`
- **OS**: Windows Server
- **Access**: RDP, PowerShell remoting
- **Services**:
  - OpenQM Database (HAL account)
  - **WebSocket Listener: Port `8768`** (Phantom Process in QM)
    - Runs directly in QM (not Python)
    - Started automatically as phantom process
    - Handles WebSocket connections natively
- **Purpose**: 
  - Database storage
  - Intent detection
  - Query routing
  - Business logic
  - Direct WebSocket communication

### 2. AI Server (Linux) - GPU-Accelerated
- **IP**: `10.1.10.20`
- **Hostname**: `ubuai`
- **Username**: `lawr`
- **OS**: Ubuntu Linux
- **Hardware**: GPU-equipped server
- **Access**: `ssh lawr@10.1.10.20`
- **Services**:
  - **Faster-Whisper: Port `9000`** - Speech-to-Text (STT)
    - GPU-accelerated transcription
    - Real-time voice recognition
    - Minimal latency for voice interface
  - **Ollama: Port `11434`** - Large Language Model inference
    - GPU-accelerated LLM
    - Multiple models available (deepseek, llama, etc.)
    - Used by QM for AI-powered responses
  - **TTS Service** (if configured) - Text-to-Speech
    - GPU-accelerated voice synthesis
    - Natural voice output
- **Purpose**:
  - Real-time AI inference with minimal latency
  - Voice transcription (STT)
  - Voice synthesis (TTS)
  - LLM processing for intelligent responses
  - GPU acceleration for sub-second response times

### 3. HAProxy (Linux)
- **IP**: `10.1.50.100`
- **Username**: `lawr`
- **SSH Port**: `2222`
- **Access**: `ssh lawr@10.1.50.100 -p 2222`
- **Purpose**:
  - Load balancing
  - SSL termination
  - Service routing

### 4. Proxmox VE (Virtualization Host)
- **IP**: `10.1.33.1`
- **Username**: `root`
- **Web UI**: `https://10.1.33.1:8006`
- **SSH Access**: `ssh root@10.1.33.1`
- **Purpose**:
  - Virtual machine management
  - Infrastructure host
  - May host above VMs

---

## Port Configuration

| Service | Server | Port | Protocol | Purpose |
|---------|--------|------|----------|---------|
| WebSocket Listener | 10.1.34.103 | 8768 | WebSocket | Mac client connection (QM phantom) |
| **Faster-Whisper (STT)** | 10.1.10.20 | 9000 | HTTP | Speech-to-Text (GPU accelerated) |
| **Ollama (LLM)** | 10.1.10.20 | 11434 | HTTP | AI language model inference (GPU) |
| TTS Service | 10.1.10.20 | (TBD) | HTTP | Text-to-Speech (if configured) |
| HAProxy SSH | 10.1.50.100 | 2222 | SSH | Admin access |
| HAProxy HTTP | 10.1.50.100 | 80/443 | HTTP/HTTPS | (if configured) |

---

## Message Flow

### Text Query Flow
```
1. Mac Client sends text query
   ↓ WebSocket ws://10.1.34.103:8768
2. QM WebSocket Listener (phantom) receives
   ↓ Native QM processing
3. Intent detected (MEDICATION/APPOINTMENT/etc.)
   ↓ Route to handler
4. Handler queries database
   ↓ OpenQM file operations
5. Response generated
   ↓ Direct response
6. WebSocket Listener sends back
   ↓ WebSocket response
7. Mac Client displays result

Note: All processing happens in QM - no separate Python gateway!
```

### Voice Query Flow (Full Voice Mode)
```
1. Mac Client captures audio (microphone)
   ↓ WebSocket audio stream
2. QM WebSocket Listener receives
   ↓ Forwards to AI Server
3. Faster-Whisper (10.1.10.20:9000) transcribes
   ↓ Returns text to QM
4. QM processes text (same as text flow)
   ↓ Intent detection & handler
5. Response generated in QM
   ↓ WebSocket response
6. Mac Client receives text
   ↓ TTS (local on Mac)
7. Mac Client speaks response

Note: Transcription on AI server, processing in QM, TTS on Mac
```

---

## Network Requirements

### Mac Client
- ✅ Network access to `10.1.34.103:8768`
- ✅ Can reach QM Server subnet (10.1.34.0/24)
- ⚠️ Firewall allows outbound WebSocket
- ⚠️ No VPN blocking internal IPs

### QM Server (Windows)
- ✅ Firewall allows inbound port 8768
- ✅ Can reach AI Server `10.1.10.20`
- ✅ Voice Gateway service running
- ✅ QM Voice Listener running

### AI Server (Linux)
- ✅ Ollama service running on 11434
- ✅ Faster-Whisper running on 9000
- ✅ Firewall allows connections from QM Server

---

## Firewall Configuration

### On QM Server (Windows)
```powershell
# Allow Voice Gateway port
New-NetFirewallRule -DisplayName "HAL Voice Gateway" -Direction Inbound -LocalPort 8768 -Protocol TCP -Action Allow

# Allow Voice Listener port (internal)
New-NetFirewallRule -DisplayName "HAL Voice Listener" -Direction Inbound -LocalPort 8767 -Protocol TCP -Action Allow
```

### On AI Server (Linux)
```bash
# Allow Ollama
sudo ufw allow 11434/tcp

# Allow Faster-Whisper
sudo ufw allow 9000/tcp
```

### On HAProxy
```bash
# SSH on custom port
sudo ufw allow 2222/tcp

# HTTP/HTTPS (if configured)
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
```

---

## Client Configuration

### Environment Variables (Mac)

**Quick Setup**:
```bash
source network_config.sh
```

**Manual Setup**:
```bash
export HAL_GATEWAY_URL="ws://10.1.34.103:8768"
export OLLAMA_HOST="10.1.10.20"
export WHISPER_URL="http://10.1.10.20:9000/transcribe"
```

**Permanent Setup** (add to `~/.zshrc`):
```bash
echo 'export HAL_GATEWAY_URL="ws://10.1.34.103:8768"' >> ~/.zshrc
source ~/.zshrc
```

---

## Connection Testing

### Test 1: Ping QM Server
```bash
ping -c 3 10.1.34.103
```
Expected: Replies received

### Test 2: Check Port 8768
```bash
nc -zv 10.1.34.103 8768
```
Expected: Connection succeeded

### Test 3: Full Connection Test
```bash
bash test_connection.sh
```
Expected: All tests pass

### Test 4: HAProxy SSH
```bash
ssh lawr@10.1.50.100 -p 2222
# Password: apgar-66
```
Expected: SSH login prompt

### Test 5: AI Server SSH
```bash
ssh lawr@10.1.10.20
# Password: apgar-66
```
Expected: SSH login prompt

### Test 6: Proxmox Access
```bash
# SSH
ssh root@10.1.33.1
# Password: apgar-66

# Or Web UI
open https://10.1.33.1:8006
# Username: root
# Password: apgar-66
```

---

## Troubleshooting

### Cannot Connect to WebSocket Listener

**Check QM Server**:
```powershell
# On Windows
netstat -an | findstr 8768
# Should show LISTENING on 0.0.0.0:8768 or 10.1.34.103:8768
```

**Check QM Phantom Process**:
```qm
* In QM terminal
LOGTO HAL
LIST.READU
* Look for WEBSOCKET.LISTENER process
```

**Restart if Needed**:
```qm
* If phantom crashed, restart:
LOGTO HAL
PHANTOM EXECUTE "WEBSOCKET.LISTENER"
```

**Check from Mac**:
```bash
telnet 10.1.34.103 8768
# Should connect (Ctrl+] then 'quit' to exit)
```

### WebSocket Listener Timeout

**Check AI Server**:
```bash
# On Mac or any machine
curl http://10.1.10.20:11434/api/tags
# Should return JSON with model list

curl http://10.1.10.20:9000/
# Should return service info
```

### Network Latency

**Test latency**:
```bash
ping -c 10 10.1.34.103
# Average should be < 10ms on LAN

traceroute 10.1.34.103
# Check for routing issues
```

---

## Service Start Commands

### On QM Server (Windows)

**WebSocket Listener Status** (runs as phantom process):
```qm
* Check if phantom process is running
LOGTO HAL
LIST.READU

* Or check from Windows command line
netstat -an | findstr 8768
```

**Start WebSocket Listener** (if not running):
```qm
* In QM terminal
LOGTO HAL
PHANTOM EXECUTE "WEBSOCKET.LISTENER"

* Or run directly (will become phantom)
WEBSOCKET.LISTENER
```

**Note**: The WebSocket listener runs as a QM phantom process, not as a Python script. It starts automatically and persists in the background.

### On AI Server (Linux) - GPU Server

**Check Ollama (LLM)**:
```bash
ssh lawr@10.1.10.20
curl http://localhost:11434/api/tags
# Should list available models (deepseek-r1, llama3, etc.)
```

**Check Faster-Whisper (STT)**:
```bash
curl http://localhost:9000/
# Should return service info
```

**Check GPU Usage**:
```bash
nvidia-smi  # or rocm-smi for AMD GPU
# Monitor GPU utilization during AI tasks
```

**Test Ollama API**:
```bash
curl -X POST http://10.1.10.20:11434/api/generate \
  -d '{"model":"deepseek-r1:32b","prompt":"Hello","stream":false}'
```

**Test Whisper API**:
```bash
# Test with sample audio (if you have test.wav)
curl -X POST http://10.1.10.20:9000/transcribe \
  -d '{"audio":"<base64_audio>","language":"en"}'
```

### On Mac

**Start HAL Client**:
```bash
source network_config.sh
python3 hal_text_client.py
```

---

## HAProxy Configuration (Optional)

If you want to route traffic through HAProxy:

### SSH to HAProxy
```bash
ssh lawr@10.1.50.100 -p 2222
# Password: apgar-66
```

### Configure HAProxy for Voice Gateway
Add to `/etc/haproxy/haproxy.cfg`:
```
frontend voice_gateway
    bind *:8768
    mode tcp
    default_backend qm_voice_gateway

backend qm_voice_gateway
    mode tcp
    server qm1 10.1.34.103:8768 check
```

Then reload:
```bash
sudo systemctl reload haproxy
```

### Use HAProxy in Client
```bash
export HAL_GATEWAY_URL="ws://10.1.50.100:8768"
```

---

## Network Diagram with Subnets

```
10.1.34.0/24 (QM Subnet)
    └─ 10.1.34.103 (QM Server)

10.1.10.0/24 (AI Subnet)
    └─ 10.1.10.20 (AI Server)

10.1.50.0/24 (Infrastructure Subnet)
    └─ 10.1.50.100 (HAProxy)

Your Mac: (needs route to all three subnets)
```

---

## Quick Reference Card

**Copy this to your desk!**

```
HAL NETWORK QUICK REFERENCE
===========================

MAC CLIENT:
export HAL_GATEWAY_URL="ws://10.1.34.103:8768"
python3 hal_text_client.py

QM SERVER (10.1.34.103):
- Voice Gateway: python PY\voice_gateway.py
- Voice Listener: VOICE.LISTENER (in QM)
- Ports: 8768 (gateway), 8767 (listener)

AI SERVER (10.1.10.20):
- Ollama: port 11434
- Whisper: port 9000

HAPROXY (10.1.50.100):
- SSH: port 2222
- ssh user@10.1.50.100 -p 2222
```

---

**Your network is configured and documented!**

Use `source network_config.sh` to load all environment variables automatically.

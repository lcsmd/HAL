# HAL Voice Interface - HAProxy Integration Summary

**Date**: October 30, 2025  
**Status**: Services Verified, Ready for Voice Integration

---

## ✅ **Verified Working**

### 1. **Ollama LLM Service**
- **URL**: `https://ollama.lcs.ai`
- **Backend**: ubuai:11434
- **Status**: ✅ Working (200 OK)
- **Models Available**: gemma3, deepseek-r1, and others
- **Usage**: Intent classification, general AI queries

### 2. **Speech Service**
- **URL**: `https://speech.lcs.ai`
- **Backend**: ubuai:???? (need to verify port)
- **Status**: ✅ Accessible (200 OK)
- **Usage**: Transcription and TTS

### 3. **DNS Resolution**
- **DNS Server**: q1 (Windows Domain Controller)
- **Wildcard**: *.lcs.ai → 10.1.50.100 (ubu6/HAProxy)
- **Status**: ✅ Working

---

## 🏗️ **Infrastructure Summary**

```
                           ┌─────────────────────┐
                           │   q1 (DNS Server)   │
                           │  Windows DC         │
                           │  10.1.35.101        │
                           └──────────┬──────────┘
                                      │ DNS: *.lcs.ai
                                      ▼
                           ┌─────────────────────┐
                           │   ubu6 (HAProxy)    │
                           │  10.1.50.100        │
                           │  Port 443 (HTTPS)   │
                           │  Wildcard SSL Cert  │
                           └──────────┬──────────┘
                                      │
              ┌───────────────────────┼───────────────────────┐
              │                       │                       │
              ▼                       ▼                       ▼
    ┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
    │  ollama.lcs.ai  │    │ speech.lcs.ai    │    │  hal.lcs.ai     │
    │  ubuai:11434    │    │  ubuai:????      │    │  Open-WebUI     │
    │  (Ollama)       │    │  (Whisper+TTS)   │    │                 │
    └─────────────────┘    └──────────────────┘    └─────────────────┘

    next.lcs.ai → Nextcloud
```

---

## 📋 **What We Need for Voice Interface**

### 1. **Add voice.lcs.ai Backend to HAProxy**

**Configuration needed on ubu6**:

```haproxy
# Add to /etc/haproxy/haproxy.cfg

frontend https_in
    bind *:443 ssl crt /etc/haproxy/certs/lcs.ai.pem
    
    # Existing ACLs...
    acl is_voice hdr(host) -i voice.lcs.ai
    acl is_websocket hdr(Upgrade) -i WebSocket
    
    # Use backend for voice
    use_backend voice_gateway if is_voice

backend voice_gateway
    mode http
    option http-server-close
    option forwardfor
    # WebSocket support
    timeout tunnel 3600s
    timeout client 3600s
    timeout server 3600s
    http-request set-header X-Forwarded-Proto https
    server voice1 q1:8765 check
    # Replace q1 with actual QM server hostname/IP
```

### 2. **Verify speech.lcs.ai API Endpoints**

**Questions**:
- What API does speech.lcs.ai expose?
- Does it support `/transcribe` endpoint?
- Does it support `/tts` endpoint?
- What format does it expect?

**Test**:
```bash
# Check what endpoints are available
curl https://speech.lcs.ai/

# Test transcription (if compatible with Faster-Whisper)
curl -X POST https://speech.lcs.ai/transcribe \
  -H "Content-Type: application/json" \
  -d '{"audio": "base64_data", "language": "en"}'
```

---

## 📝 **Updated Configuration**

### voice_config.json
```json
{
  "whisper": {
    "url": "https://speech.lcs.ai/transcribe",
    "fallback_url": "http://ubuai:9000/transcribe"
  },
  "ollama": {
    "url": "https://ollama.lcs.ai",
    "fallback_url": "http://ubuai:11434"
  },
  "tts": {
    "enabled": true,
    "url": "https://speech.lcs.ai/tts",
    "fallback_url": "http://ubuai:5000/tts"
  }
}
```

### Mac Client
```python
# Use secure WebSocket through HAProxy
GATEWAY_URL = "wss://voice.lcs.ai"
```

---

## 🎯 **Next Steps**

### Immediate:
1. **Check speech.lcs.ai API format**
   - What endpoints does it expose?
   - Is it compatible with our expected format?

2. **Add voice.lcs.ai to HAProxy**
   - SSH to ubu6
   - Edit /etc/haproxy/haproxy.cfg
   - Add voice_gateway backend
   - Reload HAProxy

3. **Test Ollama through HAProxy**
   - Update voice_gateway.py to use https://ollama.lcs.ai
   - Test intent classification

### Testing:
1. **Test speech.lcs.ai from Windows**
   ```powershell
   python tests/test_speech_api.py
   ```

2. **Start Voice Gateway**
   ```powershell
   python PY/voice_gateway.py
   ```

3. **Test through HAProxy**
   ```powershell
   # From Mac or another machine
   wscat -c wss://voice.lcs.ai
   ```

---

## 🔍 **Information Needed**

### 1. **QM Server Details**
- **Question**: What's the hostname of this QM server for HAProxy config?
- **Options**: `q1`, `qm-server`, `qmhost`, or IP address?
- **Current DNS resolution**: `ollama.lcs.ai` → 10.1.50.100

### 2. **speech.lcs.ai Details**
- **Question**: What software is running on speech.lcs.ai?
- **Options**: 
  - Faster-Whisper standalone?
  - WhisperX?
  - Custom web service?
  - Coqui STT?

### 3. **Network Topology**
- **Question**: Can this QM server (q1?) reach ubuai directly?
- **Test**: `Test-NetConnection ubuai -Port 11434`
- **Purpose**: Decide if we use HAProxy URLs or direct URLs

---

## 🌟 **Benefits of This Architecture**

### Security
- ✅ Single wildcard SSL certificate
- ✅ All external traffic encrypted
- ✅ Internal services can remain HTTP
- ✅ Centralized access control at HAProxy

### Simplicity
- ✅ Clean subdomain naming (ollama.lcs.ai, speech.lcs.ai, voice.lcs.ai)
- ✅ No need to remember ports
- ✅ Easy to add new services

### Scalability
- ✅ Load balancing built-in
- ✅ Easy to add more backends
- ✅ Health checking included
- ✅ Can run multiple instances of each service

### Flexibility
- ✅ Can route based on path, host, or headers
- ✅ Can add authentication at proxy level
- ✅ Can rate limit at proxy level

---

## 🧪 **Testing Commands**

### Test Ollama
```powershell
# Simple test
Invoke-WebRequest -Uri "https://ollama.lcs.ai/api/tags" -UseBasicParsing

# Test model inference
$body = @{
    model = "gemma3:latest"
    prompt = "Say hello"
    stream = $false
} | ConvertTo-Json

Invoke-WebRequest -Uri "https://ollama.lcs.ai/api/generate" -Method Post -Body $body -ContentType "application/json" -UseBasicParsing
```

### Test Speech Service
```powershell
# Check if it's accessible
Invoke-WebRequest -Uri "https://speech.lcs.ai" -UseBasicParsing

# Try common endpoints
Invoke-WebRequest -Uri "https://speech.lcs.ai/health" -UseBasicParsing
Invoke-WebRequest -Uri "https://speech.lcs.ai/api/transcribe" -UseBasicParsing
Invoke-WebRequest -Uri "https://speech.lcs.ai/docs" -UseBasicParsing
```

### Test Network Connectivity
```powershell
# Can this machine reach ubuai directly?
Test-NetConnection ubuai -Port 11434
Test-NetConnection ubuai -Port 9000
Test-NetConnection ubuai -Port 5000

# Can it reach HAProxy?
Test-NetConnection ubu6 -Port 443
Test-NetConnection 10.1.50.100 -Port 443
```

---

## 📞 **What to Tell Me**

1. **What's this machine's hostname?** (for HAProxy backend config)
   - Run: `hostname`
   - Or: `$env:COMPUTERNAME`

2. **What API format does speech.lcs.ai use?**
   - Try: `Invoke-WebRequest -Uri "https://speech.lcs.ai" -UseBasicParsing`
   - Look for docs, API info, or try common endpoints

3. **Do you want voice.lcs.ai subdomain?**
   - Or would you prefer a different name?

4. **Is HAProxy config managed manually or with automation?**
   - Do you edit files directly?
   - Or use Ansible/Terraform/etc?

Let me know these details and we can finalize the integration!

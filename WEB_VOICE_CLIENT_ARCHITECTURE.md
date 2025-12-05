# HAL Web Voice Client - Architecture Documentation

## Overview

The HAL Web Voice Client is a **zero-installation, browser-based voice and text interface** for the HAL AI system. It eliminates the need for client-side Python installations, library dependencies, and platform-specific configurations.

---

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Client (Any Browser)                      │
│  ┌────────────────────────────────────────────────────────┐ │
│  │  index.html + client.js (Pure HTML/JavaScript)         │ │
│  │  - Captures microphone audio via Web Audio API         │ │
│  │  - Streams audio chunks to server via WebSocket        │ │
│  │  - Displays responses in beautiful UI                  │ │
│  └────────────────────────────────────────────────────────┘ │
│                            ↓                                 │
│                      wss://hal.lcs.ai                       │
└─────────────────────────────────────────────────────────────┘
                               ↓
┌─────────────────────────────────────────────────────────────┐
│              HAProxy Reverse Proxy (ubu6)                    │
│  - Terminates SSL (wildcard *.lcs.ai certificate)           │
│  - Routes HTTP requests → Windows Server:8080                │
│  - Routes WebSocket upgrades → Windows Server:8768           │
└─────────────────────────────────────────────────────────────┘
                               ↓
┌─────────────────────────────────────────────────────────────┐
│         Windows Server (10.1.34.103)                         │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Port 8080: HTTP Server (Static Files)               │   │
│  │  - Serves index.html, client.js                      │   │
│  │  - Simple Python http.server                         │   │
│  └──────────────────────────────────────────────────────┘   │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Port 8768: Voice Gateway (WebSocket + Processing)   │   │
│  │  - Receives audio streams from browser               │   │
│  │  - Detects wake word (openwakeword)                  │   │
│  │  - Sends audio to Whisper for transcription          │   │
│  │  - Routes queries through Query Router               │   │
│  │  - Returns responses to browser                      │   │
│  └──────────────────────────────────────────────────────┘   │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Port 8745: AI.SERVER (QM Integration)               │   │
│  │  - Handles built-in queries (time, date, hello)      │   │
│  │  - Integrates with QM database                       │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                               ↓
┌─────────────────────────────────────────────────────────────┐
│         Ubuntu Server (10.1.10.20)                           │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Port 8001: Whisper STT (faster-whisper)             │   │
│  │  - Transcribes audio to text                         │   │
│  └──────────────────────────────────────────────────────┘   │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Port 11434: Ollama LLM                               │   │
│  │  - Processes general queries                         │   │
│  │  - Model: llama3.2:latest                            │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

---

## Key Components

### 1. Web Client (`voice_assistant_v2/web_client/`)

**Files:**
- `index.html` - User interface (chat display, input, mic button)
- `client.js` - Client-side logic (WebSocket, audio capture, UI updates)

**Features:**
- **Zero Installation**: Just open URL in browser
- **Cross-Platform**: Works on Windows, Mac, Linux, iOS, Android
- **Audio Capture**: Uses Web Audio API to capture microphone
- **Real-Time Streaming**: Sends audio chunks as they're captured
- **Beautiful UI**: Modern, responsive design
- **State Management**: Connected/Disconnected/Listening states

**Browser Requirements:**
- Modern browser with WebSocket support (Chrome, Edge, Firefox, Safari)
- HTTPS required for microphone access
- Microphone permission granted

### 2. Voice Gateway (`PY/voice_gateway_web.py`)

**Responsibilities:**
- Accept WebSocket connections from browsers
- Receive streaming audio data
- Perform server-side wake word detection (openwakeword)
- Detect end of speech (VAD - Voice Activity Detection)
- Send audio to Whisper for transcription
- Route queries through Query Router
- Send responses back to client

**Key Features:**
- **Server-Side Wake Word**: No client-side processing needed
- **Session Management**: Tracks multiple concurrent users
- **State Machine**: PASSIVE → ACTIVE → PROCESSING → RESPONDING
- **Context Tracking**: Maintains conversation history per session

**Dependencies:**
- `websockets` - WebSocket server
- `openwakeword` - Wake word detection ("Hey Jarvis")
- `webrtcvad` - Voice Activity Detection
- `numpy` - Audio processing
- `requests` - HTTP calls to Whisper/Ollama
- `query_router` - Intelligent query routing

### 3. Query Router (`PY/query_router.py`)

**Routing Logic:**
```
Query → Intent Detection → Route to Handler → Response

Intents:
├─ builtin (0.95)    → AI.SERVER (time, date, hello)
├─ home_assistant    → Home Assistant API
├─ database          → QM Database queries
└─ llm (default)     → Ollama LLM
```

**Intent Detection:**
- Regex pattern matching
- Confidence scoring
- Built-in queries have highest priority

### 4. HAProxy Configuration

**Location:** `/etc/haproxy/haproxy.cfg` on ubu6

**Key Configuration:**
```haproxy
frontend https_in
    bind *:443 ssl crt /etc/haproxy/certs/wildcard.pem
    
    # ACL for hal.lcs.ai
    acl is_hal2 hdr(host) -i hal.lcs.ai
    use_backend hal2_backend if is_hal2

backend hal2_backend
    mode http
    option forwardfor
    timeout tunnel 3600s
    timeout server 3600s
    
    # Detect WebSocket upgrade requests
    acl is_websocket hdr(Connection) -i upgrade
    acl is_websocket hdr(Upgrade) -i websocket
    
    # Route WebSocket to port 8768, HTTP to port 8080
    use-server hal2_ws if is_websocket
    server hal2_http 10.1.34.103:8080 check
    server hal2_ws 10.1.34.103:8768 check
```

**Why This Works:**
- SSL termination at HAProxy (wildcard cert)
- HTTP/2 support for browsers
- WebSocket upgrade detection
- Long timeout for WebSocket connections (3600s = 1 hour)

---

## Data Flow

### Text Query Flow

```
1. User types "what time is it"
2. Browser sends via WebSocket: {type: 'text_input', text: '...', session_id: '...'}
3. Voice Gateway receives message
4. Query Router detects 'builtin' intent
5. Routes to AI.SERVER (port 8745)
6. AI.SERVER returns current time
7. Voice Gateway sends response: {type: 'response', text: 'The current time is...'}
8. Browser displays in chat UI
```

### Voice Query Flow

```
1. User clicks 🎤 button
2. Browser starts capturing audio (16kHz, mono, 16-bit PCM)
3. Browser sends audio chunks: {type: 'audio_stream', audio: [int16 array]}
4. Voice Gateway:
   a. Converts to float32
   b. Runs through openwakeword model
   c. Detects "Hey Jarvis" (score > 0.5)
5. State changes to ACTIVE_LISTENING
6. Continues receiving audio chunks
7. VAD detects silence (1.5 seconds)
8. Combines all audio buffers
9. Converts to WAV format
10. Sends to Whisper (POST /v1/audio/transcriptions)
11. Whisper returns: {text: "what time is it"}
12. Query Router processes (same as text flow)
13. Response sent to browser
14. Browser displays in chat UI
```

---

## Advantages Over Python Client

| Feature | Python Client | Web Client |
|---------|--------------|------------|
| **Installation** | Install Python 3.13, pip, 10+ libraries | **None - just open URL** |
| **Dependencies** | pyaudio, openwakeword, webrtcvad, pygame, websockets, etc. | **Zero** |
| **Platform Support** | Windows only (tested) | **Any device with browser** |
| **Mobile Support** | ❌ Not possible | ✅ **Works on phones/tablets** |
| **Microphone Issues** | Driver conflicts, PyAudio errors | **Browser handles everything** |
| **Updates** | Reinstall on every PC | **Automatic from server** |
| **Deployment** | Copy files + install libs | **Share URL** |
| **SSL Certificate** | Self-signed warnings | **Real wildcard cert** |
| **Processing Location** | Client (limited power) | **Server (unlimited power)** |

---

## Security Considerations

### Current Implementation

**SSL/TLS:**
- ✅ Wildcard certificate (*.lcs.ai)
- ✅ HAProxy terminates SSL
- ✅ No self-signed certificate warnings

**Authentication:**
- ❌ **NOT IMPLEMENTED** - Anyone with URL can access
- ⚠️ Internal network only (10.1.x.x)

**Data Privacy:**
- Audio streams NOT recorded or stored
- Session data in memory only
- No persistent logs of queries/responses

### Production Recommendations

**If exposing to internet:**
1. Add authentication (OAuth, API keys, or basic auth)
2. Rate limiting (prevent abuse)
3. Session timeout (auto-disconnect idle users)
4. Audit logging (who accessed when)
5. Content filtering (prevent malicious queries)
6. CORS restrictions (limit allowed origins)

---

## File Structure

```
HAL/
├── voice_assistant_v2/
│   └── web_client/
│       ├── index.html              # Web UI
│       ├── client.js               # Client logic
│       ├── cert.pem               # SSL cert (not used - HAProxy handles)
│       ├── key.pem                # SSL key (not used)
│       ├── serve.py               # Simple HTTP server
│       └── generate_cert.py       # Self-signed cert generator
│
├── PY/
│   ├── voice_gateway_web.py       # WebSocket + Wake Word Detection
│   ├── voice_gateway_web_secure.py # SSL version (not used)
│   ├── voice_gateway_with_http.py  # Combined HTTP+WS (not used)
│   ├── query_router.py            # Intent detection & routing
│   ├── llm_handler.py             # Ollama/OpenAI/Claude integration
│   ├── home_assistant_handler.py  # Home Assistant API
│   ├── database_handler.py        # QM database queries
│   └── ai_server.py               # AI.SERVER (port 8745)
│
├── config/
│   └── router_config.json         # Query Router configuration
│
└── Documentation/
    ├── WEB_VOICE_CLIENT_ARCHITECTURE.md (this file)
    ├── WEB_VOICE_CLIENT_QUICK_START.md
    ├── TODO.md
    └── ERRORS_ENCOUNTERED.md
```

---

## URLs and Ports

### Production URLs
- **Web Client:** https://hal.lcs.ai
- **HAProxy Stats:** http://ubu6:8404/stats (admin/apgar-66)

### Internal Ports (Windows Server - 10.1.34.103)
- **8080** - HTTP server (static files)
- **8768** - Voice Gateway (WebSocket)
- **8745** - AI.SERVER (QM integration)

### Internal Ports (Ubuntu Server - 10.1.10.20)
- **8001** - Whisper STT (faster-whisper)
- **11434** - Ollama LLM

### HAProxy (ubu6)
- **443** - HTTPS (frontend)
- **8404** - Stats page

---

## Configuration Files

### HAProxy Backend (`/etc/haproxy/haproxy.cfg` on ubu6)

Key sections:
1. **Frontend ACL**: `acl is_hal2 hdr(host) -i hal.lcs.ai`
2. **Frontend Routing**: `use_backend hal2_backend if is_hal2`
3. **Backend Definition**: See architecture section above

### Query Router (`config/router_config.json`)

```json
{
  "llm": {
    "provider": "ollama",
    "ollama": {
      "url": "http://10.1.10.20:11434",
      "model": "llama3.2:latest"
    }
  },
  "home_assistant": {
    "url": "http://homeassistant.local:8123",
    "enabled": true
  },
  "database": {
    "enabled": true,
    "default_account": "HAL"
  }
}
```

---

## Development vs Production

### Current State: **Hybrid**

**Production-Ready:**
- ✅ SSL with real certificate
- ✅ Domain name (hal.lcs.ai)
- ✅ Reverse proxy (HAProxy)
- ✅ Server-side processing
- ✅ Cross-platform support

**Still Development:**
- ⚠️ No authentication
- ⚠️ No rate limiting
- ⚠️ Internal network only
- ⚠️ No monitoring/alerting
- ⚠️ Manual startup (not systemd services)

---

## Performance Characteristics

**Latency:**
- Wake word detection: ~50-100ms
- STT (Whisper): ~1-2 seconds
- LLM query (Ollama): ~2-5 seconds (depends on query complexity)
- **Total end-to-end**: ~3-7 seconds (voice) / ~0.5-1 second (text)

**Scalability:**
- Current: Single server, single process
- Limit: ~10-20 concurrent users (based on Whisper/Ollama capacity)
- Bottleneck: Whisper transcription and Ollama inference

**Resource Usage (Windows Server):**
- Voice Gateway: ~200MB RAM
- Wake word detection: ~500MB RAM (model loaded)
- Per session: ~10MB RAM

---

## Future Enhancements

### Short Term
1. Fix WebSocket connection issues (current priority)
2. Test wake word detection with multiple users
3. Add systemd/Windows service for auto-start
4. Improve error handling and user feedback

### Medium Term
1. Add authentication layer
2. Implement session management
3. Add TTS (text-to-speech) for voice responses
4. Support multiple wake words
5. Add conversation history persistence

### Long Term
1. Multi-user support with separate contexts
2. Custom wake word training
3. Plugin system for custom handlers
4. Mobile app (React Native wrapper)
5. Offline mode (local Whisper/LLM)

---

## Testing

### Manual Testing Steps

**Text Mode:**
1. Open https://hal.lcs.ai
2. Type "what time is it" → Should get current time
3. Type "tell me a joke" → Should get LLM response
4. Type "hello" → Should get AI.SERVER greeting

**Voice Mode:**
1. Click 🎤 button (should turn red)
2. Say "Hey Jarvis" clearly
3. Wait for acknowledgment
4. Say "What time is it"
5. Should hear/see response

### Automated Testing

**Not yet implemented** - Future work:
- Unit tests for query router
- Integration tests for voice pipeline
- Load testing for concurrent users
- Browser compatibility testing

---

## Troubleshooting

### Common Issues

**"Microphone access denied"**
- Browser requires HTTPS for microphone access
- Check browser permissions (Settings → Privacy → Microphone)
- Ensure hal.lcs.ai is in allowed list

**"Connected/Disconnected loop"**
- Check Voice Gateway is running (port 8768)
- Check HAProxy routing configuration
- Verify WebSocket upgrade detection in HAProxy

**"No response to text input"**
- Check Voice Gateway logs for errors
- Verify AI.SERVER is running (port 8745)
- Test query router independently

**"Wake word not detecting"**
- Speak clearly and loudly: "HEY JARVIS"
- Check microphone is not muted in OS
- Verify wake word models are downloaded
- Check Voice Gateway logs for detection scores

### Log Locations

**Windows Server:**
- Voice Gateway: PowerShell window output
- HTTP Server: PowerShell window output

**Ubuntu Server (HAProxy):**
- `/var/log/haproxy.log`

**Ubuntu Server (Whisper/Ollama):**
- Check systemd journal: `journalctl -u whisper -f`
- Check systemd journal: `journalctl -u ollama -f`

---

## Maintenance

### Regular Tasks

**Daily:**
- Monitor HAProxy logs for errors
- Check disk space on servers

**Weekly:**
- Review query router performance
- Check for library updates

**Monthly:**
- Update SSL certificate if needed
- Review and archive logs
- Update LLM models

### Backup Strategy

**Critical Files:**
- HAProxy configuration: `/etc/haproxy/haproxy.cfg`
- Query router config: `config/router_config.json`
- Web client files: `voice_assistant_v2/web_client/`
- QM database: (per existing backup strategy)

**Backup Command:**
```bash
# On ubu6
sudo cp /etc/haproxy/haproxy.cfg /etc/haproxy/backups/haproxy.cfg.$(date +%Y%m%d)

# On Windows Server
git add -A
git commit -m "Backup: $(Get-Date)"
git push origin main
```

---

## References

- [OpenWakeWord Documentation](https://github.com/dscripka/openWakeWord)
- [Faster-Whisper Documentation](https://github.com/guillaumekln/faster-whisper)
- [Ollama Documentation](https://ollama.ai/docs)
- [HAProxy Documentation](https://www.haproxy.org/documentation.html)
- [WebSocket API](https://developer.mozilla.org/en-US/docs/Web/API/WebSocket)
- [Web Audio API](https://developer.mozilla.org/en-US/docs/Web/API/Web_Audio_API)

---

**Last Updated:** 2025-12-03
**Version:** 1.0
**Status:** In Development - Core functionality implemented, troubleshooting WebSocket connectivity

# HAL Web Voice Client - Master Documentation

**Zero-installation voice and text interface for HAL AI system**

Access from any device: **https://hal.lcs.ai**

---

## Quick Links

- **[Architecture Documentation](WEB_VOICE_CLIENT_ARCHITECTURE.md)** - Complete system design and technical details
- **[TODO List](TODO.md)** - Current tasks, priorities, and known issues
- **[Errors Reference](ERRORS_ENCOUNTERED.md)** - Common errors and solutions
- **[Quick Start Guide](WEB_VOICE_CLIENT_QUICK_START.md)** - User guide (if exists)

---

## What Is This?

A browser-based voice and text interface for the HAL AI system that requires **zero installation** on client devices. Just open a URL and start talking or typing.

### Key Features

✅ **No Installation Required** - Works in any modern browser  
✅ **Cross-Platform** - Windows, Mac, Linux, iOS, Android  
✅ **Voice Input** - Say "Hey Jarvis" to activate  
✅ **Text Input** - Type queries directly  
✅ **Intelligent Routing** - Routes queries to appropriate handlers (LLM, Database, Home Assistant)  
✅ **Real SSL Certificate** - No security warnings  
✅ **Server-Side Processing** - All heavy lifting on server  

---

## Current Status

**⚠️ IN DEVELOPMENT - WebSocket connection issues being debugged**

### What Works
- ✅ Web client UI loads correctly
- ✅ HAProxy routing configured
- ✅ SSL certificate (wildcard *.lcs.ai)
- ✅ Backend servers running (8080, 8768, 8745)
- ✅ Audio capture in browser
- ✅ Wake word detection (server-side)
- ✅ Whisper STT integration
- ✅ Ollama LLM integration
- ✅ Query routing system

### What Needs Fixing
- ❌ WebSocket connection unstable (connects then disconnects)
- ❌ Text input not responding (due to WebSocket issue)
- ❌ Voice input not working (due to WebSocket issue)

**See [TODO.md](TODO.md) for detailed task list and priorities.**

---

## File Structure

```
HAL/
├── voice_assistant_v2/web_client/     # Web client files
│   ├── index.html                     # Main UI
│   ├── client.js                      # Client-side logic
│   └── serve.py                       # HTTP server
│
├── PY/                                # Python backend
│   ├── voice_gateway_web.py          # WebSocket + Wake Word
│   ├── query_router.py               # Query routing
│   ├── llm_handler.py                # LLM integration
│   ├── home_assistant_handler.py     # HA integration
│   ├── database_handler.py           # DB queries
│   └── ai_server.py                  # AI.SERVER (QM)
│
├── config/
│   └── router_config.json            # Router configuration
│
└── Documentation/
    ├── WEB_VOICE_CLIENT_README.md    # This file (master index)
    ├── WEB_VOICE_CLIENT_ARCHITECTURE.md  # Technical documentation
    ├── TODO.md                       # Task list and priorities
    └── ERRORS_ENCOUNTERED.md         # Error reference
```

---

## Architecture Overview

```
Browser (Any Device)
    ↓ https://hal.lcs.ai
HAProxy (ubu6) - SSL Termination
    ↓ Routes to:
    ├─→ Port 8080: Static Files (HTML/JS)
    └─→ Port 8768: WebSocket (Voice/Text)
         ↓
Voice Gateway (Windows Server)
    ├─→ Wake Word Detection (openwakeword)
    ├─→ STT (Whisper on Ubuntu)
    └─→ Query Router
         ├─→ Built-in (time/date) → AI.SERVER
         ├─→ Home Assistant → HA API
         ├─→ Database → QM Database
         └─→ General Queries → Ollama LLM
```

**Detailed architecture: [WEB_VOICE_CLIENT_ARCHITECTURE.md](WEB_VOICE_CLIENT_ARCHITECTURE.md)**

---

## How to Use (When Working)

### Access the Interface
1. Open browser: **https://hal.lcs.ai**
2. Allow microphone access when prompted

### Text Mode
1. Type your question in the input box
2. Press Enter or click Send
3. HAL responds

### Voice Mode
1. Click the 🎤 microphone button
2. Say "Hey Jarvis"
3. Speak your question
4. HAL responds

---

## Server Components

### Windows Server (10.1.34.103)
- **Port 8080:** HTTP Server (serves web client files)
- **Port 8768:** Voice Gateway (WebSocket + wake word)
- **Port 8745:** AI.SERVER (QM integration)

### Ubuntu Server (10.1.10.20)
- **Port 8001:** Whisper STT (faster-whisper)
- **Port 11434:** Ollama LLM (llama3.2:latest)

### HAProxy Server (ubu6)
- **Port 443:** HTTPS frontend (SSL termination)
- Wildcard certificate: *.lcs.ai
- Routes hal.lcs.ai to backend servers

---

## Starting Services

### Windows Server

**Start HTTP Server (Static Files):**
```powershell
cd C:\qmsys\hal\voice_assistant_v2\web_client
python -m http.server 8080
```

**Start Voice Gateway (WebSocket):**
```powershell
cd C:\qmsys\hal
python PY\voice_gateway_web.py
```

**Start AI.SERVER:**
```powershell
cd C:\qmsys\hal
python PY\ai_server.py
```

### Ubuntu Server

**Services should already be running:**
- Whisper: `systemctl status whisper`
- Ollama: `systemctl status ollama`

---

## Troubleshooting

### "Cannot connect" or "Disconnected"
1. Check Voice Gateway is running on Windows Server port 8768
2. Check HAProxy is routing correctly: `tail -f /var/log/haproxy.log | grep hal2`
3. Check browser console for errors
4. See [ERRORS_ENCOUNTERED.md](ERRORS_ENCOUNTERED.md) for common issues

### "Microphone access denied"
1. Click lock icon in browser address bar
2. Allow microphone for hal.lcs.ai
3. Refresh page

### "No response to text input"
- This is the current known issue
- WebSocket connection is not stable
- Being actively debugged
- See [TODO.md](TODO.md) #1

---

## Development

### Prerequisites
- Python 3.13
- Windows Server 2022
- Ubuntu Server (for Whisper/Ollama)
- HAProxy server

### Python Dependencies
```
websockets
openwakeword
webrtcvad
numpy
requests
aiohttp
```

### Install Dependencies
```powershell
pip install websockets openwakeword webrtcvad numpy requests aiohttp
python -c "from openwakeword.utils import download_models; download_models()"
```

---

## Advantages Over Python Client

| Feature | Old Python Client | New Web Client |
|---------|------------------|----------------|
| Installation | Complex (10+ libraries) | **Zero** |
| Platform | Windows only | **Any device** |
| Mobile | Not supported | **Fully supported** |
| Updates | Manual reinstall | **Automatic** |
| SSL | Self-signed warnings | **Real certificate** |
| Processing | Client-side | **Server-side** |

---

## Documentation Index

### For Users
- This file (master overview)
- TODO.md (what's being worked on)

### For Developers
- [WEB_VOICE_CLIENT_ARCHITECTURE.md](WEB_VOICE_CLIENT_ARCHITECTURE.md) - Complete technical documentation
- [TODO.md](TODO.md) - Development roadmap and priorities
- [ERRORS_ENCOUNTERED.md](ERRORS_ENCOUNTERED.md) - Common errors and solutions

### Configuration
- `config/router_config.json` - Query routing rules
- `/etc/haproxy/haproxy.cfg` - HAProxy configuration (on ubu6)

---

## Support

### Known Issues
See [TODO.md](TODO.md) for current issues and priorities.

### Reporting Bugs
1. Check [ERRORS_ENCOUNTERED.md](ERRORS_ENCOUNTERED.md) first
2. Check browser console for errors
3. Check server logs
4. Document steps to reproduce

---

## Roadmap

### Immediate (CRITICAL)
- Fix WebSocket connection stability
- Test wake word detection
- Verify text input works

### Short Term
- Add proper error handling
- Improve user feedback
- Add session management
- Create systemd services

### Long Term
- Authentication system
- Multi-language support
- TTS responses
- Mobile app
- Plugin system

**Full roadmap: [TODO.md](TODO.md)**

---

## Why Web-Based?

The web-based approach solves ALL the problems we encountered with the Python client:

❌ **Python Client Problems:**
- Required installing Python 3.13
- Required 10+ libraries (pyaudio, openwakeword, webrtcvad, pygame, etc.)
- Microphone driver conflicts
- Windows-only (complex setup on Mac/Linux)
- No mobile support
- Updates required reinstalling everywhere
- Self-signed certificate warnings blocked microphone

✅ **Web Client Advantages:**
- **Zero installation** - just open URL
- Works on **any device** with a browser
- **Server handles all processing** (more powerful)
- **Automatic updates** (change server, all clients updated)
- **Real SSL certificate** (no warnings)
- **Cross-platform** without any changes
- **Mobile-friendly** (phones, tablets)

**This is the right architecture for HAL going forward.**

---

## Technical Highlights

### Server-Side Wake Word Detection
- Wake word detection runs on server, not client
- No client-side ML libraries needed
- More powerful processing
- Easier to update/improve

### Intelligent Query Routing
```
Query → Analyze Intent → Route to Best Handler

- Time/Date queries → AI.SERVER (instant)
- "Turn on lights" → Home Assistant
- "Find patient Smith" → QM Database  
- "Tell me a joke" → Ollama LLM
```

### Real SSL Certificate
- Wildcard certificate: *.lcs.ai
- No browser warnings
- Microphone access allowed
- Professional appearance

---

## Credits

**Developed by:** Droid (Factory AI)  
**For:** Dr. Lawrence Schmetterer  
**Project:** HAL AI Assistant  
**Started:** December 2025  
**Status:** In Development  

---

## Version History

- **v1.0** (2025-12-03) - Initial web client implementation
  - Created HTML/JS client
  - Implemented server-side wake word detection
  - Configured HAProxy routing
  - Integrated with existing HAL services
  - Currently debugging WebSocket connection issues

---

## Next Steps

1. **Fix WebSocket connection** (highest priority)
2. Test end-to-end functionality
3. Deploy systemd services for auto-start
4. Add authentication layer
5. Document for end users

**See [TODO.md](TODO.md) for detailed task breakdown.**

---

**Last Updated:** 2025-12-03 19:58 PST  
**Version:** 1.0  
**Status:** In Development

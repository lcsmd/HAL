# HAL Voice System - Deployment Summary

**Quick reference: Which component runs where**

---

## 🖥️ Three Machines, Three Components

### Machine 1: QM Server (Windows)

**Hostname**: `10.1.34.103`  
**OS**: Windows Server  
**Location**: `C:\QMSYS\hal`

**What runs here**:
```
BP/VOICE.LISTENER
```

**How to start**:
```qm
qm
LOGTO HAL
BASIC BP VOICE.LISTENER
CATALOG BP VOICE.LISTENER
PHANTOM BP VOICE.LISTENER
```

**What it does**:
- Listens on TCP port 8767
- Receives JSON messages from UBUAI
- Classifies intent (MEDICATION, APPOINTMENT, etc.)
- Routes to handlers
- Returns JSON response

**Don't run**: Voice client (no microphone needed)

---

### Machine 2: UBUAI Server (Linux)

**Hostname**: `10.1.10.20`  
**OS**: Linux (Ubuntu/similar)  
**Location**: `/path/to/hal/ubuai_server`

**What runs here**:
```
ubuai_server/main.py
```

**How to start**:
```bash
ssh user@10.1.10.20
cd /path/to/hal/ubuai_server
python3 main.py
```

**What it does**:
- WebSocket server on port 8001
- Receives audio from Mac client
- Transcribes with Faster-Whisper (GPU)
- Sends text to QM via TCP
- Generates TTS with ElevenLabs
- Sends response audio back to client

**Don't run**: Voice client (no microphone needed)

---

### Machine 3: Your Mac (Client)

**Hostname**: Your Mac  
**OS**: macOS  
**Location**: `~/Projects/hal/clients` (or wherever you put it)

**What runs here**:
```
clients/hal_voice_client_full.py
```

**How to start**:
```bash
cd ~/Projects/hal/clients
source venv/bin/activate
python3 hal_voice_client_full.py
```

**What it does**:
- Wake word detection (microphone)
- Voice activity detection
- Records audio when active
- Sends to UBUAI via WebSocket
- Plays response audio (speakers)
- Manages 10s passive window
- Handles interruptions

**Don't run**: QM listener or UBUAI server

---

## 📊 Data Flow

```
┌────────────────────┐
│  YOUR MAC          │ 1. User says "Hey Jarvis"
│  (Client)          │ 2. Records audio until 3s silence
└────────┬───────────┘
         │ 3. WebSocket: Binary PCM16 audio
         ▼
┌────────────────────┐
│  UBUAI Server      │ 4. Faster-Whisper transcribes
│  10.1.10.20        │ 5. Text: "What medications..."
└────────┬───────────┘
         │ 6. TCP: JSON {"session_id", "text", ...}
         ▼
┌────────────────────┐
│  QM Server         │ 7. Parse JSON, detect intent
│  10.1.34.103       │ 8. Intent = MEDICATION
└────────┬───────────┘ 9. Route to handler
         │ 10. JSON response
         ▼
┌────────────────────┐
│  UBUAI Server      │ 11. Extract response_text
│  10.1.10.20        │ 12. ElevenLabs TTS
└────────┬───────────┘ 13. Generate audio
         │ 14. WebSocket: Binary MP3/WAV
         ▼
┌────────────────────┐
│  YOUR MAC          │ 15. Play response audio
│  (Client)          │ 16. Start 10s passive window
└────────────────────┘
```

---

## ✅ Deployment Checklist

### Before Starting

- [ ] All three machines on same network (or VPN connected)
- [ ] QM server has OpenQM installed
- [ ] UBUAI server has Python 3.8+
- [ ] Your Mac has Python 3.8+
- [ ] Your Mac has microphone and speakers

### Start Sequence

1. [ ] **QM Server**: Start VOICE.LISTENER (port 8767)
2. [ ] **UBUAI Server**: Start main.py (port 8001)
3. [ ] **Your Mac**: Start hal_voice_client_full.py

### Verify Each Component

**QM Listener**:
```bash
# From any machine
telnet 10.1.34.103 8767
# Should connect (Ctrl+C to exit)
```

**UBUAI Server**:
```bash
# From your Mac
curl http://10.1.10.20:8001/
# Should return: {"service":"UBUAI Voice Server",...}
```

**Mac Client**:
```bash
# On your Mac, in client terminal
# Should see: "Listening..." and wake word prompt
```

---

## 🔥 Quick Troubleshooting

### Client can't reach UBUAI

**From your Mac**:
```bash
ping 10.1.10.20
curl http://10.1.10.20:8001/
```

If fails: Check network, VPN, firewall

---

### UBUAI can't reach QM

**From UBUAI server**:
```bash
ping 10.1.34.103
telnet 10.1.34.103 8767
```

If fails: Check QM listener is running, firewall on Windows

---

### Wake word not detecting

**On your Mac**:
- Check microphone permissions
- System Preferences → Security & Privacy → Privacy → Microphone
- Grant access to Terminal (or iTerm2)
- Restart client

---

### No audio playback

**On your Mac**:
```bash
# Test audio playback directly
afplay activation.wav
```

If fails: Check speakers/headphones, volume, output device

---

## 📁 File Locations

### QM Server (Windows)
```
C:\QMSYS\hal\
  └── BP\
      └── VOICE.LISTENER          ← QM listener program
```

### UBUAI Server (Linux)
```
/path/to/hal/
  └── ubuai_server\
      ├── main.py                 ← UBUAI FastAPI server
      ├── requirements.txt
      └── .env                    ← Config (create from .env.example)
```

### Your Mac
```
~/Projects/hal/                   ← Or wherever you put it
  └── clients/
      ├── hal_voice_client_full.py  ← Voice client
      ├── requirements.txt
      ├── activation.wav           ← Generated sounds
      ├── acknowledgement.wav
      ├── error.wav
      └── correction.wav
```

---

## 🎯 Port Summary

| Machine | Port | Protocol | Purpose |
|---------|------|----------|---------|
| QM Server (10.1.34.103) | 8767 | TCP | Voice listener |
| UBUAI Server (10.1.10.20) | 8001 | HTTP/WS | Voice server |
| Your Mac | - | - | Client (connects outbound) |

---

## 📖 Detailed Documentation

- **Mac setup**: `clients/MAC_QUICK_START.md`
- **5-min setup**: `QUICK_START_OPTION_C.md`
- **Full deployment**: `DEPLOYMENT_GUIDE_OPTION_C.md`
- **Complete spec**: `OPTION_C_IMPLEMENTATION_COMPLETE.md`

---

## 🆘 Still Confused?

**Remember**:
1. **QM server** = Where OpenQM runs (Windows, no mic needed)
2. **UBUAI server** = Where GPU/AI runs (Linux, no mic needed)
3. **Your Mac** = Where YOU sit (macOS, mic + speakers needed)

**Only your Mac needs a microphone and speakers!**

---

**Now start all three components and say "Hey Jarvis"!** 🎉

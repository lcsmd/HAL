# HAL Voice System - Deployment Guide (Option C)

**Implementation Date**: November 11, 2025  
**Architecture**: Hybrid (UBUAI + QM TCP + Smart Client)

---

## 🎯 Overview

This deployment implements Option C (Hybrid):
- **UBUAI Server**: GPU transcription (Faster-Whisper) + TTS (ElevenLabs) + QM TCP client
- **QM Listener**: TCP server (port 8767) with intent routing and handlers
- **Voice Client**: Wake word detection + VAD + interruption handling + 10s passive window

---

## 📋 Prerequisites

### Hardware Requirements
- **GPU Server (UBUAI)**: NVIDIA GPU for Faster-Whisper (or CPU fallback)
- **QM Server**: Windows/Linux with OpenQM installed
- **Client**: Windows/Mac/Linux with microphone and speakers

### Software Requirements
- Python 3.8+ on all systems
- OpenQM on QM server
- CUDA toolkit (if using GPU on UBUAI)

---

## 🚀 Deployment Steps

### Step 1: Deploy UBUAI Server (GPU Server)

**Host**: `10.1.10.20` (or your GPU server)

```bash
# 1. Navigate to UBUAI directory
cd /path/to/hal/ubuai_server

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure environment
cp .env.example .env
nano .env

# Edit .env:
# - Set ELEVENLABS_API_KEY (if using ElevenLabs)
# - Set WHISPER_DEVICE=cuda (or cpu)
# - Set OPENQM_HOST=10.1.34.103
# - Set OPENQM_PORT=8767

# 4. Test server
python main.py

# Should see:
# ╔═══════════════════════════════════════════════════╗
# ║     UBUAI Voice Server Starting                   ║
# ╠═══════════════════════════════════════════════════╣
# ║  Whisper Model: base                              ║
# ║  Whisper Device: cuda                             ║
# ║  OpenQM Host: 10.1.34.103                         ║
# ║  OpenQM Port: 8767                                ║
# ╚═══════════════════════════════════════════════════╝

# 5. Test health endpoint
curl http://10.1.10.20:8001/
```

**Expected output**:
```json
{
  "service": "UBUAI Voice Server",
  "status": "running",
  "whisper_model": "base",
  "whisper_device": "cuda",
  "qm_host": "10.1.34.103",
  "qm_port": 8767
}
```

---

### Step 2: Deploy QM Voice Listener (OpenQM Server)

**Host**: `10.1.34.103` (Windows/Linux)

```bash
# 1. Copy updated VOICE.LISTENER to BP directory
# (Already in C:\QMSYS\hal\BP\VOICE.LISTENER)

# 2. Open QM shell
qm
```

```qm
* 3. Log into HAL account
LOGTO HAL

* 4. Compile listener
BASIC BP VOICE.LISTENER
CATALOG BP VOICE.LISTENER

* 5. Start listener (test mode first)
BP VOICE.LISTENER

* Should see:
* HAL Voice Listener (JSON Parser) starting...
* Port: 8767
* Voice Listener active on port 8767
* Waiting for connections...
```

**Leave this running** or set up as background process:

```qm
* Start as phantom process
PHANTOM BP VOICE.LISTENER
```

---

### Step 3: Test UBUAI → QM Connection

From UBUAI server:

```bash
# Test QM connection with sample message
python -c "
import socket
import json

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(('10.1.34.103', 8767))

message = json.dumps({
    'session_id': 'test-001',
    'text': 'What medications am I taking?',
    'timestamp': '2025-11-11T10:00:00'
}) + '\n'

sock.sendall(message.encode())

response = sock.recv(8192)
print('QM Response:', response.decode())

sock.close()
"
```

**Expected output**:
```
QM Response: {"response_text":"I detected a medication query: What medications am I taking?","action_taken":"medication_detected","intent":"MEDICATION","status":"success"}
```

✅ If you see this, **UBUAI ↔ QM connection works!**

---

### Step 4: Deploy Voice Client (User's Machine)

**Any Windows/Mac/Linux with mic + speakers**

```bash
# 1. Navigate to clients directory
cd C:\QMSYS\hal\clients

# 2. Install dependencies
pip install -r requirements.txt

# 3. Generate audio feedback sounds
python generate_sounds.py

# Should see:
# ✓ Generated: activation.wav
# ✓ Generated: acknowledgement.wav
# ✓ Generated: error.wav
# ✓ Generated: correction.wav

# 4. Configure UBUAI URL
set UBUAI_URL=ws://10.1.10.20:8001/transcribe

# Or edit in code if needed

# 5. Test client
python hal_voice_client_full.py
```

**Expected output**:
```
============================================================
HAL Voice Client - Full Implementation
============================================================

✓ Wake word detection enabled
  Say: 'Hey Jarvis' or 'Computer'

Listening...
(Press Ctrl+C to exit)
```

---

## 🧪 Testing the Full System

### Test 1: Wake Word Detection

**Actions**:
1. Run client
2. Say: "**Hey Jarvis**"
3. Verify: Activation sound plays
4. Say: "**What medications am I taking?**"
5. Wait 3 seconds (silence)
6. Verify: Acknowledgement sound plays
7. Verify: Response audio plays

**Expected Flow**:
```
User: "Hey Jarvis"
→ 🔊 activation.wav
User: "What medications am I taking?"
→ (3 seconds)
→ 🔊 acknowledgement.wav
→ 📤 Sending audio to UBUAI
→ ⏳ Waiting for response
→ ✓ Received audio
→ 🔊 Response plays
→ ⏱️ 10s follow-up window
```

---

### Test 2: Interruption

**Actions**:
1. Say: "**Hey Jarvis**"
2. Start saying: "Remind me to call—"
3. Say: "**Hey Jarvis**" (interrupt mid-sentence)
4. Verify: Activation sound plays AGAIN
5. Say: "**What's my appointment schedule?**"
6. Wait 3 seconds

**Expected**:
- First utterance discarded
- Only final query processed

---

### Test 3: Follow-up (10s Passive Window)

**Actions**:
1. Say: "**Hey Jarvis**"
2. Say: "**What medications am I taking?**"
3. Wait for response
4. Within 10 seconds, say: "**Tell me about Metformin**" (NO wake word)
5. Verify: Immediately starts recording (no activation sound)
6. Wait 3 seconds

**Expected**:
- Follow-up processed without wake word
- New 10s window starts after response

---

### Test 4: Passive Timeout

**Actions**:
1. Say: "**Hey Jarvis**"
2. Say: "**What medications am I taking?**"
3. Wait for response
4. Wait MORE than 10 seconds
5. Say: "**What's my schedule?**" (without wake word)

**Expected**:
- Nothing happens (10s window expired)
- Need to say wake word again

---

## 📊 Monitoring & Logs

### UBUAI Server Logs

```bash
# Running server shows:
[2025-11-11 10:30:00] Client connected: s-12345
[2025-11-11 10:30:02] Processing 48000 bytes of audio
[2025-11-11 10:30:02] Transcribed: What medications am I taking?
[2025-11-11 10:30:02] QM response: I detected a medication query...
[2025-11-11 10:30:03] Sent 25000 bytes of response audio
[2025-11-11 10:30:03] Session closed: s-12345
```

### QM Listener Logs

In QM terminal:
```
Connection accepted
Read 120 bytes after 5 attempts
Session: s-12345
Text: What medications am I taking?
Intent: MEDICATION
Response sent: 150 bytes
Request completed, connection closed
```

### Client Logs

```
👂 Wake word detected
🎤 Listening... (speak now)
🔇 Silence detected - Processing...
📤 Sending 48000 bytes to UBUAI...
⏳ Waiting for response...
✓ Received 25000 bytes of audio
🔊 Playing response...
⏱️ 10s follow-up window (speak without wake word)
```

---

## 🐛 Troubleshooting

### Client Can't Connect to UBUAI

**Symptom**: "Connection refused" or timeout

**Fixes**:
1. Verify UBUAI server is running: `curl http://10.1.10.20:8001/`
2. Check network connectivity: `ping 10.1.10.20`
3. Check firewall allows port 8001
4. Verify URL in client: `ws://10.1.10.20:8001/transcribe`

---

### UBUAI Can't Connect to QM

**Symptom**: "QM connection error" in UBUAI logs

**Fixes**:
1. Verify QM listener is running: `netstat -an | findstr 8767`
2. Test direct connection (see Step 3 above)
3. Check OpenQM host/port in `.env`
4. Ensure QM listener is accepting connections

---

### Wake Word Not Detecting

**Symptom**: No response when saying "Hey Jarvis"

**Fixes**:
1. Speak clearly and emphasize "JARVIS"
2. Try alternate: "COMPUTER"
3. Check microphone input level (should be audible)
4. Use keyboard mode fallback (automatically activates if wake word fails)

---

### No Audio Playback

**Symptom**: Client says "Received audio" but no sound

**Fixes**:
1. Check audio output device is selected
2. Verify volume is not muted
3. Test sound files manually: Open `activation.wav` in media player
4. On Windows: May need Windows Media Feature Pack

---

### Transcription Errors

**Symptom**: "Transcription failed" or "[transcription not available]"

**Fixes**:
1. Check faster-whisper installed: `pip list | grep faster-whisper`
2. If GPU error, set `WHISPER_DEVICE=cpu` in `.env`
3. Verify CUDA toolkit installed (for GPU)
4. Check audio format (should be PCM16, 16kHz, mono)

---

### QM Parse Errors

**Symptom**: "JSON Parse Error" in QM logs

**Fixes**:
1. Check message format from UBUAI
2. Verify newline at end of JSON
3. Test with simple parser (fallback activates automatically)
4. Check for special characters in transcription

---

## 🔧 Advanced Configuration

### Change Wake Word

Edit `hal_voice_client_full.py`:

```python
wake_words = ['alexa_v0.1']  # or 'hey_mycroft_v0.1', 'ok_naomi_v0.1'
```

Available models: https://github.com/dscripka/openWakeWord

---

### Adjust Silence Threshold

Edit client constants:

```python
SILENCE_THRESHOLD = 2.0  # seconds (default: 3.0)
```

---

### Change Follow-up Window

```python
FOLLOW_UP_WINDOW = 15.0  # seconds (default: 10.0)
```

---

### Switch to CPU Transcription

In UBUAI `.env`:

```
WHISPER_DEVICE=cpu
```

Performance: ~2-5 seconds per query (vs <1s on GPU)

---

### Disable ElevenLabs (Use pyttsx3)

In UBUAI `.env`:

```
ELEVENLABS_API_KEY=
```

Server automatically falls back to pyttsx3 (offline TTS)

---

## 🎉 Success Criteria

✅ **System is working if**:
1. Wake word triggers activation sound instantly (<50ms)
2. Silence detection triggers processing within 3 seconds
3. UBUAI transcribes audio and queries QM
4. QM responds with intent and action
5. Response audio plays back on client
6. 10s follow-up window allows speaking without wake word
7. Interruption (wake word during active) restarts recording

---

## 📚 Next Steps

After successful deployment:

1. **Add More Handlers**: Create `VOICE.HANDLE.APPOINTMENT`, `VOICE.HANDLE.HEALTH`, etc.
2. **Improve Intent Classification**: Use LLM for better intent detection
3. **Add Voice Biometrics**: Identify user by voice
4. **Multi-User Support**: Track multiple sessions
5. **Home Assistant Integration**: Add HA command handler
6. **Mobile Clients**: iOS/Android apps
7. **Web Interface**: Browser-based client

---

## 📞 Support

**Documentation**:
- UBUAI Server: `ubuai_server/README.md`
- Voice Client: `clients/README.md`
- QM Listener: `BP/VOICE.LISTENER` (comments)

**Architecture Diagram**: See `DOCS/docs/ARCHITECTURE.md`

**Test Scripts**:
- `tests/test_voice_complete.py` - End-to-end test
- `tests/test_qm_direct.py` - QM listener test

---

**Deployment Complete! 🎉**

Your HAL voice system is now operational with:
- ✅ Wake word detection with interruption support
- ✅ GPU-accelerated transcription
- ✅ Intent routing and handlers
- ✅ TTS response generation
- ✅ 10-second follow-up window
- ✅ Full state machine implementation

Enjoy your voice-controlled HAL assistant!

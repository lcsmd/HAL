# Starting the HAL Voice System

Complete guide to testing the voice interface across all three machines.

---

## Quick Start (All Steps)

### 1. **Ubuntu AI Server (ubuai)** - Already Running ✓

Your Faster-Whisper and Ollama should already be running:

```bash
# Verify Faster-Whisper is running
curl http://ubuai.q.lcs.ai:9000/health

# Verify Ollama is running
curl http://ubuai.q.lcs.ai:11434/api/tags
```

If not running, start them:

```bash
# Start Faster-Whisper (on ubuai)
cd /path/to/faster-whisper
python server.py --port 9000 --model large-v3

# Ollama should already be running as a service
ollama serve
```

---

### 2. **Windows QM Server** - Start Voice Services

#### A. Test Server Connections

```powershell
cd C:\qmsys\hal
python tests\test_whisper_connection.py
```

Expected output:
```
✓ Connection successful!
  Faster-Whisper: ✓ OK
  Ollama:         ✓ OK
```

#### B. Start Voice Gateway (Python WebSocket Server)

**Terminal 1** - Voice Gateway:
```powershell
cd C:\qmsys\hal\PY
python voice_gateway.py
```

Expected output:
```
[2025-10-30 ...] Starting Voice Gateway on 0.0.0.0:8765
```

#### C. Start QM Voice Listener (OpenQM TCP Server)

**Terminal 2** - QM Voice Listener:
```cmd
cd C:\qmsys\bin
qm

At TCL prompt:
LOGTO HAL
BASIC BP VOICE.LISTENER
CATALOG BP VOICE.LISTENER
PHANTOM VOICE.LISTENER
```

Expected output:
```
HAL Voice Listener starting...
Port: 8767
Voice Listener active on port 8767
Waiting for connections...
```

#### D. Test the Gateway

**Terminal 3** - Run test:
```powershell
cd C:\qmsys\hal
python tests\test_voice_simple.py
```

Expected output:
```
✓ Connection successful
✓ Acknowledgment received
✓ State changed to active listening
✓ Heartbeat sent successfully
Test suite complete!
```

---

### 3. **Your Mac** - Install and Run Client

#### A. Install Dependencies

```bash
# Install Python packages
pip install websockets sounddevice numpy

# Optional: Install wake word detection
pip install pvporcupine

# If pvporcupine installation fails (common on Mac):
# Get access key from https://console.picovoice.ai/ (free)
# You can use keyboard activation instead
```

#### B. Download the Client

You need to transfer `clients/mac_voice_client.py` from Windows to your Mac.

**Option 1: Manual copy via network**
```bash
# From your Mac, if you have network access to Windows server:
scp user@qm-server:C:/qmsys/hal/clients/mac_voice_client.py ~/hal_client.py
```

**Option 2: I can provide the file content**
Let me know and I'll output it for you to copy.

#### C. Configure the Client

Edit `mac_voice_client.py`:

```python
# Change this line to your Windows server IP
GATEWAY_URL = "ws://YOUR_QM_SERVER_IP:8765"  # e.g., "ws://192.168.1.100:8765"

# If using Porcupine, add your access key
PORCUPINE_ACCESS_KEY = "YOUR_ACCESS_KEY"  # Get from https://console.picovoice.ai/
```

#### D. Run the Client

```bash
python mac_voice_client.py
```

Expected output:
```
HAL Voice Client for Mac
============================================================

Connecting to ws://192.168.1.100:8765...
✓ Connected!
Session ID: abc123...
State: passive_listening
✓ Wake word detection enabled: ['hey computer']
✓ Audio stream started

Keyboard commands:
  [SPACE] - Simulate wake word
  h - Send 'hold' command
  s - Send 'stop' command
  r - Send 'repeat' command
  g - Send 'goodbye' command
  q - Quit
```

---

## Testing the Full Flow

### Test 1: Keyboard Activation (No Wake Word Needed)

1. **Press SPACE** on Mac client
2. Should see: `🎤 Wake word detected!`
3. Should hear: *chime sound* (if audio feedback configured)
4. State changes to: `→ State: active_listening`
5. **Speak**: "What medications am I taking?"
6. Should see: `🔄 Processing...`
7. Should see: `🤖 HAL: [response about medications]`
8. **Wait 10 seconds** - should return to passive mode

### Test 2: Wake Word Detection (If Porcupine Configured)

1. **Say**: "Hey computer"
2. Same flow as above

### Test 3: Interrupt Command

1. **Press SPACE** to activate
2. State changes to active
3. **Press 'h'** (hold command)
4. Should immediately return to passive mode

### Test 4: Follow-up Conversation

1. **Press SPACE** to activate
2. Say: "What medications am I taking?"
3. Get response
4. Within 10 seconds, say: "Tell me about Metformin" (NO SPACE/wake word needed)
5. Should get response about Metformin

---

## Troubleshooting

### Mac Client Can't Connect

**Check network connectivity:**
```bash
# From Mac, ping Windows server
ping YOUR_QM_SERVER_IP

# Test WebSocket port is open
telnet YOUR_QM_SERVER_IP 8765
```

**Check firewall on Windows:**
```powershell
# Allow port 8765
netsh advfirewall firewall add rule name="HAL Voice Gateway" dir=in action=allow protocol=TCP localport=8765
```

### Voice Gateway Not Receiving Messages

**Check Windows server logs:**
```powershell
# In Terminal 1, you should see:
[2025-10-30 ...] Client registered: abc123...
[2025-10-30 ...] Wake word detected for session abc123...
```

### QM Listener Not Responding

**Check if it's running:**
```qm
LIST.READU
```

Should show VOICE.LISTENER with a read lock.

**If not running, start again:**
```qm
PHANTOM VOICE.LISTENER
```

### Transcription Errors

**Test Whisper directly:**
```bash
# From Windows or Mac:
python tests/test_whisper_connection.py
```

If fails:
- Check ubuai server is accessible
- Check Faster-Whisper is running
- Check port 9000 is not blocked

### Audio Issues on Mac

**Check microphone permissions:**
1. System Settings → Privacy & Security → Microphone
2. Enable for Terminal (or iTerm)

**List audio devices:**
```python
python -c "import sounddevice as sd; print(sd.query_devices())"
```

**Test audio capture:**
```python
python -c "import sounddevice as sd; import numpy as np; print(sd.rec(16000, samplerate=16000, channels=1))"
```

---

## Architecture Recap

```
Mac Client (Python)
  ↓ WebSocket
Windows QM Server (Python + OpenQM)
  ↓ HTTP/TCP
Ubuntu AI Server (Faster-Whisper + Ollama)
```

All three machines working together!

---

## What I Can Do

**Yes, I can coordinate across all three:**

1. **Windows QM Server**: I'm running here now and can:
   - Start/stop voice_gateway.py
   - Compile and run QM programs
   - Monitor logs
   - Test connections

2. **Your Mac**: You can:
   - Run the client I provide
   - Test microphone/audio
   - Speak to HAL
   - I can't directly run code on your Mac, but I can provide scripts/instructions

3. **Ubuntu AI Server (ubuai)**: I can:
   - Help test connections to Faster-Whisper
   - Help test Ollama
   - Cannot start/stop services directly, but can verify they're running

---

## Next Steps

1. **Run the simple test first** (on Windows):
   ```powershell
   python tests\test_voice_simple.py
   ```

2. **If that works**, start the full services and run Mac client

3. **If you need help with Mac setup**, I can provide step-by-step instructions

**Ready to start testing?** What would you like to test first?

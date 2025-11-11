# HAL Voice Client - Mac Quick Start

**Voice client runs on YOUR MAC** (not on QM or UBUAI servers)

---

## 🖥️ Architecture Clarity

```
┌─────────────────┐
│   YOUR MAC      │ ← Voice Client runs HERE
│  (Client)       │   - Wake word detection
│  10.1.x.x       │   - Audio capture/playback
└────────┬────────┘
         │ WebSocket
         ▼
┌─────────────────┐
│  UBUAI Server   │ ← GPU server (Linux)
│  10.1.10.20     │   - Faster-Whisper
└────────┬────────┘   - TTS
         │ TCP
         ▼
┌─────────────────┐
│  QM Server      │ ← OpenQM (Windows)
│  10.1.34.103    │   - Voice Listener
└─────────────────┘   - Intent routing
```

---

## 📋 Mac Prerequisites

### 1. Check Python version
```bash
python3 --version
# Need Python 3.8 or higher
```

If not installed:
```bash
# Install via Homebrew
brew install python@3.11
```

### 2. Install Xcode Command Line Tools (if needed)
```bash
xcode-select --install
```

### 3. Install audio dependencies
```bash
# Install PortAudio (required for sounddevice)
brew install portaudio

# Install FFmpeg (for audio playback)
brew install ffmpeg
```

---

## 🚀 Installation (5 minutes)

### Step 1: Navigate to client directory
```bash
cd /path/to/hal/clients

# Example:
cd ~/Projects/hal/clients
# or if mounted from Windows share:
cd /Volumes/QMSYS/hal/clients
```

### Step 2: Create Python virtual environment (recommended)
```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Python dependencies
```bash
pip install -r requirements.txt
```

**Expected packages**:
- numpy (audio processing)
- sounddevice (audio capture)
- webrtcvad (voice activity detection)
- simpleaudio (audio playback)
- websockets (UBUAI connection)
- openwakeword (wake word detection)

### Step 4: Generate audio feedback sounds
```bash
python3 generate_sounds.py
```

**Output**:
```
Generating HAL voice feedback sounds...

✓ Generated: activation.wav
✓ Generated: acknowledgement.wav
✓ Generated: error.wav
✓ Generated: correction.wav

✓ All sounds generated successfully!
```

### Step 5: Configure UBUAI URL
```bash
# Set environment variable
export UBUAI_URL=ws://10.1.10.20:8001/transcribe

# Or edit hal_voice_client_full.py line 27:
# UBUAI_URL = 'ws://10.1.10.20:8001/transcribe'
```

---

## 🎤 Test Your Microphone

Before running the client, test your Mac's microphone:

```bash
# List audio devices
python3 -c "import sounddevice as sd; print(sd.query_devices())"
```

**Look for your microphone** (e.g., "MacBook Pro Microphone", "USB Microphone")

If you have multiple microphones, the client will auto-select or you can choose in settings.

---

## 🚀 Run the Voice Client

```bash
python3 hal_voice_client_full.py
```

**Expected output**:
```
============================================================
HAL Voice Client - Full Implementation
============================================================

Loading wake word model...
✓ Wake word loaded: hey_jarvis_v0.1
  Say: 'Hey Jarvis' or 'Computer'

Listening...
(Press Ctrl+C to exit)
```

---

## 🧪 Test It!

### Test 1: Wake Word Detection
```
YOU: "Hey Jarvis"
→ 🔊 Beep! (activation sound)
YOU: "What medications am I taking?"
→ (wait 3 seconds)
→ 🔊 Beep! (acknowledgement)
→ ⏳ Processing...
→ 🔊 Response plays!
```

### Test 2: Interruption
```
YOU: "Hey Jarvis"
YOU: "Remind me to—"
YOU: "Hey Jarvis"  ← interrupts
→ 🔊 Beep! (confirms restart)
YOU: "What's my schedule?"
→ Only final query processed
```

### Test 3: Follow-up
```
YOU: "Hey Jarvis"
YOU: "What medications am I taking?"
→ Response plays
YOU: "Tell me about Metformin"  ← no wake word
→ Follow-up processed
```

---

## 🐛 Mac-Specific Troubleshooting

### Issue: "No module named '_tkinter'"
**Fix**: Not needed for this client (we don't use tkinter)

### Issue: "PortAudio library not found"
**Fix**:
```bash
brew install portaudio
pip install --upgrade sounddevice
```

### Issue: "Microphone permission denied"
**Fix**:
1. Go to **System Preferences** → **Security & Privacy** → **Privacy** → **Microphone**
2. Check the box next to **Terminal** (or iTerm2, etc.)
3. Restart terminal and try again

### Issue: "Wake word not detecting"
**Fixes**:
- Speak clearly: "Hey JAR-VIS"
- Try alternate: "COM-PU-TER"
- Check microphone input level in System Preferences
- Client will auto-fallback to keyboard mode if wake word fails

### Issue: "No audio playback"
**Fixes**:
- Check volume: System Preferences → Sound → Output
- Test manually: `afplay activation.wav`
- Verify speakers/headphones connected

### Issue: "Connection refused to UBUAI"
**Fixes**:
```bash
# Test UBUAI server is reachable
curl http://10.1.10.20:8001/

# Test network connectivity
ping 10.1.10.20

# Check if on same network (VPN may be needed)
```

### Issue: "SSL/TLS errors"
**Fix**: Use `ws://` not `wss://` (no SSL for local network)

---

## 🎛️ Mac Audio Settings

### Recommended Settings

**System Preferences → Sound → Input**:
- Select your microphone
- Input volume: 50-80% (adjust based on distance)
- Use ambient noise reduction: ✅ (if available)

**System Preferences → Sound → Output**:
- Select speakers/headphones
- Output volume: Comfortable level

### Multiple Microphones

If you have multiple microphones, the client will try to auto-select:
1. USB microphones (preferred)
2. Webcam microphones
3. Built-in microphone

To manually select, edit `hal_voice_client_full.py` around line 200 in `select_microphone()`.

---

## 🔧 Advanced Mac Setup

### Run in Background
```bash
# Run with nohup
nohup python3 hal_voice_client_full.py > hal_client.log 2>&1 &

# View logs
tail -f hal_client.log
```

### Create Alias
Add to `~/.zshrc` or `~/.bash_profile`:
```bash
alias hal='cd ~/Projects/hal/clients && source venv/bin/activate && python3 hal_voice_client_full.py'
```

Then just run:
```bash
hal
```

### Auto-start on Login

Create `~/Library/LaunchAgents/com.hal.voiceclient.plist`:
```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.hal.voiceclient</string>
    <key>ProgramArguments</key>
    <array>
        <string>/Users/YOUR_USERNAME/Projects/hal/clients/venv/bin/python3</string>
        <string>/Users/YOUR_USERNAME/Projects/hal/clients/hal_voice_client_full.py</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
</dict>
</plist>
```

Load it:
```bash
launchctl load ~/Library/LaunchAgents/com.hal.voiceclient.plist
```

---

## 📊 Performance on Mac

**Typical latency** (M1/M2 Mac):
- Wake word detection: 20-30ms ✅
- Audio capture: 10-20ms ✅
- Network to UBUAI: 50-100ms ✅
- Total client overhead: **<150ms** ✅

**CPU usage**:
- Idle (passive listening): 5-10%
- Active (wake word + VAD): 15-25%

---

## 🔒 Security Notes

### Network
- Voice data sent to UBUAI server (local network)
- No cloud services by default (unless using ElevenLabs TTS)
- WebSocket not encrypted (use VPN if on untrusted network)

### Microphone Access
- macOS will prompt for microphone permission first time
- Client only records when wake word detected or in active mode
- Audio not saved to disk (buffered in memory only)

---

## 📝 File Locations (Mac)

```
~/Projects/hal/clients/           ← Your working directory
├── hal_voice_client_full.py      ← Main client script
├── requirements.txt               ← Python dependencies
├── generate_sounds.py             ← Sound generator
├── README.md                      ← General docs
├── MAC_QUICK_START.md            ← This file
├── venv/                          ← Virtual environment (you create)
├── activation.wav                 ← Generated sounds
├── acknowledgement.wav
├── error.wav
└── correction.wav
```

---

## 🎉 You're Ready!

**To run HAL voice client on your Mac**:

1. ✅ Servers running (UBUAI + QM on remote machines)
2. ✅ Client installed on your Mac
3. ✅ Microphone permission granted
4. ✅ Network connectivity to UBUAI

**Start the client**:
```bash
cd ~/Projects/hal/clients
source venv/bin/activate
python3 hal_voice_client_full.py
```

**Say**: "**Hey Jarvis, what medications am I taking?**"

🎤 **Enjoy your voice-controlled AI assistant!**

---

## 🆘 Still Need Help?

**Check logs**:
```bash
# Client logs (in terminal where it's running)
# Shows: wake word detection, state changes, network calls

# UBUAI logs (on UBUAI server)
# Shows: transcription, QM connection, TTS

# QM logs (in QM terminal)
# Shows: intent detection, handler routing
```

**Test individual components**:
```bash
# Test UBUAI connection
curl http://10.1.10.20:8001/

# Test microphone
python3 -c "import sounddevice as sd; print(sd.query_devices())"

# Test audio playback
afplay activation.wav
```

**Full documentation**: See `README.md` in clients folder

---

**Mac setup complete!** Your voice client is ready to run on macOS. 🍎✅

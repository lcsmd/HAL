# HAL Voice Assistant - START HERE

**Welcome to the Unified HAL Voice Assistant System!**

This document will get you started in 5 minutes.

---

## 🎯 What You Have

A complete voice-activated personal assistant with:

✅ **Wake word detection** - Say "Hey Jarvis" or "Computer"  
✅ **Natural conversation** - 10-second follow-up window  
✅ **Interruption handling** - Say wake word to restart  
✅ **Star Trek sounds** - TNG computer activation chirp  
✅ **GPU acceleration** - Fast STT with Faster-Whisper  
✅ **OpenQM integration** - Business logic and database  

---

## 📋 Quick Architecture

```
Mac Client (your computer)
    ↓ ws://10.1.10.20:8585
Voice Server (Ubuntu GPU server)
    ↓ ws://10.1.34.103:8745
AI Server (Windows OpenQM server)
```

---

## 🚀 Quick Start (15 Minutes)

### Step 1: Start AI Server (Windows - 5 min)

```powershell
# On Windows OpenQM server (10.1.34.103)
cd C:\qmsys\hal\voice_assistant_v2\ai_server
.\setup_windows.ps1 -AutoStart
```

Verify it's running:
```powershell
.\status_ai_server.bat
```

Should show port 8745 listening.

---

### Step 2: Start Voice Server (Ubuntu - 5 min)

```bash
# On Ubuntu GPU server (10.1.10.20)
cd /path/to/voice_assistant_v2/voice_server
sudo ./setup_ubuntu.sh
```

When prompted, press 'y' to start now.

Verify it's running:
```bash
sudo systemctl status voice-server
```

Should show "active (running)".

---

### Step 3: Start Client - ONE COMMAND!

**Mac / Linux:**
```bash
cd /path/to/voice_assistant_v2/client
./deploy.sh
```

**Windows:**
```powershell
cd C:\path\to\voice_assistant_v2\client
.\deploy.ps1
```

**That's it!** The deploy script handles everything:
- ✅ Checks dependencies
- ✅ Creates virtual environment  
- ✅ Installs packages
- ✅ Copies sound files
- ✅ Starts the client

---

#### Manual Deployment (Alternative)

If you prefer step-by-step:

```bash
# On your Mac
cd /path/to/voice_assistant_v2/client

# Setup (first time only)
./setup_mac.sh

# Copy sound files from existing clients/ directory
./copy_sounds.sh

# Run the client
source venv/bin/activate
python hal_voice_client.py
```

You should see:
```
✓ Wake word loaded: hey_jarvis_v0.1
  🎤 Say: "HEY JARVIS"
  
  💡 TIP: Change to 'COMPUTER' later:
     1. Train COMPUTER model (see TRAIN_COMPUTER_WAKE_WORD.md)
     2. Set: export WAKE_WORD=computer_v0.1

✓ Loaded activation: activation.mp3 (MP3)
✓ Loaded acknowledgement: acknowledgement.wav
Listening...
```

---

## 🎤 Try It!

Say: **"HEY JARVIS"**

You should hear the TNG computer chirp! 🎵

Then say: **"What time is it?"**

Wait 3 seconds of silence.

The system will respond!

---

## 💡 About the Wake Word

**Current**: "HEY JARVIS" (works immediately - no training)

**Why HEY JARVIS:**
- ✅ Works immediately (0 setup time)
- ✅ Pre-trained model available
- ✅ Sci-fi themed (Iron Man's AI assistant)
- ✅ 4 syllables - easy to detect, low false positives

**Future**: Switch to "COMPUTER" (optional - 2-3 hours to train)
```bash
# 1. Train COMPUTER model (see TRAIN_COMPUTER_WAKE_WORD.md)
# 2. Switch wake word:
export WAKE_WORD=computer_v0.1
python hal_voice_client.py
# Now say: "COMPUTER"
```

**Other Options**:
- "HEY MYCROFT" - `export WAKE_WORD=hey_mycroft_v0.1`
- "OK NAOMI" - `export WAKE_WORD=ok_naomi_v0.1`

---

## 📚 Documentation

- **`UNIFIED_ARCHITECTURE.md`** - Complete system architecture
- **`README.md`** - Full documentation
- **`QUICKSTART.md`** - Detailed 15-minute guide
- **`DEPLOYMENT_CHECKLIST.md`** - Production deployment

---

## 🔧 Configuration

### Client (Mac)

**Environment variables:**
```bash
export VOICE_SERVER_URL=ws://10.1.10.20:8585
export CLIENT_ID=mac_office_01
export USER_ID=lawr
```

**Or command line:**
```bash
python hal_voice_client.py --url ws://10.1.10.20:8585 --client-id mac_01 --user-id lawr
```

### Voice Server (Ubuntu)

Edit `voice_server.py`:
```python
CLIENT_PORT = 8585
AI_SERVER_HOST = "10.1.34.103"
AI_SERVER_PORT = 8745
WHISPER_MODEL = "large-v3"
WHISPER_DEVICE = "cuda"  # or "cpu"
```

### AI Server (Windows)

Uses `INCLUDE/MASTER.H` for all constants:
```basic
PORT = AI.SERVER.PORT  ; 8745 from CONSTANTS.H
```

---

## 🐛 Troubleshooting

### Client won't start

```bash
# Install PortAudio
brew install portaudio

# Reinstall dependencies
pip install --force-reinstall -r requirements.txt
```

### Voice server won't start

```bash
# Check logs
journalctl -u voice-server -n 50

# If CUDA not found, use CPU
# Edit voice_server.py: WHISPER_DEVICE = "cpu"

# Restart
sudo systemctl restart voice-server
```

### AI server won't start

```powershell
# Check if port is blocked
netstat -an | findstr 8745

# View logs
.\view_logs.bat

# Restart
.\start_ai_server.bat
```

### Can't connect between components

```bash
# Test voice server from Mac
nc -zv 10.1.10.20 8585

# Test AI server from voice server
nc -zv 10.1.34.103 8745

# Check firewalls
sudo ufw status  # Ubuntu
Get-NetFirewallRule | Where-Object {$_.DisplayName -like "*Voice*"}  # Windows
```

---

## 🎯 Listening Modes Explained

### PLM (Passive Listening Mode)
- Waiting for wake word
- Say "Hey Jarvis" or "Computer"

### ALM (Active Listening Mode)
- Recording your speech
- Detects 3 seconds of silence
- Can be interrupted by wake word again

### ASM (Active Speaking Mode)
- Playing response audio
- Say "wake_word stop" to interrupt

### RLM (Response Listening Mode)
- 10-second follow-up window
- Speak without wake word
- Automatic after response

---

## 📂 File Locations

```
voice_assistant_v2/
├── client/
│   ├── hal_voice_client.py     ← Run this on Mac
│   ├── setup_mac.sh             ← Setup script
│   └── copy_sounds.sh           ← Copy TNG sounds
│
├── voice_server/
│   ├── voice_server.py          ← Runs on Ubuntu GPU
│   └── setup_ubuntu.sh          ← Setup script
│
├── ai_server/
│   ├── AI.SERVER                ← Runs on Windows QM
│   └── setup_windows.ps1        ← Setup script
│
└── INCLUDE/
    ├── MASTER.H                 ← Include in all QM programs
    ├── CONSTANTS.H              ← System constants
    └── VOICE.UTILS.H            ← Utilities
```

---

## ✅ System Check

Before using, verify:

- [ ] AI Server running (Windows) - port 8745 listening
- [ ] Voice Server running (Ubuntu) - port 8585 listening
- [ ] Client connects to voice server
- [ ] Sound files copied (activation.mp3, acknowledgement.wav)
- [ ] Wake word detecting
- [ ] Can transcribe audio
- [ ] Receives responses

If all checked: **You're ready to go!** 🎉

---

## 🆘 Need Help?

1. **Check logs:**
   - Client: Terminal output
   - Voice Server: `journalctl -u voice-server -f`
   - AI Server: `.\view_logs.bat`

2. **Read full docs:**
   - `UNIFIED_ARCHITECTURE.md`
   - `README.md`

3. **Test components individually:**
   - AI Server: `.\status_ai_server.bat`
   - Voice Server: `sudo systemctl status voice-server`
   - Client: Run with `--help` flag

---

## 🎉 Success!

If you can say **"Hey Jarvis, what time is it?"** and get a response:

**Congratulations! Your HAL voice assistant is working!** 🎊

Next steps:
- Customize intent handlers in `AI.SERVER`
- Add TTS integration in `voice_server.py`
- Deploy additional clients
- Configure auto-start

---

**Enjoy your voice-controlled AI assistant!** 🎤🤖

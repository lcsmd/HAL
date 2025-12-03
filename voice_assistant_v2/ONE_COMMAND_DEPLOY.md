# 🚀 ONE COMMAND DEPLOYMENT

**Deploy HAL Voice Client with a single command on any platform.**

---

## 💻 Mac / Linux

### Single Command:

```bash
cd voice_assistant_v2/client
./deploy.sh
```

**That's it!** 🎉

The script will:
1. ✅ Check for Python 3
2. ✅ Install system dependencies (portaudio, ffmpeg via Homebrew)
3. ✅ Create virtual environment
4. ✅ Install Python packages (openwakeword, websockets, etc.)
5. ✅ Copy sound files from CLIENT/ directory
6. ✅ Start the HAL voice client

**Then say:** "HEY JARVIS, what time is it?"

---

## 🪟 Windows

### Single Command:

```powershell
cd voice_assistant_v2\client
.\deploy.ps1
```

**That's it!** 🎉

The script will:
1. ✅ Check for Python 3
2. ✅ Create virtual environment
3. ✅ Install Python packages (openwakeword, websockets, etc.)
4. ✅ Copy sound files from CLIENT\ directory
5. ✅ Start the HAL voice client

**Then say:** "HEY JARVIS, what time is it?"

---

## 📋 Prerequisites

### Mac:
- **Python 3** - Install with `brew install python3`
- **Homebrew** (optional) - https://brew.sh
  - If you have Homebrew, script installs portaudio & ffmpeg
  - If not, script still works but may need manual audio setup

### Windows:
- **Python 3** - Download from https://www.python.org/downloads/
  - Make sure "Add Python to PATH" is checked during installation

### Linux:
- **Python 3** - Usually pre-installed, or `sudo apt install python3 python3-venv`
- **portaudio** - `sudo apt install portaudio19-dev`
- **ffmpeg** - `sudo apt install ffmpeg`

---

## 🎤 What Happens Next

After running the deploy script:

```
========================================
HAL Voice Client - One-Command Deploy
========================================

✓ Found: Python 3.11.5
✓ Homebrew found
✓ portaudio already installed
✓ ffmpeg already installed
✓ Virtual environment created
✓ Python packages installed
✓ Copied activation.mp3
✓ Copied acknowledgement.wav
✓ Configuration file found

========================================
✓ Deployment Complete!
========================================

Voice Server: ws://10.1.10.20:8585
Wake Word: HEY JARVIS

Starting HAL Voice Client...

Say: "HEY JARVIS, what time is it?"

Press Ctrl+C to exit

========================================

Loading wake word model...
✓ Wake word loaded: hey_jarvis_v0.1
  🎤 Say: "HEY JARVIS"
  
  💡 TIP: Change to 'COMPUTER' later:
     1. Train COMPUTER model (see TRAIN_COMPUTER_WAKE_WORD.md)
     2. Set: export WAKE_WORD=computer_v0.1

✓ Loaded activation: activation.mp3 (MP3)
✓ Loaded acknowledgement: acknowledgement.wav
Listening...
```

**Now just say:** "HEY JARVIS"

---

## 🔄 Run Again Later

To start the client after initial deployment:

**Mac/Linux:**
```bash
cd voice_assistant_v2/client
source venv/bin/activate
python hal_voice_client.py
```

**Windows:**
```powershell
cd voice_assistant_v2\client
venv\Scripts\Activate.ps1
python hal_voice_client.py
```

Or just run the deploy script again - it's idempotent (safe to run multiple times).

---

## 🛠️ Customization

### Change Voice Server IP

Edit `voice_client.config`:
```ini
[voice_server]
host = 10.1.10.20
port = 8585
```

### Change Wake Word

**Option 1: Use environment variable**
```bash
export WAKE_WORD=hey_mycroft_v0.1
./deploy.sh
```

**Option 2: Edit the script**
```python
# In hal_voice_client.py line 108:
wake_word_pref = os.getenv('WAKE_WORD', 'hey_jarvis_v0.1')
# Change to:
wake_word_pref = os.getenv('WAKE_WORD', 'hey_mycroft_v0.1')
```

### Available Wake Words

- `hey_jarvis_v0.1` (default)
- `hey_mycroft_v0.1`
- `ok_naomi_v0.1`
- `computer_v0.1` (requires training - see TRAIN_COMPUTER_WAKE_WORD.md)

---

## 🐛 Troubleshooting

### "Python 3 not found"

**Mac:**
```bash
brew install python3
```

**Windows:**
Download from https://www.python.org/downloads/
(Check "Add Python to PATH")

**Linux:**
```bash
sudo apt update
sudo apt install python3 python3-venv python3-pip
```

---

### "portaudio not found" (Mac)

```bash
brew install portaudio
```

---

### "Sound files not copied"

The CLIENT/ directory should be at `../../CLIENT` relative to the client folder.

**Verify:**
```bash
ls ../../CLIENT/activation.mp3
ls ../../CLIENT/acknowledgement.wav
```

**Manual copy:**
```bash
mkdir -p sounds
cp ../../CLIENT/activation.mp3 sounds/
cp ../../CLIENT/acknowledgement.wav sounds/
```

---

### "Connection refused to voice server"

Make sure voice server is running on 10.1.10.20:8585

**Check voice server:**
```bash
# On Ubuntu GPU server
sudo systemctl status voice-server
```

---

## 📚 More Information

- **Complete Guide:** `START_HERE.md`
- **Ready to Use:** `READY_TO_USE.md`
- **Architecture:** `../UNIFIED_ARCHITECTURE.md`
- **Train Custom Wake Word:** `TRAIN_COMPUTER_WAKE_WORD.md`

---

## ✅ Summary

| Platform | Command |
|----------|---------|
| **Mac** | `cd voice_assistant_v2/client && ./deploy.sh` |
| **Windows** | `cd voice_assistant_v2\client && .\deploy.ps1` |
| **Linux** | `cd voice_assistant_v2/client && ./deploy.sh` |

**One command. Full deployment. Start talking to HAL!** 🎤

---

**Enjoy your voice-controlled AI assistant!** 🚀

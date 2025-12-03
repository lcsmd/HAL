# HAL Voice Mode Setup Guide

## 🎤 What You Need for Voice Mode

Voice mode requires:
1. ✅ **Voice libraries on client** (already installed!)
2. ⚠️ **Whisper server on Ubuntu** (needs setup)
3. ✅ **Voice Gateway running** (already running)
4. ⚠️ **Wake word models** (need to download)

---

## 🔧 Current Status

**On Windows Server (10.1.34.103):**
- ✅ Voice Gateway running on port 8768
- ✅ AI.SERVER running
- ✅ Query Router ready

**On Ubuntu Server (10.1.10.20):**
- ❌ Whisper server NOT running (port 9000)
- ❌ Ollama needs verification (port 11434)

**On Client PC:**
- ✅ Voice libraries installed
- ❌ Wake word models need download

---

## 📋 Setup Steps

### STEP 1: Install Whisper Server on Ubuntu (10.1.10.20)

**On the Ubuntu server, run these commands:**

```bash
# SSH to Ubuntu server
ssh user@10.1.10.20

# Navigate to services directory (you'll need to copy files first)
mkdir -p ~/hal_services
cd ~/hal_services

# Install Python dependencies
pip3 install faster-whisper fastapi uvicorn[standard] python-multipart

# Create whisper_server.py (see file below)

# Create systemd service
sudo nano /etc/systemd/system/faster-whisper.service
```

**Paste this service file:**
```ini
[Unit]
Description=Faster Whisper Transcription Server
After=network.target

[Service]
Type=simple
User=YOUR_USERNAME
WorkingDirectory=/home/YOUR_USERNAME/hal_services
ExecStart=/usr/bin/python3 /home/YOUR_USERNAME/hal_services/whisper_server.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

**Enable and start:**
```bash
sudo systemctl daemon-reload
sudo systemctl enable faster-whisper
sudo systemctl start faster-whisper
sudo systemctl status faster-whisper
```

**Test it:**
```bash
curl http://localhost:9000/health
# Should return: {"status":"ok"}
```

---

### STEP 2: Deploy Files to Ubuntu

**From Windows server, copy files to Ubuntu:**

```powershell
# Option A: Using SCP (if you have SSH access)
scp C:\qmsys\hal\ubuai_services\whisper_server.py user@10.1.10.20:~/hal_services/
scp C:\qmsys\hal\ubuai_services\faster-whisper.service user@10.1.10.20:~/

# Option B: Using network share
# Copy C:\qmsys\hal\ubuai_services\* to Ubuntu server
```

---

### STEP 3: Download Wake Word Models (Client PC)

**On your client PC, run:**

```powershell
# Create models directory
New-Item -ItemType Directory -Force -Path "C:\HAL\VOICE_ASSISTANT_V2\CLIENT\models"

# Download wake word model
$url = "https://github.com/dscripka/openWakeWord/releases/download/v0.5.1/hey_jarvis_v0.1.onnx"
Invoke-WebRequest -Uri $url -OutFile "C:\HAL\VOICE_ASSISTANT_V2\CLIENT\models\hey_jarvis_v0.1.onnx"

# Alternative models:
# - alexa_v0.1.onnx
# - hey_mycroft_v0.1.onnx  
# - hey_rhasspy_v0.1.onnx
```

---

### STEP 4: Verify Ollama (Optional - for LLM queries)

**On Ubuntu server:**

```bash
# Check if Ollama is running
curl http://localhost:11434/api/generate -d '{"model":"llama3.2:latest","prompt":"test","stream":false}'

# If not installed:
curl -fsSL https://ollama.com/install.sh | sh

# Pull model
ollama pull llama3.2:latest

# Create systemd service
sudo systemctl enable ollama
sudo systemctl start ollama
```

---

## 🧪 Testing Voice Mode

### Test 1: Verify Whisper Server

**From Windows server:**
```powershell
Invoke-WebRequest -Uri "http://10.1.10.20:9000/health"
```

Should return: `{"status":"ok"}`

### Test 2: Test Client Voice Detection

**On client PC:**
```powershell
cd C:\HAL\VOICE_ASSISTANT_V2\CLIENT

# Test imports
python -c "import pyaudio, openwakeword, webrtcvad; print('Voice libraries OK')"

# Check if models exist
Test-Path "models\hey_jarvis_v0.1.onnx"
```

### Test 3: Run Voice Client

```powershell
cd C:\HAL\VOICE_ASSISTANT_V2\CLIENT
python hal_voice_client_gui.py
```

**Should now show:** "Listening for wake word..." instead of "Voice components not available"

### Test 4: Try Voice Command

1. Say: **"Hey Jarvis"**
2. Wait for beep/tone
3. Say: **"What time is it"**
4. HAL should respond!

---

## 🔧 Alternative: Text-Only Mode

**Voice mode is optional!** Text mode works great:

```powershell
cd C:\HAL\VOICE_ASSISTANT_V2\CLIENT
python simple_gui.py
```

Just type your questions - no voice needed!

---

## 📊 Architecture

```
Client PC
  ├─ Microphone → pyaudio
  ├─ Wake word detection → openwakeword
  ├─ Voice activity → webrtcvad
  └─ WebSocket → Voice Gateway

Windows Server (10.1.34.103)
  ├─ Voice Gateway :8768
  │   └─ Routes audio to Whisper
  ├─ Query Router
  └─ AI.SERVER :8745

Ubuntu Server (10.1.10.20)
  ├─ Whisper :9000 (transcription)
  └─ Ollama :11434 (LLM)
```

---

## 🚀 Quick Deploy to Ubuntu

**Easiest method - Use prepared deployment package:**

```bash
# On Ubuntu server
cd ~
git clone https://github.com/lcsmd/HAL.git
cd HAL/ubuai_services

# Run installer
chmod +x install_services.sh
./install_services.sh

# Verify
sudo systemctl status faster-whisper
sudo systemctl status ollama
curl http://localhost:9000/health
```

---

## 📝 Troubleshooting

### "Voice components not available"
- Check libraries: `python -c "import pyaudio, openwakeword; print('OK')"`
- Install if missing: `pip install pyaudio openwakeword webrtcvad`

### "No response from voice"
- Check Whisper server: `curl http://10.1.10.20:9000/health`
- Check Voice Gateway logs on Windows server
- Verify network connectivity

### "Wake word not detected"
- Check models exist: `dir C:\HAL\VOICE_ASSISTANT_V2\CLIENT\models`
- Try different wake word model
- Check microphone permissions

### "Transcription failed"
- Whisper server not running on Ubuntu
- Network firewall blocking port 9000
- Check Ubuntu server logs: `journalctl -u faster-whisper -f`

---

## 📦 What's Already Done

✅ Voice libraries installed on client  
✅ Voice Gateway configured  
✅ Query routing ready  
✅ Deployment scripts prepared  

## 🔧 What You Need to Do

1. **Setup Whisper on Ubuntu** (port 9000)
2. **Download wake word models** (client)
3. **Test voice mode**

---

## 🎯 Summary

**For Text Mode (Works Now):**
```powershell
python simple_gui.py
```

**For Voice Mode (Need Ubuntu Setup):**
1. Install Whisper on Ubuntu (10.1.10.20)
2. Download wake word models
3. Run: `python hal_voice_client_gui.py`
4. Say "Hey Jarvis" + your question

---

**Documentation:** VOICE_MODE_SETUP.md  
**Ubuntu Services:** ubuai_services/  
**Status:** Text mode ready, Voice mode needs Ubuntu Whisper server

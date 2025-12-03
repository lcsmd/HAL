# Quick Deploy HAL Services to Ubuntu

## 🚀 One-Command Install

**On your Ubuntu server (10.1.10.20), run:**

```bash
# Clone the repo
cd ~
git clone https://github.com/lcsmd/HAL.git
cd HAL/ubuai_services

# Run installer
chmod +x install_services.sh
sudo ./install_services.sh

# This installs:
# - Faster-Whisper (port 9000)
# - Ollama (port 11434)
# - Both as systemd services
```

---

## ✅ Verify Installation

```bash
# Check services
sudo systemctl status faster-whisper
sudo systemctl status ollama

# Test Whisper
curl http://localhost:9000/health
# Should return: {"status":"ok"}

# Test Ollama
curl http://localhost:11434/api/tags
# Should list available models
```

---

## 🔧 Manual Install (If Needed)

### Install Whisper Server

```bash
# Install dependencies
pip3 install faster-whisper fastapi uvicorn[standard] python-multipart

# Copy service file
sudo cp faster-whisper.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable faster-whisper
sudo systemctl start faster-whisper
```

### Install Ollama

```bash
# Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Pull model
ollama pull llama3.2:latest

# Enable service
sudo systemctl enable ollama
sudo systemctl start ollama
```

---

## 🧪 Test from Windows

**From Windows server, test connectivity:**

```powershell
# Test Whisper
Invoke-WebRequest -Uri "http://10.1.10.20:9000/health"

# Test Ollama
Invoke-WebRequest -Uri "http://10.1.10.20:11434/api/tags"
```

---

## 🔥 Firewall Rules (If Needed)

```bash
# Allow ports
sudo ufw allow 9000/tcp   # Whisper
sudo ufw allow 11434/tcp  # Ollama
sudo ufw reload
```

---

## 📊 View Logs

```bash
# Whisper logs
sudo journalctl -u faster-whisper -f

# Ollama logs
sudo journalctl -u ollama -f
```

---

## 🎯 After Install

**Voice mode will work on the client!**

1. Download wake word models on client
2. Run: `python hal_voice_client_gui.py`
3. Say "Hey Jarvis" + your question

---

**Status:** Ready to deploy!  
**Services:** Whisper + Ollama  
**Target:** Ubuntu at 10.1.10.20

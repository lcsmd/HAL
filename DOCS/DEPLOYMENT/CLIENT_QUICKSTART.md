# HAL Client Quick Start

**5-minute setup for macOS or Windows text/voice clients**

---

## Choose Your Platform

- [macOS Quick Start](#macos-quick-start) (MacBook, iMac, Mac Mini)
- [Windows Quick Start](#windows-quick-start) (Windows 10/11)

---

## macOS Quick Start

### 1. Prerequisites (2 minutes)

```bash
# Check Python (should be 3.8+)
python3 --version

# If not installed:
brew install python3
```

### 2. Get Files (1 minute)

```bash
# From GitHub
cd ~/Documents
git clone https://github.com/lcsmd/hal.git
cd hal/mac_deployment_package

# Or download and extract ZIP
```

### 3. Setup (1 minute)

```bash
chmod +x setup_mac.sh test_connection.sh
./setup_mac.sh
source network_config.sh
```

### 4. Test (30 seconds)

```bash
./test_connection.sh
```

### 5. Run (NOW!)

```bash
# Text client
source venv/bin/activate
python3 hal_text_client.py

# Voice client (with wake word)
python3 hal_voice_client.py
```

**Done!** 🎉

---

## Windows Quick Start

### 1. Prerequisites (5 minutes)

1. Download Python: https://www.python.org/downloads/
2. Run installer
3. ✅ **CHECK**: "Add Python to PATH"
4. Click "Install Now"

Verify:
```powershell
python --version
```

### 2. Get Files (2 minutes)

```powershell
# Create directory
cd $env:USERPROFILE\Documents
mkdir hal_client
cd hal_client

# Copy files from QM server or download from GitHub
# Need: hal_text_client.py, hal_voice_client.py, requirements.txt
```

### 3. Setup (2 minutes)

```powershell
# Create virtual environment
python -m venv venv

# Activate
.\venv\Scripts\Activate.ps1

# If execution policy error:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Install dependencies
pip install websockets

# For voice (optional):
pip install pipwin
pipwin install pyaudio
pip install pvporcupine numpy simpleaudio
```

### 4. Test (30 seconds)

```powershell
python hal_text_client.py --query "Hello HAL"
```

### 5. Run (NOW!)

```powershell
# Text client
python hal_text_client.py

# Voice client
python hal_voice_client.py
```

**Done!** 🎉

---

## Example Queries

### Medical
```
What medications am I taking?
Show my appointments
List my allergies
When is my next doctor visit?
```

### Financial
```
Show recent transactions
What did I spend at Starbucks?
List reimbursable expenses
```

### General
```
Hello HAL
What can you do?
Help
```

---

## Troubleshooting

### "Connection refused"

**Check QM Server**:
```powershell
# On QM Server (10.1.34.103)
netstat -an | findstr 8768
# Should show: LISTENING

# If not, start listener:
# In QM terminal:
LOGTO HAL
PHANTOM EXECUTE "WEBSOCKET.LISTENER"
```

### "Module not found"

```bash
# macOS
source venv/bin/activate
pip install -r requirements.txt

# Windows
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### "Python not found" (Windows)

Reinstall Python with "Add to PATH" checked.

---

## Network Configuration

**Pre-configured** for:
- QM Server: `10.1.34.103`
- WebSocket: `ws://10.1.34.103:8768`
- AI Server: `10.1.10.20`
- HAProxy: `10.1.50.100:2222`

**No configuration needed!**

---

## Next Steps

### Desktop Shortcut

**macOS**:
```bash
# Add alias to ~/.zshrc
echo 'alias hal="cd ~/Documents/hal/mac_deployment_package && source venv/bin/activate && python3 hal_text_client.py"' >> ~/.zshrc
source ~/.zshrc

# Then just: hal
```

**Windows** - Create `HAL.bat`:
```batch
@echo off
cd /d %USERPROFILE%\Documents\hal_client
call venv\Scripts\activate.bat
python hal_text_client.py
pause
```

### Auto-start

**macOS** - Create LaunchAgent:
```bash
# See REMOTE_CLIENT_DEPLOYMENT.md section "Auto-start on Login"
```

**Windows** - Scheduled Task:
```powershell
# See WINDOWS_CLIENT_DEPLOYMENT.md section "Auto-start on Login"
```

---

## Full Documentation

- **Complete Guide**: `REMOTE_CLIENT_DEPLOYMENT.md`
- **Windows Guide**: `WINDOWS_CLIENT_DEPLOYMENT.md`
- **Network Info**: `../mac_deployment_package/NETWORK_INFO.md`
- **Voice Architecture**: `../FEATURES/VOICE/VOICE_INTERFACE_ARCHITECTURE.md`

---

## Architecture

```
┌─────────────────────┐
│  Your Computer      │  ← Text or Voice Client
│  (macOS or Windows) │     (hal_text_client.py)
└──────────┬──────────┘
           │ WebSocket (ws://10.1.34.103:8768)
           ↓
┌─────────────────────────────────┐
│ QM Server (10.1.34.103)         │
│                                 │
│  ┌──────────────────────────┐  │
│  │ WebSocket Listener        │  │  ← Phantom Process
│  │ Port 8768                 │  │     WEBSOCKET.LISTENER
│  └──────────┬───────────────┘  │
│             ↓                   │
│  ┌──────────────────────────┐  │
│  │ HAL Database (OpenQM)     │  │
│  │ - Medical records          │  │
│  │ - Financial data           │  │
│  │ - Appointments             │  │
│  └────────────────────────────┘  │
└─────────────────────────────────┘
```

---

## Support Checklist

Before asking for help:

- [ ] Python installed and in PATH
- [ ] Dependencies installed (`pip list`)
- [ ] Virtual environment activated
- [ ] Network connectivity (`ping 10.1.34.103`)
- [ ] QM listener running (netstat shows port 8768)
- [ ] Test connection script passed

---

## Files Needed

**Minimum** (text client):
- `hal_text_client.py`
- `requirements.txt` (just websockets)

**Full** (voice client):
- `hal_text_client.py`
- `hal_voice_client.py`
- `requirements.txt` (all dependencies)
- `network_config.sh` (macOS) or `network_config.ps1` (Windows)
- `setup_mac.sh` (macOS only)
- `test_connection.sh` (macOS) or `test_connection.py` (Windows)

All in: `C:\qmsys\hal\mac_deployment_package\`

---

**Ready? Pick your platform above and get started!** ⬆️

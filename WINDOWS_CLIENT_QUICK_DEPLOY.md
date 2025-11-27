# Windows Client Quick Deployment

**Deploy HAL text/voice client on Windows 10/11 in 10 minutes**

---

## 🚀 Quick Setup

### Prerequisites

1. **Install Python 3.11+**
   - Download: https://www.python.org/downloads/
   - ⚠️ **CHECK**: "Add Python to PATH" during installation
   - Run installer, click "Install Now"

2. **Verify Installation**
   ```powershell
   python --version
   pip --version
   ```

---

## 📦 Step 1: Get the Client Files

### Option A: Clone from GitHub (Recommended)

```powershell
cd $env:USERPROFILE\Documents
git clone https://github.com/lcsmd/HAL.git
cd HAL\mac_deployment_package
```

### Option B: Copy from QM Server

```powershell
# Map network drive
net use Z: \\10.1.34.103\qmsys /user:lawr apgar-66

# Create directory
cd $env:USERPROFILE\Documents
mkdir hal_client
cd hal_client

# Copy files
Copy-Item Z:\hal\mac_deployment_package\hal_text_client.py .
Copy-Item Z:\hal\mac_deployment_package\hal_voice_client.py .
Copy-Item Z:\hal\mac_deployment_package\requirements.txt .
```

---

## 🔧 Step 2: Setup Python Environment

```powershell
# Create virtual environment
python -m venv venv

# Activate it
.\venv\Scripts\Activate.ps1

# If you get execution policy error:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Then try activating again
.\venv\Scripts\Activate.ps1

# Install dependencies (text client)
pip install websockets
```

---

## ✅ Step 3: Test Connection

Create `test_connection.py`:

```python
import asyncio
import websockets

async def test():
    uri = "ws://10.1.34.103:8768"
    print(f"Testing {uri}...")
    try:
        async with websockets.connect(uri) as ws:
            await ws.send('{"command":"ping"}')
            response = await asyncio.wait_for(ws.recv(), timeout=5)
            print(f"✓ Connected! Response: {response[:100]}")
    except Exception as e:
        print(f"✗ Failed: {e}")

asyncio.run(test())
```

Run it:
```powershell
python test_connection.py
```

---

## 🎯 Step 4: Run Text Client

```powershell
# Make sure venv is activated
.\venv\Scripts\Activate.ps1

# Run client
python hal_text_client.py
```

**Usage**:
```
You: What medications am I taking?
HAL: [Lists medications...]

You: Show my appointments
HAL: [Shows appointments...]

You: quit
```

---

## 🎤 Step 5: Voice Client (Optional)

### Install Audio Dependencies

```powershell
# Install audio library
pip install pipwin
pipwin install pyaudio

# Install voice dependencies
pip install pvporcupine numpy simpleaudio
```

### Run Voice Client

```powershell
python hal_voice_client.py
```

**Usage**:
1. Say "Hey Hal"
2. Hear beep
3. Speak your query
4. Listen to response

---

## 🖥️ Step 6: Create Desktop Shortcuts

### Text Client Shortcut

Create `HAL_Text_Client.bat`:

```batch
@echo off
title HAL Text Client
cd /d %USERPROFILE%\Documents\HAL\mac_deployment_package
call venv\Scripts\activate.bat
python hal_text_client.py
pause
```

**Create shortcut**:
1. Right-click `HAL_Text_Client.bat`
2. Send to → Desktop (create shortcut)
3. Rename shortcut to "HAL Text Client"

### Voice Client Shortcut

Create `HAL_Voice_Client.bat`:

```batch
@echo off
title HAL Voice Client
cd /d %USERPROFILE%\Documents\HAL\mac_deployment_package
call venv\Scripts\activate.bat
python hal_voice_client.py
pause
```

---

## 🌐 Network Configuration

If you need to change server IP, create `network_config.ps1`:

```powershell
$env:QM_SERVER = "10.1.34.103"
$env:WEBSOCKET_URL = "ws://10.1.34.103:8768"

Write-Host "Network configured for: $env:QM_SERVER"
```

Load before running client:
```powershell
. .\network_config.ps1
python hal_text_client.py
```

---

## 🔥 Quick One-Liner Setup

```powershell
cd $env:USERPROFILE\Documents; git clone https://github.com/lcsmd/HAL.git; cd HAL\mac_deployment_package; python -m venv venv; .\venv\Scripts\Activate.ps1; pip install websockets; python hal_text_client.py
```

---

## 🐛 Troubleshooting

### "Python not found"

**Fix**: Reinstall Python with "Add to PATH" checked

Or add to PATH manually:
```powershell
$env:Path += ";C:\Users\YourName\AppData\Local\Programs\Python\Python311"
```

### "Cannot run scripts"

**Fix**:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### "Connection refused"

**Check**:
1. QM server is on (10.1.34.103)
2. WebSocket listener is running (port 8768)
3. Windows firewall allows connection

**Test**:
```powershell
Test-NetConnection -ComputerName 10.1.34.103 -Port 8768
```

### PyAudio installation fails

**Fix**:
```powershell
pip install pipwin
pipwin install pyaudio
```

---

## 📋 Complete File List Needed

**Minimum** (text client):
- `hal_text_client.py`
- `requirements.txt` (or just install websockets)

**Full** (voice client):
- `hal_text_client.py`
- `hal_voice_client.py`
- `requirements.txt`

---

## ✅ Verification Checklist

- [ ] Python 3.11+ installed with PATH
- [ ] Virtual environment created
- [ ] Dependencies installed (websockets minimum)
- [ ] Connection test passed
- [ ] Client runs and connects to HAL
- [ ] Desktop shortcuts created (optional)

---

## 🎯 Quick Commands Reference

```powershell
# Setup
cd $env:USERPROFILE\Documents\HAL\mac_deployment_package
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install websockets

# Run text client
python hal_text_client.py

# Run voice client (after audio deps installed)
python hal_voice_client.py

# Test connection
python test_connection.py

# Deactivate venv
deactivate
```

---

## 📚 Full Documentation

For complete details, see:
- `DOCS/DEPLOYMENT/WINDOWS_CLIENT_DEPLOYMENT.md` - Complete guide
- `DOCS/DEPLOYMENT/REMOTE_CLIENT_DEPLOYMENT.md` - Mac + Windows guide
- `DOCS/DEPLOYMENT/CLIENT_QUICKSTART.md` - 5-minute quick start

---

## 🔐 Network Requirements

**Server Access**:
- QM Server: `10.1.34.103:8768` (WebSocket)
- HAProxy: `10.1.50.100:2222` (SSH tunnel if needed)

**If remote** (not on same network), use SSH tunnel:
```powershell
# Install PuTTY first
# Configure tunnel: Local port 8768 → 10.1.34.103:8768
# Then connect to localhost:8768 instead
```

---

## 🎉 You're Done!

Once setup is complete:

1. **Double-click** desktop shortcut, or
2. **Run** `python hal_text_client.py`, or
3. **Voice mode**: `python hal_voice_client.py`

---

**Estimated Setup Time**: 10 minutes  
**Status**: Production Ready  
**Tested On**: Windows 10 21H2, Windows 11 23H2

---

**Need help?** See full documentation in `DOCS/DEPLOYMENT/` directory or visit https://github.com/lcsmd/HAL

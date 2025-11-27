# HAL Windows Client Deployment Guide

**Complete instructions for deploying HAL voice and text clients on Windows 10/11**

---

## 📋 Overview

Deploy HAL text or voice client on a Windows computer to interact with your HAL assistant running on the QM server.

**Client Options**:
- **Text Client**: Command-line interface (no audio)
- **Voice Client**: Full voice with wake word detection

---

## 🚀 Quick Start

### Prerequisites

1. **Install Python 3.11+**:
   - Download: https://www.python.org/downloads/
   - ⚠️ **CRITICAL**: Check "Add Python to PATH" during installation
   - Click "Install Now"

2. **Verify Installation**:
   ```powershell
   python --version
   # Should show Python 3.11.x or higher
   ```

---

### 5-Minute Setup

```powershell
# 1. Create client directory
cd $env:USERPROFILE\Documents
mkdir hal_client
cd hal_client

# 2. Copy files from QM server
# Copy these files from C:\qmsys\hal\mac_deployment_package\:
#   - hal_text_client.py
#   - hal_voice_client.py (for voice)
#   - requirements.txt
#   - network_config.sh (convert to .ps1)

# 3. Create virtual environment
python -m venv venv

# 4. Activate virtual environment
.\venv\Scripts\Activate.ps1

# 5. Install dependencies
pip install websockets

# For voice client, also install:
pip install pipwin
pipwin install pyaudio
pip install pvporcupine numpy simpleaudio

# 6. Test connection
python hal_text_client.py --query "Hello HAL"
```

---

## 📝 Step-by-Step Guide

### Step 1: Install Python

1. Download Python 3.11+ from https://www.python.org/downloads/
2. Run installer
3. **CHECK THE BOX**: "Add Python to PATH" ✅
4. Click "Install Now"
5. Click "Disable path length limit" when prompted

**Verify**:
```powershell
python --version
pip --version
```

---

### Step 2: Create Client Directory

```powershell
# Navigate to Documents folder
cd $env:USERPROFILE\Documents

# Create hal_client directory
New-Item -ItemType Directory -Path hal_client
cd hal_client
```

---

### Step 3: Get Client Files

**Option A**: Copy from QM server via network share
```powershell
# Map network drive to QM server
net use Z: \\10.1.34.103\qmsys /user:lawr apgar-66

# Copy files
Copy-Item Z:\hal\mac_deployment_package\hal_text_client.py .
Copy-Item Z:\hal\mac_deployment_package\hal_voice_client.py .
Copy-Item Z:\hal\mac_deployment_package\requirements.txt .
```

**Option B**: Copy from GitHub
```powershell
# If Git is installed
git clone https://github.com/lcsmd/hal.git
cd hal\mac_deployment_package
```

**Option C**: Manual copy
- Use Remote Desktop to QM server
- Copy files from `C:\qmsys\hal\mac_deployment_package\`
- Paste to your local `Documents\hal_client\`

---

### Step 4: Setup Python Environment

```powershell
# Create virtual environment
python -m venv venv

# Activate virtual environment
.\venv\Scripts\Activate.ps1
```

**If you get "execution policy" error**:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
# Then try activating again
.\venv\Scripts\Activate.ps1
```

**Verify activation** (you should see `(venv)` in prompt):
```
(venv) PS C:\Users\YourName\Documents\hal_client>
```

---

### Step 5: Install Dependencies

**For Text Client Only**:
```powershell
pip install websockets
```

**For Voice Client** (includes text):
```powershell
# Install websockets
pip install websockets

# Install PyAudio (audio library)
pip install pipwin
pipwin install pyaudio

# Install voice dependencies
pip install pvporcupine numpy simpleaudio

# Or install everything from requirements.txt
pip install -r requirements.txt
```

---

### Step 6: Create Configuration File

Create `network_config.ps1`:
```powershell
@"
# HAL Network Configuration
`$env:QM_SERVER = "10.1.34.103"
`$env:QM_WEBSOCKET_PORT = "8768"
`$env:HAPROXY_SERVER = "10.1.50.100"
`$env:HAPROXY_SSH_PORT = "2222"
`$env:AI_SERVER = "10.1.10.20"
`$env:WEBSOCKET_URL = "ws://10.1.34.103:8768"

Write-Host "✓ Network configuration loaded" -ForegroundColor Green
Write-Host "  QM Server: `$env:QM_SERVER"
Write-Host "  WebSocket: `$env:WEBSOCKET_URL"
"@ | Out-File -FilePath network_config.ps1 -Encoding UTF8
```

**Load configuration**:
```powershell
. .\network_config.ps1
```

---

### Step 7: Test Connection

Create `test_connection.py`:
```python
import asyncio
import websockets

async def test():
    uri = "ws://10.1.34.103:8768"
    print(f"Testing connection to {uri}...")
    try:
        async with websockets.connect(uri, ping_interval=None) as ws:
            print("✓ Connected!")
            await ws.send('{"command":"ping"}')
            response = await asyncio.wait_for(ws.recv(), timeout=5.0)
            print(f"✓ Response: {response[:100]}")
            return True
    except Exception as e:
        print(f"✗ Failed: {e}")
        return False

if __name__ == "__main__":
    asyncio.run(test())
```

**Run test**:
```powershell
python test_connection.py
```

**Expected**:
```
Testing connection to ws://10.1.34.103:8768...
✓ Connected!
✓ Response: {"status":"ok"}
```

---

### Step 8: Run Text Client

```powershell
# Make sure virtual environment is active
.\venv\Scripts\Activate.ps1

# Run text client (interactive mode)
python hal_text_client.py

# Or single query
python hal_text_client.py --query "What appointments do I have?"
```

**Usage**:
```
HAL Text Client
===============
Connected to HAL at ws://10.1.34.103:8768

You: What medications am I taking?
HAL: [Lists your medications...]

You: Show my appointments
HAL: [Shows appointments...]

You: quit
Goodbye!
```

---

### Step 9: Run Voice Client (Optional)

**Only if you installed voice dependencies**:

```powershell
# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Run voice client
python hal_voice_client.py
```

**Usage**:
1. Wait for "Listening for wake word..."
2. Say "Hey Hal"
3. Hear activation beep
4. Speak your query
5. Hear HAL's response
6. Returns to wake word detection

**Controls**:
- **Space Bar**: Manual trigger (skip wake word)
- **Q**: Quit
- **Ctrl+C**: Force stop

---

## 🖥️ Create Desktop Shortcuts

### Text Client Shortcut

Create `HAL_Text_Client.bat`:
```batch
@echo off
title HAL Text Client
cd /d %USERPROFILE%\Documents\hal_client
call venv\Scripts\activate.bat
python hal_text_client.py --interactive
pause
```

**Create shortcut**:
1. Right-click on desktop → New → Shortcut
2. Location: `%USERPROFILE%\Documents\hal_client\HAL_Text_Client.bat`
3. Name: "HAL Text Client"
4. Right-click shortcut → Properties
5. Change icon (optional): `C:\Windows\System32\imageres.dll` (pick one)

---

### Voice Client Shortcut

Create `HAL_Voice_Client.bat`:
```batch
@echo off
title HAL Voice Client
cd /d %USERPROFILE%\Documents\hal_client
call venv\Scripts\activate.bat
python hal_voice_client.py
pause
```

Create shortcut same as text client above.

---

## 🔧 Troubleshooting

### Issue: "Python not found"

**Problem**: Python not in PATH

**Fix**:
```powershell
# Check if Python is installed
Get-Command python

# If not found, reinstall Python with "Add to PATH" checked
# Or manually add to PATH:
$env:Path += ";C:\Users\YourName\AppData\Local\Programs\Python\Python311"
$env:Path += ";C:\Users\YourName\AppData\Local\Programs\Python\Python311\Scripts"

# Verify
python --version
```

---

### Issue: "pip not found"

**Fix**:
```powershell
# Use Python module syntax
python -m pip install websockets
```

---

### Issue: "Cannot run scripts" (execution policy)

**Fix**:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

---

### Issue: PyAudio installation fails

**Fix**:
```powershell
# Method 1: Use pipwin
pip install pipwin
pipwin install pyaudio

# Method 2: Download precompiled wheel
# Visit: https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio
# Download matching your Python version (e.g., cp311 = Python 3.11)
# Example: PyAudio-0.2.11-cp311-cp311-win_amd64.whl
pip install PyAudio-0.2.11-cp311-cp311-win_amd64.whl
```

---

### Issue: "Connection refused"

**Causes**:
- QM server not reachable
- WebSocket listener not running
- Firewall blocking

**Fix**:
```powershell
# Test network connectivity
Test-NetConnection -ComputerName 10.1.34.103 -Port 8768

# Check if port is open
telnet 10.1.34.103 8768

# If firewall blocking, allow Python:
# Settings → Windows Security → Firewall & network protection
# → Allow an app through firewall → Add Python
```

**On QM Server** (10.1.34.103):
```powershell
# Check if listener is running
netstat -an | findstr 8768
# Should show: TCP    0.0.0.0:8768    0.0.0.0:0    LISTENING

# If not running, start phantom process:
# In QM terminal:
LOGTO HAL
PHANTOM EXECUTE "WEBSOCKET.LISTENER"
```

---

### Issue: Microphone not working

**Fix**:
```
1. Settings → Privacy → Microphone
2. Enable "Allow apps to access your microphone"
3. Scroll down and enable for "Python"
```

**Test microphone**:
```powershell
python -c "import pyaudio; p = pyaudio.PyAudio(); print(f'Audio devices: {p.get_device_count()}')"
```

---

### Issue: Wake word not detected

**Fix**:
```powershell
# List audio devices
python -c "import pyaudio; p = pyaudio.PyAudio(); [print(f'{i}: {p.get_device_info_by_index(i)[\"name\"]} (channels: {p.get_device_info_by_index(i)[\"maxInputChannels\"]})') for i in range(p.get_device_count())]"

# Edit hal_voice_client.py to specify your microphone:
# Find: stream = p.open(...)
# Change: input_device_index=None
# To: input_device_index=2  (your mic's index)
```

---

## 🎯 Configuration Options

### Change WebSocket URL

**Temporary** (current session):
```powershell
$env:WEBSOCKET_URL = "ws://10.1.34.103:8768"
```

**Permanent** (edit client files):
```python
# In hal_text_client.py or hal_voice_client.py
# Change:
WEBSOCKET_URL = "ws://10.1.34.103:8768"
```

---

### Auto-start on Login

**Create scheduled task**:
```powershell
$action = New-ScheduledTaskAction `
    -Execute "python" `
    -Argument "hal_voice_client.py" `
    -WorkingDirectory "$env:USERPROFILE\Documents\hal_client"

$trigger = New-ScheduledTaskTrigger -AtLogon

$settings = New-ScheduledTaskSettingsSet `
    -AllowStartIfOnBatteries `
    -DontStopIfGoingOnBatteries

Register-ScheduledTask `
    -TaskName "HAL Voice Client" `
    -Action $action `
    -Trigger $trigger `
    -Settings $settings `
    -Description "Auto-start HAL voice client at login"
```

---

## 📊 System Requirements

### Minimum
- **OS**: Windows 10 (1809 or later)
- **Python**: 3.8+
- **RAM**: 2 GB
- **Network**: 10 Mbps LAN
- **Microphone**: Any (for voice)

### Recommended
- **OS**: Windows 11
- **Python**: 3.11+
- **RAM**: 4 GB
- **Network**: 100 Mbps LAN
- **Microphone**: USB headset or quality built-in mic

---

## 🔐 Security Notes

1. **Unencrypted**: WebSocket traffic is not encrypted (ws://)
2. **No Authentication**: WebSocket doesn't require credentials
3. **LAN Only**: Design assumes trusted local network
4. **For Remote Access**: Use SSH tunnel (see Advanced section)

---

## 🚀 Advanced: SSH Tunnel

**For secure remote access from outside LAN**:

### Using PuTTY

1. Download PuTTY: https://www.putty.org/
2. Configure session:
   - Host: `10.1.50.100`
   - Port: `2222`
3. Configure tunnel:
   - Connection → SSH → Tunnels
   - Source port: `8768`
   - Destination: `10.1.34.103:8768`
   - Click "Add"
4. Save session as "HAL Tunnel"
5. Connect (username: `lawr`, password: `apgar-66`)

**Then edit client to use**:
```python
WEBSOCKET_URL = "ws://localhost:8768"
```

---

## 📞 Support

**Connection Issues**:
```powershell
# Test connection
python test_connection.py

# Check server
Test-NetConnection -ComputerName 10.1.34.103 -Port 8768
```

**Python Issues**:
```powershell
# Verify installation
python --version
pip --version

# Reinstall dependencies
pip install --force-reinstall websockets
```

**Voice Issues**:
```powershell
# Test microphone
python -c "import pyaudio; p = pyaudio.PyAudio(); print(p.get_default_input_device_info())"

# Check Windows microphone settings
start ms-settings:privacy-microphone
```

---

## 📚 Related Documentation

- **macOS Deployment**: `REMOTE_CLIENT_DEPLOYMENT.md`
- **Network Architecture**: `C:\qmsys\hal\DOCS\DEPLOYMENT\MAC_DEPLOYMENT_READY.md`
- **Voice System**: `C:\qmsys\hal\DOCS\FEATURES\VOICE\VOICE_INTERFACE_ARCHITECTURE.md`

---

**Last Updated**: 2025-11-27  
**Status**: PRODUCTION READY  
**Tested On**: Windows 10 21H2, Windows 11 23H2

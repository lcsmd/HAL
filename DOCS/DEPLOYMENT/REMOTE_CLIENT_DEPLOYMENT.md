# HAL Remote Client Deployment Guide

**Complete instructions for deploying HAL voice and text clients on macOS and Windows**

---

## 📋 Overview

This guide covers deploying HAL clients on remote computers (macOS or Windows) to interact with your HAL Personal AI Assistant running on the QM server.

**Two Client Options**:
1. **Text Client** - Simple command-line interface (no audio dependencies)
2. **Voice Client** - Full voice interface with wake word detection ("Hey Hal")

**Supported Platforms**:
- macOS (Intel and Apple Silicon)
- Windows 10/11

---

## 🎯 Prerequisites

### Network Requirements

**You need access to**:
- **QM Server**: `10.1.34.103` (Windows Server running OpenQM)
- **HAProxy**: `10.1.50.100:2222` (SSH tunnel access)
- **AI Server** (optional for voice): `10.1.10.20` (GPU-accelerated STT/TTS)

### Server-Side Requirements

**On QM Server** (`10.1.34.103`):
- OpenQM phantom process listening on port `8768`
- Process: `VOICE.LISTENER.NEW` running as phantom
- To verify: `LOGTO HAL` → `LIST.READU`

**On HAProxy Server** (`10.1.50.100`):
- SSH access enabled on port `2222`
- Port forwarding configured: `8768` → QM Server
- SSH credentials: username `lawr`, password `apgar-66`

---

## 📦 Quick Start - Choose Your Platform

### macOS Quick Start

```bash
# 1. Download deployment package
cd ~/Downloads
# (Get mac_deployment_package from QM server or GitHub)

# 2. Run automated setup
cd mac_deployment_package
chmod +x setup_mac.sh
./setup_mac.sh

# 3. Test connection
./test_connection.sh

# 4. Choose your client:

# Text client (simple)
python3 hal_text_client.py

# Voice client (with wake word)
python3 hal_voice_client.py
```

### Windows Quick Start

```powershell
# 1. Download deployment package
cd $env:USERPROFILE\Downloads
# (Get deployment package from QM server or GitHub)

# 2. Install Python (if not installed)
# Download from: https://www.python.org/downloads/
# IMPORTANT: Check "Add Python to PATH" during installation

# 3. Install dependencies
cd deployment_package
pip install -r requirements.txt

# 4. Test connection
python test_connection.py

# 5. Choose your client:

# Text client (simple)
python hal_text_client.py

# Voice client (with wake word)
python hal_voice_client.py
```

---

## 🍎 macOS Detailed Deployment

### Step 1: Prerequisites

**Check Python Version**:
```bash
python3 --version
# Should be Python 3.8 or higher
```

**If Python not installed**:
```bash
# Install Homebrew (if not installed)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Python
brew install python3
```

**Check Audio (for voice client)**:
```bash
# Install PortAudio (required for voice)
brew install portaudio
```

---

### Step 2: Get Deployment Package

**Option A - From GitHub**:
```bash
cd ~/Documents
git clone https://github.com/lcsmd/hal.git
cd hal/mac_deployment_package
```

**Option B - Direct Download**:
```bash
# Download from QM server via SSH
cd ~/Documents
scp -P 2222 lawr@10.1.50.100:/path/to/mac_deployment_package.zip .
unzip mac_deployment_package.zip
cd mac_deployment_package
```

---

### Step 3: Automated Setup

```bash
# Make setup script executable
chmod +x setup_mac.sh

# Run setup (installs all dependencies)
./setup_mac.sh

# This script will:
# - Create Python virtual environment
# - Install required packages (websockets, pyaudio, etc.)
# - Generate audio files (beep sounds)
# - Set up SSH keys
# - Create desktop shortcuts
```

**Manual Setup** (if automated fails):
```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install websockets pyaudio pvporcupine numpy simpleaudio

# Generate audio files
python3 generate_sounds.py

# Test SSH connection
ssh -p 2222 lawr@10.1.50.100 "echo Connection successful"
```

---

### Step 4: Configure Network

**Edit `network_config.sh`** (if IPs change):
```bash
nano network_config.sh
```

Current configuration:
```bash
export QM_SERVER="10.1.34.103"
export QM_WEBSOCKET_PORT="8768"
export HAPROXY_SERVER="10.1.50.100"
export HAPROXY_SSH_PORT="2222"
export AI_SERVER="10.1.10.20"
export WEBSOCKET_URL="ws://10.1.34.103:8768"
```

---

### Step 5: Test Connection

```bash
# Test SSH tunnel
./test_connection.sh

# Expected output:
# ✓ HAProxy SSH accessible
# ✓ QM WebSocket listener responding
# ✓ AI services accessible (if voice enabled)
```

**Manual test**:
```bash
# Test WebSocket connection
python3 << EOF
import asyncio
import websockets

async def test():
    uri = "ws://10.1.34.103:8768"
    async with websockets.connect(uri) as websocket:
        await websocket.send('{"command":"test"}')
        response = await websocket.recv()
        print(f"Response: {response}")

asyncio.run(test())
EOF
```

---

### Step 6: Run Text Client

**Simple text interface** (no audio required):

```bash
# Activate virtual environment
source venv/bin/activate

# Run text client
python3 hal_text_client.py

# Or use interactive mode
python3 hal_text_client.py --interactive

# Or single query
python3 hal_text_client.py --query "What appointments do I have today?"
```

**Usage**:
```
HAL Text Client
===============
Connected to HAL at ws://10.1.34.103:8768

Commands:
  Type your message and press Enter
  'quit' or 'exit' to close
  Ctrl+C to interrupt

You: What's the weather?
HAL: [Response from server]

You: List my medications
HAL: [Response from server]

You: quit
Goodbye!
```

---

### Step 7: Run Voice Client

**Full voice interface with wake word**:

```bash
# Activate virtual environment
source venv/bin/activate

# Run voice client
python3 hal_voice_client.py
```

**Usage Flow**:
```
1. Client starts listening for wake word
   → Say "Hey Hal" (or configured wake word)
   
2. Activation sound plays (beep)
   → Indicates HAL is listening

3. Speak your query
   → "What appointments do I have today?"
   → Voice Activity Detection captures your speech
   
4. Audio sent to server for processing
   → Server performs STT (Speech-to-Text)
   → HAL processes query
   → Server performs TTS (Text-to-Speech)
   
5. Response audio plays
   → HAL speaks the answer
   
6. Returns to wake word detection
   → Say "Hey Hal" again for next query
```

**Voice Client Controls**:
```
Space Bar: Manual trigger (skip wake word)
Q: Quit
Ctrl+C: Force stop
```

---

### Step 8: Troubleshooting (macOS)

**Issue: "Module websockets not found"**
```bash
# Ensure virtual environment is activated
source venv/bin/activate
pip install websockets
```

**Issue: "PyAudio not found" or audio errors**
```bash
# Reinstall PortAudio
brew reinstall portaudio

# Reinstall PyAudio
pip uninstall pyaudio
pip install pyaudio
```

**Issue: "Permission denied" on microphone**
```bash
# Grant microphone access:
# System Preferences → Security & Privacy → Privacy → Microphone
# Check the box for Terminal (or your terminal app)
```

**Issue: "Connection refused to 10.1.34.103:8768"**
```bash
# Check if listener is running on QM server
# On QM server:
LOGTO HAL
LIST.READU
# Should show VOICE.LISTENER.NEW process

# Check network connectivity
ping 10.1.34.103
telnet 10.1.34.103 8768
```

**Issue: Wake word not detected**
```bash
# Test microphone
python3 << EOF
import pyaudio
p = pyaudio.PyAudio()
print("Audio devices:")
for i in range(p.get_device_count()):
    info = p.get_device_info_by_index(i)
    print(f"{i}: {info['name']} (channels: {info['maxInputChannels']})")
EOF

# If wrong device, edit hal_voice_client.py:
# Change input_device_index parameter
```

---

## 🪟 Windows Detailed Deployment

### Step 1: Prerequisites

**Install Python**:
1. Download Python 3.11+ from: https://www.python.org/downloads/
2. Run installer
3. **CRITICAL**: Check "Add Python to PATH"
4. Click "Install Now"

**Verify Installation**:
```powershell
python --version
# Should show Python 3.11.x or higher

pip --version
# Should show pip version
```

**Install Git** (optional, for GitHub clone):
1. Download from: https://git-scm.com/download/win
2. Run installer with default settings

---

### Step 2: Get Deployment Package

**Option A - From GitHub**:
```powershell
cd $env:USERPROFILE\Documents
git clone https://github.com/lcsmd/hal.git
cd hal\mac_deployment_package
```

**Option B - Direct Download**:
```powershell
# Download ZIP from GitHub or server
# Extract to: C:\Users\YourName\Documents\hal_client
cd $env:USERPROFILE\Documents\hal_client
```

**Option C - Copy from QM Server**:
```powershell
# Use WinSCP or similar to copy files from:
# QM Server: C:\qmsys\hal\mac_deployment_package\
# To Local: C:\Users\YourName\Documents\hal_client\
```

---

### Step 3: Setup Python Environment

```powershell
# Navigate to deployment directory
cd $env:USERPROFILE\Documents\hal_client

# Create virtual environment
python -m venv venv

# Activate virtual environment
.\venv\Scripts\Activate.ps1

# If you get execution policy error:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Upgrade pip
python -m pip install --upgrade pip

# Install dependencies
pip install websockets
pip install pyaudio
pip install pvporcupine
pip install numpy
pip install simpleaudio

# Or install from requirements.txt
pip install -r requirements.txt
```

---

### Step 4: Install Audio Dependencies (for Voice Client)

**For Voice Client Only**:

1. **Download PyAudio wheel** (precompiled):
   ```powershell
   # For Python 3.11, 64-bit Windows:
   pip install pipwin
   pipwin install pyaudio
   
   # Alternative: Download from:
   # https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio
   # Then: pip install PyAudio-0.2.11-cp311-cp311-win_amd64.whl
   ```

2. **Test audio**:
   ```powershell
   python -c "import pyaudio; print('PyAudio OK')"
   ```

**Skip audio for Text Client** - no audio dependencies needed!

---

### Step 5: Configure Network

**Edit `network_config.sh`** (create Windows version):

Create `network_config.ps1`:
```powershell
# Network Configuration for HAL Client
$env:QM_SERVER = "10.1.34.103"
$env:QM_WEBSOCKET_PORT = "8768"
$env:HAPROXY_SERVER = "10.1.50.100"
$env:HAPROXY_SSH_PORT = "2222"
$env:AI_SERVER = "10.1.10.20"
$env:WEBSOCKET_URL = "ws://10.1.34.103:8768"

Write-Host "Network configuration loaded:"
Write-Host "  QM Server: $env:QM_SERVER"
Write-Host "  WebSocket: $env:WEBSOCKET_URL"
Write-Host "  HAProxy: $env:HAPROXY_SERVER:$env:HAPROXY_SSH_PORT"
```

**Load configuration**:
```powershell
. .\network_config.ps1
```

---

### Step 6: Test Connection

**Create `test_connection.py`**:
```python
import asyncio
import websockets
import sys

async def test_connection():
    uri = "ws://10.1.34.103:8768"
    print(f"Testing connection to {uri}...")
    
    try:
        async with websockets.connect(uri, ping_interval=None) as websocket:
            print("✓ Connected successfully!")
            
            # Send test message
            test_msg = '{"command":"ping"}'
            await websocket.send(test_msg)
            print("✓ Message sent")
            
            # Wait for response (with timeout)
            try:
                response = await asyncio.wait_for(websocket.recv(), timeout=5.0)
                print(f"✓ Response received: {response[:100]}")
                return True
            except asyncio.TimeoutError:
                print("⚠ Timeout waiting for response (listener may not be running)")
                return False
                
    except Exception as e:
        print(f"✗ Connection failed: {e}")
        return False

if __name__ == "__main__":
    result = asyncio.run(test_connection())
    sys.exit(0 if result else 1)
```

**Run test**:
```powershell
python test_connection.py
```

**Expected output**:
```
Testing connection to ws://10.1.34.103:8768...
✓ Connected successfully!
✓ Message sent
✓ Response received: {"status":"ok"}
```

---

### Step 7: Run Text Client (Windows)

```powershell
# Activate virtual environment (if not already active)
.\venv\Scripts\Activate.ps1

# Run text client
python hal_text_client.py

# Interactive mode
python hal_text_client.py --interactive

# Single query mode
python hal_text_client.py --query "Show my appointments"
```

**Create Desktop Shortcut** (optional):

Create `HAL_Text_Client.bat`:
```batch
@echo off
cd /d %USERPROFILE%\Documents\hal_client
call venv\Scripts\activate.bat
python hal_text_client.py --interactive
pause
```

Right-click → "Send to Desktop (create shortcut)"

---

### Step 8: Run Voice Client (Windows)

```powershell
# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Run voice client
python hal_voice_client.py
```

**Create Desktop Shortcut**:

Create `HAL_Voice_Client.bat`:
```batch
@echo off
cd /d %USERPROFILE%\Documents\hal_client
call venv\Scripts\activate.bat
python hal_voice_client.py
pause
```

---

### Step 9: Troubleshooting (Windows)

**Issue: "Python not found"**
```powershell
# Reinstall Python with "Add to PATH" checked
# Or manually add to PATH:
$env:Path += ";C:\Users\YourName\AppData\Local\Programs\Python\Python311;C:\Users\YourName\AppData\Local\Programs\Python\Python311\Scripts"
```

**Issue: "pip not found"**
```powershell
# Use full path
python -m pip install websockets
```

**Issue: "Cannot run scripts" (execution policy)**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

**Issue: PyAudio installation fails**
```powershell
# Use pipwin
pip install pipwin
pipwin install pyaudio

# Or download wheel from:
# https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio
# Match your Python version (cp311 = Python 3.11)
pip install PyAudio-0.2.11-cp311-cp311-win_amd64.whl
```

**Issue: Microphone access denied**
```
Settings → Privacy → Microphone
Enable microphone access for Python
```

**Issue: "Connection refused"**
```powershell
# Test network connectivity
Test-NetConnection -ComputerName 10.1.34.103 -Port 8768

# Check Windows Firewall
# Settings → Windows Security → Firewall & network protection
# Allow Python through firewall
```

**Issue: Wake word not working**
```powershell
# List audio devices
python -c "import pyaudio; p = pyaudio.PyAudio(); [print(f'{i}: {p.get_device_info_by_index(i)[\"name\"]}') for i in range(p.get_device_count())]"

# Edit hal_voice_client.py to specify device
# Change: input_device_index=None
# To: input_device_index=2  (your microphone index)
```

---

## 🔧 Advanced Configuration

### Custom Wake Word

**Available wake words** (Porcupine):
- "hey hal" (default)
- "jarvis"
- "computer"
- "alexa"
- "ok google"

**Change wake word**:

Edit `hal_voice_client.py`:
```python
# Find this line:
porcupine = pvporcupine.create(
    access_key="YOUR_KEY",
    keywords=["hey hal"]  # Change to: ["jarvis"], etc.
)
```

### SSH Tunnel (for secure remote access)

**macOS**:
```bash
# Create SSH tunnel through HAProxy
ssh -p 2222 -L 8768:10.1.34.103:8768 lawr@10.1.50.100 -N

# In another terminal, connect via localhost
# Edit client to use: ws://localhost:8768
```

**Windows**:
```powershell
# Using PuTTY:
# 1. Session: 10.1.50.100, Port 2222
# 2. Connection → SSH → Tunnels:
#    Source port: 8768
#    Destination: 10.1.34.103:8768
#    Click "Add"
# 3. Connect (username: lawr, password: apgar-66)

# Edit client to use: ws://localhost:8768
```

### Auto-start on Login

**macOS**:
```bash
# Create LaunchAgent
mkdir -p ~/Library/LaunchAgents

cat > ~/Library/LaunchAgents/com.hal.voice.plist << 'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.hal.voice</string>
    <key>ProgramArguments</key>
    <array>
        <string>/Users/YourName/Documents/mac_deployment_package/venv/bin/python3</string>
        <string>/Users/YourName/Documents/mac_deployment_package/hal_voice_client.py</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
</dict>
</plist>
EOF

# Load agent
launchctl load ~/Library/LaunchAgents/com.hal.voice.plist
```

**Windows**:
```powershell
# Create scheduled task
$action = New-ScheduledTaskAction -Execute "python" -Argument "hal_voice_client.py" -WorkingDirectory "$env:USERPROFILE\Documents\hal_client"
$trigger = New-ScheduledTaskTrigger -AtLogon
Register-ScheduledTask -TaskName "HAL Voice Client" -Action $action -Trigger $trigger
```

---

## 📊 Comparison: Text vs Voice Client

| Feature | Text Client | Voice Client |
|---------|-------------|--------------|
| Dependencies | websockets only | websockets, pyaudio, pvporcupine |
| Setup Time | 2 minutes | 10-15 minutes |
| Audio Required | No | Yes (microphone + speakers) |
| Wake Word | No | Yes ("Hey Hal") |
| STT/TTS | No | Yes (requires AI server) |
| Resource Usage | Minimal | Moderate (CPU for wake word detection) |
| Best For | Quick queries, debugging | Hands-free interaction, natural UX |
| Works Offline | No (needs QM server) | No (needs QM + AI server) |

---

## 🌐 Network Architecture

```
[Remote Client]
  ├── macOS/Windows computer
  ├── Python 3.8+
  ├── hal_text_client.py OR hal_voice_client.py
  │
  ↓ WebSocket (ws://10.1.34.103:8768)
  │
[QM Server] 10.1.34.103
  ├── OpenQM database
  ├── VOICE.LISTENER.NEW phantom process
  ├── Port 8768 listener
  │
  ↓ API calls (when voice enabled)
  │
[AI Server] 10.1.10.20 (ubuai)
  ├── Faster-Whisper STT (port 9000)
  ├── Ollama LLM (port 11434)
  └── TTS service (optional)
```

---

## 📱 Mobile Clients (Future)

**iOS**:
- Not yet implemented
- Future: SwiftUI app with native voice

**Android**:
- Not yet implemented  
- Future: Kotlin app with native voice

---

## 🔐 Security Considerations

1. **Network**: All communication currently unencrypted WebSocket
   - **Recommendation**: Use SSH tunnel for remote access outside LAN
   
2. **Authentication**: No authentication on WebSocket currently
   - **Recommendation**: Add token-based auth in future
   
3. **Firewall**: QM port 8768 should not be exposed to internet
   - **Current**: Only accessible on 10.1.x.x LAN
   - **For remote**: Use SSH tunnel through HAProxy

4. **Credentials**: Stored in plaintext in scripts
   - **Recommendation**: Use environment variables or keychain

---

## 📞 Support

**Server Issues**:
- Check VOICE.LISTENER.NEW is running: `LOGTO HAL; LIST.READU`
- Restart listener: `LOGTO HAL; EXECUTE "START.VOICE.LISTENER"`

**Client Issues**:
- Test connection: `python test_connection.py`
- Check logs in terminal output
- Verify Python version: `python --version` (need 3.8+)

**Network Issues**:
- Ping QM server: `ping 10.1.34.103`
- Test WebSocket port: `telnet 10.1.34.103 8768`
- Check firewall rules

**Voice Issues**:
- Test microphone: See troubleshooting sections above
- Check AI server: `curl http://10.1.10.20:9000/health`
- Verify audio devices in system settings

---

## 📚 Related Documentation

- **Mac Deployment Package**: `C:\qmsys\hal\mac_deployment_package\README.md`
- **Network Configuration**: `C:\qmsys\hal\DOCS\DEPLOYMENT\MAC_DEPLOYMENT_READY.md`
- **Voice System Architecture**: `C:\qmsys\hal\DOCS\FEATURES\VOICE\VOICE_INTERFACE_ARCHITECTURE.md`
- **AI Services**: `C:\qmsys\hal\mac_deployment_package\AI_SERVICES.md`
- **Phantom Process Info**: `C:\qmsys\hal\mac_deployment_package\PHANTOM_PROCESS_INFO.md`

---

**Last Updated**: 2025-11-27  
**Status**: PRODUCTION READY  
**Tested On**: macOS 14.x (Sonoma), Windows 11  
**Repository**: https://github.com/lcsmd/hal

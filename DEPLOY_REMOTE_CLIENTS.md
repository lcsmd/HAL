# Deploy HAL Remote Clients - Quick Reference

**Complete deployment instructions for macOS and Windows text/voice clients**

---

## 📚 Documentation Available

### 1. **Quick Start** (Start Here!)
**File**: `DOCS/DEPLOYMENT/CLIENT_QUICKSTART.md`

- 5-minute setup for both platforms
- Choose macOS or Windows section
- Minimal steps to get running
- **Best for**: Quick deployment

### 2. **Complete macOS & Windows Guide**
**File**: `DOCS/DEPLOYMENT/REMOTE_CLIENT_DEPLOYMENT.md`

- Comprehensive guide for both platforms
- Detailed troubleshooting
- Advanced configuration
- Security notes
- SSH tunnels
- **Best for**: Full understanding

### 3. **Windows-Specific Guide**
**File**: `DOCS/DEPLOYMENT/WINDOWS_CLIENT_DEPLOYMENT.md`

- Windows 10/11 specific instructions
- PowerShell commands
- Desktop shortcuts
- Auto-start configuration
- **Best for**: Windows-only deployments

---

## 🚀 Quick Deploy Summary

### macOS (5 minutes)

```bash
# 1. Get files
cd ~/Documents
git clone https://github.com/lcsmd/hal.git
cd hal/mac_deployment_package

# 2. Setup
chmod +x setup_mac.sh test_connection.sh
./setup_mac.sh
source network_config.sh

# 3. Test
./test_connection.sh

# 4. Run
source venv/bin/activate
python3 hal_text_client.py  # Text mode
python3 hal_voice_client.py # Voice mode (optional)
```

---

### Windows (10 minutes)

```powershell
# 1. Install Python (if needed)
# Download from python.org
# CHECK: "Add Python to PATH" during installation

# 2. Setup
cd $env:USERPROFILE\Documents
mkdir hal_client
cd hal_client
# Copy files: hal_text_client.py, hal_voice_client.py, requirements.txt

# 3. Create environment
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install websockets

# 4. Run
python hal_text_client.py  # Text mode
```

---

## 📦 Files Needed

**All files in**: `C:\qmsys\hal\mac_deployment_package\`

### Text Client Only (minimal)
- `hal_text_client.py` (8KB)
- `requirements.txt` (just websockets)

### Voice Client (full)
- `hal_text_client.py` (8KB)
- `hal_voice_client.py` (19KB)
- `requirements.txt` (all audio dependencies)
- `network_config.sh` (1.5KB)
- `setup_mac.sh` (2.6KB) - macOS only
- `test_connection.sh` (3.2KB) - macOS only

---

## 🎯 Client Types

### Text Client
- **Dependencies**: websockets only
- **Setup Time**: 2-5 minutes
- **Use Case**: Quick queries, debugging
- **Interface**: Command-line typing
- **Best For**: Simple, reliable access

### Voice Client
- **Dependencies**: websockets, pyaudio, pvporcupine, numpy, simpleaudio
- **Setup Time**: 10-15 minutes
- **Use Case**: Hands-free interaction
- **Interface**: Wake word ("Hey Hal") + speech
- **Best For**: Natural conversation

---

## 🌐 Network Requirements

**Pre-configured for**:
- **QM Server**: `10.1.34.103` (Windows/OpenQM)
- **WebSocket**: `ws://10.1.34.103:8768`
- **AI Server**: `10.1.10.20` (GPU for voice STT/TTS)
- **HAProxy**: `10.1.50.100:2222` (SSH tunnel)

**Client must have**:
- Network access to 10.1.34.103 (QM server)
- Open port 8768 (WebSocket)
- For voice: Access to 10.1.10.20 (AI server)

---

## ✅ Deployment Checklist

### Pre-deployment
- [ ] Python 3.8+ installed on client
- [ ] Client can reach QM server (ping 10.1.34.103)
- [ ] QM WebSocket listener running (check port 8768)
- [ ] Files copied to client machine

### macOS Deployment
- [ ] Ran setup_mac.sh successfully
- [ ] Virtual environment created
- [ ] Dependencies installed
- [ ] Network config loaded
- [ ] Test connection passed
- [ ] Client runs and connects

### Windows Deployment
- [ ] Python installed with PATH
- [ ] Virtual environment created
- [ ] Dependencies installed (websockets minimum)
- [ ] Test connection successful
- [ ] Client runs and connects

---

## 🔧 Common Issues

### "Connection refused"
**Check**: QM listener running
```powershell
# On QM server
netstat -an | findstr 8768
# Should show LISTENING
```

### "Module not found"
**Fix**: Install dependencies
```bash
# macOS
source venv/bin/activate
pip install -r requirements.txt

# Windows
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### "Python not found" (Windows)
**Fix**: Reinstall Python with "Add to PATH" checked

### Voice not working
**Check**:
- Microphone permissions (macOS: System Preferences, Windows: Settings)
- PyAudio installed correctly
- AI server accessible (10.1.10.20)

---

## 📖 Example Queries

### Medical
```
What medications am I taking?
Show my appointments
List my allergies
What were my last vital signs?
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

## 🏗️ Architecture

```
┌─────────────────────────┐
│  Remote Client          │
│  (macOS or Windows)     │
│                         │
│  hal_text_client.py OR  │
│  hal_voice_client.py    │
└────────────┬────────────┘
             │
             │ WebSocket
             │ ws://10.1.34.103:8768
             ↓
┌─────────────────────────────────────┐
│ QM Server (10.1.34.103)             │
│                                     │
│ ┌─────────────────────────────┐    │
│ │ WebSocket Listener           │    │
│ │ (Phantom Process)            │    │
│ │ Port 8768                    │    │
│ └──────────┬──────────────────┘    │
│            ↓                        │
│ ┌─────────────────────────────┐    │
│ │ HAL Database (OpenQM)        │    │
│ │ - Medical records             │    │
│ │ - Financial transactions      │    │
│ │ - Appointments                │    │
│ └─────────────────────────────┘    │
└─────────────────────────────────────┘
             │
             │ (Voice only)
             ↓
┌─────────────────────────────────────┐
│ AI Server (10.1.10.20)              │
│ - Faster-Whisper STT (port 9000)    │
│ - Ollama LLM (port 11434)           │
│ - TTS (optional)                    │
└─────────────────────────────────────┘
```

---

## 📁 File Locations

### On QM Server
- **Source Files**: `C:\qmsys\hal\mac_deployment_package\`
- **Documentation**: `C:\qmsys\hal\DOCS\DEPLOYMENT\`

### On Client (macOS)
- **Install Location**: `~/Documents/hal/mac_deployment_package/`
- **Virtual Env**: `~/Documents/hal/mac_deployment_package/venv/`

### On Client (Windows)
- **Install Location**: `C:\Users\YourName\Documents\hal_client\`
- **Virtual Env**: `C:\Users\YourName\Documents\hal_client\venv\`

---

## 🔐 Security Notes

- **No Encryption**: WebSocket traffic unencrypted (ws://, not wss://)
- **No Authentication**: WebSocket doesn't require login
- **LAN Only**: Designed for trusted local network (10.1.x.x)
- **For Remote**: Use SSH tunnel through HAProxy (10.1.50.100:2222)

---

## 📞 Support Resources

### Documentation
1. **Quick Start**: `DOCS/DEPLOYMENT/CLIENT_QUICKSTART.md`
2. **Full Guide**: `DOCS/DEPLOYMENT/REMOTE_CLIENT_DEPLOYMENT.md`
3. **Windows Guide**: `DOCS/DEPLOYMENT/WINDOWS_CLIENT_DEPLOYMENT.md`
4. **Network Info**: `mac_deployment_package/NETWORK_INFO.md`
5. **Voice Architecture**: `DOCS/FEATURES/VOICE/VOICE_INTERFACE_ARCHITECTURE.md`

### Troubleshooting Steps
1. Check Python installation and version
2. Verify network connectivity (ping QM server)
3. Test WebSocket port (telnet 10.1.34.103 8768)
4. Confirm QM listener running (netstat on server)
5. Check firewall rules (both client and server)
6. Review client logs (terminal output)

### Common Commands

**Check QM Listener** (on QM server):
```powershell
netstat -an | findstr 8768
```

**Start QM Listener** (if not running):
```qm
LOGTO HAL
PHANTOM EXECUTE "WEBSOCKET.LISTENER"
```

**Test from Client**:
```bash
# macOS
./test_connection.sh

# Windows
python test_connection.py
```

---

## 🎯 Deployment Scenarios

### Scenario 1: Single macOS Client
**Time**: 5 minutes  
**Steps**: Quick Start → macOS section  
**Files**: Basic package (8 files)

### Scenario 2: Multiple Windows Clients
**Time**: 10 minutes per client  
**Steps**: Windows Guide + batch scripts  
**Files**: Basic package + PowerShell scripts

### Scenario 3: Mixed Environment (macOS + Windows)
**Time**: 15 minutes total  
**Steps**: Deploy to each platform separately  
**Files**: Full package for both

### Scenario 4: Voice Client with Wake Word
**Time**: 15-20 minutes  
**Steps**: Full Guide → Voice section  
**Files**: Complete package with audio deps

---

## 🚀 Quick Deploy Commands

### Copy Deployment Package

**Via Network** (from any client):
```bash
# macOS
scp -r user@10.1.34.103:/qmsys/hal/mac_deployment_package ~/Documents/

# Windows (use WinSCP or similar)
```

**Via GitHub**:
```bash
git clone https://github.com/lcsmd/hal.git
cd hal/mac_deployment_package
```

---

## 📊 Comparison Matrix

| Feature | Text Client | Voice Client |
|---------|-------------|--------------|
| Setup Time | 5 min | 15 min |
| Dependencies | 1 (websockets) | 5 (audio libs) |
| Audio Required | No | Yes |
| Wake Word | No | Yes |
| Use Case | Quick queries | Hands-free |
| Resource Usage | Minimal | Moderate |
| Best For | Developers | End users |

---

## ✨ Next Steps After Deployment

1. **Test queries**: Try medical, financial, general queries
2. **Create shortcuts**: Add desktop shortcuts or aliases
3. **Configure auto-start**: Set up auto-launch (optional)
4. **Train users**: Show example queries
5. **Monitor usage**: Check QM logs for issues
6. **Document customizations**: Note any client-specific changes

---

## 📅 Maintenance

### Regular Tasks
- [ ] Update Python dependencies monthly
- [ ] Check QM listener status weekly
- [ ] Review client logs for errors
- [ ] Test connectivity periodically

### Updates
- [ ] Pull latest from GitHub when available
- [ ] Re-run setup if dependencies change
- [ ] Update network config if IPs change

---

**Ready to deploy?**

1. **Start with**: `DOCS/DEPLOYMENT/CLIENT_QUICKSTART.md`
2. **For details**: `DOCS/DEPLOYMENT/REMOTE_CLIENT_DEPLOYMENT.md`
3. **Windows-specific**: `DOCS/DEPLOYMENT/WINDOWS_CLIENT_DEPLOYMENT.md`

All files in: `C:\qmsys\hal\DOCS\DEPLOYMENT\`

---

**Last Updated**: 2025-11-27  
**Status**: PRODUCTION READY  
**Repository**: https://github.com/lcsmd/hal

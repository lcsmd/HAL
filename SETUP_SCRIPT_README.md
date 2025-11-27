# Windows Client Setup Script

**Automated one-click setup for HAL Windows client**

---

## 🚀 Usage

### Basic Setup (Text Client Only)

```powershell
.\setup_windows_client.ps1
```

This will:
1. Check Python installation
2. Clone repository from GitHub
3. Create virtual environment
4. Install dependencies (websockets)
5. Test connection to HAL server
6. Create desktop shortcuts
7. Optionally run the client

**Time**: 3-5 minutes

---

### Full Setup (Text + Voice Client)

```powershell
.\setup_windows_client.ps1 -IncludeVoice
```

This includes everything above PLUS:
- PyAudio installation
- Voice dependencies (pvporcupine, numpy, simpleaudio)
- Voice client desktop shortcut

**Time**: 5-10 minutes

---

### Custom Installation Path

```powershell
.\setup_windows_client.ps1 -InstallPath "D:\MyApps\HAL"
```

Default: `C:\Users\YourName\Documents\HAL`

---

## 📋 What the Script Does

### Step 1: Check Python
- Verifies Python 3.8+ is installed
- If missing, opens download page

### Step 2: Fix Execution Policy
- Checks PowerShell execution policy
- Sets to RemoteSigned if needed

### Step 3: Check Git
- Verifies Git is installed
- If missing, opens download page

### Step 4: Get Files
- Clones from https://github.com/lcsmd/HAL
- Or updates existing installation

### Step 5: Virtual Environment
- Creates Python virtual environment
- Isolates dependencies

### Step 6: Install Dependencies
- Installs websockets (always)
- Installs voice dependencies (if -IncludeVoice)

### Step 7: Test Connection
- Tests connection to QM server (10.1.34.103:8768)
- Reports success or provides troubleshooting

### Step 8: Desktop Shortcuts
- Creates clickable shortcuts
- `HAL Text Client.lnk`
- `HAL Voice Client.lnk` (if voice enabled)

### Step 9: Summary
- Shows installation directory
- Displays usage instructions
- Offers to run client immediately

---

## 🎯 Prerequisites

The script will check and help you install:

1. **Python 3.11+**
   - https://www.python.org/downloads/
   - ⚠️ Check "Add Python to PATH"

2. **Git** (for cloning)
   - https://git-scm.com/download/win
   - Or manually copy files from server

---

## ✅ After Setup

### Desktop Shortcuts Created

**HAL Text Client**:
- Double-click to start
- Type queries, get responses
- Type `quit` to exit

**HAL Voice Client** (if -IncludeVoice):
- Double-click to start
- Say "Hey Hal"
- Speak your query
- Hear response

---

## 🔧 Manual Alternative

If script fails, run commands manually:

```powershell
# 1. Clone repository
cd $env:USERPROFILE\Documents
git clone https://github.com/lcsmd/HAL.git
cd HAL\mac_deployment_package

# 2. Create venv
python -m venv venv
.\venv\Scripts\Activate.ps1

# 3. Install deps
pip install websockets

# 4. Run client
python hal_text_client.py
```

---

## 🐛 Troubleshooting

### "Cannot run script"

**Error**: `execution policy`

**Fix**:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Then run script again.

---

### "Python not found"

**Cause**: Python not installed or not in PATH

**Fix**:
1. Install Python: https://www.python.org/downloads/
2. ⚠️ Check "Add Python to PATH" during install
3. Restart PowerShell
4. Run script again

---

### "Git not found"

**Cause**: Git not installed

**Options**:
1. Install Git: https://git-scm.com/download/win
2. Or copy files manually from QM server

---

### "Connection failed"

**Causes**:
- QM server offline
- WebSocket listener not running
- Firewall blocking
- Not on same network

**Check**:
```powershell
Test-NetConnection -ComputerName 10.1.34.103 -Port 8768
```

**On QM Server**:
```powershell
netstat -an | findstr 8768
# Should show LISTENING
```

---

### PyAudio installation fails (voice client)

**Fix**: Script uses `pipwin` which usually works

**Manual fix**:
```powershell
pip install pipwin
pipwin install pyaudio
```

Or download wheel from:
https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio

---

## 📊 Script Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `-IncludeVoice` | Switch | False | Install voice client dependencies |
| `-InstallPath` | String | Documents\HAL | Where to install client |

---

## 🎯 Examples

### Basic text client
```powershell
.\setup_windows_client.ps1
```

### Full installation with voice
```powershell
.\setup_windows_client.ps1 -IncludeVoice
```

### Custom location
```powershell
.\setup_windows_client.ps1 -InstallPath "C:\HAL"
```

### Custom location + voice
```powershell
.\setup_windows_client.ps1 -IncludeVoice -InstallPath "D:\Apps\HAL"
```

---

## 📁 What Gets Installed

```
Documents\HAL\
├── mac_deployment_package\
│   ├── venv\                    # Virtual environment
│   ├── hal_text_client.py       # Text client
│   ├── hal_voice_client.py      # Voice client
│   ├── requirements.txt         # Dependencies
│   ├── network_config.sh        # Network config
│   ├── HAL_Text_Client.bat      # Launch script
│   └── HAL_Voice_Client.bat     # Launch script (if voice)
├── BP\                          # OpenQM programs
├── PY\                          # Python scripts
├── DOCS\                        # Documentation
└── README.md

Desktop\
├── HAL Text Client.lnk          # Shortcut
└── HAL Voice Client.lnk         # Shortcut (if voice)
```

---

## ⏱️ Timing

- **Text client only**: 3-5 minutes
- **With voice**: 5-10 minutes
- **Update existing**: 1-2 minutes

---

## 🔐 Security Notes

- Virtual environment isolates dependencies
- No admin privileges required
- Connects to 10.1.34.103:8768 (local network)
- No secrets stored in client

---

## 📚 Related Documentation

- **Quick Guide**: `WINDOWS_CLIENT_QUICK_DEPLOY.md`
- **Complete Guide**: `DOCS/DEPLOYMENT/WINDOWS_CLIENT_DEPLOYMENT.md`
- **Both Platforms**: `DOCS/DEPLOYMENT/REMOTE_CLIENT_DEPLOYMENT.md`
- **Troubleshooting**: `DOCS/DEPLOYMENT/CLIENT_QUICKSTART.md`

---

## ✅ Success Indicators

Script succeeded if you see:

✓ Python found  
✓ Execution policy OK  
✓ Git found  
✓ Repository cloned  
✓ Virtual environment created  
✓ All dependencies installed  
✓ Connection successful  
✓ Desktop shortcuts created  

---

## 🎉 You're Done!

After script completes:

1. **Double-click** `HAL Text Client` on desktop
2. **Type** your query
3. **Get** HAL's response

Or for voice:
1. **Double-click** `HAL Voice Client`
2. **Say** "Hey Hal"
3. **Speak** your query
4. **Listen** to response

---

**Last Updated**: 2025-11-27  
**Status**: Production Ready  
**Tested On**: Windows 10 21H2, Windows 11 23H2

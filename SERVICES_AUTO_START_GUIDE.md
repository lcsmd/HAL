# HAL Services Auto-Start Configuration Guide

This guide covers setting up automatic startup for all HAL services on both Windows and Ubuntu servers.

## Overview

### Windows Server (10.1.34.103)
1. **AI.SERVER** (port 8745) - QM BASIC phantom for core AI logic
2. **Voice Gateway** (port 8768) - Python WebSocket server for client connections

### Ubuntu Server (ubuai - 10.1.10.20)
1. **Faster-Whisper** (port 9000) - GPU-accelerated speech-to-text
2. **Ollama** (port 11434) - LLM inference service

---

## Part 1: Windows Auto-Start Configuration

### AI.SERVER: Use MASTER.LOGIN (Recommended)

**This is the proper QM-native method for auto-starting phantoms.**

#### Step 1: Create Q-Pointer (if not exists)

```qm
LOGTO QMSYS
CREATE.FILE VOC HAL.BP Q
* Type: Q
* Path: HAL,BP
```

#### Step 2: Add to MASTER.LOGIN

```qm
LOGTO QMSYS
ED VOC MASTER.LOGIN

* Add line:
PHANTOM HAL.BP AI.SERVER

* Save:
FI
```

#### Step 3: Verify After QMSvc Restart

```powershell
# Restart QMSvc
Restart-Service QMSvc
Start-Sleep -Seconds 5

# Check phantom started
"LISTU" | Out-File "COM.DIR\INPUT.COMMANDS.txt" -Encoding ASCII
C:\QMSYS\BIN\qm.exe -aHAL "RUN BP COMMAND.EXECUTOR"
Get-Content "COM.DIR\OUTPUT.txt"

# Check port
netstat -ano | findstr :8745
```

**Benefits:**
- ✅ Native QM functionality
- ✅ No wrapper scripts
- ✅ Proper QM environment
- ✅ Automatic with QMSvc

### Voice Gateway: Windows Service

**Prerequisites**:
- Windows Server with Administrator access
- PowerShell 5.1 or later
- OpenQM installed and running (QMSvc service)
- Python 3.13 installed at `C:\Python313\python.exe`

### Step 1: Install Voice Gateway Service

Open PowerShell **as Administrator**:

```powershell
cd C:\qmsys\hal
.\install_services.ps1
```

This will:
- Create HAL-AIServer service
- Create HAL-VoiceGateway service
- Configure automatic restart on failure
- Set dependencies (VoiceGateway depends on AIServer)

### Step 2: Enable Auto-Start

```powershell
# Services are already set to Automatic startup
# Verify:
Get-Service HAL-* | Select-Object Name, StartType
```

### Step 3: Start Services

```powershell
.\start_services.ps1
```

Or manually:
```powershell
Start-Service HAL-AIServer
Start-Service HAL-VoiceGateway
```

### Step 4: Verify

```powershell
# Check service status
Get-Service HAL-*

# Check ports are listening
netstat -ano | findstr "8745 8768"

# View logs
Get-Content C:\qmsys\hal\LOGS\ai_server_service.log -Tail 20
Get-Content C:\qmsys\hal\LOGS\voice_gateway_service.log -Tail 20
```

### Windows Service Management

**Stop Services:**
```powershell
.\stop_services.ps1
# Or:
Stop-Service HAL-VoiceGateway
Stop-Service HAL-AIServer
```

**Restart Services:**
```powershell
Restart-Service HAL-AIServer
Restart-Service HAL-VoiceGateway
```

**Uninstall Services:**
```powershell
.\uninstall_services.ps1
```

---

## Part 2: Ubuntu Services Installation

### Prerequisites
- Ubuntu server with root/sudo access
- NVIDIA GPU with CUDA installed (for GPU acceleration)
- Network access to download packages and models

### Step 1: Copy Files to Ubuntu

From Windows PowerShell:

```powershell
cd C:\qmsys\hal\ubuai_services

# Option 1: Using SCP
scp -r * root@10.1.10.20:/root/hal_services/

# Option 2: Using WinSCP or FileZilla (GUI)
# Connect to: 10.1.10.20
# Copy folder: C:\qmsys\hal\ubuai_services
# To: /root/hal_services/
```

### Step 2: SSH to Ubuntu and Run Installer

```bash
ssh root@10.1.10.20

cd /root/hal_services
chmod +x install_services.sh
sudo bash install_services.sh
```

The installer will:
1. Update system packages
2. Install Python, ffmpeg, dependencies
3. Set up Faster-Whisper with virtual environment
4. Download Whisper large-v3 model (~3GB)
5. Install Ollama
6. Pull Ollama models
7. Create systemd services
8. Configure firewall (ufw)
9. Prompt to enable auto-start
10. Prompt to start services now

### Step 3: Verify Ubuntu Services

```bash
# Check service status
sudo systemctl status faster-whisper
sudo systemctl status ollama

# Check ports
netstat -tlnp | grep -E ':9000|:11434'

# View logs
sudo journalctl -u faster-whisper -n 20
sudo journalctl -u ollama -n 20
```

### Step 4: Test from Windows

```powershell
cd C:\qmsys\hal

# Test Faster-Whisper
curl http://10.1.10.20:9000/health

# Test Ollama
curl http://10.1.10.20:11434/

# Test with Python
python -c "import requests; print(requests.get('http://10.1.10.20:9000/').json())"
```

### Ubuntu Service Management

**Enable Auto-Start:**
```bash
sudo systemctl enable faster-whisper
sudo systemctl enable ollama
```

**Disable Auto-Start:**
```bash
sudo systemctl disable faster-whisper
sudo systemctl disable ollama
```

**Start Services:**
```bash
sudo systemctl start faster-whisper
sudo systemctl start ollama
```

**Stop Services:**
```bash
sudo systemctl stop faster-whisper
sudo systemctl stop ollama
```

**Restart Services:**
```bash
sudo systemctl restart faster-whisper
sudo systemctl restart ollama
```

**View Logs:**
```bash
# Follow logs in real-time
sudo journalctl -u faster-whisper -f
sudo journalctl -u ollama -f

# View recent logs
sudo journalctl -u faster-whisper -n 50
sudo journalctl -u ollama -n 50
```

---

## Part 3: End-to-End Testing

After all services are installed and running:

### Test Full Voice Pipeline

From Windows:

```powershell
cd C:\qmsys\hal

# Test Voice Gateway connection
python test_voice_gateway.py

# Test AI.SERVER directly
python test_ai_server_direct.py

# Run full system test
python test_all_connections.ps1
```

### Expected Results

**Windows Services:**
- ✅ HAL-AIServer running on port 8745
- ✅ HAL-VoiceGateway running on port 8768

**Ubuntu Services:**
- ✅ faster-whisper running on port 9000
- ✅ ollama running on port 11434

**Network Connectivity:**
- ✅ Windows → Ubuntu port 9000 (Whisper)
- ✅ Windows → Ubuntu port 11434 (Ollama)
- ✅ Clients → Windows port 8768 (Voice Gateway)

---

## Troubleshooting

### Windows: Service Won't Start

**Check logs:**
```powershell
Get-Content C:\qmsys\hal\LOGS\ai_server_service.log
Get-Content C:\qmsys\hal\LOGS\voice_gateway_service.log
```

**Common Issues:**

1. **Python not found**
   - Verify: `Test-Path C:\Python313\python.exe`
   - Fix: Update path in `service_voice_gateway.ps1`

2. **QM not running**
   - Check: `Get-Service QMSvc`
   - Fix: `Start-Service QMSvc`

3. **Port already in use**
   - Check: `netstat -ano | findstr "8745"`
   - Fix: Kill existing process or change port

### Ubuntu: Service Won't Start

**Check logs:**
```bash
sudo journalctl -u faster-whisper -n 100
sudo journalctl -u ollama -n 100
```

**Common Issues:**

1. **CUDA not found**
   - Check: `nvidia-smi`
   - Fix: Install CUDA toolkit

2. **Model not downloaded**
   - Check: `ls /opt/faster-whisper/models`
   - Fix: Re-run installer or manually download

3. **Port already in use**
   - Check: `netstat -tlnp | grep 9000`
   - Fix: Kill existing process

### Network Connectivity Issues

**Test from Windows:**
```powershell
Test-NetConnection 10.1.10.20 -Port 9000
Test-NetConnection 10.1.10.20 -Port 11434
```

**Test from Ubuntu:**
```bash
curl http://localhost:9000/health
curl http://localhost:11434/
```

---

## Service Dependencies

### Windows
```
QMSvc (OpenQM) 
    ↓
HAL-AIServer (port 8745)
    ↓
HAL-VoiceGateway (port 8768)
```

### Ubuntu
```
faster-whisper (port 9000)  [Independent]
ollama (port 11434)         [Independent]
```

---

## Auto-Start Verification

### After Windows Reboot

```powershell
# Check services started automatically
Get-Service HAL-* | Format-Table Name, Status, StartType

# Should show:
# Name               Status  StartType
# ----               ------  ---------
# HAL-AIServer       Running Automatic
# HAL-VoiceGateway   Running Automatic
```

### After Ubuntu Reboot

```bash
# Check services started automatically
systemctl status faster-whisper
systemctl status ollama

# Should show "active (running)" and "enabled"
```

---

## Files Created

### Windows
- `service_ai_server.ps1` - AI.SERVER service wrapper
- `service_voice_gateway.ps1` - Voice Gateway service wrapper
- `install_services.ps1` - Service installer
- `start_services.ps1` - Start all services
- `stop_services.ps1` - Stop all services
- `uninstall_services.ps1` - Uninstall services
- `LOGS/ai_server_service.log` - AI.SERVER logs
- `LOGS/voice_gateway_service.log` - Voice Gateway logs

### Ubuntu
- `/etc/systemd/system/faster-whisper.service` - Whisper service
- `/etc/systemd/system/ollama.service` - Ollama service
- `/opt/faster-whisper/whisper_server.py` - Whisper HTTP server
- `/opt/faster-whisper/venv/` - Python virtual environment
- `/opt/faster-whisper/models/` - Whisper models

---

## Summary

✅ **Windows Services**: Configured as Windows Services with automatic startup  
✅ **Ubuntu Services**: Configured as systemd services with automatic startup  
✅ **Restart on Failure**: Both platforms configured to auto-restart services  
✅ **Logs**: Centralized logging for troubleshooting  
✅ **Management Scripts**: Easy start/stop/restart commands  

**Next Steps:**
1. Install Windows services: `.\install_services.ps1`
2. Install Ubuntu services: `bash install_services.sh`
3. Test end-to-end: `python test_voice_gateway.py`
4. Reboot both servers to verify auto-start

---

**Created**: 2025-12-03  
**Status**: Ready for deployment

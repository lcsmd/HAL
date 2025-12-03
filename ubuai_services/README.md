# Ubuntu AI Services (ubuai) Auto-Start Setup

This directory contains scripts and service files to configure automatic startup for the AI services on the Ubuntu server (ubuai - 10.1.10.20).

## Services

1. **Faster-Whisper** (Port 9000) - Speech-to-Text using GPU
2. **Ollama** (Port 11434) - LLM inference

## Installation

### Step 1: Copy Files to Ubuntu Server

From Windows, copy the files to ubuai:

```powershell
# Using SCP (from Windows PowerShell)
cd C:\qmsys\hal\ubuai_services
scp -r * root@10.1.10.20:/root/hal_services/

# Or using WinSCP, FileZilla, etc.
```

### Step 2: Run Installation Script

SSH to ubuai and run the installer:

```bash
ssh root@10.1.10.20
cd /root/hal_services
chmod +x install_services.sh
sudo bash install_services.sh
```

The installer will:
1. Update system packages
2. Install Python, ffmpeg, and dependencies
3. Set up Faster-Whisper with GPU support
4. Download Whisper model (large-v3)
5. Install Ollama
6. Pull Ollama models
7. Install systemd services
8. Configure firewall
9. Optionally enable auto-start at boot
10. Optionally start services immediately

### Step 3: Enable Auto-Start

If you didn't enable during installation:

```bash
sudo systemctl enable faster-whisper
sudo systemctl enable ollama
```

### Step 4: Start Services

```bash
sudo systemctl start faster-whisper
sudo systemctl start ollama
```

## Service Management

### Check Status

```bash
sudo systemctl status faster-whisper
sudo systemctl status ollama
```

### View Logs

```bash
# Follow logs in real-time
sudo journalctl -u faster-whisper -f
sudo journalctl -u ollama -f

# View recent logs
sudo journalctl -u faster-whisper -n 50
sudo journalctl -u ollama -n 50
```

### Restart Services

```bash
sudo systemctl restart faster-whisper
sudo systemctl restart ollama
```

### Stop Services

```bash
sudo systemctl stop faster-whisper
sudo systemctl stop ollama
```

### Disable Auto-Start

```bash
sudo systemctl disable faster-whisper
sudo systemctl disable ollama
```

## Testing

### Test Faster-Whisper (Port 9000)

From Windows:

```powershell
# Health check
curl http://10.1.10.20:9000/health

# From Python
python -c "import requests; print(requests.get('http://10.1.10.20:9000/').json())"
```

### Test Ollama (Port 11434)

```powershell
# Health check
curl http://10.1.10.20:11434/

# Generate text
curl http://10.1.10.20:11434/api/generate -d '{
  "model": "llama3.2",
  "prompt": "Hello, how are you?",
  "stream": false
}'
```

## Troubleshooting

### Faster-Whisper Not Starting

Check logs:
```bash
sudo journalctl -u faster-whisper -n 100
```

Common issues:
- CUDA not found: Check `nvidia-smi` works
- Model not downloaded: Check `/opt/faster-whisper/models`
- Port in use: Check `netstat -tlnp | grep 9000`

### Ollama Not Starting

Check logs:
```bash
sudo journalctl -u ollama -n 100
```

Common issues:
- Ollama not installed: Run `curl -fsSL https://ollama.com/install.sh | sh`
- Models not pulled: Run `ollama pull llama3.2`
- GPU issues: Check `nvidia-smi`

### Services Not Auto-Starting After Reboot

Verify enabled:
```bash
systemctl is-enabled faster-whisper
systemctl is-enabled ollama
```

Should show "enabled". If not:
```bash
sudo systemctl enable faster-whisper
sudo systemctl enable ollama
```

## Service Files

### faster-whisper.service

Located at: `/etc/systemd/system/faster-whisper.service`

- Runs as root
- Uses Python virtual environment at `/opt/faster-whisper/venv`
- Auto-restarts on failure (5 second delay)
- GPU enabled (CUDA_VISIBLE_DEVICES=0)

### ollama.service

Located at: `/etc/systemd/system/ollama.service`

- Runs as root
- Listens on all interfaces (0.0.0.0:11434)
- Auto-restarts on failure (5 second delay)
- GPU enabled

## Ports

| Service | Port | Protocol | Firewall |
|---------|------|----------|----------|
| Faster-Whisper | 9000 | HTTP | ✅ Open |
| Ollama | 11434 | HTTP | ✅ Open |

## Files

- `faster-whisper.service` - Systemd service file for Faster-Whisper
- `ollama.service` - Systemd service file for Ollama
- `whisper_server.py` - Faster-Whisper HTTP server
- `install_services.sh` - Installation script
- `README.md` - This file

## Next Steps

After services are running:

1. Test from Windows: `python C:\qmsys\hal\test_ai_server_direct.py`
2. Test voice gateway: `python C:\qmsys\hal\test_voice_gateway.py`
3. Connect clients from Mac/Windows/Linux

---

**Status**: Ready for deployment to ubuai

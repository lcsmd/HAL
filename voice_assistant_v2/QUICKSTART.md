# Voice Assistant - Quick Start Guide

Get your voice assistant running in 15 minutes!

## Prerequisites

- **AI Server:** Windows Server with OpenQM installed (10.1.34.103)
- **Voice Server:** Ubuntu with NVIDIA GPU (10.1.10.20)
- **Client:** Mac or PC with microphone and speakers

## 5-Minute Setup (Each Component)

### Step 1: AI Server (Windows) - 5 minutes

```powershell
# Open PowerShell as Administrator
cd C:\qmsys\hal\voice_assistant_v2\ai_server
.\setup_windows.ps1 -AutoStart

# Verify running
.\status_ai_server.bat
```

✅ **Success:** Port 8745 should be listening

---

### Step 2: Voice Server (Ubuntu) - 10 minutes

```bash
# SSH to Ubuntu server
ssh lawr@10.1.10.20

# Run setup
cd /path/to/voice_assistant_v2/voice_server
sudo ./setup_ubuntu.sh

# When prompted, press 'y' to start now

# Verify running
sudo systemctl status voice-server
```

✅ **Success:** Service should show "active (running)"

**Note:** First run downloads the Whisper model (~3GB), takes 5-10 minutes

---

### Step 3: Client (Mac) - 5 minutes

```bash
# On your Mac
cd /path/to/voice_assistant_v2/client

# Run setup
./setup_mac.sh

# Edit config file (optional)
nano voice_client.config
# Change client_id and default_user_id if needed

# Start client
source venv/bin/activate
python voice_client.py
```

✅ **Success:** Should see "Listening for wake word: computer"

---

## First Test

### Simple Test (Manual Trigger)

Since real wake word detection needs additional setup, test with file trigger:

```bash
# In another terminal, while client is running:
cd /path/to/voice_assistant_v2/client
touch .wake_trigger

# Watch client terminal - should show:
# "Entering Active Listening Mode (ALM)"
```

Speak: **"What time is it?"**

Wait 3 seconds of silence.

Should hear acknowledgement sound and receive response.

---

## Full Test (With Real Voice)

### Option 1: Add pvporcupine (Recommended)

```bash
cd client/
source venv/bin/activate
pip install pvporcupine

# Get API key from https://console.picovoice.ai/
# Free tier available
```

Edit `voice_client.py` to integrate pvporcupine (see README.md).

### Option 2: Use Keyboard Trigger

Modify `voice_client.py` to add keyboard listener:

```python
# Add at top
import keyboard

# In passive_listening_mode():
if keyboard.is_pressed('space'):
    await self.active_listening_mode('computer')
```

Press spacebar to simulate wake word.

---

## Typical Interaction

```
User: "computer"
Client: *beep*

User: "what time is it?"
[3 seconds silence]

Client: *beep*
[Processing...]

AI: "The current time is 3:30 PM"

[10 seconds to respond]

User: "and what's the date?"
[3 seconds silence]

Client: *beep*
[Processing...]

AI: "Today's date is Wednesday, December 3rd, 2025"

[10 seconds of silence - returns to passive mode]
```

---

## Troubleshooting Quick Fixes

### Client won't start
```bash
# Install PortAudio
brew install portaudio

# Reinstall pyaudio
pip install --force-reinstall pyaudio
```

### Voice server won't start
```bash
# Check logs
journalctl -u voice-server -n 50

# Common issue: CUDA not found
# Edit voice_server.py, change:
WHISPER_DEVICE = "cpu"  # Use CPU instead of GPU

# Restart
sudo systemctl restart voice-server
```

### AI server won't start
```batch
REM Check if port is blocked
netstat -an | findstr 8745

REM If in use, kill the process
taskkill /F /PID <pid>

REM Restart
start_ai_server.bat
```

### Can't connect between components
```bash
# Test connectivity
# From client:
nc -zv 10.1.10.20 8585  # Test voice server

# From voice server:
nc -zv 10.1.34.103 8745  # Test AI server

# Check firewalls
# Ubuntu:
sudo ufw status

# Windows:
Get-NetFirewallRule | Where-Object {$_.DisplayName -like "*Voice*"}
```

---

## Next Steps

1. **Customize Responses:** Edit `ai_server/AI.SERVER` to add your own logic
2. **Add TTS:** Integrate Piper or ElevenLabs in `voice_server.py`
3. **Auto-start:** 
   - Mac: `./setup_launchagent.sh`
   - Ubuntu: `sudo systemctl enable voice-server`
   - Windows: Already enabled if you used `setup_windows.ps1`
4. **Add Features:** See README.md for development guide

---

## Support Commands

### Client
```bash
# Start
python voice_client.py

# Start with custom config
python voice_client.py --config my_config.config

# Debug mode (add to code)
python voice_client.py --debug
```

### Voice Server
```bash
# Start/stop
sudo systemctl start voice-server
sudo systemctl stop voice-server

# View logs
journalctl -u voice-server -f

# Status
sudo systemctl status voice-server
```

### AI Server
```batch
REM Start
start_ai_server.bat

REM Stop
stop_ai_server.bat

REM Status
status_ai_server.bat

REM View logs
view_logs.bat
```

---

## Common Issues & Solutions

| Issue | Solution |
|-------|----------|
| Wake word not working | Use file trigger (`.wake_trigger`) or install pvporcupine |
| No sound output | Check speaker settings, verify TTS is implemented |
| High latency | Check network, use GPU for STT, reduce model size |
| Client crashes | Check pyaudio installation, verify config file |
| Server disconnects | Check websocket timeout settings, verify network |

---

## Performance Tips

1. **Use GPU:** Ensure CUDA is properly installed on voice server
2. **Reduce Model Size:** Use `base` or `small` instead of `large-v3` for faster STT
3. **Local Network:** All components should be on same local network
4. **Wired Connection:** Use ethernet instead of WiFi for client if possible
5. **Resource Monitor:** Keep an eye on CPU/RAM usage

---

## Security Reminder

⚠️ **Current setup is for PRIVATE NETWORKS ONLY**

- No authentication
- No encryption
- Plain WebSocket

For production:
- Add TLS/SSL certificates
- Implement token-based auth
- Use WSS instead of WS
- Add rate limiting
- Enable firewall rules

---

## Success Checklist

- [ ] AI Server running (port 8745 listening)
- [ ] Voice Server running (port 8585 listening)
- [ ] Client connects to voice server
- [ ] Voice server connects to AI server
- [ ] Can trigger recording (manual or wake word)
- [ ] Audio gets transcribed
- [ ] AI server responds
- [ ] Response plays back

If all checked, you're good to go! 🎉

---

## Need Help?

See full documentation in README.md

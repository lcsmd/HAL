# Voice Assistant Deployment Checklist

Use this checklist to ensure proper deployment of all components.

## Pre-Deployment

### Network Requirements
- [ ] All servers accessible on local network
- [ ] AI Server: 10.1.34.103 (or update IP in configs)
- [ ] Voice Server: 10.1.10.20 (or update IP in configs)
- [ ] Ports available:
  - [ ] 8585 (voice server - clients)
  - [ ] 8745 (AI server - voice server)

### Software Requirements

**AI Server (Windows):**
- [ ] Windows Server 2016+ or Windows 10/11
- [ ] OpenQM installed and working
- [ ] HAL account exists
- [ ] Administrator access
- [ ] PowerShell 5.0+

**Voice Server (Ubuntu):**
- [ ] Ubuntu 20.04+ or similar Linux
- [ ] Python 3.8+
- [ ] NVIDIA GPU with CUDA (optional but recommended)
- [ ] 8GB+ RAM
- [ ] 20GB+ free disk space
- [ ] Root/sudo access

**Client (Mac):**
- [ ] macOS 10.14+
- [ ] Python 3.8+
- [ ] Homebrew installed
- [ ] Microphone and speakers
- [ ] Admin access for auto-start setup

---

## AI Server Deployment

### Installation
- [ ] Copy `ai_server/` directory to Windows server
- [ ] Open PowerShell as Administrator
- [ ] Run `.\setup_windows.ps1`
- [ ] Verify no compilation errors
- [ ] Verify files created: VOICE.ASSISTANT.LOG, VOICE.SESSIONS

### Configuration
- [ ] Port 8745 open in Windows Firewall
- [ ] HAL account accessible
- [ ] QM binaries in PATH

### Verification
- [ ] Run `status_ai_server.bat`
- [ ] Verify port 8745 is LISTENING
- [ ] Check `netstat -an | findstr 8745`
- [ ] Review logs with `view_logs.bat`

### Start Service
- [ ] Run `start_ai_server.bat`
- [ ] Verify phantom process running: `tasklist | findstr qm`
- [ ] Test WebSocket connection:
  ```bash
  # From another machine
  wscat -c ws://10.1.34.103:8745
  ```

---

## Voice Server Deployment

### Installation
- [ ] Copy `voice_server/` directory to Ubuntu server
- [ ] Run `sudo ./setup_ubuntu.sh`
- [ ] Wait for Whisper model download (~3GB)
- [ ] Verify no errors during installation

### Configuration
- [ ] Port 8585 open in firewall: `sudo ufw allow 8585/tcp`
- [ ] CUDA installed (if using GPU): `nvidia-smi`
- [ ] Environment variables set
- [ ] systemd service created

### Verification
- [ ] Run `sudo systemctl status voice-server`
- [ ] Should show "active (running)"
- [ ] Check logs: `journalctl -u voice-server -n 50`
- [ ] Verify port: `sudo netstat -tlnp | grep 8585`
- [ ] Test GPU: `nvidia-smi` (should show python process when active)

### Start Service
- [ ] Run `sudo systemctl start voice-server`
- [ ] Enable auto-start: `sudo systemctl enable voice-server`
- [ ] Monitor logs: `journalctl -u voice-server -f`

---

## Client Deployment

### Installation (Per Client)
- [ ] Copy `client/` directory to Mac
- [ ] Run `./setup_mac.sh`
- [ ] Wait for dependencies installation
- [ ] Verify virtual environment created

### Configuration
- [ ] Edit `voice_client.config`:
  - [ ] Set unique `client_id`
  - [ ] Set `default_user_id`
  - [ ] Verify `voice_server_url` (should be ws://10.1.10.20:8585)
  - [ ] Set wake words
- [ ] Verify sound files exist:
  - [ ] `activation_sound.wav`
  - [ ] `acknowledgement_sound.wav`

### Verification
- [ ] Run `source venv/bin/activate`
- [ ] Run `python voice_client.py`
- [ ] Should see "Listening for wake word: computer"
- [ ] Create test trigger: `touch .wake_trigger`
- [ ] Verify mode changes to ALM

### Auto-Start Setup (Optional)
- [ ] Run `./setup_launchagent.sh`
- [ ] Verify LaunchAgent loaded: `launchctl list | grep voice`
- [ ] Reboot and verify auto-start

---

## Integration Testing

### Test 1: AI Server Standalone
```bash
# From any machine with wscat installed
wscat -c ws://10.1.34.103:8745

# Send:
{"type":"session_start","client_id":"test","user_id":"test","wake_word":"test","timestamp":"2025-12-03T10:00:00"}

# Then send:
{"type":"text_input","client_id":"test","user_id":"test","text":"what time is it","timestamp":"2025-12-03T10:00:01"}

# Should receive text_response
```

- [ ] Connection successful
- [ ] Session start acknowledged
- [ ] Text response received

### Test 2: Voice Server Standalone
```bash
# From any machine
wscat -c ws://10.1.10.20:8585

# Send session start (same format as Test 1)

# Send binary audio data
# Or use Python client test script
```

- [ ] Connection successful
- [ ] Session established
- [ ] Audio transcription working

### Test 3: Voice Server to AI Server
```bash
# Check voice server logs
journalctl -u voice-server -f

# Should see:
# "Connected to AI server"
# "Sent to AI server: ..."
```

- [ ] Voice server connects to AI server
- [ ] Messages forwarded correctly
- [ ] Responses received

### Test 4: End-to-End
- [ ] Start client
- [ ] Trigger wake word (or use `.wake_trigger`)
- [ ] Speak command: "what time is it"
- [ ] Wait 3 seconds
- [ ] Verify:
  - [ ] Acknowledgement sound plays
  - [ ] Client shows "Transcribed: ..."
  - [ ] Response received
  - [ ] Audio plays (if TTS implemented)

### Test 5: Follow-Up Conversation
- [ ] Complete Test 4
- [ ] Within 10 seconds, speak again: "and the date"
- [ ] Wait 3 seconds
- [ ] Verify follow-up processed

### Test 6: Interrupt Command
- [ ] Trigger wake word
- [ ] Start speaking
- [ ] Say "belay that" before 3 seconds silence
- [ ] Verify:
  - [ ] Recording cancelled
  - [ ] No transcription sent
  - [ ] Returns to appropriate mode

---

## Performance Validation

### Latency Check
- [ ] Wake word to activation sound: <500ms
- [ ] Silence detection: ~3 seconds
- [ ] STT processing: 1-2 seconds (GPU) or 3-5 seconds (CPU)
- [ ] AI processing: <500ms
- [ ] TTS generation: 0.5-1 second
- [ ] Total end-to-end: <5 seconds

### Resource Usage
**Voice Server:**
- [ ] CPU idle: <20%
- [ ] CPU active: <80%
- [ ] RAM: <6GB
- [ ] GPU: <50% (if applicable)

**AI Server:**
- [ ] CPU: <10%
- [ ] RAM: <500MB (OpenQM process)

**Client:**
- [ ] CPU: <10%
- [ ] RAM: <150MB

### Stress Test
- [ ] Multiple clients (3+) connected simultaneously
- [ ] Rapid fire requests (5+ in quick succession)
- [ ] Long running session (1+ hour)
- [ ] System remains stable

---

## Security Checklist

⚠️ **Current Version: Development/Private Network Only**

- [ ] Confirmed all components on private network
- [ ] External access blocked by firewall
- [ ] No sensitive data in logs
- [ ] No credentials in source code

### Production Checklist (Future)
- [ ] TLS/SSL certificates installed
- [ ] WSS (secure WebSocket) configured
- [ ] Authentication implemented
- [ ] Rate limiting enabled
- [ ] Input validation on all endpoints
- [ ] Audit logging enabled
- [ ] VPN or bastion host for remote access

---

## Backup & Recovery

### Configuration Backup
- [ ] Copy of all `.config` files
- [ ] Copy of sound files
- [ ] AI Server QM BASIC source code
- [ ] Setup scripts saved

### Data Backup
- [ ] OpenQM files backed up:
  - [ ] VOICE.ASSISTANT.LOG
  - [ ] VOICE.SESSIONS
- [ ] Voice server logs archived
- [ ] Client configurations documented

### Recovery Plan
- [ ] Document server IP addresses
- [ ] Document port numbers
- [ ] Document user accounts
- [ ] Tested restoration process

---

## Monitoring Setup

### AI Server
- [ ] Windows Event Viewer monitoring
- [ ] OpenQM logs reviewed daily
- [ ] Disk space monitoring
- [ ] Process health check script

### Voice Server
- [ ] systemd service monitoring
- [ ] journalctl log aggregation
- [ ] GPU monitoring (nvidia-smi)
- [ ] Disk space monitoring
- [ ] Network connectivity checks

### Client
- [ ] LaunchAgent logs reviewed
- [ ] Connection status monitoring
- [ ] Audio device availability check

---

## Documentation

- [ ] Network diagram created/updated
- [ ] IP addresses documented
- [ ] Credentials stored securely (password manager)
- [ ] User guide created for end users
- [ ] Troubleshooting guide accessible
- [ ] Contact information for support

---

## Post-Deployment

### Week 1
- [ ] Monitor logs daily
- [ ] Check for errors/crashes
- [ ] Verify auto-start working
- [ ] Gather user feedback

### Week 2-4
- [ ] Review performance metrics
- [ ] Optimize as needed
- [ ] Update documentation with learnings
- [ ] Plan feature additions

### Ongoing
- [ ] Regular backups (weekly)
- [ ] Security updates (monthly)
- [ ] Performance review (quarterly)
- [ ] User training as needed

---

## Sign-Off

### AI Server
Deployed by: _________________ Date: _______
Verified by: _________________ Date: _______

### Voice Server
Deployed by: _________________ Date: _______
Verified by: _________________ Date: _______

### Client(s)
Number deployed: _______
Deployed by: _________________ Date: _______
Verified by: _________________ Date: _______

### Final Sign-Off
System operational: ☐ Yes ☐ No
Date: _______
Signature: _________________

---

## Notes

Use this section for deployment-specific notes, issues encountered, or customizations made:

```
[Add notes here]
```

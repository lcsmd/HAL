# HAL Mac Deployment Checklist

**Complete this checklist to ensure successful deployment**

---

## ✅ Pre-Deployment (Windows)

- [ ] Windows server is running
- [ ] OpenQM is installed and accessible
- [ ] HAL account exists in QM (`LOGTO HAL` works)
- [ ] Voice Listener compiled: `BASIC BP VOICE.LISTENER` + `CATALOG BP VOICE.LISTENER`
- [ ] Voice Gateway exists: `PY\voice_gateway.py`
- [ ] Python installed on Windows with dependencies
- [ ] Windows IP address known: `ipconfig | findstr IPv4`
- [ ] Windows firewall configured (see below)

### Windows Firewall Rule
```powershell
# Run as Administrator
New-NetFirewallRule -DisplayName "HAL Voice Gateway" -Direction Inbound -LocalPort 8768 -Protocol TCP -Action Allow
```

---

## ✅ Deployment Package (Mac)

- [ ] `mac_deployment_package` folder copied to Mac
- [ ] All files present:
  - [ ] `hal_text_client.py`
  - [ ] `hal_voice_client.py`
  - [ ] `requirements.txt`
  - [ ] `setup_mac.sh`
  - [ ] `test_connection.sh`
  - [ ] `generate_sounds.py`
  - [ ] `README.md`
  - [ ] `QUICKSTART.md`
  - [ ] `DEPLOYMENT_CHECKLIST.md` (this file)

---

## ✅ Mac Prerequisites

- [ ] macOS 10.15 or higher
- [ ] Python 3.8+ installed: `python3 --version`
- [ ] Terminal access
- [ ] Network connectivity to Windows server
- [ ] Can ping Windows: `ping WINDOWS_IP`

---

## ✅ Installation (Mac)

```bash
cd ~/Documents/mac_deployment_package  # or your location
chmod +x setup_mac.sh test_connection.sh
bash setup_mac.sh
```

- [ ] Setup script completed without errors
- [ ] Virtual environment created: `venv/` directory exists
- [ ] Dependencies installed: `websockets` package present

---

## ✅ Configuration

- [ ] Windows IP address set:
  ```bash
  export HAL_GATEWAY_URL=ws://YOUR_WINDOWS_IP:8768
  ```
- [ ] Environment variable persisted (optional):
  ```bash
  echo 'export HAL_GATEWAY_URL=ws://YOUR_IP:8768' >> ~/.zshrc
  source ~/.zshrc
  ```

---

## ✅ Check QM WebSocket Listener (Phantom Process)

### Verify Listener Running
```cmd
# On QM Server
netstat -an | findstr 8768
```

- [ ] Port 8768 shows LISTENING
- [ ] WebSocket listener responding

### Check QM Phantom Process
```qm
# In QM terminal
LOGTO HAL
LIST.READU
```

- [ ] WEBSOCKET.LISTENER process visible
- [ ] No error status
- [ ] Phantom process active

### Restart if Needed (Rare)
```qm
LOGTO HAL
PHANTOM EXECUTE "WEBSOCKET.LISTENER"
```

- [ ] Phantom started successfully
- [ ] Port 8768 now listening
- [ ] No error messages

---

## ✅ Connection Test (Mac)

```bash
bash test_connection.sh
```

- [ ] Test 1 passed: Network connectivity (can ping Windows)
- [ ] Test 2 passed: Port connectivity (port 8768 open)
- [ ] Test 3 passed: WebSocket connection (received response)
- [ ] Shows: "All Tests Passed! ✓"

---

## ✅ Functional Test (Mac)

```bash
source venv/bin/activate
python3 hal_text_client.py --query "Hello HAL"
```

- [ ] Client connects successfully
- [ ] Receives session ID
- [ ] Query sent
- [ ] Response received from HAL
- [ ] Shows intent and action
- [ ] No error messages

---

## ✅ Interactive Test (Mac)

```bash
python3 hal_text_client.py
```

Try each query:

- [ ] "What medications am I taking?" → MEDICATION intent
- [ ] "Show my appointments" → APPOINTMENT intent  
- [ ] "What are my vital signs?" → HEALTH_DATA intent
- [ ] "Hello HAL" → GENERAL intent
- [ ] "quit" → Exits cleanly

---

## ✅ Performance Test

- [ ] Response time < 2 seconds for simple queries
- [ ] No timeouts or connection drops
- [ ] Multiple queries work in sequence
- [ ] Can exit and restart client successfully

---

## ✅ Voice Mode Test (Optional)

If installing voice features:

```bash
brew install portaudio ffmpeg
pip install numpy sounddevice webrtcvad simpleaudio openwakeword
python3 hal_voice_client.py
```

- [ ] Audio dependencies installed
- [ ] Wake word model loaded
- [ ] Microphone detected
- [ ] Can say "Hey Jarvis" and get activation sound
- [ ] Voice commands recognized
- [ ] Audio playback works

---

## ✅ Documentation

- [ ] README.md reviewed
- [ ] QUICKSTART.md reviewed
- [ ] Example queries tested
- [ ] Troubleshooting section understood

---

## ✅ Production Readiness

- [ ] Client works reliably for 10+ consecutive queries
- [ ] Network connection stable
- [ ] Services auto-restart after errors (optional)
- [ ] User knows how to start/stop services
- [ ] User knows how to troubleshoot common issues

---

## 🐛 If Any Test Fails

### Connection Test Fails

**Test 1 (Network) fails**:
- Verify Windows IP: `ipconfig` on Windows
- Check both machines on same network
- Try `ping WINDOWS_IP` from Mac

**Test 2 (Port) fails**:
- Check WebSocket Listener: `netstat -an | findstr 8768`
- Check QM phantom process: `LIST.READU` in QM
- Check Windows firewall (see rule above)
- Try connecting from Windows itself: `Test-NetConnection localhost -Port 8768`

**Test 3 (WebSocket) fails**:
- Check QM phantom process status
- Restart WebSocket Listener: `PHANTOM EXECUTE "WEBSOCKET.LISTENER"`
- Check QM logs for errors
- Verify JSON format compatibility

### Functional Test Fails

**"No module named websockets"**:
```bash
source venv/bin/activate
pip install -r requirements.txt
```

**"Connection refused"**:
- Voice Gateway not running
- Wrong IP address
- Firewall blocking

**"Timeout"**:
- Network latency too high
- Services overloaded
- VPN interfering

**No response from HAL**:
- QM WebSocket Listener phantom not running
- Phantom process crashed (check with LIST.READU)
- JSON parsing error (check QM logs)
- Restart phantom: `PHANTOM EXECUTE "WEBSOCKET.LISTENER"`

---

## 📊 Deployment Status

**Date**: _______________

**Deployed by**: _______________

**Windows IP**: _______________

**Mac Name**: _______________

**Status**: ⬜ In Progress  ⬜ Complete  ⬜ Failed

**Notes**:
```
_________________________________________________

_________________________________________________

_________________________________________________
```

---

## ✅ Final Verification

All checkboxes above checked? Then:

**🎉 Deployment Complete!**

Your MacBook Pro can now communicate with HAL!

---

## 📞 Support

If you encounter issues not covered in this checklist:

1. Review `README.md` troubleshooting section
2. Check Windows service logs
3. Check QM Voice Listener output
4. Run `bash test_connection.sh` for diagnostics
5. Verify network connectivity and firewall settings

---

**Deployment package version**: 1.0
**Last updated**: 2025-11-26

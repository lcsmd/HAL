# HAL Mac Client - Quick Start Guide

**Get up and running in 5 minutes!**

---

## 🎯 What You'll Do

1. ✅ Get Windows server IP
2. ✅ Copy files to Mac
3. ✅ Run setup script
4. ✅ Test connection
5. ✅ Chat with HAL!

---

## Step 1: Network Information (Pre-Configured)

Your HAL network is already configured:

- **QM Server**: `10.1.34.103` (Windows/OpenQM)
- **AI Server**: `10.1.10.20` (Ollama/Faster-Whisper)
- **HAProxy**: `10.1.50.100` (SSH port 2222)

**Voice Gateway URL**: `ws://10.1.34.103:8768`

✅ No need to look up IPs - already configured!

---

## Step 2: Copy to Mac (2 minutes)

Transfer the **entire mac_deployment_package folder** to your MacBook Pro:

**Option A - USB Drive**:
1. Copy folder to USB
2. Plug USB into Mac
3. Copy folder to `~/Documents/`

**Option B - Network Share**:
1. On Mac, connect to Windows share (Finder → Go → Connect to Server)
2. Copy folder to your Mac

**Option C - Cloud**:
1. Upload to Dropbox/Google Drive
2. Download on Mac

---

## Step 3: Setup (1 minute)

On your **Mac**, open Terminal:

```bash
cd ~/Documents/mac_deployment_package  # or wherever you copied it

# Make scripts executable
chmod +x setup_mac.sh test_connection.sh

# Run setup
bash setup_mac.sh
```

**You'll see**:
```
============================================================
HAL Mac Client Setup
============================================================

✓ Found Python 3.11.5
✓ Virtual environment created
✓ Virtual environment activated
✓ Dependencies installed

Setup Complete!
```

---

## Step 4: Configure (10 seconds)

Load your network configuration:

```bash
source network_config.sh
```

**That's it!** All IPs are pre-configured.

To make permanent (optional):
```bash
echo 'source ~/Documents/mac_deployment_package/network_config.sh' >> ~/.zshrc
source ~/.zshrc
```

---

## Step 5: Check QM Server (should already be running)

On your **QM Server** (10.1.34.103):

### Check WebSocket Listener (Phantom Process)
```powershell
# On Windows - check if port is listening
netstat -an | findstr 8768
```

**Expected output**:
```
TCP    0.0.0.0:8768           0.0.0.0:0              LISTENING
```

If port 8768 is listening, **you're good to go!** The phantom process is running.

### If NOT Running (rare)
```qm
* In QM terminal
LOGTO HAL
PHANTOM EXECUTE "WEBSOCKET.LISTENER"
```

**Note**: The WebSocket listener runs as a QM phantom process (background process), not as a separate Python script. It should already be running on your QM server.

---

## Step 6: Test Connection (30 seconds)

On your **Mac**:

```bash
bash test_connection.sh
```

**Expected output**:
```
============================================================
HAL Connection Test
============================================================

Test 1: Network Connectivity
─────────────────────────────
✓ Host 192.168.1.100 is reachable

Test 2: Port Connectivity
─────────────────────────────
✓ Port 8768 is open on 192.168.1.100

Test 3: WebSocket Connection
─────────────────────────────
✓ Connected to HAL Voice Gateway

🤖 HAL: I received your message: Hello HAL

✓ WebSocket connection successful!

============================================================
All Tests Passed! ✓
============================================================
```

---

## Step 7: Chat with HAL! (Now!)

```bash
source venv/bin/activate
python3 hal_text_client.py
```

**Try these**:

```
You: What medications am I taking?

You: Show my appointments

You: Hello HAL

You: help
```

---

## 🎉 That's It!

You're now chatting with HAL from your MacBook Pro!

---

## 🐛 Troubleshooting

### Problem: "Connection refused"

**Check**:
1. Windows IP correct? (`ipconfig` on Windows)
2. Voice Gateway running? (`python PY\voice_gateway.py`)
3. Firewall blocking? (see below)

**Fix Windows Firewall**:
```powershell
# On Windows (as Administrator)
New-NetFirewallRule -DisplayName "HAL Voice Gateway" -Direction Inbound -LocalPort 8768 -Protocol TCP -Action Allow
```

### Problem: "Module not found"

**Fix**:
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### Problem: No response from HAL

**Check on Windows**:
1. Voice Gateway running? (should show incoming connections)
2. QM Listener running? (should show `Waiting for connections...`)
3. Both services responding?

**Restart services**:
- Stop Voice Gateway (Ctrl+C) and restart
- Stop QM Listener (Ctrl+C) and restart

---

## 📝 Quick Reference

### Mac Commands
```bash
# Setup (once)
bash setup_mac.sh

# Load network config
source network_config.sh

# Test
bash test_connection.sh

# Run
source venv/bin/activate
python3 hal_text_client.py

# Single query
python3 hal_text_client.py --query "What medications am I taking?"
```

### QM Server (10.1.34.103) Commands
```cmd
# Check if WebSocket Listener is running
netstat -an | findstr 8768
```

### QM Commands
```qm
* Check phantom processes
LOGTO HAL
LIST.READU

* Restart WebSocket Listener (if needed)
PHANTOM EXECUTE "WEBSOCKET.LISTENER"
```

---

## 🚀 Next Steps

### Voice Mode (Optional)

Want wake word detection and voice input? See `README.md` section "Voice Mode (Optional)"

### Shell Alias

Make it easier to run:
```bash
echo 'alias hal="cd ~/Documents/mac_deployment_package && source venv/bin/activate && python3 hal_text_client.py"' >> ~/.zshrc
source ~/.zshrc

# Now just type:
hal
```

---

## 📞 Need Help?

1. Check `README.md` for detailed troubleshooting
2. Run `bash test_connection.sh` to diagnose issues
3. Check Windows firewall settings
4. Verify both machines on same network

---

**Ready to start? Go to Step 1!** ⬆️

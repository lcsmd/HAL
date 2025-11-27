# Apply HAProxy Configuration for voice.lcs.ai

**Target**: ubu6 (HAProxy server)  
**Backend**: MV1 (10.1.34.103:8765)  
**Result**: voice.lcs.ai will route to Voice Gateway

---

## 🚀 Quickest Method (Copy & Paste)

### From Your Mac or Linux Machine:

**One command to copy and run the script**:
```bash
scp -P 2222 lawr@MV1:/c/qmsys/hal/SCRIPTS/add_voice_backend.sh /tmp/ && \
ssh -p 2222 lawr@ubu6 'bash /tmp/add_voice_backend.sh'
```
Password: `apgar-66` (you'll be asked twice - once for scp, once for ssh)

---

## 📋 Step-by-Step Method (If you prefer manual control)

### Step 1: Copy the script from MV1 to your Mac
```bash
scp -P 22 lawr@MV1:/c/qmsys/hal/SCRIPTS/add_voice_backend.sh ~/add_voice_backend.sh
# Password: apgar-66
```

### Step 2: Copy the script from Mac to ubu6
```bash
scp -P 2222 ~/add_voice_backend.sh lawr@ubu6:/tmp/
# Password: apgar-66
```

### Step 3: SSH to ubu6 and run the script
```bash
ssh -p 2222 lawr@ubu6
# Password: apgar-66

# Once logged in:
bash /tmp/add_voice_backend.sh
```

The script will:
1. ✅ Backup current config
2. ✅ Add voice ACL
3. ✅ Add use_backend rule
4. ✅ Add voice_gateway backend
5. ✅ Test configuration
6. ✅ Reload HAProxy

---

## ✋ Manual Method (Complete Control)

If you prefer to do it manually:

### Step 1: SSH to ubu6
```bash
ssh -p 2222 lawr@ubu6
# Password: apgar-66
```

### Step 2: Backup config
```bash
sudo cp /etc/haproxy/haproxy.cfg /etc/haproxy/haproxy.cfg.backup
```

### Step 3: Edit config
```bash
sudo nano /etc/haproxy/haproxy.cfg
```

### Step 4: Find the frontend section
Look for existing ACLs (you'll see things like `acl is_ollama`, `acl is_speech`, etc.)

**Add this line** with the other ACLs:
```haproxy
    acl is_voice hdr(host) -i voice.lcs.ai
```

### Step 5: Find the use_backend section
Look for existing `use_backend` lines

**Add this line** with the other use_backend rules:
```haproxy
    use_backend voice_gateway if is_voice
```

### Step 6: Scroll to the bottom
**Add this complete backend** at the end of the file:
```haproxy

# Voice Gateway WebSocket - HAL Voice Interface
backend voice_gateway
    mode http
    option http-server-close
    option forwardfor
    # WebSocket support
    timeout tunnel 3600s
    timeout client 3600s
    timeout server 3600s
    http-request set-header X-Forwarded-Proto https
    http-request set-header X-Forwarded-Host %[req.hdr(Host)]
    server voice1 10.1.34.103:8765 check
```

Save: `Ctrl+O`, `Enter`, `Ctrl+X`

### Step 7: Test config
```bash
sudo haproxy -c -f /etc/haproxy/haproxy.cfg
```

Should say: `Configuration file is valid`

### Step 8: Reload HAProxy
```bash
sudo systemctl reload haproxy
```

### Step 9: Check status
```bash
sudo systemctl status haproxy
```

Should show: `active (running)`

---

## ✅ Verify It Worked

### From ubu6:
```bash
# Test if MV1:8765 is reachable
curl http://10.1.34.103:8765

# Check HAProxy is listening
sudo netstat -tulpn | grep :443
```

### From MV1 (PowerShell):
```powershell
# Test DNS
nslookup voice.lcs.ai

# Test connection (should fail gracefully with WebSocket upgrade message)
curl https://voice.lcs.ai
```

### Test WebSocket (if you have wscat installed):
```bash
wscat -c wss://voice.lcs.ai

# Should connect and receive:
# < {"type": "connected", "session_id": "...", ...}
```

---

## 🐛 Troubleshooting

### If configuration test fails:
```bash
# View errors
sudo haproxy -c -f /etc/haproxy/haproxy.cfg

# Restore backup
sudo cp /etc/haproxy/haproxy.cfg.backup /etc/haproxy/haproxy.cfg
```

### If HAProxy won't reload:
```bash
# Check logs
sudo journalctl -u haproxy -n 50

# Or
sudo tail -f /var/log/haproxy.log

# Try restart instead
sudo systemctl restart haproxy
```

### If voice.lcs.ai doesn't connect:
```bash
# From ubu6, test backend directly
telnet 10.1.34.103 8765

# Check if backend is up
echo "show servers state" | sudo socat stdio /var/run/haproxy/admin.sock | grep voice
```

### Check firewall on MV1:
```powershell
# Check if port 8765 is allowed
Get-NetFirewallRule | Where-Object {$_.DisplayName -like "*8765*"}

# Check if port is listening
Get-NetTCPConnection -LocalPort 8765
```

---

## 📱 Alternative: Direct from Windows

If you have Git Bash or WSL on Windows, you can run the commands directly from MV1:

### Using Git Bash:
```bash
# Copy script to ubu6
scp -P 2222 /c/qmsys/hal/SCRIPTS/add_voice_backend.sh lawr@ubu6:/tmp/

# SSH and run
ssh -p 2222 lawr@ubu6 'bash /tmp/add_voice_backend.sh'
```

### Using WSL (Windows Subsystem for Linux):
```bash
wsl
scp -P 2222 /mnt/c/qmsys/hal/SCRIPTS/add_voice_backend.sh lawr@ubu6:/tmp/
ssh -p 2222 lawr@ubu6 'bash /tmp/add_voice_backend.sh'
```

---

## 📊 After Success

Once the HAProxy backend is added, you'll be able to:

1. **Test WebSocket connection**:
   ```bash
   wscat -c wss://voice.lcs.ai
   ```

2. **Run Mac voice client**:
   ```bash
   python mac_voice_client.py
   # (with GATEWAY_URL = "wss://voice.lcs.ai")
   ```

3. **Say "Hey HAL"** and have a conversation!

---

## ⏭️ Next Steps After HAProxy

Once voice.lcs.ai is working:

1. **Start QM Voice Listener** (in the QM window on MV1):
   ```
   PHANTOM VOICE.LISTENER
   ```

2. **Test end-to-end**:
   - Connect from Mac
   - Send wake word
   - Send audio/text
   - Get response from QM

3. **Deploy Mac client**:
   - Configure wss://voice.lcs.ai
   - Test wake word detection
   - Have a conversation with HAL!

---

## Need Help?

The Voice Gateway is already running on MV1:8765 and responding perfectly. Once you add the HAProxy configuration, everything will be connected!

Let me know when it's done and I'll help test it! 🚀

# Instructions to Add voice.lcs.ai to HAProxy

**Quick Guide**: Copy and paste commands below

---

## Option 1: Automated Script (Recommended)

### Step 1: Copy the script to ubu6
```bash
# From your Mac or another machine with SSH access:
scp -P 2222 C:/qmsys/hal/SCRIPTS/add_voice_backend.sh lawr@ubu6:/tmp/
```

### Step 2: SSH and run the script
```bash
ssh -p 2222 lawr@ubu6
# Password: apgar-66

bash /tmp/add_voice_backend.sh
```

The script will:
- ✅ Backup current config
- ✅ Add voice ACL and backend
- ✅ Test configuration
- ✅ Reload HAProxy

---

## Option 2: Manual Configuration

### Step 1: SSH to ubu6
```bash
ssh -p 2222 lawr@ubu6
# Password: apgar-66
```

### Step 2: Backup current config
```bash
sudo cp /etc/haproxy/haproxy.cfg /etc/haproxy/haproxy.cfg.backup.$(date +%Y%m%d_%H%M%S)
```

### Step 3: Edit HAProxy config
```bash
sudo nano /etc/haproxy/haproxy.cfg
```

### Step 4: Add ACL in frontend section

Find the section with other ACLs (look for `acl is_ollama`, `acl is_speech`, etc.) and add:
```haproxy
    acl is_voice hdr(host) -i voice.lcs.ai
```

### Step 5: Add use_backend rule

Find the section with `use_backend` rules and add:
```haproxy
    use_backend voice_gateway if is_voice
```

### Step 6: Add backend at the end

Scroll to the end of the file and add:
```haproxy

# Voice Gateway WebSocket - HAL Voice Interface
backend voice_gateway
    mode http
    option http-server-close
    option forwardfor
    # WebSocket support - long timeouts for persistent connections
    timeout tunnel 3600s
    timeout client 3600s
    timeout server 3600s
    # Forward proper headers
    http-request set-header X-Forwarded-Proto https
    http-request set-header X-Forwarded-Host %[req.hdr(Host)]
    http-request set-header X-Real-IP %[src]
    # Backend server - MV1 Voice Gateway
    server voice1 10.1.10.20:8765 check inter 5000 rise 2 fall 3
```

Save with `Ctrl+O`, `Enter`, `Ctrl+X`

### Step 7: Test configuration
```bash
sudo haproxy -c -f /etc/haproxy/haproxy.cfg
```

Should see: `Configuration file is valid`

### Step 8: Reload HAProxy (zero downtime)
```bash
sudo systemctl reload haproxy
```

### Step 9: Check status
```bash
sudo systemctl status haproxy
```

---

## Option 3: Quick One-Liner (Risky but Fast)

**⚠️ Use with caution - only if you're confident**

```bash
ssh -p 2222 lawr@ubu6 'sudo bash -s' < /path/to/add_voice_backend.sh
```

---

## Verification

After adding the backend, test from MV1:

```powershell
# Test that voice.lcs.ai resolves
nslookup voice.lcs.ai

# Test HTTP connection (should upgrade to WebSocket)
curl https://voice.lcs.ai
```

Test WebSocket connection:
```powershell
# Install wscat if needed (Node.js required)
npm install -g wscat

# Test WebSocket connection
wscat -c wss://voice.lcs.ai

# Should see:
# Connected
# < {"type": "connected", "session_id": "...", ...}
```

---

## Troubleshooting

### If HAProxy config test fails:
```bash
# Check for syntax errors
sudo haproxy -c -f /etc/haproxy/haproxy.cfg

# Restore backup
sudo cp /etc/haproxy/haproxy.cfg.backup.* /etc/haproxy/haproxy.cfg
```

### If HAProxy won't reload:
```bash
# Check HAProxy logs
sudo tail -f /var/log/haproxy.log

# Check status
sudo systemctl status haproxy

# Restart if needed
sudo systemctl restart haproxy
```

### If connection fails:
```bash
# From ubu6, test if MV1:8765 is reachable
telnet 10.1.10.20 8765

# Or
curl http://10.1.10.20:8765
```

### Check HAProxy stats:
```bash
# If stats page is enabled
curl http://ubu6:9000/stats
```

---

## Files for Reference

All configuration snippets are in:
- `SCRIPTS/haproxy_voice_backend.cfg` - Config snippets
- `SCRIPTS/add_voice_backend.sh` - Automated script
- `SCRIPTS/check_haproxy_config.sh` - Inspection script

---

## What Happens After

Once voice.lcs.ai is configured:

1. **From Mac**: `wscat -c wss://voice.lcs.ai` will connect
2. **Voice Gateway** on MV1 will receive the connection
3. **SSL termination** happens at HAProxy (wss → ws)
4. You can run the **Mac voice client** with the secure URL

Then just need to start the QM Voice Listener and you're fully live!

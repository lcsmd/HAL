# HAL Web Voice Client - Quick Reference Card

## 🚀 Quick Start (3 Steps)

### 1. Update HAProxy
```bash
ssh lawr@10.1.50.100 -p 2222
sudo cp /path/to/hal/haproxy.cfg /etc/haproxy/haproxy.cfg
sudo haproxy -c -f /etc/haproxy/haproxy.cfg && sudo systemctl reload haproxy
```

### 2. Start Servers (Windows)
```bash
cd C:\qmsys\hal
start_web_voice_servers.bat
```

### 3. Test
Open browser: **https://hal.lcs.ai**

---

## 🔧 Common Commands

### Start/Stop Services
```bash
# Start (Linux/Mac/Git Bash)
./start_web_voice_servers.sh

# Start (Windows)
start_web_voice_servers.bat

# Stop
./stop_web_voice_servers.sh
# Or: taskkill /F /IM python.exe
```

### Check Status
```bash
# Are servers running?
netstat -an | grep "8080\|8768"       # Linux/Mac
netstat -an | findstr "8080 8768"     # Windows

# View logs
tail -f logs/voice_gateway.log
tail -f logs/http_server.log
```

### Test Connection
```bash
# HTTP server
curl http://10.1.34.103:8080

# WebSocket (requires wscat)
wscat -c ws://10.1.34.103:8768

# Through HAProxy
curl -I https://hal.lcs.ai
```

---

## 🐛 Troubleshooting (90% of issues)

### "Disconnected. Reconnecting..." Loop

**Check 1: Are services running?**
```bash
ps aux | grep voice_gateway_web
netstat -an | grep 8768
```

**Check 2: HAProxy routing correctly?**
```bash
sudo tail -f /var/log/haproxy.log
# Look for "hal2_backend/hal2_ws"
```

**Quick Fix:**
```bash
# Restart services
./stop_web_voice_servers.sh
./start_web_voice_servers.sh

# Reload HAProxy
sudo systemctl reload haproxy
```

### Text Input No Response

**Check 1: Is WebSocket really connected?**
- Open browser console (F12)
- Type: `document.querySelector('#status').textContent`
- Should say "Connected!"

**Check 2: Check Voice Gateway logs**
```bash
tail -20 logs/voice_gateway.log
# Look for "Client connected" and message handling
```

**Quick Fix:**
```bash
# Restart Voice Gateway
pkill -f voice_gateway_web
cd PY && python voice_gateway_web.py &
```

### Can't Access https://hal.lcs.ai

**Check 1: DNS**
```bash
nslookup hal.lcs.ai
# Should resolve to HAProxy server
```

**Check 2: HAProxy running?**
```bash
ssh lawr@10.1.50.100 -p 2222
sudo systemctl status haproxy
```

**Quick Fix:**
```bash
# Access directly (bypass HAProxy)
# Open: http://10.1.34.103:8080
# Change client.js serverUrl to: ws://10.1.34.103:8768
```

---

## 📊 Health Check Commands

```bash
# One-liner to check everything
echo "HTTP Server:" && curl -s -o /dev/null -w "%{http_code}" http://10.1.34.103:8080 && \
echo " | WebSocket:" && netstat -an | grep -q 8768 && echo "LISTENING" || echo "DOWN" && \
echo " | HAProxy:" && curl -s -I https://hal.lcs.ai | head -1

# Expected output:
# HTTP Server: 200
# WebSocket: LISTENING
# HAProxy: HTTP/2 200
```

---

## 📁 Important Files

| File | Purpose |
|------|---------|
| `haproxy.cfg` | HAProxy routing config (on ubu6) |
| `PY/voice_gateway_web.py` | WebSocket server |
| `voice_assistant_v2/web_client/client.js` | Browser client code |
| `voice_assistant_v2/web_client/index.html` | UI |
| `start_web_voice_servers.sh` | Startup script |
| `WEB_VOICE_CLIENT_TESTING.md` | Full testing guide |

---

## 🌐 Network Layout

```
Browser → wss://hal.lcs.ai (HAProxy:443)
           ↓
         HAProxy routes to:
           ↓
         ws://10.1.34.103:8768 (Voice Gateway)
         http://10.1.34.103:8080 (HTTP Server)
           ↓
         Queries Ollama at 10.1.10.20:11434
         Transcribes at 10.1.10.20:8001
```

---

## ⚡ Performance Targets

- **Connection:** < 1 second
- **Text query:** 1-3 seconds
- **Voice query:** 3-5 seconds
- **Uptime:** 99%+ (should not disconnect)

---

## 📞 When All Else Fails

1. **Restart everything:**
   ```bash
   # Windows Server
   ./stop_web_voice_servers.sh
   ./start_web_voice_servers.sh
   
   # HAProxy
   ssh lawr@10.1.50.100 -p 2222
   sudo systemctl restart haproxy
   ```

2. **Check Python dependencies:**
   ```bash
   cd PY
   python -c "import websockets, aiohttp; print('OK')"
   # If error: pip install websockets aiohttp
   ```

3. **Test components independently:**
   ```bash
   # Test QueryRouter
   cd PY
   python -c "from query_router import QueryRouter; r=QueryRouter(); print(r.route_query('hello','test',[]))"
   
   # Test Ollama
   curl http://10.1.10.20:11434/api/version
   ```

4. **Read full docs:**
   - WEB_VOICE_CLIENT_TESTING.md (complete troubleshooting)
   - WEB_VOICE_CLIENT_FIX_SUMMARY.md (what was fixed)
   - WEB_VOICE_CLIENT_ARCHITECTURE.md (how it works)

---

## 🎯 Success Criteria

System is working when:
- ✅ Browser shows "Connected!"
- ✅ Text "hello" gets response
- ✅ No errors in logs
- ✅ Connection stays stable 10+ minutes

---

**Quick Links:**
- Public URL: https://hal.lcs.ai
- HAProxy Stats: http://10.1.50.100:8404/stats (admin/apgar-66)
- Docs: WEB_VOICE_CLIENT_TESTING.md

**Last Updated:** 2025-12-04

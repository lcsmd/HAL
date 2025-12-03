# Fix Whisper Server Connection

## 🔴 Problem

Windows server can't connect to Whisper on Ubuntu (port 9000 blocked).

**Symptoms:**
```
TCP connect to (10.1.10.20 : 9000) failed
```

---

## ✅ Solutions

### OPTION 1: Check Whisper Server Binding (Most Likely)

**On Ubuntu server, run:**

```bash
# Check if Whisper is listening on all interfaces
sudo netstat -tlnp | grep 9000
```

**Should show:**
```
tcp  0  0  0.0.0.0:9000  0.0.0.0:*  LISTEN  12345/python3
```

**If it shows `127.0.0.1:9000` instead**, it's only listening locally!

**Fix: Edit whisper_server.py**

```bash
sudo nano /opt/faster-whisper/whisper_server.py
```

**Find the last lines (near line 120):**
```python
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=9000)
```

**Change to:**
```python
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=9000)
```

**Restart service:**
```bash
sudo systemctl restart faster-whisper
sudo systemctl status faster-whisper
```

**Test again:**
```bash
curl http://localhost:9000/health
```

---

### OPTION 2: Check Firewall

**On Ubuntu server:**

```bash
# Check if UFW is active
sudo ufw status

# If active, allow port 9000
sudo ufw allow 9000/tcp
sudo ufw reload

# Verify
sudo ufw status | grep 9000
```

---

### OPTION 3: Check Whisper Service

**On Ubuntu server:**

```bash
# Check if service is running
sudo systemctl status faster-whisper

# View logs
sudo journalctl -u faster-whisper -n 50

# Restart if needed
sudo systemctl restart faster-whisper
```

---

## 🧪 Test from Windows

**After fixing, test from Windows server:**

```powershell
# Test connection
Test-NetConnection -ComputerName 10.1.10.20 -Port 9000

# Test Whisper health
curl http://10.1.10.20:9000/health
# Should return: {"status":"running"...}
```

---

## 🎯 Quick Fix Commands (Ubuntu)

**Run all these on Ubuntu server:**

```bash
# 1. Check what's running
sudo netstat -tlnp | grep 9000

# 2. Allow firewall
sudo ufw allow 9000/tcp

# 3. Edit server to bind to 0.0.0.0
sudo sed -i 's/host="127.0.0.1"/host="0.0.0.0"/g' /opt/faster-whisper/whisper_server.py

# 4. Restart service
sudo systemctl restart faster-whisper

# 5. Check status
sudo systemctl status faster-whisper

# 6. Test locally
curl http://localhost:9000/health
```

---

## 📊 After Fix

**Voice mode will work!**

1. Client has wake word model ✅
2. Client has voice libraries ✅
3. Whisper server accessible ✅

**Run on client:**
```powershell
cd C:\HAL\VOICE_ASSISTANT_V2\CLIENT
python hal_voice_client_gui.py
```

**Say:** "Hey Jarvis" + your question

---

## 🔍 Troubleshooting

### Still can't connect?

**Check if service is actually running:**
```bash
ps aux | grep whisper_server
```

**Check logs for errors:**
```bash
sudo journalctl -u faster-whisper -f
```

**Test locally on Ubuntu:**
```bash
curl http://localhost:9000/health
```

If local works but remote doesn't = firewall issue  
If local doesn't work = service issue

---

**Most Common Fix:** Change `host="127.0.0.1"` to `host="0.0.0.0"` in whisper_server.py

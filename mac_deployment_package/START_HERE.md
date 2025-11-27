# 🚀 START HERE - HAL Mac Client

**Your network is pre-configured and ready to use!**

---

## ✅ Your Network (Pre-Configured)

```
QM Server:      10.1.34.103   (Windows/OpenQM)         user: lawr
AI Server:      10.1.10.20    (GPU: Ollama/Whisper)   user: lawr  ⚡
HAProxy:        10.1.50.100   (SSH port 2222)          user: lawr
Proxmox:        10.1.33.1     (Virtualization)         user: root

Gateway URL:    ws://10.1.34.103:8768
```

**⚡ = GPU-accelerated for real-time AI & voice processing**

**Everything is configured! See CREDENTIALS.txt for access details.**

---

## 🎯 Quick Start (3 Steps)

### 1. Setup (1 minute)
```bash
chmod +x setup_mac.sh test_connection.sh
bash setup_mac.sh
```

### 2. Load Config (5 seconds)
```bash
source network_config.sh
```

### 3. Test & Run (30 seconds)
```bash
bash test_connection.sh
source venv/bin/activate
python3 hal_text_client.py
```

**That's it!** Start chatting with HAL!

---

## 📚 Documentation

| File | Purpose |
|------|---------|
| **START_HERE.md** | ← You are here (quick overview) |
| **QUICKSTART.md** | 5-minute step-by-step guide |
| **README.md** | Complete documentation |
| **NETWORK_INFO.md** | Detailed network architecture |
| **DEPLOYMENT_CHECKLIST.md** | Verification checklist |

---

## 🎯 Try These Queries

```
You: What medications am I taking?
You: Show my appointments
You: What are my vital signs?
You: Hello HAL
You: help
```

---

## 🐛 Troubleshooting

### Problem: Connection refused

**Check WebSocket Listener on QM Server (10.1.34.103)**:
```cmd
# Check if port 8768 is listening
netstat -an | findstr 8768
```

**Check QM Phantom Process**:
```qm
# In QM terminal
LOGTO HAL
LIST.READU
# Look for WEBSOCKET.LISTENER
```

**Restart if needed**:
```qm
LOGTO HAL
PHANTOM EXECUTE "WEBSOCKET.LISTENER"
```

**Check firewall**:
```powershell
# On QM Server as Administrator
New-NetFirewallRule -DisplayName "HAL WebSocket" -Direction Inbound -LocalPort 8768 -Protocol TCP -Action Allow
```

### Run Diagnostics
```bash
bash test_connection.sh
```

---

## 📖 Full Guides

**New to HAL?** → Read `QUICKSTART.md`

**Want details?** → Read `README.md`

**Network info?** → Read `NETWORK_INFO.md`

**AI services?** → Read `AI_SERVICES.md` (GPU, Ollama, Whisper)

**Phantom process?** → Read `PHANTOM_PROCESS_INFO.md`

---

## 🎉 Ready!

Your Mac client is configured for:
- ✅ QM Server at 10.1.34.103
- ✅ AI Server at 10.1.10.20
- ✅ HAProxy at 10.1.50.100

Just run the 3 steps above and start using HAL!

---

**Commands to remember**:
```bash
source network_config.sh          # Load config
python3 hal_text_client.py        # Start HAL
bash test_connection.sh           # Test connection
```

**Enjoy your HAL assistant!** 🚀

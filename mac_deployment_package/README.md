# HAL Mac Client Deployment Package

**Text-based interface for HAL assistant on your MacBook Pro**

This package provides a simple, lightweight text interface to communicate with your HAL assistant running on Windows/OpenQM.

---

## 🎯 What's Included

- **hal_text_client.py** - Main text client (no audio dependencies)
- **setup_mac.sh** - Automated setup script
- **test_connection.sh** - Connection testing script
- **requirements.txt** - Python dependencies
- **README.md** - This file

---

## 📋 Prerequisites

- **MacBook Pro** (macOS 10.15+)
- **Python 3.8+** (usually pre-installed)
- **Network connection** to Windows HAL server
- **HAL Voice Gateway** running on Windows

---

## 🚀 Quick Start (5 Minutes)

### Step 1: Get Windows Server IP

On your Windows machine, open PowerShell:
```powershell
ipconfig | findstr IPv4
```

Example output: `IPv4 Address. . . . . . . . . . . : 192.168.1.100`

**Write down this IP address!**

### Step 2: Copy Files to Mac

Transfer this entire folder to your MacBook Pro:
- Via USB drive
- Via network share
- Via email/cloud storage
- Direct copy if machines are networked

### Step 3: Run Setup Script

On your Mac, open Terminal and navigate to this folder:
```bash
cd ~/Downloads/mac_deployment_package  # or wherever you put it
chmod +x setup_mac.sh test_connection.sh
bash setup_mac.sh
```

### Step 4: Configure Gateway URL

Set the Windows server IP:
```bash
export HAL_GATEWAY_URL=ws://192.168.1.100:8768
```

**Replace `192.168.1.100` with your actual Windows IP!**

To make this permanent, add to `~/.zshrc` (or `~/.bash_profile`):
```bash
echo 'export HAL_GATEWAY_URL=ws://192.168.1.100:8768' >> ~/.zshrc
source ~/.zshrc
```

### Step 5: Test Connection

```bash
bash test_connection.sh
```

If all tests pass, you're ready!

### Step 6: Start Using HAL

```bash
source venv/bin/activate  # Activate virtual environment
python3 hal_text_client.py
```

---

## 💬 Usage Examples

### Interactive Mode

```bash
python3 hal_text_client.py
```

Then type your queries:
```
You: What medications am I taking?
🤖 HAL: I detected a medication query: What medications am I taking?

You: Show my appointments
🤖 HAL: I detected an appointment query: Show my appointments

You: quit
👋 Goodbye!
```

### Single Query Mode

```bash
python3 hal_text_client.py --query "What medications am I taking?"
```

### Help

```bash
python3 hal_text_client.py
You: help
```

---

## 🎯 Example Queries

### Medical Information
- "What medications am I taking?"
- "Show my allergy list"
- "When is my next doctor appointment?"
- "What were my last vital signs?"
- "Show my immunization records"

### Financial Information
- "Show recent transactions"
- "What did I spend at Starbucks?"
- "List my reimbursable expenses"
- "Show transactions from this month"

### General
- "Hello HAL"
- "What can you do?"
- "Tell me about yourself"

---

## 🔧 Troubleshooting

### "Connection refused"

**Cause**: Cannot connect to Windows server

**Solutions**:
1. Verify Windows IP address: `ipconfig` on Windows
2. Check Voice Gateway is running: `python PY/voice_gateway.py`
3. Check Windows firewall (see below)
4. Verify both machines on same network

### Windows Firewall

On Windows, allow port 8768:
```powershell
New-NetFirewallRule -DisplayName "HAL Voice Gateway" -Direction Inbound -LocalPort 8768 -Protocol TCP -Action Allow
```

### "No module named websockets"

**Solution**:
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### Gateway not responding

**Check on Windows**:
1. Is Voice Gateway running?
   ```cmd
   python PY\voice_gateway.py
   ```

2. Is QM Voice Listener running?
   ```qm
   In QM terminal: Check if listener is active
   ```

3. Check logs on Windows

### Wrong Python version

**Solution**:
```bash
# Install newer Python via Homebrew
brew install python@3.11

# Update virtual environment
rm -rf venv
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

## 🏗️ Architecture

```
┌─────────────────┐
│  MacBook Pro    │  ← hal_text_client.py (you are here)
│   Your Mac      │     Text input/output
└────────┬────────┘
         │ WebSocket (ws://10.1.34.103:8768)
         ↓
┌─────────────────────────────────────┐
│ QM Server (Windows)                 │
│ 10.1.34.103                         │
│                                     │
│  ┌──────────────────────────┐     │
│  │ WebSocket Listener        │     │  ← Phantom Process
│  │ Port 8768                 │     │     (runs in QM)
│  └──────────┬────────────────┘     │
│             │                       │
│             ↓                       │
│  ┌──────────────────────────┐     │
│  │ Intent Detection          │     │
│  │ MEDICATION, APPOINTMENT   │     │
│  │ HEALTH_DATA, GENERAL      │     │
│  └──────────┬────────────────┘     │
│             │                       │
│             ↓                       │
│  ┌──────────────────────────┐     │
│  │ OpenQM HAL Database       │     │
│  │ - Medical records          │     │
│  │ - Financial data           │     │
│  │ - Personal information     │     │
│  └────────────────────────────┘     │
└─────────────────────────────────────┘

Note: Everything runs in QM - no separate Python gateway!
The WebSocket listener is a QM phantom process.
```

---

## 📁 File Structure

```
mac_deployment_package/
├── README.md                 ← You are here
├── QUICKSTART.md             ← 5-minute setup guide
├── START_HERE.md             ← Quick overview
├── NETWORK_INFO.md           ← Network architecture
├── AI_SERVICES.md            ← GPU & AI services
├── PHANTOM_PROCESS_INFO.md   ← QM phantom details
├── hal_text_client.py        ← Main client script
├── hal_voice_client.py       ← Full voice client
├── network_config.sh         ← Network configuration
├── requirements.txt          ← Python dependencies
├── setup_mac.sh              ← Setup script
├── test_connection.sh        ← Connection test
└── venv/                     ← Virtual environment (created by setup)
```

---

## 🔐 Security Notes

- **No encryption**: WebSocket traffic is unencrypted (ws://)
- **Local network only**: Designed for trusted home/office network
- **No authentication**: Gateway assumes trusted clients
- **For VPN/internet use**: Consider setting up SSL (wss://)

---

## ⚙️ Advanced Configuration

### Custom Port

If using non-standard port:
```bash
export HAL_GATEWAY_URL=ws://192.168.1.100:9999
```

### Multiple Servers

Switch between servers easily:
```bash
# Home server
export HAL_GATEWAY_URL=ws://192.168.1.100:8768

# Work server
export HAL_GATEWAY_URL=ws://10.0.0.50:8768
```

### Shell Alias

Add to `~/.zshrc`:
```bash
alias hal='cd ~/hal/mac_deployment_package && source venv/bin/activate && python3 hal_text_client.py'
```

Then just run:
```bash
hal
```

---

## 🎵 Voice Mode (Optional)

This package includes text mode only. For full voice features:

1. Copy full voice client:
   ```bash
   cp ../clients/hal_voice_client_full.py .
   ```

2. Install audio dependencies:
   ```bash
   brew install portaudio ffmpeg
   pip install numpy sounddevice webrtcvad simpleaudio openwakeword
   ```

3. Run voice client:
   ```bash
   python3 hal_voice_client_full.py
   ```

See `../clients/MAC_QUICK_START.md` for details.

---

## 📞 Getting Help

### Check Status

**On Mac**:
```bash
# Test connection
bash test_connection.sh

# Check Python environment
python3 --version
source venv/bin/activate
pip list
```

**On Windows**:
```cmd
# Check if Voice Gateway is running
netstat -an | findstr 8768

# Check if QM Listener is running  
netstat -an | findstr 8767

# View Gateway logs
python PY\voice_gateway.py
```

### Common Issues

| Issue | Solution |
|-------|----------|
| Connection refused | Check Windows firewall, verify IP |
| No response | Restart Voice Gateway on Windows |
| Timeout | Check network latency, VPN issues |
| JSON errors | Update Windows Voice Gateway |

---

## ✅ Checklist

Before you start, verify:

- [ ] Python 3.8+ installed on Mac
- [ ] Windows server IP address known
- [ ] Voice Gateway running on Windows (`python PY/voice_gateway.py`)
- [ ] QM Voice Listener running on Windows
- [ ] Both machines on same network
- [ ] Firewall allows port 8768
- [ ] Setup script completed successfully
- [ ] Connection test passes

---

## 🎉 You're Ready!

Everything you need is in this package. Just follow the Quick Start and you'll be chatting with HAL in minutes!

**Start now**:
```bash
bash setup_mac.sh
export HAL_GATEWAY_URL=ws://YOUR_WINDOWS_IP:8768
python3 hal_text_client.py
```

Enjoy your HAL assistant! 🚀

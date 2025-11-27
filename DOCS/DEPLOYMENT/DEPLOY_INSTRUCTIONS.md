# HAL Voice System - Deployment Instructions

## Your Server Configuration

**QM Server IP:** 10.1.34.103
**Voice Gateway Port:** 8768
**QM Listener Port:** 8767

---

## Deploy Mac Client - One Line Installation

### Step 1: Start Installer Server (On Windows QM Server)

```bash
cd C:\qmsys\hal\clients
python serve_installer.py
```

### Step 2: Install on Mac (Run ONE of these commands)

#### Option A: Local Network
```bash
curl -fsSL http://10.1.34.103:8080/install_hal_mac.sh | \
HAL_SERVER_URL=http://10.1.34.103:8768 bash
```

#### Option B: External via HAProxy (if configured)
```bash
curl -fsSL http://10.1.34.103:8080/install_hal_mac.sh | \
HAL_SERVER_URL=https://hal.yourdomain.com bash
```

#### Option C: Interactive (will prompt)
```bash
curl -fsSL http://10.1.34.103:8080/install_hal_mac.sh | bash
```

---

## Using HAL from Mac

After installation, restart your terminal and:

### Interactive Mode
```bash
hal
```

### Single Query
```bash
hal --query "What medications am I taking?"
```

---

## Testing the Connection

### 1. Check Voice Gateway is Running
On Windows:
```powershell
netstat -an | findstr "8768"
```
Should show: `TCP 0.0.0.0:8768 ... LISTENING`

### 2. Check QM Listener is Running
In QM:
```
LIST.READU
```
Look for phantom process on port 8767

### 3. Test from Mac
```bash
# Test installer server
curl http://10.1.34.103:8080/

# Test after installation
hal --query "test"
```

---

## Firewall Configuration

### Windows Server (Required)

Allow port 8768 for Voice Gateway:
```powershell
New-NetFirewallRule -DisplayName "HAL Voice Gateway" `
    -Direction Inbound -LocalPort 8768 -Protocol TCP -Action Allow
```

Allow port 8080 for installer server (temporary):
```powershell
New-NetFirewallRule -DisplayName "HAL Installer Server" `
    -Direction Inbound -LocalPort 8080 -Protocol TCP -Action Allow
```

### After Mac Installation

Stop the installer server (Ctrl+C). Port 8080 only needed during installation.

---

## Architecture

```
Mac Client
    ↓ WebSocket
Voice Gateway (10.1.34.103:8768)
    ↓ TCP Socket
QM Listener (10.1.34.103:8767)
    ↓ Native QM
HAL Database
```

---

## Troubleshooting

### "Connection refused" on Mac

1. Check Windows firewall allows port 8768
2. Verify Voice Gateway is running:
   ```powershell
   netstat -an | findstr "8768"
   ```
3. Test connectivity from Mac:
   ```bash
   nc -zv 10.1.34.103 8768
   ```

### "No response from HAL"

1. Check QM Listener is running (port 8767)
2. In QM, view recent commands:
   ```
   SEE.NEW.COM
   ```
3. Check COMO logs for phantom process

### Mac client installed but `hal` command not found

Restart terminal or:
```bash
source ~/.zshrc
# or
source ~/.bashrc
```

Or run directly:
```bash
~/.hal-client/hal
```

---

## Manual Installation (Alternative)

If one-line installer doesn't work:

1. Download client file:
   ```bash
   curl -O http://10.1.34.103:8080/install_hal_mac.sh
   chmod +x install_hal_mac.sh
   ```

2. Run with server URL:
   ```bash
   HAL_SERVER_URL=http://10.1.34.103:8768 ./install_hal_mac.sh
   ```

---

## Review Commands in QM

To see what commands HAL is processing:

In QM:
```
SEE.NEW.COM
```

This shows all new commands and outputs with navigation:
- **SPACE** = Next command
- **UP ARROW** = Previous command
- **Q** = Quit

---

## Next Steps

1. ✅ Install on Mac using one-line command
2. ✅ Test with: `hal --query "test"`
3. ✅ Try medication query: `hal --query "What medications am I taking?"`
4. ✅ Review commands in QM: `SEE.NEW.COM`

---

## Support

**Server:** 10.1.34.103
**Voice Gateway:** :8768
**QM Listener:** :8767
**Installation Server:** :8080 (temporary)

# Network Troubleshooting Guide - HAL Mac Client

**Error**: "No route to host" or "Cannot reach host"

---

## 🔍 Quick Diagnosis

### Step 1: Verify Your Mac's Network

```bash
# Check your Mac's IP address
ifconfig | grep "inet " | grep -v 127.0.0.1

# Example output:
#   inet 10.1.34.150 netmask 0xffffff00 broadcast 10.1.34.255
#   inet 192.168.1.100 netmask 0xffffff00 broadcast 192.168.1.255
```

**Look for an IP address starting with `10.1.`** - that's your network!

---

### Step 2: Can You Reach the QM Server?

```bash
# Test basic connectivity
ping -c 3 10.1.34.103

# Expected if working:
# 64 bytes from 10.1.34.103: icmp_seq=0 ttl=128 time=1.234 ms

# If NOT working:
# Request timeout for icmp_seq 0
# ping: sendto: No route to host
```

---

## 🚨 Common Issues and Solutions

### Issue 1: Mac Not on Same Network as Server

**Symptoms**:
- Mac IP: `192.168.x.x` or `172.16.x.x`
- Server IP: `10.1.34.103`
- Ping fails with "No route to host"

**Solutions**:

#### Option A: Connect to Same Network
```bash
# Check available networks
networksetup -listallnetworkservices

# List Wi-Fi networks
/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport -s

# Connect to the same network as the server
# (Use System Preferences → Network)
```

#### Option B: Use VPN (if available)
```bash
# If you have VPN to the 10.1.34.x network
# Connect to VPN first, then try again
```

#### Option C: Use SSH Tunnel Through HAProxy
```bash
# Create SSH tunnel
ssh -p 2222 -L 8768:10.1.34.103:8768 lawr@10.1.50.100 -N

# In another terminal, edit network_config.sh:
export WEBSOCKET_URL="ws://localhost:8768"

# Then run client
python3 hal_text_client.py
```

---

### Issue 2: QM Server Not Running or Not Reachable

**Check from another Windows machine** (if you have access):

```powershell
# On another Windows computer on the network
ping 10.1.34.103

# Check if port 8768 is listening
Test-NetConnection -ComputerName 10.1.34.103 -Port 8768
```

**On the QM Server itself** (10.1.34.103):

```powershell
# Check if QM WebSocket listener is running
netstat -an | findstr 8768

# Expected output if running:
# TCP    0.0.0.0:8768           0.0.0.0:0              LISTENING
# TCP    [::]:8768              [::]:0                 LISTENING

# If NOT showing, start the listener:
# In QM terminal:
LOGTO HAL
LIST.READU
# Should show VOICE.LISTENER.NEW running as phantom
```

---

### Issue 3: Firewall Blocking Connection

#### On QM Server (Windows)

```powershell
# Check if firewall allows port 8768
Get-NetFirewallRule | Where-Object {$_.LocalPort -eq 8768}

# If not allowed, add rule:
New-NetFirewallRule -DisplayName "HAL WebSocket" `
    -Direction Inbound `
    -LocalPort 8768 `
    -Protocol TCP `
    -Action Allow
```

#### On Mac

```bash
# Check Mac firewall status
sudo /usr/libexec/ApplicationFirewall/socketfilterfw --getglobalstate

# Usually Mac firewall doesn't block outgoing connections
# But if needed, allow Python:
sudo /usr/libexec/ApplicationFirewall/socketfilterfw --add $(which python3)
```

---

### Issue 4: Wrong IP Address

**Find the correct QM Server IP**:

On the Windows QM Server:
```powershell
# Get all IP addresses
ipconfig

# Look for "IPv4 Address" that starts with 10.1.34.x
# Example output:
#   IPv4 Address. . . . . . . . . . . : 10.1.34.103
```

**Update your Mac configuration**:
```bash
cd ~/Documents/hal/mac_deployment_package
nano network_config.sh

# Change this line to the correct IP:
export QM_SERVER="10.1.34.XXX"  # Replace XXX with actual
export WEBSOCKET_URL="ws://10.1.34.XXX:8768"
```

---

## 🔧 Diagnostic Script

Create this script on your Mac: `diagnose_network.sh`

```bash
#!/bin/bash

echo "HAL Network Diagnostics"
echo "======================"
echo ""

# Check Mac IP
echo "1. Your Mac's IP addresses:"
ifconfig | grep "inet " | grep -v 127.0.0.1
echo ""

# Check if on 10.1.34.x network
MY_IP=$(ifconfig | grep "inet " | grep "10.1.34" | awk '{print $2}')
if [ -n "$MY_IP" ]; then
    echo "✓ Mac is on 10.1.34.x network: $MY_IP"
else
    echo "✗ Mac is NOT on 10.1.34.x network"
    echo "  You need to connect to the same network as the server"
fi
echo ""

# Check connectivity to server
echo "2. Testing connectivity to QM Server (10.1.34.103):"
if ping -c 2 -W 2 10.1.34.103 > /dev/null 2>&1; then
    echo "✓ Can reach QM Server"
else
    echo "✗ Cannot reach QM Server"
    echo "  Server may be off, or you're on different network"
fi
echo ""

# Check if HAProxy is reachable (alternate route)
echo "3. Testing HAProxy (10.1.50.100) SSH:"
if nc -z -w 2 10.1.50.100 2222 > /dev/null 2>&1; then
    echo "✓ Can reach HAProxy on port 2222"
    echo "  You can use SSH tunnel as alternate"
else
    echo "✗ Cannot reach HAProxy"
fi
echo ""

# Check if port 8768 is reachable
echo "4. Testing WebSocket port (8768):"
if nc -z -w 2 10.1.34.103 8768 > /dev/null 2>&1; then
    echo "✓ Port 8768 is open"
else
    echo "✗ Port 8768 is not reachable"
    echo "  Listener may not be running, or firewall blocking"
fi
echo ""

# Network route check
echo "5. Network route to server:"
route -n get 10.1.34.103
echo ""

echo "Diagnostics complete!"
```

**Run it**:
```bash
chmod +x diagnose_network.sh
./diagnose_network.sh
```

---

## 🎯 Step-by-Step Troubleshooting

### Step 1: Verify You're on the Right Network

```bash
# Check your IP
ifconfig | grep "inet " | grep -v 127.0.0.1

# You should see an IP like:
# inet 10.1.34.XXX
# If you see 192.168.x.x or 172.16.x.x, you're on wrong network
```

**Action**: Connect to the same network as the server

---

### Step 2: Test Basic Ping

```bash
ping -c 3 10.1.34.103

# Working:
# 64 bytes from 10.1.34.103: icmp_seq=0 ttl=128 time=1.234 ms

# Not working:
# Request timeout
# No route to host
```

**If ping fails**: Network issue, VPN needed, or server is off

---

### Step 3: Test WebSocket Port

```bash
# Check if port 8768 is listening
nc -zv 10.1.34.103 8768

# Working:
# Connection to 10.1.34.103 port 8768 [tcp/*] succeeded!

# Not working:
# nc: connectx to 10.1.34.103 port 8768 (tcp) failed: No route to host
```

**If port test fails**: Listener not running or firewall blocking

---

### Step 4: Check QM Listener Status

**On QM Server** (Windows):
```powershell
# Check if listener process exists
netstat -an | findstr 8768

# Should show:
# TCP    0.0.0.0:8768           0.0.0.0:0              LISTENING
```

**If not listening**, start it:
```qm
LOGTO HAL
PHANTOM EXECUTE "WEBSOCKET.LISTENER"
```

---

## 🌐 Alternative Connection Methods

### Option 1: SSH Tunnel (Recommended for Remote Access)

```bash
# Terminal 1: Create tunnel
ssh -p 2222 -L 8768:10.1.34.103:8768 lawr@10.1.50.100 -N

# Terminal 2: Connect via localhost
export WEBSOCKET_URL="ws://localhost:8768"
python3 hal_text_client.py
```

### Option 2: VPN

If your organization has VPN to the 10.1.34.x network:
1. Connect to VPN
2. Verify you get a 10.1.34.x IP
3. Try connection again

### Option 3: Direct Network Connection

Connect your Mac directly to the same switch/router as the QM server.

---

## 📋 Checklist Before Calling for Help

- [ ] Verified Mac IP address with `ifconfig`
- [ ] Checked Mac is on 10.1.34.x network
- [ ] Pinged 10.1.34.103 successfully
- [ ] Tested port 8768 with `nc -zv 10.1.34.103 8768`
- [ ] Verified QM server is running
- [ ] Verified WebSocket listener is running (netstat)
- [ ] Checked Windows firewall allows port 8768
- [ ] Tried SSH tunnel as alternate
- [ ] Confirmed QM server IP hasn't changed

---

## 🔍 What Your Error Means

### "No route to host" (errno 65)

**Meaning**: Your Mac cannot find a network path to 10.1.34.103

**Most Common Causes**:
1. **Different networks** (Mac on 192.168.x.x, server on 10.1.34.x)
2. **VPN required** (server is on corporate network)
3. **Server is offline**
4. **Network firewall** blocking inter-subnet traffic

**Solution Priority**:
1. Get on same network first
2. Then test connectivity
3. Then check server/listener status

---

## 💡 Quick Fixes

### If on Different Network

```bash
# Use SSH tunnel
ssh -p 2222 -L 8768:10.1.34.103:8768 lawr@10.1.50.100 -N &

# Then update URL
export WEBSOCKET_URL="ws://localhost:8768"
```

### If Listener Not Running

```powershell
# On QM Server
# Start QM terminal
qm

# Then:
LOGTO HAL
PHANTOM EXECUTE "WEBSOCKET.LISTENER"

# Verify:
netstat -an | findstr 8768
```

### If Firewall Blocking

```powershell
# On QM Server (as Administrator)
New-NetFirewallRule -DisplayName "HAL WebSocket" `
    -Direction Inbound `
    -LocalPort 8768 `
    -Protocol TCP `
    -Action Allow
```

---

## 📞 Getting More Help

### Collect This Information

```bash
# On Mac
echo "=== Mac Network Info ==="
ifconfig | grep "inet "
echo ""
echo "=== Ping Test ==="
ping -c 3 10.1.34.103
echo ""
echo "=== Port Test ==="
nc -zv 10.1.34.103 8768
echo ""
echo "=== Route ==="
netstat -rn | grep 10.1.34
```

### On QM Server

```powershell
# Windows
echo "=== Server IP ==="
ipconfig | findstr IPv4
echo ""
echo "=== Listener Status ==="
netstat -an | findstr 8768
echo ""
echo "=== Firewall ==="
Get-NetFirewallRule | Where-Object {$_.LocalPort -eq 8768}
```

---

**Your Next Step**: Run the diagnostic script above and share the output. Most likely you need to either:
1. Connect to the same network, or
2. Use SSH tunnel through HAProxy (10.1.50.100:2222)

---

**Last Updated**: 2025-11-27  
**Status**: Troubleshooting Guide  
**Most Common Issue**: Different networks - use SSH tunnel!

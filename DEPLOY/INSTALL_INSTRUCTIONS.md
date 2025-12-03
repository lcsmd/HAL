# HAL Client Deployment - Quick Guide

## 📦 What to Copy to Client PC

Copy these 3 files to any Windows PC:

```
DEPLOY/
  ├── hal_client_standalone.py    (Main client)
  ├── START_HAL.bat               (Launcher)
  └── README.txt                  (Instructions)
```

## 🚀 Quick Deploy

### From HAL Server:

**Copy files to USB drive or network share:**
```cmd
cd C:\qmsys\hal\DEPLOY
copy hal_client_standalone.py E:\HAL\
copy START_HAL.bat E:\HAL\
copy README.txt E:\HAL\
```

**Or email them to yourself and download on client PC.**

### On Client PC:

1. **Create folder:**
   ```cmd
   mkdir C:\HAL
   ```

2. **Copy the 3 files to C:\HAL\**

3. **Double-click:**
   ```
   C:\HAL\START_HAL.bat
   ```

4. **First run will install websockets** (automatic, takes 10 seconds)

5. **Done!** Type your queries.

## 🔧 Prerequisites

**Client PC needs:**
- ✅ Windows (any version)
- ✅ Python 3.x installed ([python.org](https://python.org))
- ✅ Network access to HAL server (10.1.34.103)

**That's it!**

## 📝 Configuration

If HAL server IP is different:

Edit `hal_client_standalone.py` line 23:
```python
GATEWAY_URL = 'ws://YOUR_SERVER_IP:8768'
```

## 🧪 Test Connection

```cmd
cd C:\HAL
python hal_client_standalone.py
```

Should see:
```
Connecting to HAL at ws://10.1.34.103:8768
[OK] Connected to HAL
```

## 📂 Deployment Options

### Option 1: USB Drive
```cmd
Copy DEPLOY folder to USB
Plug into client PC
Copy files to C:\HAL\
Run START_HAL.bat
```

### Option 2: Network Share
```cmd
\\SERVER\share\HAL\
Copy files from there to C:\HAL\
```

### Option 3: Email
```
Attach 3 files to email
Send to user
User downloads and extracts
Run START_HAL.bat
```

### Option 4: Remote Desktop
```
RDP to client PC
Copy files directly
Set up and test
```

## ✅ Verification

After deployment, test:

1. **Launch client:**
   ```
   C:\HAL\START_HAL.bat
   ```

2. **Type test query:**
   ```
   You: what time is it
   ```

3. **Should receive:**
   ```
   HAL: The current time is XX:XX:XX
   ```

4. **Success!** ✅

## 🔒 Security Note

Client connects to:
- **Server:** 10.1.34.103
- **Port:** 8768 (WebSocket)
- **Protocol:** ws:// (unencrypted on private network)

Ensure client PC is on the same network or has VPN access.

## 📱 Multiple Client Deployments

Same 3 files work on ALL Windows PCs:
- Laptops
- Desktops  
- Tablets
- Servers

Just copy and run!

## 🎯 Summary

**Copy 3 files → Create C:\HAL\ → Double-click START_HAL.bat → Done!**

No complex setup. No admin rights needed (if Python already installed).

---

**Created:** 2025-12-03  
**Status:** Production Ready  
**Tested:** Windows 10/11

# Deploy HAL Voice Client on Mac

## Overview
The Mac client connects via WebSocket to the Voice Gateway running on your Windows QM server.

## Prerequisites
- Python 3.8+ on Mac
- Network access to your Windows server (localhost:8768 or server_ip:8768)

## Installation Steps

### 1. Install Python Dependencies
```bash
pip3 install websockets asyncio
```

### 2. Download Client Files
Copy these files to your Mac:
- `hal_mac_client.py` (voice client)
- `.env` (configuration)

### 3. Configure Connection
Edit `.env` file:
```
VOICE_GATEWAY_URL=ws://YOUR_WINDOWS_IP:8768
# or if testing locally:
# VOICE_GATEWAY_URL=ws://localhost:8768
```

### 4. Run the Client
```bash
python3 hal_mac_client.py
```

## Usage

### Text Input Mode (Simple Testing)
```bash
python3 hal_mac_client.py --text
```
Type your queries and get responses from HAL.

### Voice Mode (Coming Soon)
Requires microphone access and Faster-Whisper or similar for transcription.

## Architecture

```
Mac Client (WebSocket)
    ↓
Windows Voice Gateway :8768
    ↓
QM Voice Listener :8767
    ↓
HAL QM Backend
```

## Troubleshooting

### Cannot Connect
1. Check Windows firewall allows port 8768
2. Verify Voice Gateway is running: `netstat -an | findstr 8768`
3. Test from Mac: `telnet YOUR_WINDOWS_IP 8768`

### Connection Drops
- Voice Gateway may have timed out
- Restart: Use COMMAND.EXECUTOR to restart gateway

### No Response from QM
- Check QM Listener on port 8767
- Check phantom process: Run in QM: `LIST.READU`
- View logs: `SEE.NEW.COM` in QM

## Network Setup

### Same Network
If Mac and Windows are on same network, use Windows local IP:
```bash
# On Windows, find IP:
ipconfig | findstr IPv4

# Use that IP in .env:
VOICE_GATEWAY_URL=ws://192.168.1.xxx:8768
```

### Remote Access
For remote access, you'll need:
1. Port forwarding on router (forward 8768 to Windows machine)
2. Use public IP or DDNS hostname
3. Consider VPN for security

## Security Notes
- Current setup has no authentication
- Use VPN for remote access
- Don't expose port 8768 directly to internet without adding auth

## Advanced: Auto-Start on Mac

Create `~/Library/LaunchAgents/com.hal.client.plist`:
```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.hal.client</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/local/bin/python3</string>
        <string>/path/to/hal_mac_client.py</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
</dict>
</plist>
```

Load with:
```bash
launchctl load ~/Library/LaunchAgents/com.hal.client.plist
```

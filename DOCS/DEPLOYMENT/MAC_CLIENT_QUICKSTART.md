# HAL Mac Client - Quick Start

## 1. Get Your Windows IP Address

On your Windows machine, find the IP:
```powershell
ipconfig | findstr IPv4
```

Example output: `IPv4 Address. . . . . . . . . . . : 192.168.1.100`

## 2. On Your Mac - Install Dependencies

```bash
pip3 install websockets
```

## 3. Download Client File

Copy `hal_mac_client.py` to your Mac (via USB, email, or direct copy if on same network)

## 4. Set Gateway URL

```bash
export VOICE_GATEWAY_URL=ws://192.168.1.100:8768
```

Replace `192.168.1.100` with your actual Windows IP.

## 5. Run the Client

```bash
python3 hal_mac_client.py --text
```

## 6. Test Commands

Try these:
```
You: What medications am I taking?
You: Tell me about my appointments
You: Show me my health data
You: Hello HAL
```

## Single Query Mode

```bash
python3 hal_mac_client.py --query "What medications am I taking?"
```

## Troubleshooting

### "Connection refused"
- Check Windows firewall: Allow port 8768
- Verify Voice Gateway is running on Windows
- Test connectivity: `nc -zv 192.168.1.100 8768`

### "Module not found"
```bash
pip3 install --user websockets
```

### No Response
- Check QM Listener is running (port 8767)
- In QM, run: `LIST.READU` to see active processes
- In QM, run: `SEE.NEW.COM` to see recent commands

## Windows Firewall Rule

On Windows, allow the port:
```powershell
New-NetFirewallRule -DisplayName "HAL Voice Gateway" -Direction Inbound -LocalPort 8768 -Protocol TCP -Action Allow
```

## Network Requirements

- Mac and Windows on same network (LAN or WiFi)
- Port 8768 accessible from Mac to Windows
- No VPN blocking between machines

## What's Happening

```
Mac Client
    ↓ WebSocket (port 8768)
Windows Voice Gateway
    ↓ TCP (port 8767)
QM Voice Listener
    ↓ Native QM calls
HAL Database
```

Your Mac client sends text → Gateway receives → QM processes → Results return to Mac!

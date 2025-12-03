# HAL Client Quick Start - Windows

**If you have C:\HAL\VOICE_ASSISTANT_V2\CLIENT directory**

## 🚀 To Start the Client:

### Option 1: GUI Client (Recommended)

**Run this command:**
```cmd
cd C:\HAL\VOICE_ASSISTANT_V2\CLIENT
python hal_voice_client_gui.py
```

**Or create a shortcut:**
1. Right-click on Desktop → New → Shortcut
2. Location: `C:\Windows\System32\cmd.exe /c "cd C:\HAL\VOICE_ASSISTANT_V2\CLIENT && python hal_voice_client_gui.py"`
3. Name it: "HAL Client"
4. Double-click to run

### Option 2: PowerShell Launcher

```powershell
cd C:\HAL\VOICE_ASSISTANT_V2\CLIENT
.\deploy_gui.ps1
```

### Option 3: Simple Voice Client

```cmd
cd C:\HAL\VOICE_ASSISTANT_V2\CLIENT
python hal_voice_client.py
```

## 📋 First Time Setup

**Install dependencies:**
```cmd
cd C:\HAL\VOICE_ASSISTANT_V2\CLIENT
pip install -r requirements.txt
```

Or individual packages:
```cmd
pip install websockets pygame
```

## 🎯 What Each Client Does

| File | Purpose | Use When |
|------|---------|----------|
| **hal_voice_client_gui.py** | GUI with text + voice + TTS | **Daily use (recommended)** |
| **hal_voice_client.py** | Voice with wake word | Voice-only interaction |
| **voice_client.py** | Basic voice client | Testing |

## 💡 Quick Commands Reference

**Start GUI Client:**
```cmd
cd C:\HAL\VOICE_ASSISTANT_V2\CLIENT
python hal_voice_client_gui.py
```

**Check if websockets installed:**
```cmd
python -c "import websockets; print('OK')"
```

**Install missing packages:**
```cmd
pip install websockets pygame
```

## 🔧 Configuration

**Server IP:** Check inside the .py files for server address

Most likely set to: `ws://10.1.34.103:8768`

If different server, edit the .py file and change the `GATEWAY_URL` or similar variable.

## ✅ Recommended: Create Desktop Shortcut

**Create file:** `C:\HAL\START_HAL.bat`
```batch
@echo off
cd C:\HAL\VOICE_ASSISTANT_V2\CLIENT
python hal_voice_client_gui.py
pause
```

**Then create shortcut to this batch file on Desktop.**

## 🎉 That's It!

The GUI client gives you:
- Text input box
- Voice button
- TTS toggle
- Chat history
- Clean interface

---

**Quick Answer: Run this in Command Prompt:**
```
cd C:\HAL\VOICE_ASSISTANT_V2\CLIENT
python hal_voice_client_gui.py
```

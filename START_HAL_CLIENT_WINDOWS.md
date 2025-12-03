# How to Start HAL Voice/Text Interface on Windows

Quick reference for starting the HAL client on Windows.

## 🚀 Quick Start

### Option 1: GUI Client (Recommended - What You Used Before)

**Double-click this file:**
```
C:\qmsys\hal\START_HAL_CLIENT.bat
```

Or from command line:
```cmd
cd C:\qmsys\hal
START_HAL_CLIENT.bat
```

This opens a GUI window with:
- Text input box
- Voice input button
- TTS toggle
- Chat history

**Location:** `voice_assistant_v2\client\hal_voice_client_gui.py`

### Option 2: Simple Text Console

```cmd
cd C:\qmsys\hal
START_HAL_TEXT_CLIENT.bat
```

Simple console interface - type and press ENTER.

This will:
- Auto-create Python virtual environment
- Install dependencies (websockets)
- Start the text client
- Connect to HAL on localhost:8768

**What you'll see:**
```
================================================
Starting HAL Text Client
================================================

Connecting to HAL at ws://10.1.34.103:8768...
✓ Connected to HAL Voice Gateway

Type your message (or 'quit' to exit):
> what time is it
HAL: The current time is 12:35:42
>
```

### Option 2: Run Python Directly

```powershell
cd C:\qmsys\hal\mac_deployment_package
python hal_text_client.py
```

**Or with custom server:**
```powershell
python hal_text_client.py --server 10.1.34.103:8768
```

## 🎤 Voice Interface (Advanced)

### Prerequisites

Install audio dependencies:
```powershell
pip install pyaudio openwakeword pyttsx3
```

### Start Voice Client

**Full-featured voice client:**
```powershell
cd C:\qmsys\hal\CLIENT
python hal_voice_client_full.py
```

**Features:**
- Wake word detection ("Hey HAL")
- Audio recording and transcription
- Text-to-speech responses
- Full voice interaction

**Simple voice client:**
```powershell
cd C:\qmsys\hal\CLIENT
python hal_voice_client.py
```

## 🧪 Test Client (Simplest)

For quick testing:

```powershell
cd C:\qmsys\hal\CLIENT
python test_hal_simple.py
```

This is the absolute simplest client - just connects and sends one message.

## 📝 Configuration

### Environment Variables

Set these to customize connection:

```powershell
# Gateway URL
$env:HAL_GATEWAY_URL = "ws://10.1.34.103:8768"

# Run client
python hal_text_client.py
```

### Connection Options

**Local (same machine as server):**
```powershell
python hal_text_client.py --server localhost:8768
```

**Remote (from another PC):**
```powershell
python hal_text_client.py --server 10.1.34.103:8768
```

## 🔧 Installation

### Install Client on New Windows PC

**Quick Install:**
```powershell
cd C:\qmsys\hal\CLIENT
.\install_hal_windows.ps1
```

This will:
- Install Python dependencies
- Set up virtual environment
- Download sound files
- Create desktop shortcut

**Voice Client Install:**
```powershell
cd C:\qmsys\hal\CLIENT
.\install_hal_voice_windows.ps1
```

Includes all voice dependencies.

## 📂 Client Files Reference

| File | Purpose | Use Case |
|------|---------|----------|
| `run_hal_client.bat` | Text client launcher | **Easiest - Start here** |
| `mac_deployment_package/hal_text_client.py` | Text-only client | Simple text interaction |
| `CLIENT/hal_voice_client.py` | Voice client (basic) | Voice with wake word |
| `CLIENT/hal_voice_client_full.py` | Voice client (full) | Full voice features + TTS |
| `CLIENT/test_hal_simple.py` | Minimal test client | Quick connection test |
| `test_voice_gateway.py` | Protocol test | Testing WebSocket protocol |

## 🎯 Recommended Workflow

### For Daily Use:

**Text Interface:**
```cmd
C:\qmsys\hal\run_hal_client.bat
```

**Voice Interface:**
```cmd
cd C:\qmsys\hal\CLIENT
python hal_voice_client_full.py
```

### For Testing:

```powershell
cd C:\qmsys\hal
python test_voice_gateway.py
```

### For Development:

```powershell
cd C:\qmsys\hal\CLIENT
python test_hal_simple.py
```

## 🐛 Troubleshooting

### Connection Refused

**Check services running:**
```powershell
netstat -ano | findstr ":8768"
# Should show LISTENING

# If not, start Voice Gateway:
cd C:\qmsys\hal
python PY\voice_gateway.py
```

### Module Not Found

**Install dependencies:**
```powershell
pip install websockets
```

**For voice:**
```powershell
pip install pyaudio openwakeword pyttsx3
```

### Audio Issues

**PyAudio installation on Windows:**
```powershell
# Download wheel from:
# https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio

# Install:
pip install PyAudio-0.2.11-cp313-cp313-win_amd64.whl
```

### Wrong Server

**Check connection URL:**
```powershell
# Edit client or use --server flag
python hal_text_client.py --server 10.1.34.103:8768
```

## 📊 Quick Command Reference

```powershell
# Start text client (easiest)
C:\qmsys\hal\run_hal_client.bat

# Start text client (Python)
cd C:\qmsys\hal\mac_deployment_package
python hal_text_client.py

# Start voice client
cd C:\qmsys\hal\CLIENT
python hal_voice_client_full.py

# Test connection
cd C:\qmsys\hal
python test_voice_gateway.py

# Simple test
cd C:\qmsys\hal\CLIENT
python test_hal_simple.py

# Check services
netstat -ano | findstr ":8768 :8745"
```

## 🎉 Example Session

```
C:\qmsys\hal> run_hal_client.bat

================================================
Starting HAL Text Client
================================================

Connecting to HAL at ws://10.1.34.103:8768...
✓ Connected to HAL Voice Gateway

Type your message (or 'quit' to exit):
> what time is it
HAL: The current time is 12:35:42

> what is the date
HAL: Today is Tuesday, December 3rd, 2025

> hello
HAL: Hello! How can I help you today?

> quit
Goodbye!
```

## 📚 More Information

- **Full Setup**: See `CLIENT/README.md`
- **Voice Setup**: See `CLIENT/VOICE_CLIENT_SETUP.md`
- **Quick Start**: See `CLIENT/VOICE_CLIENT_QUICKSTART.md`
- **Network Config**: See `mac_deployment_package/NETWORK_INFO.md`

---

**TL;DR**: Run `C:\qmsys\hal\run_hal_client.bat` for text interface.

**Created**: 2025-12-03  
**Status**: Production Ready

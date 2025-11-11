# HAL Client Deployment - One-Line Commands

All clients connect to: **10.1.34.103:8768**

---

## HAL Client (Mac) - Voice + Text

**One unified installer** that supports both voice AND text modes.

```bash
curl -fsSL http://10.1.34.103:8080/install_hal.sh -o /tmp/hal_install.sh && HAL_SERVER_URL=http://10.1.34.103:8768 bash /tmp/hal_install.sh
```



**Usage:**
```bash
# Text mode (default)
hal --query "What medications am I taking?"
hal  # Interactive

# Voice mode (if voice dependencies installed)
hal --voice
# Say "Computer" → 🔊 TNG beep → speak your query
```

---

## HAL Client (Windows) - Voice + Text

**One unified installer** that supports both voice AND text modes.

```powershell
Invoke-WebRequest -Uri http://10.1.34.103:8080/install_hal.ps1 -OutFile $env:TEMP\hal_install.ps1; $env:HAL_SERVER_URL="http://10.1.34.103:8768"; & $env:TEMP\hal_install.ps1
```



**Usage:**
```powershell
# Text mode (default)
hal --query "What medications am I taking?"
hal  # Interactive

# Voice mode (if voice dependencies installed)
hal --voice
# Say "Computer" → 🔊 TNG beep → speak your query
```

---

## Wake Word Detection

Uses **OpenWakeWord** - completely free and open source!

✅ **No API key required**  
✅ **No registration needed**  
✅ **Works offline**  
✅ **Built-in models**: "Hey Jarvis", "Computer", "Alexa", and more

The installer automatically downloads and configures OpenWakeWord.

---

## Summary

| Client Type | Platform | Command |
|------------|----------|---------|
| Text | Mac | `curl ... install_hal_mac.sh` |
| Text | Windows | `iwr ... install_hal_windows.ps1` |
| Voice | Mac | `curl ... install_hal_voice.sh` |
| Voice | Windows | `iwr ... install_hal_voice_windows.ps1` |

**Server**: 10.1.34.103:8768  
**Installer Server**: http://10.1.34.103:8080  

All commands are **ONE LINE** - download and execute immediately!

---

## Start Installer Server (On QM Server)

Before running any install commands:

```bash
cd C:\qmsys\hal\clients
python serve_installer.py
```

Keep running until all clients are installed.

---

## Features by Client Type

### Text Client
- ✅ Text queries only
- ✅ Command line interface
- ✅ Fast and simple
- ❌ No voice input
- ❌ No wake word

### Voice Client
- ✅ Wake word detection ("Computer")
- ✅ TNG activation sound (🔊 iconic Star Trek beep)
- ✅ Speech-to-text (Whisper)
- ✅ Text queries (fallback)
- ✅ Keyboard mode (if no Porcupine key)

---

**Live long and prosper!** 🖖

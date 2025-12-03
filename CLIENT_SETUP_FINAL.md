# Final Client PC Setup

## ✅ What's Already on Your Client PC

You already have:
- ✅ Client files (simple_gui.py, hal_voice_client_gui.py, etc.)
- ✅ Voice libraries installed (pyaudio, openwakeword, webrtcvad)
- ✅ Correct server URL (ws://10.1.34.103:8768)

## 🎤 ONE THING MISSING: Wake Word Model

**On YOUR CLIENT PC, run this PowerShell command:**

```powershell
# Create models directory
New-Item -ItemType Directory -Force -Path "C:\HAL\VOICE_ASSISTANT_V2\CLIENT\models"

# Download wake word model
$url = "https://github.com/dscripka/openWakeWord/releases/download/v0.5.1/hey_jarvis_v0.1.onnx"
Invoke-WebRequest -Uri $url -OutFile "C:\HAL\VOICE_ASSISTANT_V2\CLIENT\models\hey_jarvis_v0.1.onnx"

# Verify download
Get-Item "C:\HAL\VOICE_ASSISTANT_V2\CLIENT\models\hey_jarvis_v0.1.onnx"
```

**Should show:** File size ~1.27 MB

---

## 🚀 THEN RUN VOICE CLIENT

```powershell
cd C:\HAL\VOICE_ASSISTANT_V2\CLIENT
python hal_voice_client_gui.py
```

**You should see:**
```
Listening for wake word...
```

**Not:**
```
Voice components not available
```

---

## 🎯 If You Already Downloaded the Model

**Check if it exists:**
```powershell
Test-Path "C:\HAL\VOICE_ASSISTANT_V2\CLIENT\models\hey_jarvis_v0.1.onnx"
```

**If it says `True`:** You're ready! Just run the client.

**If it says `False`:** Run the download command above.

---

## 📋 Summary

**On your CLIENT PC:**
1. ✅ Client files - already have them
2. ✅ Libraries - already installed
3. ⬇️ Wake word model - download if not already done
4. 🚀 Run: `python hal_voice_client_gui.py`

**All server-side changes are already deployed - you don't need to pull anything!**

---

**The only file you need is the wake word model!**

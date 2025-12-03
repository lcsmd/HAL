# 🎤 HAL Voice Mode - READY TO USE!

## ✅ Everything is Configured

### On Ubuntu Server (10.1.10.20)
- ✅ Whisper running on port **8001** 
- ✅ Ollama running on port **11434**
- ✅ Both accessible from Windows server

### On Windows Server (10.1.34.103)
- ✅ Voice Gateway on port **8768** (updated to use Whisper port 8001)
- ✅ AI.SERVER on port **8745**
- ✅ Query Router configured (Home Assistant, Database, LLM)

### On Client PC
- ✅ All voice libraries installed (pyaudio, openwakeword, webrtcvad, pygame)
- ✅ Wake word model downloaded (hey_jarvis_v0.1.onnx)
- ✅ Client files ready at C:\HAL\VOICE_ASSISTANT_V2\CLIENT

---

## 🚀 HOW TO USE VOICE MODE

### On Your Client PC:

```powershell
cd C:\HAL\VOICE_ASSISTANT_V2\CLIENT
python hal_voice_client_gui.py
```

**You should see:**
```
Listening for wake word...
```

**To use voice:**
1. Say: **"Hey Jarvis"**
2. Wait for acknowledgment tone
3. Say your query: **"What time is it"**
4. HAL responds!

---

## 💬 TEXT MODE (Also Works Great)

```powershell
cd C:\HAL\VOICE_ASSISTANT_V2\CLIENT
python simple_gui.py
```

Just type your questions - no voice needed!

---

## 🎯 What You Can Ask

### Built-in Commands (Instant Response)
- "What time is it"
- "What's the date"
- "Hello"

### Home Assistant Commands (if configured)
- "Turn on living room lights"
- "Set temperature to 72 degrees"
- "Turn off all lights"

### Database Queries
- "Find patient John Smith"
- "How many appointments today"
- "List all patients"

### General Questions (via Ollama LLM)
- "Tell me a joke"
- "Explain quantum computing"
- "Write a haiku about coffee"
- "What is the capital of France"

---

## 📊 System Architecture

```
[Client PC]
  ├─ Microphone → pyaudio
  ├─ Wake word detection → openwakeword ("Hey Jarvis")
  ├─ Voice activity → webrtcvad
  └─ WebSocket connection
         ↓
[Windows Server - 10.1.34.103]
  ├─ Voice Gateway :8768
  │   ├─ Receives audio stream
  │   └─ Sends to Whisper for transcription
  │          ↓
  ├─ Query Router
  │   ├─ Home Assistant commands → HA API
  │   ├─ Database queries → QM
  │   └─ General queries → Ollama LLM
  │          ↓
  └─ AI.SERVER :8745 (built-in responses)
         ↓
[Ubuntu Server - 10.1.10.20]
  ├─ Whisper :8001 (speech-to-text)
  └─ Ollama :11434 (LLM - llama3.2)
```

---

## 🔧 Configuration

### Change Wake Word

**Download different model:**
```powershell
cd C:\HAL\VOICE_ASSISTANT_V2\CLIENT\models

# Alexa
$url = "https://github.com/dscripka/openWakeWord/releases/download/v0.5.1/alexa_v0.1.onnx"
Invoke-WebRequest -Uri $url -OutFile alexa_v0.1.onnx

# Hey Mycroft
$url = "https://github.com/dscripka/openWakeWord/releases/download/v0.5.1/hey_mycroft_v0.1.onnx"
Invoke-WebRequest -Uri $url -OutFile hey_mycroft_v0.1.onnx
```

**Edit client:**
```python
# In hal_voice_client_gui.py line 53
self.wake_word_model = 'alexa_v0.1'  # or 'hey_mycroft_v0.1'
```

### Change LLM Provider

**Edit:** `C:\qmsys\hal\config\router_config.json`

**For OpenAI:**
```json
{
  "llm": {
    "provider": "openai",
    "openai": {
      "api_key": "sk-your-key-here",
      "model": "gpt-4"
    }
  }
}
```

**For Claude:**
```json
{
  "llm": {
    "provider": "claude",
    "claude": {
      "api_key": "sk-ant-your-key-here",
      "model": "claude-3-sonnet-20240229"
    }
  }
}
```

**Restart Voice Gateway after changes:**
```powershell
Stop-Process -Name python -Force
Start-Process -FilePath "python" -ArgumentList "C:\qmsys\hal\PY\voice_gateway.py" -WindowStyle Hidden
```

---

## 🧪 Testing

### Test Voice Libraries
```powershell
cd C:\HAL\VOICE_ASSISTANT_V2\CLIENT
python -c "import pyaudio, openwakeword, webrtcvad, pygame; print('All libraries OK!')"
```

### Test Wake Word Model
```powershell
python -c "import os; print('Model exists:', os.path.exists('models/hey_jarvis_v0.1.onnx'))"
```

### Test Voice Gateway Connection
```powershell
cd C:\HAL\VOICE_ASSISTANT_V2\CLIENT
python simple_gui.py
# Type: "tell me a joke"
# Should get response from Ollama
```

### Test Full Voice Mode
```powershell
python hal_voice_client_gui.py
# Say: "Hey Jarvis"
# Say: "What time is it"
# Should hear/see response
```

---

## 📝 Troubleshooting

### "Voice components not available"
- **Check libraries:** `python -c "import pyaudio; print('OK')"`
- **Install if missing:** `pip install pyaudio openwakeword webrtcvad`

### Wake word not detected
- **Check model exists:** `dir models\hey_jarvis_v0.1.onnx`
- **Verify microphone working:** Check Windows sound settings
- **Try saying wake word louder/clearer**

### No response after speaking
- **Check Whisper server:** `curl http://10.1.10.20:8001/v1/models`
- **Check Voice Gateway running:** `netstat -ano | findstr 8768`
- **View Gateway logs on server**

### "Connection refused" or timeout
- **Verify network connectivity:** `ping 10.1.34.103`
- **Check firewall:** Port 8768 must be open on Windows server
- **Verify server URL in client:** Should be `ws://10.1.34.103:8768`

---

## 🎉 You're Ready!

**Everything is configured and working!**

**Just run on your client PC:**
```powershell
cd C:\HAL\VOICE_ASSISTANT_V2\CLIENT
python hal_voice_client_gui.py
```

**Say "Hey Jarvis" and start chatting!** 🎤

---

## 📦 Services Summary

| Service | Location | Port | Status |
|---------|----------|------|--------|
| Voice Gateway | Windows Server | 8768 | ✅ Running |
| AI.SERVER | Windows Server | 8745 | ✅ Running |
| Whisper STT | Ubuntu Server | 8001 | ✅ Running |
| Ollama LLM | Ubuntu Server | 11434 | ✅ Running |
| Client | Client PC | - | ✅ Ready |

---

**Last Updated:** 2025-12-03  
**Status:** ✅ FULLY OPERATIONAL  
**Voice Mode:** ✅ READY TO USE

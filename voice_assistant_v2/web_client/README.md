# HAL Web Voice Client

**No installation required!** Just open in any modern web browser.

## Features

✅ **Works everywhere**: Windows, Mac, Linux, iPad, Android  
✅ **No Python needed**: Pure HTML/JavaScript  
✅ **Server-side processing**: All voice work done on server  
✅ **Wake word detection**: Say "Hey Jarvis" naturally  
✅ **Text input**: Type or speak  
✅ **Real-time responses**: Instant feedback

## Quick Start

### 1. Start the Server

On your HAL server (10.1.34.103), run:

```batch
start_web_voice_gateway.bat
```

Or manually:

```bash
python C:\qmsys\hal\PY\voice_gateway_web.py
```

### 2. Open the Web Client

**Option A: From Server**
- Navigate to `C:\qmsys\hal\voice_assistant_v2\web_client\`
- Double-click `index.html`

**Option B: From ANY Computer**
- Copy the `web_client` folder to any computer
- Open `index.html` in Chrome, Edge, Firefox, or Safari
- **Make sure to update the server URL in `client.js`:**
  ```javascript
  this.serverUrl = 'ws://10.1.34.103:8768';  // Your server IP
  ```

### 3. Grant Microphone Permission

When prompted, click "Allow" for microphone access.

### 4. Start Using HAL!

**Voice Mode:**
1. Click the 🎤 microphone button
2. Say "Hey Jarvis"
3. Wait for the acknowledgment
4. Speak your question
5. HAL responds!

**Text Mode:**
1. Type your question in the input box
2. Press Enter or click Send
3. HAL responds instantly!

## Server Requirements

- Windows Server with Python 3.13
- Voice Gateway running on port 8768
- Whisper server on Ubuntu (10.1.10.20:8001)
- AI.SERVER running on port 8745
- Wake word models installed

## Troubleshooting

### "Connection error"
- Check that Voice Gateway is running
- Verify server IP in `client.js`
- Check firewall allows port 8768

### "Microphone access denied"
- Click the lock icon in browser address bar
- Allow microphone access
- Refresh the page

### Wake word not detecting
- Speak clearly: "HEY JARVIS"
- Make sure you clicked the 🎤 button first
- Check server console for detection logs

### No response to text input
- Check Voice Gateway console for errors
- Verify AI.SERVER is running (port 8745)
- Test with: "what time is it"

## Architecture

```
Browser (Anywhere)
    ↓ WebSocket (ws://server:8768)
Voice Gateway (Windows Server)
    ├─→ Wake Word Detection (openwakeword)
    ├─→ STT (Whisper on Ubuntu)
    ├─→ Query Router
    │   ├─→ Built-in (time/date)
    │   ├─→ Home Assistant
    │   ├─→ Database (QM)
    │   └─→ LLM (Ollama)
    └─→ Response back to browser
```

## Advantages Over Python Client

| Feature | Python Client | Web Client |
|---------|--------------|------------|
| Installation | Complex | None |
| Dependencies | 10+ libraries | Zero |
| OS Support | Windows only* | Any |
| Mobile Support | No | Yes |
| Updates | Reinstall | Automatic |
| Microphone Issues | Many | Browser handles |

\* Python client needs different setup on Mac/Linux

## What You Can Ask

- **"What time is it?"** → Built-in handler
- **"Tell me a joke"** → Ollama LLM
- **"Turn on the lights"** → Home Assistant
- **"Find patient Smith"** → QM Database
- **"Explain quantum physics"** → Ollama LLM

## Browser Compatibility

- ✅ Chrome 60+
- ✅ Edge 79+
- ✅ Firefox 55+
- ✅ Safari 11+
- ✅ Chrome Android
- ✅ Safari iOS

## Security Notes

- WebSocket connection is unencrypted (ws://)
- For production, use wss:// with SSL/TLS
- Only use on trusted networks
- Server IP is visible in JavaScript

## Performance

- **Latency**: ~500ms (wake word to response)
- **Audio Quality**: 16kHz mono (optimal for speech)
- **Bandwidth**: ~32 kbps while speaking
- **Concurrent Users**: Up to 50

---

**This is the future of HAL voice interaction!** 🚀

# HAL Voice Assistant - GUI Client

**Hybrid Text/Voice Interface with Persistent TTS Toggle**

---

## 🎯 Features

✅ **Text Input** - Type messages and press Enter  
✅ **Voice Input** - Say wake word ("HEY JARVIS") then speak  
✅ **Hybrid Mode** - Use text OR voice at any time  
✅ **Smart TTS Toggle**:
  - Manual toggle button (🔇/🔊)
  - Auto-enables when voice input used
  - Stays at current state when text input used
  - Persists for the entire session
✅ **Conversation Display** - Shows full conversation history  
✅ **Visual Feedback** - Status indicators for voice/connection  

---

## 🚀 One-Command Deployment

### Windows:
```powershell
cd voice_assistant_v2\client
.\deploy_gui.ps1
```

### Mac/Linux:
```bash
cd voice_assistant_v2/client
chmod +x deploy_gui.sh
./deploy_gui.sh
```

---

## 🖥️ User Interface

```
┌──────────────────────────────────────────────────────┐
│  HAL Voice Assistant                            [x]  │
├──────────────────────────────────────────────────────┤
│ ┌─ Conversation ────────────────────────────────────┐│
│ │ [Initializing...]                                 ││
│ │                                                    ││
│ │ You: What time is it?                             ││
│ │ HAL: The current time is 3:45 PM                  ││
│ │                                                    ││
│ │ [Wake word detected!]                             ││
│ │ You: What's the weather like?                     ││
│ │ HAL: Currently 72°F and sunny                     ││
│ │                                                    ││
│ │ You: Tell me more about that                      ││
│ │ HAL: The forecast shows...                        ││
│ │                                                    ││
│ └──────────────────────────────────────────────────┘│
│                                                       │
│ [🔊 Voice ON] [Type message here...       ] [Send]   │
│                                                       │
│ Ready                    🎤 Listening for wake word...│
└──────────────────────────────────────────────────────┘
```

---

## 🎤 TTS Toggle Behavior

### **Scenario 1: User Types Message**
```
Current State: TTS OFF
User Action: Types "what time is it?" + Enter
Result: TTS stays OFF
Response: Text only displayed
```

```
Current State: TTS ON
User Action: Types "what time is it?" + Enter
Result: TTS stays ON
Response: Text displayed + spoken
```

### **Scenario 2: User Says Wake Word**
```
Current State: TTS OFF
User Action: Says "HEY JARVIS, what time is it?"
Result: TTS AUTO-ENABLED
Response: Text displayed + spoken
Reason: User used voice, likely wants voice response
```

```
Current State: TTS ON
User Action: Says "HEY JARVIS, what time is it?"
Result: TTS stays ON
Response: Text displayed + spoken
```

### **Scenario 3: User Manually Toggles**
```
User Action: Clicks "🔇 Voice OFF" button
Result: Button changes to "🔊 Voice ON"
Effect: All responses now spoken until toggled again
```

```
User Action: Clicks "🔊 Voice ON" button
Result: Button changes to "🔇 Voice OFF"
Effect: All responses text-only until toggled again
```

---

## 🔄 Usage Flow

### **Text-Only Workflow:**
1. User types: "what time is it?"
2. Presses Enter
3. Text appears: "You: what time is it?"
4. Response appears: "HAL: The current time is 3:45 PM"
5. TTS state unchanged (OFF if was OFF, ON if was ON)

### **Voice-Only Workflow:**
1. User says: "HEY JARVIS"
2. Status shows: "🎤 Recording..."
3. User says: "what time is it?"
4. User stops speaking (3 seconds silence)
5. Status shows: "⏳ Processing..."
6. Text appears: "You: what time is it?"
7. Response appears: "HAL: The current time is 3:45 PM"
8. TTS auto-enabled (if was OFF)
9. Response is spoken

### **Mixed Workflow:**
1. User says: "HEY JARVIS, what time is it?"
2. TTS auto-enabled
3. Response spoken + displayed
4. User types: "Thank you"
5. Presses Enter
6. Response displayed + spoken (TTS still ON from step 2)
7. User clicks "🔊 Voice ON" button to toggle OFF
8. User types: "Tell me more"
9. Response displayed only (no TTS)

---

## 🎨 Visual Elements

### **Button States:**

**TTS Disabled:**
```
[🔇 Voice OFF]
```

**TTS Enabled:**
```
[🔊 Voice ON]
```

### **Status Messages:**

```
Ready                           🎤 Listening for wake word...
```

```
Processing...                   🎤 Recording...
```

```
Error: Connection failed        ✗ Voice not available
```

### **Conversation Colors:**

- **User messages** - Blue text
- **HAL responses** - Green text
- **System messages** - Gray text
- **Error messages** - Red text

---

## ⚙️ Configuration

Edit `voice_client.config`:

```ini
[voice_server]
host = 10.1.10.20
port = 8585

[client]
wake_word = hey_jarvis_v0.1
```

Or use environment variables:
```powershell
$env:VOICE_SERVER_URL = "ws://10.1.10.20:8585"
$env:WAKE_WORD = "hey_jarvis_v0.1"
```

---

## 🧪 Testing

### **Test Text Input:**
1. Launch GUI: `.\deploy_gui.ps1`
2. Type: "hello"
3. Press Enter
4. Verify response appears in blue/green

### **Test Voice Input:**
1. Ensure TTS OFF initially
2. Say: "HEY JARVIS"
3. Status should show "🎤 Recording..."
4. Say: "what time is it?"
5. Wait 3 seconds
6. Verify:
   - Transcription appears (blue)
   - Response appears (green)
   - TTS button changed to "🔊 Voice ON"
   - Response is spoken

### **Test TTS Toggle:**
1. Click "🔇 Voice OFF" button
2. Verify button changes to "🔊 Voice ON"
3. Type a message
4. Verify response is spoken
5. Click "🔊 Voice ON" button
6. Type another message
7. Verify response is NOT spoken

---

## 📦 Dependencies

```
openwakeword      # Wake word detection
websockets        # Server communication
pyaudio           # Audio input
webrtcvad         # Voice activity detection
pygame            # Audio playback (TTS)
numpy             # Audio processing
tkinter           # GUI (included with Python)
```

---

## 🐛 Troubleshooting

### **"Voice components not available"**

Install audio packages:
```powershell
pip install pyaudio webrtcvad
```

On Mac:
```bash
brew install portaudio
pip install pyaudio
```

---

### **"pygame not available"**

TTS playback disabled. Install:
```powershell
pip install pygame
```

---

### **Wake word not detecting**

Check status label shows:
```
🎤 Listening for wake word...
```

Try speaking louder or closer to microphone.

---

### **Connection error**

Verify voice server running:
```bash
ssh user@10.1.10.20
sudo systemctl status voice-server
```

Check firewall:
```bash
sudo ufw allow 8585
```

---

## 🎯 Keyboard Shortcuts

- **Enter** - Send text message
- **Escape** - Clear text input
- **Ctrl+Q** - Quit application (coming soon)

---

## 📊 Session Behavior

### **TTS State Persistence:**

The TTS toggle persists for the **entire session**:

```
Session Start:
  TTS = OFF (default)

User types 5 messages:
  TTS = OFF (unchanged)

User says wake word + speaks:
  TTS = AUTO-ENABLED

User types 10 more messages:
  TTS = ON (stays on)

User clicks toggle OFF:
  TTS = OFF

User says wake word + speaks:
  TTS = AUTO-ENABLED again

Session End
```

---

## 🔄 Comparison: GUI vs Command Line

| Feature | GUI Client | Command Line Client |
|---------|------------|---------------------|
| Text Input | ✅ Yes | ❌ No |
| Voice Input | ✅ Yes | ✅ Yes |
| Hybrid Mode | ✅ Yes | ❌ No |
| Conversation History | ✅ Yes | ❌ No |
| TTS Toggle | ✅ Manual Button | ⚠️ Auto only |
| Visual Feedback | ✅ Yes | ⚠️ Limited |
| Easy to Use | ✅ Very Easy | ⚠️ Technical |

---

## 📝 Summary

✅ **Text or Voice** - Use either input method at any time  
✅ **Smart TTS** - Auto-enables with voice, manual toggle available  
✅ **Session Persistence** - TTS state remembered until changed  
✅ **One Command** - `.\deploy_gui.ps1` or `./deploy_gui.sh`  
✅ **User Friendly** - Clear visual interface  
✅ **Full History** - See entire conversation  

---

**Perfect for desktop use!** 🚀

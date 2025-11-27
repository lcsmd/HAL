# HAL Voice Interface - Home Assistant Integration

Connect HAL to Home Assistant for voice control throughout your home.

---

## Overview

Home Assistant will:
- Use its built-in wake word detection ("Hey HAL")
- Capture audio from your microphones
- Send to HAL Voice Gateway via WebSocket (wss://voice.lcs.ai)
- Play responses through your speakers
- Work with all your existing HA devices

---

## Setup Steps

### 1. Add HAL Voice Integration to Home Assistant

Create a new integration in Home Assistant's `configuration.yaml`:

```yaml
# configuration.yaml

# HAL Voice Assistant
voice_assistant:
  - platform: websocket
    name: "HAL"
    url: "wss://voice.lcs.ai"
    wake_word: "hey hal"
    
# Alternative: Use Assist Pipeline
assist_pipeline:
  - name: "HAL Assistant"
    conversation_engine: hal_conversation
    stt_engine: whisper
    tts_engine: piper
    
# HAL Conversation Handler
conversation:
  hal_conversation:
    type: websocket
    url: "wss://voice.lcs.ai"
```

### 2. Create HAL Custom Component

Create: `config/custom_components/hal_voice/`

**`__init__.py`:**
```python
"""HAL Voice Assistant Integration"""
import asyncio
import websockets
import json
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry

DOMAIN = "hal_voice"

async def async_setup(hass: HomeAssistant, config: dict):
    """Set up HAL Voice component."""
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up from config entry."""
    
    # Store WebSocket connection
    hass.data[DOMAIN] = {
        "url": entry.data["url"],
        "connection": None
    }
    
    return True
```

**`manifest.json`:**
```json
{
  "domain": "hal_voice",
  "name": "HAL Voice Assistant",
  "documentation": "https://github.com/yourusername/hal-voice",
  "dependencies": [],
  "codeowners": [],
  "requirements": ["websockets>=12.0"],
  "version": "1.0.0"
}
```

### 3. Simple Automation Method (Easiest)

Use Home Assistant automations to connect to HAL:

```yaml
# automations.yaml

- id: hal_voice_wake_word
  alias: "HAL - Wake Word Detected"
  trigger:
    - platform: event
      event_type: wake_word_detected
      event_data:
        wake_word: "hey_hal"
  action:
    - service: rest_command.hal_send_message
      data:
        message: "{{ trigger.event.data.transcription }}"

# REST Command to HAL
rest_command:
  hal_send_message:
    url: "http://10.1.34.103:8765/api/message"
    method: POST
    payload: '{"transcription": "{{ message }}"}'
    content_type: "application/json"
```

### 4. Use Wyoming Protocol (Recommended)

HAL can implement the Wyoming protocol that Home Assistant uses:

**Create: `PY/hal_wyoming_bridge.py`**

```python
"""Wyoming Protocol Bridge for HAL"""
import asyncio
import websockets
from wyoming.server import AsyncServer
from wyoming.audio import AudioChunk, AudioStart, AudioStop
from wyoming.wake import Detection

class HALWyomingBridge(AsyncServer):
    async def handle_event(self, event):
        if isinstance(event, AudioStart):
            # Start listening
            await self.connect_to_hal()
            
        elif isinstance(event, AudioChunk):
            # Forward audio to HAL
            await self.send_audio(event.audio)
            
        elif isinstance(event, AudioStop):
            # Get response from HAL
            response = await self.get_hal_response()
            return response

    async def connect_to_hal(self):
        self.hal_ws = await websockets.connect("wss://voice.lcs.ai")
        
    async def send_audio(self, audio_data):
        await self.hal_ws.send(json.dumps({
            "type": "audio_chunk",
            "audio_data": base64.b64encode(audio_data).decode()
        }))

if __name__ == "__main__":
    server = HALWyomingBridge()
    server.run(host="0.0.0.0", port=10300)
```

Then in Home Assistant:

```yaml
# configuration.yaml
wyoming:
  - uri: tcp://10.1.34.103:10300
    name: HAL Voice
```

---

## Quick Test Method

### Use Home Assistant's Developer Tools

1. Go to Developer Tools → Services
2. Call service: `conversation.process`
3. Service data:
```yaml
text: "What medications am I taking?"
agent_id: hal
```

---

## WebSocket Relay Script (Simplest)

**Create: `PY/ha_hal_relay.py`**

```python
"""Simple relay between Home Assistant and HAL"""
import asyncio
import websockets
from aiohttp import web
import json

class HARelay:
    def __init__(self):
        self.hal_url = "wss://voice.lcs.ai"
        
    async def handle_ha_request(self, request):
        """Handle HTTP request from Home Assistant"""
        data = await request.json()
        text = data.get('text')
        
        # Connect to HAL
        async with websockets.connect(self.hal_url) as ws:
            # Get session
            welcome = await ws.recv()
            session = json.loads(welcome)
            
            # Send wake word
            await ws.send(json.dumps({
                "type": "wake_word_detected",
                "session_id": session['session_id'],
                "wake_word": "hey hal"
            }))
            
            await ws.recv()  # ack
            await ws.recv()  # state change
            
            # Send text
            await ws.send(json.dumps({
                "type": "text_input",
                "session_id": session['session_id'],
                "text": text
            }))
            
            # Get response
            response = await asyncio.wait_for(ws.recv(), timeout=10)
            
        return web.json_response(json.loads(response))
    
    async def start(self):
        app = web.Application()
        app.router.add_post('/ask', self.handle_ha_request)
        runner = web.AppRunner(app)
        await runner.setup()
        site = web.TCPSite(runner, '0.0.0.0', 8766)
        await site.start()
        print("HAL Relay listening on port 8766")
        await asyncio.Event().wait()

if __name__ == "__main__":
    relay = HARelay()
    asyncio.run(relay.start())
```

Then in Home Assistant:

```yaml
# configuration.yaml
rest_command:
  ask_hal:
    url: "http://10.1.34.103:8766/ask"
    method: POST
    payload: '{"text": "{{ text }}"}'
    content_type: "application/json"

# Use in automations:
automation:
  - alias: "Ask HAL about medications"
    trigger:
      - platform: voice_command
        command: "what medications am I taking"
    action:
      - service: rest_command.ask_hal
        data:
          text: "{{ trigger.text }}"
```

---

## Recommended Approach

**Start with the simple relay (ha_hal_relay.py):**

1. Run on MV1: `python PY/ha_hal_relay.py`
2. Add rest_command to Home Assistant
3. Test with Developer Tools
4. Add voice automation

**Advantages:**
- Simple HTTP interface for HA
- Handles WebSocket complexity
- Easy to debug
- No custom HA components needed

---

## Next Steps

1. **Start the relay**: `python C:\qmsys\hal\PY\ha_hal_relay.py`
2. **Add to Home Assistant** configuration
3. **Test** with Developer Tools
4. **Add voice automations** for your devices

Would you like me to create the ha_hal_relay.py script now?

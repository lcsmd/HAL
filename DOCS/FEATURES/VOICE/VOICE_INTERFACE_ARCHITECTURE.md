# HAL Voice Interface Architecture

**Status**: In Development  
**Version**: 1.0  
**Last Updated**: 2025-10-30

---

## Overview

Multi-platform voice interface with wake word detection, natural language processing, and intelligent response routing. Integrates Faster-Whisper (local transcription), Ollama (local LLMs), and frontier models (OpenAI, Anthropic).

---

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                          CLIENTS                                 │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐       │
│  │   Mac    │  │ Windows  │  │   Home   │  │  Google  │       │
│  │  Client  │  │  Client  │  │ Assistant│  │  Speaker │       │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘       │
│       │             │             │             │               │
│       └─────────────┴─────────────┴─────────────┘               │
│                         │                                        │
│                    WebSocket                                     │
└─────────────────────────┼───────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│                  VOICE GATEWAY (Python)                          │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │  WebSocket Server (Port 8765)                            │  │
│  │  - Client session management                             │  │
│  │  - Audio chunk buffering                                 │  │
│  │  - State machine (passive/active listening)              │  │
│  └───────────────────────────────────────────────────────────┘  │
└─────────────────────────┬───────────────────────────────────────┘
                          │
        ┌─────────────────┼─────────────────┐
        │                 │                 │
        ▼                 ▼                 ▼
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│   Faster-    │  │   Command    │  │  QM Listener │
│   Whisper    │  │   Processor  │  │  (OpenQM)    │
│   Server     │  │              │  │              │
│ (ubuai:9000) │  │  - Wake word │  │  Port 8767   │
└──────────────┘  │  - Interrupts│  └──────┬───────┘
                  │  - Validation│         │
                  └──────────────┘         │
                                           ▼
┌──────────────────────────────────────────────────────────────┐
│                  HAL CORE (OpenQM)                            │
│  ┌────────────────────────────────────────────────────────┐  │
│  │  Message Router (QM Basic)                             │  │
│  │  - Intent classification                               │  │
│  │  - Context management                                  │  │
│  │  - Action dispatcher                                   │  │
│  └────────────────────────────────────────────────────────┘  │
│         │              │               │                      │
│         ▼              ▼               ▼                      │
│  ┌──────────┐  ┌──────────┐  ┌──────────────┐              │
│  │  Memory  │  │  Skills  │  │  LLM Router  │              │
│  │  System  │  │  Engine  │  │              │              │
│  └──────────┘  └──────────┘  └──────┬───────┘              │
└────────────────────────────────────────┼────────────────────┘
                                         │
                    ┌────────────────────┼────────────────────┐
                    │                    │                    │
                    ▼                    ▼                    ▼
            ┌──────────────┐    ┌──────────────┐    ┌──────────────┐
            │   Ollama     │    │   OpenAI     │    │  Anthropic   │
            │   (Local)    │    │   (Cloud)    │    │   (Cloud)    │
            │ ubuai:11434  │    │  GPT-4o/etc  │    │ Claude 3.5   │
            └──────────────┘    └──────────────┘    └──────────────┘
```

---

## State Machine

### Listening States

```
┌──────────────────────────────────────────────────────────────┐
│                     PASSIVE LISTENING                         │
│  - Continuous wake word detection                            │
│  - Low CPU usage                                             │
│  - No transcription                                          │
│  - Trigger: Wake word ("Hey HAL", "OK HAL", etc.)          │
└──────────────────────┬───────────────────────────────────────┘
                       │ Wake word detected
                       ▼
┌──────────────────────────────────────────────────────────────┐
│                   ACKNOWLEDGMENT                              │
│  - Play ACK sound (beep/chime)                              │
│  - Visual feedback (LED, UI indicator)                       │
│  - Duration: ~200ms                                          │
└──────────────────────┬───────────────────────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────────────────────┐
│                    ACTIVE LISTENING                           │
│  - Full transcription active                                 │
│  - Voice Activity Detection (VAD)                            │
│  - Buffer audio until pause (>1s silence)                    │
│  - Interrupt detection: "HAL, hold" → returns to passive     │
│  - Timeout: 30 seconds max                                   │
└──────────────────────┬───────────────────────────────────────┘
                       │ Speech pause detected (>1s silence)
                       ▼
┌──────────────────────────────────────────────────────────────┐
│                      PROCESSING                               │
│  - Play processing sound (working tone)                      │
│  - Send transcription to QM listener                         │
│  - Visual: "Processing..." or spinner                        │
│  - Timeout: 60 seconds                                       │
└──────────────────────┬───────────────────────────────────────┘
                       │ Response received
                       ▼
┌──────────────────────────────────────────────────────────────┐
│                      RESPONDING                               │
│  - Text-to-Speech (TTS) output                              │
│  - Visual: Display response text                            │
│  - Cancelable: "HAL, stop" interrupts                       │
└──────────────────────┬───────────────────────────────────────┘
                       │ Response complete
                       ▼
┌──────────────────────────────────────────────────────────────┐
│              ACTIVE LISTENING (Follow-up)                     │
│  - 10 second window                                          │
│  - No wake word needed                                       │
│  - User can speak immediately                                │
│  - Countdown visual indicator                                │
└──────────────────────┬───────────────────────────────────────┘
                       │ 10 seconds elapsed OR "HAL, goodbye"
                       ▼
                  [Return to PASSIVE]
```

---

## Component Details

### 1. Voice Gateway (Python WebSocket Server)

**File**: `PY/voice_gateway.py`

```python
# Responsibilities:
# - WebSocket server (asyncio)
# - Client session management
# - Audio chunk handling
# - State machine implementation
# - Audio feedback coordination

# Ports:
# - 8765: WebSocket server (clients connect here)

# State storage:
# - SESSION file in OpenQM with:
#   - Client ID
#   - State (passive/active/processing/responding)
#   - Last activity timestamp
#   - Context (conversation history)
```

### 2. Faster-Whisper Server

**Existing**: Already running on `ubuai` (Ubuntu server with 3 GPUs)

```python
# Configuration:
# - Host: ubuai.q.lcs.ai
# - Port: 9000 (or as configured)
# - Model: large-v3 or distil-large-v3 (for speed)
# - Language: auto-detect or en
# - VAD: Enabled for pause detection

# API:
# POST /transcribe
# {
#   "audio": "<base64 audio data>",
#   "language": "en",
#   "task": "transcribe"
# }
```

### 3. Command Processor (Python)

**File**: `PY/voice_commands.py`

```python
# Special commands that bypass QM:
# - "HAL, hold" → Interrupt, return to passive
# - "HAL, stop" → Cancel current response/action
# - "HAL, goodbye" → End session, return to passive
# - "HAL, repeat" → Replay last response

# All other utterances forwarded to QM
```

### 4. QM Listener (OpenQM TCP Server)

**File**: `BP/VOICE.LISTENER`

```basic
* QM Basic program that listens for voice messages
* Opens TCP socket on port 8767
* Receives JSON messages:
* {
*   "session_id": "client-uuid",
*   "transcription": "what's my medication schedule",
*   "timestamp": "2025-10-30T10:30:00Z",
*   "client_type": "mac|windows|homeassistant"
* }
*
* Sends JSON responses:
* {
*   "response_text": "You have Metformin at 8am...",
*   "response_audio": "<base64 TTS audio>" (optional),
*   "action_taken": "MEDICATION_QUERY",
*   "status": "success|error"
* }

PROGRAM VOICE.LISTENER

$INCLUDE INCLUDES/COMMON.VAR

SOCKET.PORT = 8767
MAX.CONNECTIONS = 10

* Create server socket
CALL CREATE.SERVER.SOCKET(SOCKET.PORT, SOCKET.HANDLE, STATUS)
IF STATUS < 0 THEN
   PRINT "Failed to create socket on port ":SOCKET.PORT
   STOP
END

PRINT "Voice Listener active on port ":SOCKET.PORT

* Main listen loop
LOOP
   * Accept connection
   CALL ACCEPT.SOCKET.CONNECTION(SOCKET.HANDLE, CLIENT.HANDLE, CLIENT.ADDR, STATUS)
   IF STATUS < 0 THEN CONTINUE
   
   * Read message
   MESSAGE.JSON = ''
   CALL READ.SOCKET(CLIENT.HANDLE, MESSAGE.JSON, 10000, STATUS)
   
   * Process message
   GOSUB PROCESS.VOICE.MESSAGE
   
   * Send response
   CALL WRITE.SOCKET(CLIENT.HANDLE, RESPONSE.JSON, STATUS)
   
   * Close client connection
   CALL CLOSE.SOCKET(CLIENT.HANDLE)
REPEAT

RETURN

PROCESS.VOICE.MESSAGE:
   * Parse JSON
   CALL PARSE.JSON(MESSAGE.JSON, MSG.OBJ)
   
   SESSION.ID = MSG.OBJ<'session_id'>
   TRANSCRIPTION = MSG.OBJ<'transcription'>
   TIMESTAMP = MSG.OBJ<'timestamp'>
   
   * Route to appropriate handler
   GOSUB ROUTE.MESSAGE
   
   * Build response
   CALL BUILD.JSON.RESPONSE(RESPONSE.TEXT, ACTION.TAKEN, RESPONSE.JSON)
RETURN

ROUTE.MESSAGE:
   * Intent classification
   CALL CLASSIFY.INTENT(TRANSCRIPTION, INTENT)
   
   BEGIN CASE
      CASE INTENT = 'MEDICATION'
         CALL HANDLE.MEDICATION.QUERY(TRANSCRIPTION, SESSION.ID, RESPONSE.TEXT)
         ACTION.TAKEN = 'MEDICATION_QUERY'
         
      CASE INTENT = 'APPOINTMENT'
         CALL HANDLE.APPOINTMENT.QUERY(TRANSCRIPTION, SESSION.ID, RESPONSE.TEXT)
         ACTION.TAKEN = 'APPOINTMENT_QUERY'
         
      CASE INTENT = 'HEALTH_DATA'
         CALL HANDLE.HEALTH.QUERY(TRANSCRIPTION, SESSION.ID, RESPONSE.TEXT)
         ACTION.TAKEN = 'HEALTH_QUERY'
         
      CASE INTENT = 'TRANSACTION'
         CALL HANDLE.TRANSACTION.QUERY(TRANSCRIPTION, SESSION.ID, RESPONSE.TEXT)
         ACTION.TAKEN = 'TRANSACTION_QUERY'
         
      CASE INTENT = 'AI_QUERY'
         CALL HANDLE.AI.QUERY(TRANSCRIPTION, SESSION.ID, RESPONSE.TEXT)
         ACTION.TAKEN = 'AI_QUERY'
         
      CASE 1
         * General query - route to AI
         CALL HANDLE.GENERAL.QUERY(TRANSCRIPTION, SESSION.ID, RESPONSE.TEXT)
         ACTION.TAKEN = 'GENERAL_QUERY'
   END CASE
RETURN

END
```

### 5. Message Router (OpenQM)

**File**: `BP/VOICE.ROUTER`

```basic
* Intent classification and routing
* Uses AI for intent detection
* Maintains conversation context
* Handles multi-turn conversations

SUBROUTINE ROUTE.MESSAGE(TRANSCRIPTION, SESSION.ID, RESPONSE.TEXT, ACTION.TAKEN)

* Get session context
CALL GET.SESSION.CONTEXT(SESSION.ID, CONTEXT)

* Classify intent using AI
PROMPT = "Classify this user request into one of these categories: "
PROMPT := "MEDICATION, APPOINTMENT, HEALTH_DATA, TRANSACTION, PASSWORD, REMINDER, AI_QUERY, GENERAL. "
PROMPT := "Request: ":TRANSCRIPTION
PROMPT := @FM:"Previous context: ":CONTEXT

CALL ASK.AI('gpt-4o-mini', PROMPT, INTENT.RESPONSE)
INTENT = TRIM(INTENT.RESPONSE)

* Update context
CONTEXT<-1> = TRANSCRIPTION
CALL UPDATE.SESSION.CONTEXT(SESSION.ID, CONTEXT)

* Return for routing
ACTION.TAKEN = INTENT

RETURN
```

---

## WebSocket Protocol

### Client → Server Messages

```json
{
  "type": "audio_chunk",
  "session_id": "client-uuid-1234",
  "audio": "<base64 encoded audio>",
  "format": "wav|opus|mp3",
  "sample_rate": 16000,
  "timestamp": "2025-10-30T10:30:00.123Z"
}

{
  "type": "wake_word_detected",
  "session_id": "client-uuid-1234",
  "wake_word": "hey hal",
  "confidence": 0.95,
  "timestamp": "2025-10-30T10:30:00.123Z"
}

{
  "type": "speech_ended",
  "session_id": "client-uuid-1234",
  "duration_ms": 3500,
  "timestamp": "2025-10-30T10:30:03.623Z"
}

{
  "type": "command",
  "session_id": "client-uuid-1234",
  "command": "hold|stop|repeat|goodbye",
  "timestamp": "2025-10-30T10:30:00.123Z"
}

{
  "type": "heartbeat",
  "session_id": "client-uuid-1234",
  "timestamp": "2025-10-30T10:30:00.123Z"
}
```

### Server → Client Messages

```json
{
  "type": "ack",
  "sound": "chime",
  "timestamp": "2025-10-30T10:30:00.456Z"
}

{
  "type": "processing",
  "sound": "working_tone",
  "message": "Processing your request...",
  "timestamp": "2025-10-30T10:30:01.789Z"
}

{
  "type": "response",
  "text": "You have Metformin scheduled for 8am and 8pm daily.",
  "audio": "<base64 TTS audio>",
  "duration_ms": 4200,
  "actions": [
    {
      "type": "display",
      "content": {
        "medications": [
          {"name": "Metformin", "time": "8:00 AM", "dosage": "500mg"},
          {"name": "Metformin", "time": "8:00 PM", "dosage": "500mg"}
        ]
      }
    }
  ],
  "timestamp": "2025-10-30T10:30:05.123Z"
}

{
  "type": "state_change",
  "new_state": "active_listening|passive_listening|processing|responding",
  "countdown_ms": 10000,
  "timestamp": "2025-10-30T10:30:00.123Z"
}

{
  "type": "error",
  "code": "TRANSCRIPTION_FAILED|QM_TIMEOUT|AI_ERROR",
  "message": "Failed to transcribe audio. Please try again.",
  "recoverable": true,
  "timestamp": "2025-10-30T10:30:00.123Z"
}
```

---

## Client Implementation

### Mac/Windows Client (Python)

**File**: `clients/desktop_voice_client.py`

```python
import asyncio
import websockets
import sounddevice as sd
import numpy as np
import base64
import json
from pvporcupine import Porcupine  # Wake word detection

class HALVoiceClient:
    def __init__(self):
        self.ws = None
        self.session_id = str(uuid.uuid4())
        self.state = 'passive'
        self.porcupine = Porcupine(
            access_key="YOUR_KEY",
            keywords=["hey hal"]
        )
        
    async def connect(self):
        self.ws = await websockets.connect('ws://localhost:8765')
        
    async def audio_stream(self):
        def callback(indata, frames, time, status):
            if self.state == 'passive':
                # Only wake word detection
                result = self.porcupine.process(indata)
                if result >= 0:
                    asyncio.create_task(self.on_wake_word())
            elif self.state == 'active':
                # Send audio for transcription
                audio_b64 = base64.b64encode(indata.tobytes()).decode()
                asyncio.create_task(self.send_audio(audio_b64))
                
        with sd.InputStream(callback=callback, channels=1, 
                           samplerate=16000, blocksize=512):
            await asyncio.Event().wait()
```

### Home Assistant Integration

**File**: `clients/homeassistant_voice/`

```yaml
# configuration.yaml
hal_voice:
  websocket_url: ws://qm-server:8765
  session_id: homeassistant-main
  wake_word: "hey hal"
  tts_engine: piper
  audio_feedback: true
```

---

## Audio Feedback

### Sound Files

Location: `VOICE/SOUNDS/`

```
ack.wav          - Acknowledgment sound (200ms chime)
processing.wav   - Processing sound (looping ambient tone)
error.wav        - Error sound (warning beep)
goodbye.wav      - Session end sound (descending tone)
```

### TTS Integration

**Options**:
1. **Piper TTS** (Local, fast, good quality)
   - Running on same server as Faster-Whisper
   - Models: en_US-lessac-medium, en_US-amy-medium
   
2. **ElevenLabs** (Cloud, best quality)
   - For premium experience
   - Voice: Professional male/female
   
3. **OpenAI TTS** (Cloud, good quality)
   - tts-1 or tts-1-hd model
   - Voice: alloy, echo, fable, onyx, nova, shimmer

---

## Session Management

### Session File (OpenQM)

**File**: `SESSION`

```
Record ID: {session_id}

Field 1: CLIENT_TYPE (mac|windows|homeassistant|google|alexa)
Field 2: STATE (passive|active|processing|responding)
Field 3: LAST_ACTIVITY (timestamp)
Field 4: CONTEXT (conversation history, @VM delimited)
Field 5: USER_ID (linked person record)
Field 6: LOCATION (home|office|mobile)
Field 7: PREFERENCES (JSON: volume, voice, speed)
Field 8: ACTIVE_SINCE (timestamp when entered active mode)
Field 9: TURN_COUNT (number of back-and-forth turns)
Field 10: LAST_RESPONSE (for "repeat" command)
```

---

## Performance Targets

| Metric | Target | Current |
|--------|--------|---------|
| Wake word latency | <500ms | TBD |
| Transcription latency | <2s | ~1.5s (Whisper large-v3) |
| QM routing latency | <100ms | TBD |
| Total response time | <5s | TBD |
| Active listening timeout | 30s | Configurable |
| Follow-up window | 10s | Configurable |
| Max concurrent sessions | 20 | TBD |

---

## Security

### Authentication
- WebSocket: Session tokens (JWT)
- QM Listener: IP whitelist + shared secret
- API Keys: Stored in OpenQM `API.KEYS` file

### Privacy
- Audio: Not stored by default
- Transcriptions: Logged in `CONVERSATION` file
- Sensitive commands: Masked in logs (passwords, etc.)
- TTS audio: Generated on-demand, not stored

---

## Deployment

### Server Components

```bash
# 1. Start Faster-Whisper server (already running on ubuai)
# 2. Start Ollama (already running on ubuai:11434)

# 3. Start Voice Gateway
cd C:\QMSYS\HAL\PY
python voice_gateway.py

# 4. Start QM Voice Listener (from QM)
LOGTO HAL
BASIC BP VOICE.LISTENER
CATALOG BP VOICE.LISTENER
VOICE.LISTENER
```

### Client Deployment

```bash
# Mac/Windows Desktop
pip install -r clients/requirements.txt
python clients/desktop_voice_client.py

# Home Assistant
# Copy files to custom_components/hal_voice/
# Restart Home Assistant
# Configure in configuration.yaml
```

---

## Development Roadmap

### Phase 1: Core Infrastructure (2 weeks)
- [ ] WebSocket server (voice_gateway.py)
- [ ] QM listener (VOICE.LISTENER)
- [ ] Message router (VOICE.ROUTER)
- [ ] Basic desktop client (Mac/Windows)
- [ ] Audio feedback system

### Phase 2: Intelligence (2 weeks)
- [ ] Intent classification
- [ ] Context management
- [ ] Multi-turn conversations
- [ ] Action handlers (medication, appointment, etc.)

### Phase 3: Multi-Platform (2 weeks)
- [ ] Home Assistant integration
- [ ] Mobile apps (iOS/Android)
- [ ] Web interface

### Phase 4: Advanced Features (Ongoing)
- [ ] Voice biometrics (user identification)
- [ ] Emotion detection
- [ ] Proactive suggestions
- [ ] Multi-language support

---

## Testing

### Unit Tests
```bash
pytest tests/test_voice_gateway.py
pytest tests/test_voice_commands.py
pytest tests/test_qm_listener.py
```

### Integration Tests
```bash
# Test wake word → transcription → response
python tests/test_voice_flow.py

# Test multi-turn conversation
python tests/test_conversation_context.py

# Test error handling
python tests/test_error_recovery.py
```

### Load Tests
```bash
# Simulate multiple concurrent clients
python tests/load_test_voice_gateway.py --clients 20
```

---

## Monitoring

### Metrics
- WebSocket connections: Active sessions count
- Transcription latency: p50, p95, p99
- QM response time: p50, p95, p99
- Error rate: % of failed requests
- Audio quality: Signal-to-noise ratio

### Logs
- `LOGS/voice_gateway.log` - WebSocket server events
- `LOGS/voice_commands.log` - Command processing
- `LOGS/qm_voice_listener.log` - QM listener events
- `CONVERSATION` file - All transcriptions and responses

---

## Configuration

**File**: `config/voice_config.json`

```json
{
  "gateway": {
    "host": "0.0.0.0",
    "port": 8765,
    "max_connections": 50
  },
  "whisper": {
    "url": "http://ubuai.q.lcs.ai:9000",
    "model": "large-v3",
    "language": "en"
  },
  "qm_listener": {
    "host": "localhost",
    "port": 8767
  },
  "ollama": {
    "url": "http://ubuai.q.lcs.ai:11434",
    "default_model": "deepseek-r1:32b"
  },
  "audio": {
    "ack_sound": "VOICE/SOUNDS/ack.wav",
    "processing_sound": "VOICE/SOUNDS/processing.wav",
    "error_sound": "VOICE/SOUNDS/error.wav"
  },
  "timing": {
    "wake_word_timeout": 5000,
    "active_listening_timeout": 30000,
    "follow_up_window": 10000,
    "processing_timeout": 60000
  },
  "tts": {
    "engine": "piper",
    "voice": "en_US-lessac-medium",
    "speed": 1.0
  }
}
```

---

## Troubleshooting

### Common Issues

**1. WebSocket connection fails**
```bash
# Check if gateway is running
netstat -an | findstr 8765

# Check firewall
netsh advfirewall firewall show rule name="HAL Voice Gateway"
```

**2. Transcription errors**
```bash
# Test Faster-Whisper server
curl -X POST http://ubuai.q.lcs.ai:9000/transcribe \
  -H "Content-Type: application/json" \
  -d '{"audio": "...", "language": "en"}'
```

**3. QM listener not responding**
```qm
# Check if listener is running
LIST.READU

# Restart listener
KILL.PHANTOM listener_phantom_id
VOICE.LISTENER
```

---

## References

- [Faster-Whisper Documentation](https://github.com/guillaumekln/faster-whisper)
- [Porcupine Wake Word](https://github.com/Picovoice/porcupine)
- [WebSocket Protocol](https://developer.mozilla.org/en-US/docs/Web/API/WebSockets_API)
- [OpenQM Socket Programming](../../QM_HELP/using_socket_connections.htm)
- [Piper TTS](https://github.com/rhasspy/piper)

---

**Next Steps**: 
1. Review architecture with team
2. Set up development environment
3. Begin Phase 1 implementation

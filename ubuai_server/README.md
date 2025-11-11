# UBUAI Voice Server

FastAPI server for HAL voice interface that handles:
- Audio transcription (Faster-Whisper GPU)
- Routing to OpenQM listener
- Text-to-speech (ElevenLabs + pyttsx3 fallback)

## Installation

### 1. Install Python dependencies

```bash
cd C:\QMSYS\hal\ubuai_server
pip install -r requirements.txt
```

### 2. Configure environment

Copy `.env.example` to `.env` and configure:

```bash
copy .env.example .env
```

Edit `.env`:
- Set `ELEVENLABS_API_KEY` if using ElevenLabs TTS
- Set `WHISPER_DEVICE=cpu` if no GPU available
- Adjust `OPENQM_HOST` and `OPENQM_PORT` if needed

### 3. Start the server

```bash
python main.py
```

Or using uvicorn directly:

```bash
uvicorn main:app --host 0.0.0.0 --port 8001
```

## Endpoints

### WebSocket: `/transcribe`

Main voice interaction endpoint.

**Protocol:**
1. Client connects to `ws://host:8001/transcribe`
2. Client sends binary audio chunks (PCM16, 16kHz, mono)
3. Client sends `"__END__"` text message when done
4. Server transcribes audio
5. Server routes to OpenQM
6. Server generates TTS response
7. Server sends response audio (binary)
8. Connection closes

**Example (Python):**

```python
import asyncio
import websockets

async def test_transcribe():
    async with websockets.connect('ws://10.1.10.20:8001/transcribe') as ws:
        # Send audio data
        with open('test_audio.pcm', 'rb') as f:
            audio = f.read()
        
        await ws.send(audio)
        await ws.send("__END__")
        
        # Receive response audio
        response = await ws.recv()
        
        # Save to file
        with open('response.mp3', 'wb') as f:
            f.write(response)

asyncio.run(test_transcribe())
```

### POST: `/speak`

Text-to-speech endpoint.

**Request:**
```json
{
    "text": "Hello, how can I help you?",
    "voice": "nPczCjzI2devNBz1zQrb"
}
```

**Response:**
Audio file (MP3 or WAV)

**Example:**

```bash
curl -X POST http://10.1.10.20:8001/speak \
  -H "Content-Type: application/json" \
  -d '{"text": "Hello world"}' \
  --output response.mp3
```

### POST: `/transcribe_http`

HTTP transcription endpoint (for testing).

**Request:**
```json
{
    "audio": "base64-encoded PCM16 audio"
}
```

**Response:**
```json
{
    "text": "transcribed text"
}
```

### GET: `/`

Health check endpoint.

**Response:**
```json
{
    "service": "UBUAI Voice Server",
    "status": "running",
    "whisper_model": "base",
    "whisper_device": "cuda",
    "qm_host": "10.1.34.103",
    "qm_port": 8767
}
```

## Architecture

```
Client → WebSocket → UBUAI Server
                        ↓
                  Faster-Whisper (GPU)
                        ↓
                  OpenQM (TCP 8767)
                        ↓
                  Intent Routing
                        ↓
                  Response Text
                        ↓
                  ElevenLabs TTS
                        ↓
                  Audio Response → Client
```

## Performance

- **Transcription**: 50-300ms (GPU), 500-2000ms (CPU)
- **QM Routing**: 50-100ms
- **TTS**: 200-600ms (ElevenLabs), 500-1500ms (pyttsx3)
- **Total**: 300-1000ms end-to-end

## Troubleshooting

### Faster-Whisper not found

Install CUDA toolkit if using GPU:

```bash
pip install faster-whisper
```

If GPU not available, set `WHISPER_DEVICE=cpu` in `.env`

### ElevenLabs API errors

Check API key is valid. Server will automatically fall back to pyttsx3.

### QM connection refused

Ensure OpenQM VOICE.LISTENER is running:

```qm
LOGTO HAL
PHANTOM BP VOICE.LISTENER
```

Check port is correct (default 8767).

## Development

### Running in development mode

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8001
```

### Testing

```bash
# Test health check
curl http://localhost:8001/

# Test TTS
curl -X POST http://localhost:8001/speak \
  -H "Content-Type: application/json" \
  -d '{"text": "This is a test"}' \
  --output test.mp3
```

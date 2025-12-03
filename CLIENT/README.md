# HAL Voice Client

**⚠️ IMPORTANT: This client runs on YOUR MAC (not on QM or UBUAI servers)**

Voice interface client for HAL assistant with wake word detection, VAD, and interruption handling.

## 🖥️ Which Machine?

```
✅ Run this on: YOUR MAC (macOS)
❌ Don't run on: QM Server (Windows) or UBUAI Server (Linux)

Your Mac needs: Microphone + Speakers
```

**See**: `MAC_QUICK_START.md` in this directory for Mac-specific setup instructions.

## Features

- ✅ Wake word detection ("Hey Jarvis" / "Computer")
- ✅ Voice Activity Detection (VAD) with 3-second silence threshold
- ✅ Interruption handling (say wake word during recording to restart)
- ✅ 10-second passive listening window (no wake word needed for follow-ups)
- ✅ Audio feedback sounds (activation, acknowledgement, error)
- ✅ Keyboard fallback mode (if wake word not available)

## Installation (macOS)

**Complete Mac instructions**: See `MAC_QUICK_START.md`

### 1. Install system dependencies (Mac)

```bash
# Install Homebrew if not already installed
# /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install PortAudio and FFmpeg
brew install portaudio ffmpeg
```

### 2. Install Python dependencies

```bash
cd ~/Projects/hal/clients  # or wherever you put the client

# Create virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Setup audio feedback sounds

```bash
# Option A: Use TNG activation sound (recommended)
bash setup_sounds.sh

# Option B: Generate simple tones (fallback)
python3 generate_sounds.py
```

The client uses:
- **activation.mp3** - Star Trek TNG computer chirp (from VOICE/SOUNDS)
- **acknowledgement.wav** - Ack tone
- **error.wav** - Error beep

### 4. Configure UBUAI URL (Mac)

```bash
# Set environment variable
export UBUAI_URL=ws://10.1.10.20:8001/transcribe

# Or edit hal_voice_client_full.py line 27 directly
```

### 5. Grant microphone permissions (Mac)

When you first run the client, macOS will prompt for microphone access:
- **System Preferences** → **Security & Privacy** → **Privacy** → **Microphone**
- Check the box next to **Terminal** (or iTerm2)
- Restart terminal if needed

## Usage

### Full Voice Mode (Wake Word) - Mac

```bash
cd ~/Projects/hal/clients
source venv/bin/activate  # If using virtual environment
python3 hal_voice_client_full.py
```

Say "Hey Jarvis" or "Computer" to activate. Speak your query. Wait 3 seconds of silence for processing.

### Keyboard Mode (No Wake Word)

If OpenWakeWord is not installed, client automatically falls back to keyboard mode:

```bash
python hal_voice_client_full.py
```

Press ENTER, speak for 5 seconds, then processing starts automatically.

## Usage Flow

### Normal Interaction

```
User: "Hey Jarvis"
→ 🔊 activation.wav plays
User: "What medications am I taking?"
→ (3 seconds silence)
→ 🔊 acknowledgement.wav plays
→ ⏳ Processing...
→ 🔊 Response plays
→ ⏱️ 10s follow-up window
```

### Interruption

```
User: "Hey Jarvis"
→ 🔊 activation.wav plays
User: "Remind me to call John tomorrow at 3pm no wait"
User: "Hey Jarvis"  ← interrupts
→ 🔊 activation.wav plays AGAIN
User: "What's my medication schedule?"
→ Only final query processed
```

### Follow-up (No Wake Word)

```
User: "Hey Jarvis"
User: "What medications am I taking?"
→ Response plays
→ ⏱️ 10s follow-up window
User: "Tell me about Metformin"  ← no wake word needed
→ Follow-up processed
→ ⏱️ 10s follow-up window again
```

## State Machine

```
PASSIVE (wake word required)
    ↓
    Wake word detected
    → Play activation.wav
    ↓
ACTIVE (recording)
    ↓
    Wake word detected AGAIN → Clear buffer, restart (interruption)
    ↓
    3s silence detected
    → Play acknowledgement.wav
    ↓
PROCESSING (waiting for response)
    ↓
    Response received
    → Play response audio
    ↓
PASSIVE (10s follow-up window)
    ↓
    Voice detected → ACTIVE (no wake word)
    OR
    10s timeout → PASSIVE (wake word required)
```

## Configuration

### Environment Variables

- `UBUAI_URL` - WebSocket URL (default: `ws://10.1.10.20:8001/transcribe`)

### Constants (in code)

- `SAMPLE_RATE` - 16000 Hz (required for wake word and VAD)
- `SILENCE_THRESHOLD` - 3.0 seconds
- `FOLLOW_UP_WINDOW` - 10.0 seconds
- `VAD_AGGRESSIVENESS` - 2 (0-3, higher = more strict)

## Troubleshooting

### Wake word not detecting

- Speak clearly: "Hey JARVIS" (emphasize "Jarvis")
- Or say: "COMPUTER"
- Check microphone input level
- Try adjusting VAD aggressiveness

### Audio not playing back

- Check audio output device
- Ensure WAV/MP3 codecs installed
- On Windows, may need to install media codecs

### Connection errors

- Ensure UBUAI server is running on port 8001
- Check network connectivity: `ping 10.1.10.20`
- Verify firewall allows WebSocket connections

### High CPU usage

- Wake word detection is CPU-intensive
- Consider using faster model or keyboard mode
- Close other audio applications

## Advanced

### Custom Wake Words

Edit `init_wake_word()` to use different models:

```python
wake_words = ['alexa_v0.1', 'hey_mycroft_v0.1', 'ok_naomi_v0.1']
```

Available wake words: https://github.com/dscripka/openWakeWord

### Custom Audio Feedback

Replace WAV files with your own sounds. Requirements:
- Format: WAV (PCM)
- Channels: 1 or 2
- Sample rate: Any (16kHz recommended)
- Duration: <1 second for feedback sounds

### Integration

Use `HALVoiceClient` class in your own code:

```python
from hal_voice_client_full import HALVoiceClient

client = HALVoiceClient('ws://10.1.10.20:8001/transcribe')
await client.run()
```

## Performance

- **Wake word detection**: <50ms
- **VAD silence detection**: <50ms
- **Audio upload**: 100-300ms (LAN)
- **Total latency**: See UBUAI server for end-to-end timing

## License

Part of HAL voice assistant system.

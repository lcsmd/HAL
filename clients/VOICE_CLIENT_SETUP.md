# HAL Voice Client Setup

Full voice pipeline: Wake word → Acknowledgement sound → Record → Transcribe → Send to HAL

## Installation

### 1. Install Dependencies

**Mac:**
```bash
# Install PortAudio (required for PyAudio)
brew install portaudio

# Install Python packages
pip3 install pyaudio pvporcupine openai-whisper
```

**Windows:**
```powershell
# Install Python packages
pip install pyaudio pvporcupine openai-whisper
```

**Linux:**
```bash
# Install PortAudio
sudo apt-get install portaudio19-dev

# Install Python packages
pip3 install pyaudio pvporcupine openai-whisper
```

### 2. Get Porcupine Wake Word Key (FREE)

1. Go to: https://console.picovoice.ai/
2. Sign up for free account
3. Copy your Access Key
4. Set environment variable:

**Mac/Linux:**
```bash
export PORCUPINE_ACCESS_KEY="your-key-here"
```

**Windows:**
```powershell
$env:PORCUPINE_ACCESS_KEY="your-key-here"
```

### 3. Download Voice Client

```bash
curl -O http://10.1.34.103:8080/hal_voice_client.py
chmod +x hal_voice_client.py
```

## Usage

### Voice Mode (with Wake Word)

```bash
# Set your HAL server URL
export HAL_GATEWAY_URL="ws://10.1.34.103:8768"

# Run voice client
python3 hal_voice_client.py
```

Then:
1. Say **"Jarvis"** (wake word)
2. Wait for beep
3. Speak your query: "What medications am I taking?"
4. HAL responds

### Keyboard Mode (no wake word)

If you don't have a Porcupine key, it falls back to keyboard mode:

```bash
python3 hal_voice_client.py
```

Then:
1. Press ENTER
2. Speak your query (5 seconds)
3. HAL transcribes and responds

### Text Mode (testing)

```bash
python3 hal_voice_client.py --query "What medications am I taking?"
```

## Configuration

### Environment Variables

```bash
# Gateway URL (required)
export HAL_GATEWAY_URL="ws://10.1.34.103:8768"

# Porcupine wake word key (optional - for wake word detection)
export PORCUPINE_ACCESS_KEY="your-key-here"

# Whisper model size (optional - default: base)
# Options: tiny, base, small, medium, large
export WHISPER_MODEL="base"
```

### Whisper Models

- **tiny**: Fastest, least accurate (~1GB RAM)
- **base**: Good balance (~1GB RAM) ✓ Recommended
- **small**: Better accuracy (~2GB RAM)
- **medium**: High accuracy (~5GB RAM)
- **large**: Best accuracy (~10GB RAM)

## Built-in Wake Words

Porcupine includes these free wake words:
- **jarvis** ✓ Default
- **computer**
- **hey google**
- **hey siri**
- **alexa**
- **americano**
- **blueberry**
- **bumblebee**
- **grapefruit**
- **grasshopper**
- **picovoice**
- **porcupine**
- **terminator**

To change wake word, edit the line in `hal_voice_client.py`:
```python
keywords=["jarvis"]  # Change to any wake word above
```

## Custom Acknowledgement Sound

To use a custom sound file instead of the beep:

1. Place your sound file (WAV format) in the same directory
2. Edit `load_acknowledgement_sound()` method:

```python
def load_acknowledgement_sound(self):
    with wave.open('my_sound.wav', 'rb') as wf:
        return wf.readframes(wf.getnframes())
```

## Audio Settings

Adjust in the code if needed:

```python
SAMPLE_RATE = 16000  # Hz
RECORDING_TIMEOUT = 5  # seconds
```

## Troubleshooting

### "No module named pyaudio"

**Mac:**
```bash
brew install portaudio
pip3 install pyaudio
```

**Linux:**
```bash
sudo apt-get install portaudio19-dev python3-pyaudio
```

**Windows:**
Download wheel from: https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio

### "Invalid sample rate"

Your microphone may not support 16kHz. Check available rates:
```python
import pyaudio
p = pyaudio.PyAudio()
for i in range(p.get_device_count()):
    info = p.get_device_info_by_index(i)
    print(info['name'], info['defaultSampleRate'])
```

### Whisper model download slow

First run downloads the model (~100MB-3GB depending on size).
Models are cached in `~/.cache/whisper/`

### Wake word not detecting

1. Check microphone is working: `python3 -m pyaudio`
2. Verify Porcupine key is set: `echo $PORCUPINE_ACCESS_KEY`
3. Try different wake words
4. Increase microphone volume

## Architecture

```
Microphone
    ↓
Wake Word Detection (Porcupine)
    ↓
Play Acknowledgement Sound
    ↓
Record Audio (5 seconds)
    ↓
Transcribe (Whisper)
    ↓
Send to Voice Gateway (WebSocket)
    ↓
QM Listener processes query
    ↓
Response back to client
```

## Performance

- **Wake word detection**: ~5ms latency
- **Acknowledgement**: Instant
- **Recording**: 5 seconds
- **Transcription (base model)**: ~1-3 seconds
- **Gateway response**: ~100ms
- **Total**: ~10 seconds from speaking to response

## Next Steps

1. Add text-to-speech for HAL responses (pyttsx3 or gTTS)
2. Implement voice activity detection (stop on silence)
3. Add continuous conversation mode
4. Create auto-start service

## Support

Server: 10.1.34.103:8768
Wake word key: https://console.picovoice.ai/
Whisper docs: https://github.com/openai/whisper

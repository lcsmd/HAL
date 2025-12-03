# HAL Voice Client - Quick Start

Complete voice interaction with wake word, TNG activation sound, and transcription.

## Your Workflow

1. **Say "Computer"** (wake word)
2. **🔊 Hear TNG activation sound** (iconic Star Trek beep)
3. **Speak your query** (5 seconds to speak)
4. **Transcription** happens automatically
5. **HAL responds** with text

## One-Line Install (Mac/Linux)

```bash
curl -fsSL http://10.1.34.103:8080/install_hal_voice.sh -o /tmp/install_hal_voice.sh && HAL_SERVER_URL=http://10.1.34.103:8768 PORCUPINE_ACCESS_KEY=your-key bash /tmp/install_hal_voice.sh
```

Or without wake word (keyboard mode):
```bash
curl -fsSL http://10.1.34.103:8080/install_hal_voice.sh -o /tmp/install_hal_voice.sh && HAL_SERVER_URL=http://10.1.34.103:8768 bash /tmp/install_hal_voice.sh
```

Then:
```bash
hal-voice
```

## Quick Install (Windows - PowerShell)

```powershell
# 1. Install dependencies
pip install pyaudio pvporcupine openai-whisper

# 2. Get free Porcupine wake word key
# Visit: https://console.picovoice.ai/
# Sign up and copy your Access Key

# 3. Download voice client and TNG sound
curl -O http://10.1.34.103:8080/hal_voice_client.py
curl -O http://10.1.34.103:8080/ack.wav
New-Item -ItemType Directory -Path "VOICE\SOUNDS" -Force
Move-Item ack.wav VOICE\SOUNDS\

# 4. Set environment and run
$env:HAL_GATEWAY_URL="ws://10.1.34.103:8768"
$env:PORCUPINE_ACCESS_KEY="your-key-here"
python hal_voice_client.py
```

## Usage

### Voice Mode (Recommended)

```bash
python3 hal_voice_client.py
```

Then:
1. Say **"Computer"**
2. 🔊 Hear TNG beep
3. Speak: "What medications am I taking?"
4. Get HAL's response

### Keyboard Mode (No Wake Word)

If you don't set PORCUPINE_ACCESS_KEY, it falls back to keyboard:

```bash
python3 hal_voice_client.py
```

Then:
1. Press ENTER
2. Speak (5 seconds)
3. Get response

### Text Mode (No Voice)

```bash
python3 hal_voice_client.py --query "What are my appointments?"
```

## Sound Files

The TNG activation sound (`ack.wav`) will be loaded from:
- `VOICE/SOUNDS/ack.wav` (recommended location)
- `~/.hal-client/sounds/ack.wav` (user directory)
- `ack.wav` (current directory)

If not found, generates a simple beep as fallback.

## Configuration

```bash
# Required
export HAL_GATEWAY_URL="ws://10.1.34.103:8768"

# Optional (enables wake word)
export PORCUPINE_ACCESS_KEY="your-key-here"

# Optional (default: base)
export WHISPER_MODEL="base"  # tiny, base, small, medium, large
```

## Wake Word

- **"Computer"** is the built-in wake word (free with Porcupine)
- No custom training needed
- Works out of the box
- To use "HAL" instead, you'd need custom wake word training

## The TNG Sound

When you say "Computer", you'll hear the iconic Star Trek: The Next Generation computer acknowledgement sound - the same beep heard when crew members interact with the ship's computer!

**Audio Details:**
- Format: WAV, mono, 16kHz
- Duration: 0.65 seconds  
- Source: Star Trek TNG
- File: `ack.wav` (20KB)

## Troubleshooting

### PyAudio Installation Issues

**Mac:**
```bash
brew install portaudio
pip3 install --global-option='build_ext' \
  --global-option='-I/opt/homebrew/include' \
  --global-option='-L/opt/homebrew/lib' \
  pyaudio
```

**Linux:**
```bash
sudo apt-get install portaudio19-dev python3-pyaudio
pip3 install pyaudio
```

**Windows:**
Download precompiled wheel from:
https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio

### Wake Word Not Detecting

1. Test microphone: `python3 -m sounddevice`
2. Verify key is set: `echo $PORCUPINE_ACCESS_KEY`
3. Speak clearly: "Computer" (not too loud, not too quiet)
4. Check microphone permissions

### No TNG Sound

1. Verify file exists: `ls VOICE/SOUNDS/ack.wav`
2. Check file format: `file VOICE/SOUNDS/ack.wav`
3. Test playback: `afplay VOICE/SOUNDS/ack.wav` (Mac)
4. Client will use fallback beep if not found

### Transcription Slow

- Use smaller model: `export WHISPER_MODEL="tiny"`
- First run downloads model (~100MB)
- Subsequent runs are cached

## Performance

- **Wake word detection**: 5ms
- **TNG sound playback**: 0.65s
- **Recording**: 5s
- **Transcription (base)**: 2-3s
- **Gateway response**: 100ms
- **Total**: ~10 seconds

## Complete Architecture

```
Microphone
    ↓
Wake Word Detection (Porcupine: "Computer")
    ↓
🔊 Play TNG Activation Sound (ack.wav)
    ↓
Record Audio (5 seconds)
    ↓
Transcribe with Whisper
    ↓
Send to Voice Gateway (ws://10.1.34.103:8768)
    ↓
QM Voice Listener processes
    ↓
Response from HAL
    ↓
Display to user
```

## Files

- `hal_voice_client.py` - Voice client with wake word
- `ack.wav` - TNG activation sound
- `VOICE/SOUNDS/` - Sound directory

## Support

**Server**: 10.1.34.103:8768  
**Wake word key**: https://console.picovoice.ai/ (free)  
**Whisper**: https://github.com/openai/whisper  
**Porcupine**: https://picovoice.ai/platform/porcupine/

**Live long and prosper!** 🖖

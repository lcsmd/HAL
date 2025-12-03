# HAL Voice Client - Audio Feedback Sounds

## Sound Files Used

The HAL voice client uses three audio feedback sounds:

### 1. Activation Sound
**File**: `activation.mp3`  
**Source**: `../VOICE/SOUNDS/TNG_activation.mp3`  
**Description**: Star Trek: The Next Generation computer activation chirp  
**When played**: Immediately when wake word detected  
**Duration**: ~200ms  
**Format**: MP3

This is the iconic TNG computer sound that plays when you say "Hey Jarvis" or "Computer".

---

### 2. Acknowledgement Sound
**File**: `acknowledgement.wav`  
**Source**: `../VOICE/SOUNDS/ack.wav`  
**Description**: Acknowledgement tone  
**When played**: After 3 seconds of silence (processing begins)  
**Duration**: ~150ms  
**Format**: WAV

Confirms your speech has been captured and is being processed.

---

### 3. Error Sound
**File**: `error.wav`  
**Source**: Same as `acknowledgement.wav` (fallback)  
**Description**: Error/warning tone  
**When played**: When connection fails or processing errors occur  
**Duration**: ~150ms  
**Format**: WAV

Alerts you to errors without being jarring.

---

## Setup Instructions

### Automatic Setup (Recommended)

**On Mac/Linux**:
```bash
cd ~/Projects/hal/clients
bash setup_sounds.sh
```

**On Windows**:
```powershell
cd C:\QMSYS\hal\clients
.\setup_sounds.ps1
```

This copies the TNG activation sound and ack.wav from `VOICE/SOUNDS` directory.

---

### Manual Setup

If the automatic script doesn't work:

**On Mac**:
```bash
cd ~/Projects/hal/clients

# Copy TNG activation sound
cp ../VOICE/SOUNDS/TNG_activation.mp3 activation.mp3

# Copy acknowledgement sound
cp ../VOICE/SOUNDS/ack.wav acknowledgement.wav

# Use ack as error sound
cp acknowledgement.wav error.wav
```

**On Windows**:
```powershell
cd C:\QMSYS\hal\clients

# Copy TNG activation sound
Copy-Item ..\VOICE\SOUNDS\TNG_activation.mp3 -Destination activation.mp3

# Copy acknowledgement sound
Copy-Item ..\VOICE\SOUNDS\ack.wav -Destination acknowledgement.wav

# Use ack as error sound
Copy-Item acknowledgement.wav -Destination error.wav
```

---

### Alternative: Generate Simple Tones

If you don't have the TNG sounds or prefer simple tones:

```bash
python3 generate_sounds.py
```

This generates basic sine wave tones:
- Activation: Two rising tones (800Hz → 1200Hz)
- Acknowledgement: Single gentle tone (600Hz)
- Error: Two descending tones (800Hz → 400Hz)

---

## File Format Support

The client supports both:
- **WAV files**: Direct playback via simpleaudio (instant)
- **MP3 files**: System playback via `afplay` (Mac), `mpg123` (Linux), or Windows Media Player

MP3 is used for the TNG activation sound for quality, while WAV is used for ack/error for speed.

---

## Customizing Sounds

Want to use your own sounds?

1. **Replace files**: Just replace `activation.mp3`, `acknowledgement.wav`, `error.wav` with your own
2. **Format requirements**:
   - Activation: MP3 or WAV, mono/stereo, any sample rate
   - Acknowledgement: WAV preferred (faster), 16kHz recommended
   - Error: WAV preferred (faster), 16kHz recommended
3. **Duration recommendations**:
   - Activation: <500ms (should be instant feedback)
   - Acknowledgement: <300ms (confirms processing start)
   - Error: <500ms (alerts without being annoying)

---

## Troubleshooting

### "Could not load activation.mp3"

**Mac**: Install FFmpeg
```bash
brew install ffmpeg
```

**Linux**: Install mpg123
```bash
sudo apt-get install mpg123
```

---

### No sound plays

**Check files exist**:
```bash
ls -l activation.mp3 acknowledgement.wav error.wav
```

**Test manually**:
```bash
# Mac
afplay activation.mp3
afplay acknowledgement.wav

# Linux
mpg123 activation.mp3
aplay acknowledgement.wav
```

**Check volume**: System Preferences → Sound

---

### Sounds play but are delayed

- Use WAV files instead of MP3 for faster playback
- MP3 decoding adds ~50-100ms latency
- WAV playback is instant

---

## Credits

- **TNG Activation Sound**: Star Trek: The Next Generation LCARS computer interface
- **Ack Sound**: Custom generated or from HAL system
- **Generated Sounds**: Simple sine wave tones (fallback option)

---

**Enjoy the authentic Star Trek computer experience!** 🖖

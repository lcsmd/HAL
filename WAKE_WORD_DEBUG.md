# Wake Word Detection Debugging Guide

## Issue
The `hal --voice` command does not respond to wake word detection.

## Fixed Issues
1. **TNG Activation Sound**: Fixed missing `ack_sample_rate` and `ack_channels` attributes
2. **Sound Loading**: Now properly loads `ack.wav` from clients directory

## Testing Steps

### 1. Test Wake Word Detection Directly
Run the test script to verify OpenWakeWord is working:

```bash
python test_wake_word.py
```

This will:
- List available microphones
- Load the wake word model
- Test audio stream
- Listen for wake word with real-time scores

**Expected output:**
- Scores should be near 0.0 normally
- Scores should spike above 0.5 when you say "Hey Jarvis" or "Computer"

### 2. Check Dependencies
Make sure all required packages are installed:

```bash
pip install pyaudio openwakeword openai-whisper numpy pyttsx3
```

### 3. Common Issues

#### A. Wake Word Not Detected
**Symptoms**: Scores always near 0.0, never responds to voice

**Possible Causes:**
1. **Wrong microphone selected** - Check test script output for selected device
2. **Microphone volume too low** - Check system sound settings
3. **Wrong wake word model** - Try different models:
   - `hey_jarvis` (default)
   - `alexa`
   - `hey_mycroft`
   - `ok_naomi`

**Fix:**
Edit `clients/hal_voice_client.py` line 25:
```python
WAKE_WORD_MODEL = os.getenv('WAKE_WORD_MODEL', 'hey_jarvis')  # Try: alexa, hey_mycroft, ok_naomi
```

#### B. Audio Permission Issues
**Symptoms**: "Error opening audio device" or similar

**Fix (Windows):**
- Check Privacy Settings → Microphone → Allow apps to access microphone
- Make sure Python is allowed

**Fix (Mac):**
- System Preferences → Security & Privacy → Microphone
- Grant permission to Terminal or Python

#### C. TNG Sound Not Playing
**Symptoms**: Wake word detected but no sound plays

**Fix:**
- Verify `clients/ack.wav` exists
- Check system audio output is working
- Volume is not muted

### 4. Adjust Wake Word Sensitivity

If wake word detection is:
- **Too sensitive** (false positives): Increase threshold
- **Not sensitive enough** (misses wake word): Decrease threshold

Edit `clients/hal_voice_client.py` around line 186:

```python
# Current threshold
if predictions[self.wake_word_name] > 0.5:

# Try lower threshold (more sensitive)
if predictions[self.wake_word_name] > 0.3:

# Try higher threshold (less sensitive)  
if predictions[self.wake_word_name] > 0.7:
```

### 5. Test Full Voice Client

Once wake word detection works in test script:

```bash
cd clients
python hal_voice_client.py
```

**Expected behavior:**
1. Listens continuously for wake word
2. When detected: Plays TNG sound
3. Records your voice for 5 seconds
4. Transcribes and sends to HAL
5. Speaks response
6. Returns to listening for wake word

### 6. Debug Mode

Add debug logging to see what's happening:

Edit `clients/hal_voice_client.py`, add after line 184:

```python
# Get predictions
predictions = self.oww_model.predict(audio_float)

# Add debug logging
if hasattr(self, 'debug_count'):
    self.debug_count += 1
else:
    self.debug_count = 0
    
if self.debug_count % 50 == 0:  # Print every ~4 seconds
    print(f"[DEBUG] Score: {predictions[self.wake_word_name]:.3f}")
```

## Environment Variables

You can customize behavior without editing code:

```bash
# Windows
set WAKE_WORD_MODEL=alexa
set WHISPER_MODEL=tiny
set HAL_GATEWAY_URL=ws://10.1.34.103:8768

# Linux/Mac
export WAKE_WORD_MODEL=alexa
export WHISPER_MODEL=tiny
export HAL_GATEWAY_URL=ws://10.1.34.103:8768
```

## Microphone Selection

The client tries to auto-select the best microphone in this order:
1. Devices with "brio" in name (Logitech Brio webcam)
2. Devices with "usb" in name
3. Devices with "microphone" in name
4. Devices with "webcam" in name
5. Built-in microphone
6. First available device

To force a specific microphone, edit `select_microphone()` around line 120.

## Performance Notes

- **Whisper model size** affects transcription speed:
  - `tiny`: Fastest, less accurate
  - `base`: Good balance (default)
  - `small`: Better accuracy, slower
  - `medium/large`: Best accuracy, very slow

- **Wake word detection** runs continuously at ~12.5 Hz (80ms chunks)
- Should be negligible CPU usage when idle

## Next Steps

If wake word still doesn't work after these steps:
1. Capture test script output
2. Check if microphone works in other apps
3. Try different wake word models
4. Consider using keyboard mode (press ENTER instead of wake word)

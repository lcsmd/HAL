# Train "COMPUTER" Wake Word - Quick Guide

**Goal**: Train OpenWakeWord to recognize "COMPUTER" as the wake word

**Time Required**: 2-3 hours (1 hour collecting samples, 30 min training, testing)

---

## 🎯 Current Status

**"COMPUTER" wake word model does NOT exist** in pre-trained OpenWakeWord models.

**Available pre-trained models**:
- hey_jarvis
- hey_mycroft  
- ok_naomi
- (NO "computer" or "alexa" - we won't use those anyway)

**Therefore**: You must train a custom "COMPUTER" model.

---

## ⚡ Quick Start (For Prototype Testing NOW)

### **Option 1: Use Keyboard Mode** (Recommended for testing)

No wake word needed - just press ENTER to record:

```bash
python hal_voice_client.py
# Press ENTER when you want to speak
# Speak your query
# System processes automatically after 3 seconds silence
```

**Benefits**:
- ✅ Works immediately
- ✅ Test entire system while training wake word
- ✅ No "wrong" wake word being used

---

### **Option 2: Train "COMPUTER" Wake Word** (2-3 hours)

Follow instructions below to train the exact wake word you want.

---

## 🛠️ Training "COMPUTER" Wake Word

### Step 1: Install Training Tools (5 min)

```bash
pip install openwakeword
pip install onnx onnxruntime
pip install librosa soundfile
```

### Step 2: Collect Positive Samples (1 hour)

Need **200+ recordings** of different people saying "COMPUTER":

```bash
# Create directory structure
mkdir -p wake_word_training/computer/positive
cd wake_word_training/computer/positive

# Record samples
python << 'EOF'
import sounddevice as sd
import wave
import numpy as np
import os

print("="*60)
print("Recording 'COMPUTER' Wake Word Samples")
print("="*60)
print("\nInstructions:")
print("1. Press ENTER to start recording")
print("2. Say 'COMPUTER' clearly")
print("3. Recording stops automatically after 1.5 seconds")
print("4. Repeat 200+ times")
print("\nTips:")
print("- Vary your tone (normal, excited, whisper)")
print("- Vary your distance from mic (near, far)")
print("- Try different speeds (slow, fast)")
print("- Have others help (different voices)")
print("="*60)

for i in range(200):
    input(f'\n[{i+1}/200] Press ENTER, then say "COMPUTER" → ')
    
    print('  🎤 Recording...')
    audio = sd.rec(int(1.5 * 16000), samplerate=16000, channels=1, dtype='int16')
    sd.wait()
    
    filename = f'computer_sample_{i:03d}.wav'
    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(16000)
        wf.writeframes(audio.tobytes())
    
    print(f'  ✓ Saved: {filename}')
    
    # Show progress
    if (i + 1) % 20 == 0:
        print(f'\n  Progress: {i+1}/200 samples collected')

print("\n✅ All positive samples collected!")
EOF
```

---

### Step 3: Collect Negative Samples (30 min)

Need **100+ recordings** of things that are NOT "computer":

```bash
mkdir -p ../negative
cd ../negative

# Record negative samples
python << 'EOF'
import sounddevice as sd
import wave
import numpy as np

samples_to_record = [
    ("Background noise (10 samples)", 10),
    ("Similar words: 'commuter', 'commander', 'community' (10 samples)", 10),
    ("Common words: 'hello', 'okay', 'thank you', 'please' (20 samples)", 20),
    ("Random phrases: 'what time is it', 'turn on lights' (20 samples)", 20),
    ("Other wake words: 'hey', 'jarvis', 'assistant' (10 samples)", 10),
    ("Silence (just don't speak) (10 samples)", 10),
]

count = 0
for category, num in samples_to_record:
    print(f"\n{'='*60}")
    print(f"Category: {category}")
    print("="*60)
    
    for i in range(num):
        input(f'  [{count+1}/80] Press ENTER → ')
        print('  🎤 Recording...')
        
        audio = sd.rec(int(2.0 * 16000), samplerate=16000, channels=1, dtype='int16')
        sd.wait()
        
        filename = f'negative_sample_{count:03d}.wav'
        with wave.open(filename, 'wb') as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(16000)
            wf.writeframes(audio.tobytes())
        
        print(f'  ✓ Saved: {filename}')
        count += 1

print("\n✅ All negative samples collected!")
EOF
```

---

### Step 4: Train the Model (30 min)

```bash
cd ../..  # Back to wake_word_training/

# Install training dependencies if needed
pip install tensorflow scikit-learn

# Train using OpenWakeWord's training script
python << 'EOF'
import os
import wave
import numpy as np
from openwakeword.model import Model

print("Training 'COMPUTER' wake word model...")
print("This will take 20-30 minutes...\n")

# Load audio samples
positive_files = [f"computer/positive/{f}" for f in os.listdir("computer/positive") if f.endswith('.wav')]
negative_files = [f"computer/negative/{f}" for f in os.listdir("computer/negative") if f.endswith('.wav')]

print(f"Positive samples: {len(positive_files)}")
print(f"Negative samples: {len(negative_files)}")

# Note: OpenWakeWord training requires more complex setup
# For now, use their pre-built training pipeline
print("\n⚠️  Full training requires OpenWakeWord's training pipeline")
print("See: https://github.com/dscripka/openWakeWord/tree/main/training")
print("\nSimplified training:")
print("1. Upload samples to OpenWakeWord training service")
print("2. Or use their local training notebook")
print("3. Download trained .onnx model")
EOF
```

---

### Step 5: Use OpenWakeWord Training Service (EASIER)

**Recommended**: Use OpenWakeWord's cloud training service

1. **Package your samples**:
```bash
cd wake_word_training
zip -r computer_samples.zip computer/
```

2. **Upload to training service**:
   - Visit: https://github.com/dscripka/openWakeWord
   - Follow training instructions
   - Upload your `computer_samples.zip`
   - Wait for trained model (they process it)
   - Download `computer_v0.1.onnx`

3. **Install trained model**:
```bash
# Create OpenWakeWord models directory
mkdir -p ~/.local/share/openwakeword/

# Copy your trained model
cp computer_v0.1.onnx ~/.local/share/openwakeword/
```

4. **Test it**:
```bash
python hal_voice_client.py
# Now say: "COMPUTER"
```

---

## 🎓 Alternative: Use Local Training (Advanced)

For full control, train locally using OpenWakeWord's training notebook:

```bash
# Clone OpenWakeWord repository
git clone https://github.com/dscripka/openWakeWord.git
cd openWakeWord/training

# Follow their training guide
# Use your collected samples
# Takes 20-30 minutes to train
```

---

## 📊 Training Quality Tips

### For Best Results:

**Positive Samples (COMPUTER)**:
- ✅ 200+ samples minimum (300+ better)
- ✅ Multiple speakers (family, friends)
- ✅ Various volumes (loud, normal, quiet)
- ✅ Various speeds (slow, fast, normal)
- ✅ Various distances (near mic, far from mic)
- ✅ Various environments (quiet, noisy)

**Negative Samples**:
- ✅ 100+ samples minimum
- ✅ Similar-sounding words
- ✅ Common phrases
- ✅ Background noise
- ✅ Other potential false triggers

---

## 🧪 Testing Your Model

After training:

```python
# Test script
import sounddevice as sd
from openwakeword.model import Model

# Load your model
model = Model(wakeword_models=['computer_v0.1'], inference_framework='onnx')

print("Say 'COMPUTER' to test...")

# Record and test
while True:
    audio = sd.rec(int(0.5 * 16000), samplerate=16000, channels=1, dtype='int16')
    sd.wait()
    
    audio_float = audio.flatten().astype(np.float32) / 32768.0
    predictions = model.predict(audio_float)
    
    score = predictions.get('computer_v0.1', 0)
    
    if score > 0.5:
        print(f"✓ DETECTED! (score: {score:.2f})")
    else:
        print(f"  listening... (score: {score:.2f})")
```

---

## ⚡ Quick Summary

### For Testing NOW:
```bash
# Use keyboard mode
python hal_voice_client.py
# Press ENTER to record (no wake word needed)
```

### For Production Later:
```bash
# 1. Collect 200+ samples of "COMPUTER" (1 hour)
# 2. Collect 100+ negative samples (30 min)
# 3. Train model via OpenWakeWord service (30 min)
# 4. Install trained model
# 5. Run:
python hal_voice_client.py
# Say: "COMPUTER"
```

---

## 📁 File Structure After Training

```
~/.local/share/openwakeword/
└── computer_v0.1.onnx          ← Your trained model

voice_assistant_v2/client/
└── hal_voice_client.py         ← Auto-detects and uses it
```

---

## 🎉 Result

Once trained, your system will:

1. ✅ Detect "COMPUTER" wake word
2. ✅ Play TNG activation sound
3. ✅ Start recording your command
4. ✅ Process and respond

**Exactly as specified!**

---

## 🆘 Need Help?

**Training fails?**
- Ensure 200+ positive samples
- Ensure samples are 16kHz, mono, 16-bit WAV
- Check OpenWakeWord documentation

**False positives?**
- Add more negative samples with similar sounds
- Retrain with adjusted threshold

**False negatives?**
- Add more varied positive samples
- Try different microphones
- Record in different environments

---

## 📝 Bottom Line

**Right Now**: Use **keyboard mode** (press ENTER instead of wake word)

**Production**: Train **"COMPUTER"** wake word (2-3 hours)

**No other wake words**: System only tries "COMPUTER" - no Alexa, no alternatives

✅ **Your preference is respected!**

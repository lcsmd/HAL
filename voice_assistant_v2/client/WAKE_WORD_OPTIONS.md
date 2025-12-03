# Wake Word Options for HAL Voice Client

**Goal**: Use "COMPUTER" as wake word

---

## 🎯 Quick Start (Working Prototype NOW)

### **Option 1: Use Keyboard Mode** (Recommended for Quick Start)

**Why**: "COMPUTER" wake word doesn't exist yet and must be trained

**How to use**:
```bash
# Client automatically uses keyboard mode if wake word not available
python hal_voice_client.py

# Press ENTER to record (no wake word needed)
```

**Benefits**:
- ✅ Works immediately (0 setup time)
- ✅ Tests entire system
- ✅ Train "COMPUTER" wake word in parallel

**Output**:
```
✓ Wake word loaded: alexa_v0.1
  🎤 Say: "ALEXA" (temporary - closest to "HAL")
  
  💡 NOTE: Using 'ALEXA' temporarily
     Custom 'HAL' wake word can be trained later
```

---

### **Option 2: Use "HEY JARVIS"**

**Why**: Longer phrase, more distinctive
- ✅ Pre-trained model
- ✅ Works immediately
- ✅ Good for testing

**How to use**:
```bash
export WAKE_WORD=hey_jarvis_v0.1
python hal_voice_client.py

# Say: "HEY JARVIS"
```

---

### **Option 3: Use "HEY MYCROFT"**

**Why**: Open-source assistant name
- ✅ Pre-trained model
- ✅ Works immediately

**How to use**:
```bash
export WAKE_WORD=hey_mycroft_v0.1
python hal_voice_client.py

# Say: "HEY MYCROFT"
```

---

## 🎓 Future: Train Custom "HAL" Wake Word

### Why Not Available Now?

OpenWakeWord doesn't have a pre-trained "HAL" model. Custom models need:
1. 200+ audio samples of different voices saying "HAL"
2. Background noise samples
3. Training time (~30 minutes)
4. Validation and testing

### Timeline for Custom "HAL"

**Immediate** (0 min): Use "ALEXA" temporarily ✅  
**Later** (2-3 hours): Train custom "HAL" model  

---

## 🛠️ How to Train Custom "HAL" Wake Word

### Prerequisites
```bash
pip install openwakeword-trainer
# Requires: microphone, ~200 voice samples, quiet room
```

### Step 1: Collect Audio Samples (1 hour)

Record yourself and others saying "HAL" in different ways:
```bash
# Create sample directory
mkdir -p wake_word_samples/hal/positive

# Record samples (need 200+)
python -c "
import sounddevice as sd
import wave
import numpy as np

for i in range(200):
    print(f'Sample {i+1}/200: Say HAL... (Press Enter)')
    input()
    print('Recording...')
    audio = sd.rec(int(1.5 * 16000), samplerate=16000, channels=1, dtype='int16')
    sd.wait()
    
    with wave.open(f'wake_word_samples/hal/positive/sample_{i:03d}.wav', 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(16000)
        wf.writeframes(audio.tobytes())
    print('Saved!')
"
```

### Step 2: Collect Negative Samples (30 min)

Background noise, other words, false positives:
```bash
mkdir -p wake_word_samples/hal/negative

# Record 100+ samples of:
# - Background noise
# - Similar words ("help", "hall", "hill")
# - Normal speech without "HAL"
# - Other wake words ("alexa", "hey")
```

### Step 3: Train Model (30 min)

```bash
# Train the model
openwakeword-trainer train \
    --positive-dir wake_word_samples/hal/positive \
    --negative-dir wake_word_samples/hal/negative \
    --output hal_v0.1.onnx

# Takes ~30 minutes depending on CPU/GPU
```

### Step 4: Use Custom Model

```bash
# Copy trained model to OpenWakeWord directory
cp hal_v0.1.onnx ~/.local/share/openwakeword/

# Use in client
export WAKE_WORD=hal_v0.1
python hal_voice_client.py
```

**Result**:
```
✓ Wake word loaded: hal_v0.1
  🎤 Say: "HAL"
```

---

## 📊 Comparison of Options

| Wake Word | Syllables | Availability | Setup Time | Recommended For |
|-----------|-----------|--------------|------------|-----------------|
| **ALEXA** | 3 (A-LEX-A) | ✅ Pre-trained | 0 min | **Quick prototype** ✅ |
| HEY JARVIS | 4 | ✅ Pre-trained | 0 min | Testing, demo |
| HEY MYCROFT | 4 | ✅ Pre-trained | 0 min | Alternative |
| **HAL** | 1 | ❌ Need training | 2-3 hrs | **Final product** |
| HEY HAL | 2 | ❌ Need training | 2-3 hrs | Alternative final |

---

## 🎯 Recommendation

### **For Working Prototype NOW:**

Use **"ALEXA"** temporarily:
```bash
python hal_voice_client.py
# Say: "ALEXA"
```

**Why**:
- ✅ Works immediately (0 setup time)
- ✅ Closest phonetically to "HAL"
- ✅ Can train custom "HAL" later without code changes

---

### **For Production Later:**

Train custom **"HAL"** model:
1. Collect 200+ voice samples (1 hour)
2. Train model (30 minutes)
3. Deploy (5 minutes)
4. Update environment: `export WAKE_WORD=hal_v0.1`

---

## 🔧 Configuration

### Change Wake Word (Easy!)

**Environment Variable**:
```bash
export WAKE_WORD=alexa_v0.1
python hal_voice_client.py
```

**Command Line**:
```bash
python hal_voice_client.py --wake-word alexa_v0.1
```

**In Code** (permanent change):

Edit `hal_voice_client.py` line ~70:
```python
wake_word_pref = os.getenv('WAKE_WORD', 'alexa_v0.1')  # Change default here
```

---

## 🎤 Available Pre-trained Models

Check available models:
```python
from openwakeword.model import Model
import openwakeword

# List available models
print(openwakeword.utils.get_pretrained_model_paths())
```

**Common models**:
- `alexa_v0.1` - "Alexa"
- `hey_jarvis_v0.1` - "Hey Jarvis"
- `hey_mycroft_v0.1` - "Hey Mycroft"
- `ok_naomi_v0.1` - "OK Naomi"
- `timer_v0.1` - "Timer" (single word example)

---

## 💡 Pro Tips

### Temporary Workaround

While using "ALEXA" temporarily, you can:
1. **Think of it as "HAL"** in your mind
2. **Train yourself** to say "Alexa" naturally
3. **Later swap** to custom "HAL" with one config change

### Better Alternatives to Consider

If "ALEXA" feels wrong:
- **"Hey Mycroft"** - Open source, 4 syllables
- **"OK Naomi"** - Different but works
- **Train "HAL"** - Takes 2-3 hours but perfect

---

## 📝 Summary

**Get working prototype NOW:**
```bash
# Use ALEXA (temporary)
python hal_voice_client.py
# Say: "ALEXA"
```

**Train custom HAL later:**
```bash
# 1. Collect samples (1 hour)
# 2. Train model (30 min)
# 3. Deploy
export WAKE_WORD=hal_v0.1
python hal_voice_client.py
# Say: "HAL"
```

---

## 🎉 Bottom Line

**For working prototype RIGHT NOW**: Use **"ALEXA"** ✅

**For final product**: Train custom **"HAL"** (2-3 hours total)

**Current code**: Already supports both! Just change one environment variable when ready.

---

**Recommendation**: Start with "ALEXA", get system working, train "HAL" later! 🚀

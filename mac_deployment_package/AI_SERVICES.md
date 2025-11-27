# HAL AI Services - GPU Server Configuration

## Overview

The HAL system uses a dedicated **GPU-powered AI server** (ubuai at 10.1.10.20) for compute-intensive AI tasks, providing minimal latency for real-time voice interaction and intelligent query processing.

---

## AI Server: ubuai (10.1.10.20)

### Hardware
- **GPU-equipped** server (NVIDIA/AMD)
- **Purpose**: Accelerated AI inference
- **Location**: 10.1.10.20
- **OS**: Ubuntu Linux
- **Username**: lawr

### Why GPU?
- ⚡ **10-100x faster** than CPU for AI inference
- 🎤 **Real-time voice processing** (<100ms latency)
- 🧠 **Large model support** (billions of parameters)
- 🔄 **Concurrent requests** handled efficiently

---

## Service 1: Faster-Whisper (STT)

### Speech-to-Text Transcription

**Port**: `9000`  
**Endpoint**: `http://10.1.10.20:9000/transcribe`  
**GPU Accelerated**: ✅ Yes

### What It Does
Converts spoken audio to text in real-time:
1. Mac client records audio
2. Audio sent to Faster-Whisper
3. GPU transcribes to text
4. Text returned to QM for processing

### Performance
- **Latency**: 50-200ms (with GPU)
- **Accuracy**: 95%+ for clear speech
- **Languages**: English primarily (configurable)
- **Model**: Whisper Large-v2 or similar

### API Example
```bash
curl -X POST http://10.1.10.20:9000/transcribe \
  -H "Content-Type: application/json" \
  -d '{
    "audio": "<base64_encoded_audio>",
    "language": "en",
    "task": "transcribe"
  }'
```

### Response
```json
{
  "text": "What medications am I taking?",
  "language": "en",
  "duration": 2.5,
  "processing_time": 0.15
}
```

### Used By
- Voice client (Mac) for voice queries
- QM WebSocket Listener for voice interface
- Any application needing STT

---

## Service 2: Ollama (LLM)

### Large Language Model Inference

**Port**: `11434`  
**Endpoint**: `http://10.1.10.20:11434/api/generate`  
**GPU Accelerated**: ✅ Yes

### What It Does
Provides AI-powered intelligent responses:
1. QM sends query/prompt to Ollama
2. LLM generates response
3. Response returned to QM
4. QM integrates with database results

### Available Models
Check installed models:
```bash
curl http://10.1.10.20:11434/api/tags
```

**Common models**:
- `deepseek-r1:32b` - Reasoning model
- `llama3:70b` - General purpose
- `codellama:34b` - Code generation
- `mistral:latest` - Fast inference
- `phi3:medium` - Lightweight

### Performance
- **Latency**: 100ms - 2s (depending on model size)
- **Throughput**: 20-50 tokens/second (GPU dependent)
- **Context**: 4k-32k tokens
- **Concurrent**: 2-4 requests (GPU memory limited)

### API Example
```bash
curl -X POST http://10.1.10.20:11434/api/generate \
  -H "Content-Type: application/json" \
  -d '{
    "model": "deepseek-r1:32b",
    "prompt": "Explain what EGPA is in simple terms.",
    "stream": false
  }'
```

### Response
```json
{
  "model": "deepseek-r1:32b",
  "created_at": "2025-11-27T12:00:00Z",
  "response": "EGPA (Eosinophilic Granulomatosis with Polyangiitis) is a rare autoimmune disease...",
  "done": true
}
```

### Used By
- QM for intelligent query responses
- Medical information explanations
- Natural language understanding
- Context-aware suggestions

### QM Integration
```qm
* Call Ollama from QM Basic
PROGRAM ASK.OLLAMA
   PROMPT = "What is hypertension?"
   MODEL = "deepseek-r1:32b"
   
   URL = "http://10.1.10.20:11434/api/generate"
   JSON = '{"model":"':MODEL:'","prompt":"':PROMPT:'","stream":false}'
   
   EXECUTE "curl -X POST ":URL:" -d '":JSON:"'" CAPTURING RESPONSE
   
   RESPONSE.OBJ = JPARSE(RESPONSE)
   ANSWER = RESPONSE.OBJ{"response"}
   
   PRINT ANSWER
END
```

---

## Service 3: TTS (Text-to-Speech)

### Status: Optional / To Be Configured

**Port**: TBD (commonly 5000 or 5002)  
**Options**:
- Coqui TTS
- ElevenLabs API
- OpenAI TTS API
- piper-tts (lightweight)

### If Configured on ubuai
Voice synthesis would happen on GPU server:
1. QM sends text response
2. GPU synthesizes natural voice
3. Audio returned to client
4. Client plays audio

### If NOT Configured
Voice synthesis happens on Mac client:
- Using local TTS (pyttsx3 or say command)
- Lower quality but no network latency
- No GPU required

### To Check if Running
```bash
ssh lawr@10.1.10.20
# Check for TTS service
ps aux | grep tts
netstat -tulpn | grep 5000
```

---

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                    AI Processing Flow                       │
└─────────────────────────────────────────────────────────────┘

Voice Query:
┌──────────────┐
│ Mac Client   │ Records audio
└──────┬───────┘
       │ Raw audio (WebSocket)
       ↓
┌──────────────┐
│ QM Server    │ Receives audio
└──────┬───────┘
       │ Forward to STT
       ↓
┌────────────────────────────┐
│ GPU Server (10.1.10.20)    │
│ ┌────────────────────────┐ │
│ │ Faster-Whisper (STT)   │ │ ← GPU accelerated
│ │ Port 9000              │ │
│ └────────┬───────────────┘ │
│          │ Transcribed text │
│          ↓                  │
└──────────┼──────────────────┘
           │
           ↓
┌──────────────┐
│ QM Server    │ Process intent, query DB
└──────┬───────┘
       │ Need AI explanation?
       ↓
┌────────────────────────────┐
│ GPU Server (10.1.10.20)    │
│ ┌────────────────────────┐ │
│ │ Ollama (LLM)           │ │ ← GPU accelerated
│ │ Port 11434             │ │
│ └────────┬───────────────┘ │
│          │ AI response      │
└──────────┼──────────────────┘
           │
           ↓
┌──────────────┐
│ QM Server    │ Format response
└──────┬───────┘
       │ Response text
       ↓
┌──────────────┐
│ Mac Client   │ Display/speak result
└──────────────┘
```

---

## Performance Characteristics

### With GPU (Current Setup)
| Task | CPU Time | GPU Time | Speedup |
|------|----------|----------|---------|
| STT (Whisper) | 5-10s | 0.1-0.5s | **20-50x** |
| LLM (deepseek-r1) | 30-60s | 1-3s | **20-30x** |
| TTS (if configured) | 2-5s | 0.2-0.5s | **10x** |

### End-to-End Latency
**Voice Query → Response**:
- Audio capture: 50ms
- Network to GPU: 10-20ms
- STT processing: 100-200ms
- QM processing: 50-100ms
- LLM (if needed): 1000-2000ms
- Network back: 10-20ms
- **Total**: 1.2-2.4 seconds

**Text Query → Response**:
- Network: 10ms
- QM processing: 50-100ms
- LLM (if needed): 1000-2000ms
- Network back: 10ms
- **Total**: 1.1-2.1 seconds

---

## Configuration Files

### On AI Server (10.1.10.20)

**Faster-Whisper Service**:
```bash
# Location: /etc/systemd/system/faster-whisper.service
[Unit]
Description=Faster-Whisper STT Service
After=network.target

[Service]
Type=simple
User=lawr
WorkingDirectory=/home/lawr/faster-whisper
ExecStart=/home/lawr/faster-whisper/venv/bin/python server.py
Restart=always

[Install]
WantedBy=multi-user.target
```

**Ollama Service**:
```bash
# Ollama is typically installed as systemd service
sudo systemctl status ollama
```

### Check Services
```bash
# SSH to AI server
ssh lawr@10.1.10.20

# Check Faster-Whisper
curl http://localhost:9000/

# Check Ollama
curl http://localhost:11434/api/tags

# Check GPU usage
nvidia-smi  # or rocm-smi for AMD
```

---

## Model Management

### List Installed Models
```bash
ssh lawr@10.1.10.20
curl http://localhost:11434/api/tags
```

### Pull New Model
```bash
ssh lawr@10.1.10.20
ollama pull deepseek-r1:32b
```

### Remove Model
```bash
ollama rm old-model:tag
```

### Model Storage
```bash
# Ollama models stored in:
~/.ollama/models/
# or
/usr/share/ollama/.ollama/models/
```

---

## QM Integration Examples

### Ask Ollama from QM
```qm
PROGRAM ASK.AI
   * Simple wrapper for Ollama queries
   PROMPT = @SENTENCE
   IF PROMPT = "" THEN
      INPUT "Ask: ": PROMPT
   END
   
   * Build JSON request
   JSON.OBJ = COLLECTION()
   JSON.OBJ{"model"} = "deepseek-r1:32b"
   JSON.OBJ{"prompt"} = PROMPT
   JSON.OBJ{"stream"} = 0
   
   JSON.REQ = JBUILD(JSON.OBJ)
   
   * Call Ollama API
   URL = "http://10.1.10.20:11434/api/generate"
   CMD = "curl -s -X POST ":URL:" -H 'Content-Type: application/json' -d '":JSON.REQ:"'"
   
   EXECUTE CMD CAPTURING OUTPUT
   
   * Parse response
   RESPONSE.OBJ = JPARSE(OUTPUT)
   ANSWER = RESPONSE.OBJ{"response"}
   
   PRINT ANSWER
END
```

### Transcribe Audio from QM
```qm
PROGRAM TRANSCRIBE.AUDIO
   AUDIO.FILE = @SENTENCE
   
   * Read audio file and encode base64
   OSREAD AUDIO.DATA FROM AUDIO.FILE ELSE
      PRINT "Error reading audio file"
      STOP
   END
   
   AUDIO.B64 = BASE64.ENCODE(AUDIO.DATA)
   
   * Build request
   JSON.OBJ = COLLECTION()
   JSON.OBJ{"audio"} = AUDIO.B64
   JSON.OBJ{"language"} = "en"
   JSON.OBJ{"task"} = "transcribe"
   
   JSON.REQ = JBUILD(JSON.OBJ)
   
   * Call Faster-Whisper
   URL = "http://10.1.10.20:9000/transcribe"
   CMD = "curl -s -X POST ":URL:" -H 'Content-Type: application/json' -d '":JSON.REQ:"'"
   
   EXECUTE CMD CAPTURING OUTPUT
   
   * Parse response
   RESPONSE.OBJ = JPARSE(OUTPUT)
   TEXT = RESPONSE.OBJ{"text"}
   
   PRINT "Transcribed: ":TEXT
END
```

---

## Monitoring

### GPU Utilization
```bash
# SSH to AI server
ssh lawr@10.1.10.20

# Watch GPU usage in real-time
watch -n 1 nvidia-smi

# Log GPU usage
nvidia-smi dmon -s u -i 0
```

### Service Health
```bash
# Check Faster-Whisper
curl http://10.1.10.20:9000/ || echo "STT down"

# Check Ollama
curl http://10.1.10.20:11434/api/tags || echo "Ollama down"

# Check from Mac
bash test_connection.sh
```

### Performance Logging
```bash
# Faster-Whisper logs
ssh lawr@10.1.10.20
tail -f /var/log/faster-whisper.log

# Ollama logs
journalctl -u ollama -f
```

---

## Troubleshooting

### GPU Not Being Used

**Check GPU availability**:
```bash
nvidia-smi
# or for AMD
rocm-smi
```

**Faster-Whisper GPU check**:
```bash
# Should show CUDA/ROCm device
curl http://10.1.10.20:9000/info
```

**Ollama GPU check**:
```bash
# Check model is using GPU
curl http://10.1.10.20:11434/api/ps
```

### High Latency

**Network latency**:
```bash
# From Mac
ping -c 10 10.1.10.20
# Should be <5ms on LAN
```

**GPU memory full**:
```bash
nvidia-smi
# Check memory usage
# May need to stop other processes or use smaller models
```

### Service Crashes

**Restart Faster-Whisper**:
```bash
ssh lawr@10.1.10.20
sudo systemctl restart faster-whisper
```

**Restart Ollama**:
```bash
sudo systemctl restart ollama
```

---

## Best Practices

1. ✅ **Keep models loaded** - First query is slower (model load time)
2. ✅ **Monitor GPU memory** - Don't run too many large models
3. ✅ **Use appropriate model sizes** - Balance speed vs. quality
4. ✅ **Cache frequent queries** - Store common AI responses in QM
5. ✅ **Timeout handling** - Set reasonable timeouts (10-30 seconds)
6. ✅ **Fallback logic** - Have CPU fallback if GPU unavailable
7. ✅ **Regular updates** - Keep Ollama and models updated

---

## Summary

The **ubuai GPU server (10.1.10.20)** provides:

✅ **Faster-Whisper (Port 9000)** - Real-time voice transcription  
✅ **Ollama (Port 11434)** - AI language model inference  
⚙️ **TTS (Optional)** - Voice synthesis if configured  

**All GPU-accelerated for minimal latency and real-time voice interaction!**

Your HAL system leverages GPU power for:
- Sub-second voice transcription
- Intelligent AI responses
- Natural conversation flow
- Multi-modal AI capabilities

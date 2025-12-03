# Voice Assistant System v2

A complete voice-activated personal assistant system with three components:
- **Client** (Mac/PC) - Voice interface with wake word detection
- **Voice Server** (Ubuntu/GPU) - STT/TTS processing with Faster-Whisper
- **AI Server** (Windows/OpenQM) - Logic processing and database

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      VOICE ASSISTANT                         │
└─────────────────────────────────────────────────────────────┘

┌──────────────┐   WebSocket (8585)   ┌──────────────┐
│    Client    │ ───────────────────> │Voice Server  │
│  (Mac/PC)    │ <─────────────────── │  (Ubuntu)    │
│              │      Audio/TTS       │   GPU/STT    │
└──────────────┘                      └──────┬───────┘
     │                                       │
     │ Wake Word                             │ WebSocket (8745)
     │ Detection                             │ Text/JSON
     │                                       ▼
     │                                ┌──────────────┐
     └────────────────────────────────│  AI Server   │
                                      │   (OpenQM)   │
                                      │   Windows    │
                                      └──────────────┘
```

## Network Configuration

| Component | IP Address | Port | Protocol |
|-----------|------------|------|----------|
| Client | Various | - | - |
| Voice Server | 10.1.10.20 | 8585 | WebSocket |
| AI Server | 10.1.34.103 | 8745 | WebSocket |

## Components

### 1. Client (Mac/PC)

**Location:** `client/`

**Purpose:** User interface with voice interaction

**Features:**
- Wake word detection ("HEY JARVIS" - works immediately)
  - Pre-trained model, no setup needed
  - Optional: Switch to "COMPUTER" later (requires 2-3 hours training)
  - See `client/TRAIN_COMPUTER_WAKE_WORD.md` for custom training
- Multiple listening modes: PLM, ALM, ASM, RLM
- Audio recording and streaming
- Interrupt commands (say wake word again)
- Auto-start at system boot
- Minimal resource usage

**Key Files:**
- `voice_client.py` - Main client program
- `voice_client.config` - Configuration file
- `setup_mac.sh` - Mac setup script
- `activation_sound.wav` - Wake word confirmation sound
- `acknowledgement_sound.wav` - Recording complete sound

**Configuration:** Edit `voice_client.config`:
```ini
[client]
client_id = mac_office_01
default_user_id = lawr
default_wake_words = computer,hey assistant

[server]
voice_server_url = ws://10.1.10.20:8585
```

**Setup:**
```bash
cd client/
./setup_mac.sh
```

**Run:**
```bash
source venv/bin/activate
python voice_client.py
```

**Auto-start:**
```bash
./setup_launchagent.sh
```

### 2. Voice Server (Ubuntu/GPU)

**Location:** `voice_server/`

**Purpose:** STT/TTS processing with GPU acceleration

**Features:**
- Faster-Whisper GPU-accelerated STT (large-v3 model)
- WebSocket server for clients (port 8585)
- WebSocket client to AI server (port 8745)
- Audio transcription and synthesis
- Session management

**Key Files:**
- `voice_server.py` - Main server program
- `setup_ubuntu.sh` - Ubuntu setup script
- `requirements.txt` - Python dependencies

**Requirements:**
- Ubuntu Linux (20.04+ recommended)
- NVIDIA GPU with CUDA support (optional but recommended)
- Python 3.8+
- 8GB+ RAM
- 10GB+ disk space (for model)

**Setup:**
```bash
cd voice_server/
sudo ./setup_ubuntu.sh
```

**Start:**
```bash
sudo systemctl start voice-server
```

**Enable auto-start:**
```bash
sudo systemctl enable voice-server
```

**View logs:**
```bash
journalctl -u voice-server -f
```

### 3. AI Server (Windows/OpenQM)

**Location:** `ai_server/`

**Purpose:** Logic processing and database operations

**Features:**
- OpenQM BASIC phantom process
- Native WebSocket support (port 8745)
- Intent detection and routing
- Database operations
- Session and log management

**Key Files:**
- `AI.SERVER` - QM BASIC program
- `setup_windows.ps1` - Windows setup script (PowerShell)
- `start_ai_server.bat` - Start script
- `stop_ai_server.bat` - Stop script
- `view_logs.bat` - View logs script

**Requirements:**
- Windows Server (or Windows 10/11)
- OpenQM installed
- HAL account configured
- Administrator access

**Setup:**
```powershell
# Run as Administrator
cd ai_server\
.\setup_windows.ps1
```

**Start:**
```batch
start_ai_server.bat
```

**Check status:**
```batch
status_ai_server.bat
```

**View logs:**
```batch
view_logs.bat
```

## Listening Modes

The client operates in four distinct modes:

### 1. Passive Listening Mode (PLM)
- **State:** Waiting for wake word
- **Action:** Monitors microphone for wake word only
- **Next:** Switches to ALM when wake word detected

### 2. Active Listening Mode (ALM)
- **State:** Recording user command
- **Trigger:** Wake word detected OR sound in RLM
- **Action:** 
  - Plays activation sound
  - Records audio (starts after 1 second of sound)
  - Streams to voice server
  - Stops after 3 seconds of silence or "OK"
- **Interrupt:** "belay that" cancels recording
- **Next:** Switches to RLM after recording

### 3. Response Listening Mode (RLM)
- **State:** Waiting for follow-up or server response
- **Duration:** 10 seconds of silence
- **Action:**
  - Listens for audio from voice server
  - Monitors for user speech
- **Next:** 
  - ALM if user speaks (1+ second sound)
  - PLM after 10 seconds of silence
  - ASM if audio received from server

### 4. Active Speaking Mode (ASM)
- **State:** Playing audio response
- **Action:**
  - Plays TTS audio from server
  - Monitors for "wake_word stop" command
- **Interrupt:** "wake_word stop" stops playback
- **Next:** RLM after playback complete

## Data Flow

### Example Interaction

```
[PLM] User: "computer"
      ↓
[ALM] Client: *plays activation sound*
      Client: *recording*
      User: "what time is it?"
      User: *3 seconds silence*
      ↓
      Client: *plays acknowledgement sound*
      Client: → Voice Server (audio stream)
      ↓
      Voice Server: → Faster-Whisper (STT)
      Voice Server: "what time is it?" → AI Server
      ↓
      AI Server: Process text
      AI Server: "The current time is 3:30 PM" → Voice Server
      ↓
      Voice Server: → TTS (generate audio)
      Voice Server: → Client (audio stream)
      ↓
[ASM] Client: *plays "The current time is 3:30 PM"*
      ↓
[RLM] *10 second timer*
      User: "and what's the date?"
      ↓
[ALM] *continues conversation...*
```

## Deployment

### Step 1: Deploy AI Server (Windows)

```powershell
# On Windows OpenQM server (10.1.34.103)
cd C:\qmsys\hal\voice_assistant_v2\ai_server
.\setup_windows.ps1 -AutoStart
```

### Step 2: Deploy Voice Server (Ubuntu)

```bash
# On Ubuntu GPU server (10.1.10.20)
cd /path/to/voice_assistant_v2/voice_server
sudo ./setup_ubuntu.sh
sudo systemctl enable voice-server
sudo systemctl start voice-server
```

### Step 3: Deploy Client (Mac)

```bash
# On each Mac client
cd /path/to/voice_assistant_v2/client
./setup_mac.sh

# Edit configuration
nano voice_client.config

# Run client
source venv/bin/activate
python voice_client.py

# Optional: Setup auto-start
./setup_launchagent.sh
```

## Testing

### Test 1: Check AI Server
```powershell
# On Windows
status_ai_server.bat
# Should show port 8745 listening
```

### Test 2: Check Voice Server
```bash
# On Ubuntu
sudo systemctl status voice-server
# Should show "active (running)"

# Check logs
journalctl -u voice-server -n 50
```

### Test 3: Test Client
```bash
# On Mac
cd client/
source venv/bin/activate

# Create wake trigger (since real wake word detection needs pvporcupine)
touch .wake_trigger

# Check client logs
python voice_client.py
```

### Test 4: End-to-End Test
1. Start AI server on Windows
2. Start voice server on Ubuntu
3. Start client on Mac
4. Say wake word: "computer"
5. Say command: "what time is it?"
6. Wait for response

## Troubleshooting

### Client Issues

**Problem:** PyAudio installation fails on Mac
```bash
# Install PortAudio first
brew install portaudio
pip install pyaudio
```

**Problem:** Wake word not detecting
- Current implementation uses file trigger for testing
- For production, integrate pvporcupine or similar
- Create `.wake_trigger` file to simulate wake word

**Problem:** Can't connect to voice server
- Check voice server is running: `sudo systemctl status voice-server`
- Check network connectivity: `ping 10.1.10.20`
- Check firewall: `sudo ufw status`

### Voice Server Issues

**Problem:** CUDA not found
```bash
# Install CUDA toolkit
# See: https://developer.nvidia.com/cuda-downloads

# Or use CPU mode (slower)
# Edit voice_server.py: WHISPER_DEVICE = "cpu"
```

**Problem:** Model download fails
- Check internet connection
- May need to download manually and place in cache
- Cache location: `~/.cache/huggingface/`

**Problem:** Can't connect to AI server
- Check AI server is running: `status_ai_server.bat`
- Check network: `ping 10.1.34.103`
- Check port: `netstat -an | findstr 8745`

### AI Server Issues

**Problem:** Compilation errors
```
# Check QM BASIC syntax
# Run in QM:
LOGTO HAL
ED BP AI.SERVER
# Fix syntax errors
BASIC BP AI.SERVER
CATALOG BP AI.SERVER
```

**Problem:** Phantom process not starting
```
# Check if already running
tasklist | findstr qm.exe

# Kill existing phantom
taskkill /F /IM qm.exe

# Restart
start_ai_server.bat
```

**Problem:** Port 8745 already in use
```
# Check what's using the port
netstat -ano | findstr 8745

# Kill the process
taskkill /F /PID <pid>
```

## Development

### Adding New Intent Handlers

Edit `ai_server/AI.SERVER`:

```basic
SUBROUTINE PROCESS.USER.INPUT(USER.ID, INPUT.TEXT, RESPONSE.TEXT, VOICE.ID, VOLUME)
   INPUT.LOWER = DOWNCASE(INPUT.TEXT)
   
   BEGIN CASE
      CASE INDEX(INPUT.LOWER, 'your_keyword', 1)
         CALL HANDLE.YOUR.FEATURE(USER.ID, INPUT.TEXT, RESPONSE.TEXT)
      
      * ... existing cases ...
   END CASE
   
   RETURN
END

SUBROUTINE HANDLE.YOUR.FEATURE(USER.ID, INPUT.TEXT, RESPONSE.TEXT)
   * Your logic here
   RESPONSE.TEXT = 'Your response'
   RETURN
END
```

Recompile:
```
LOGTO HAL
BASIC BP AI.SERVER
CATALOG BP AI.SERVER
```

Restart phantom process.

### Adding TTS Integration

Edit `voice_server/voice_server.py`:

```python
async def text_to_speech(self, text: str, voice_id: str = "default", 
                        volume: float = 1.0) -> bytes:
    # Integrate your TTS service here
    # Options:
    # - Piper TTS (local, fast)
    # - Coqui TTS (local, customizable)
    # - ElevenLabs API (cloud, high quality)
    # - Azure TTS (cloud, multiple voices)
    
    # Return WAV audio bytes
    return audio_bytes
```

### Implementing Real Wake Word Detection

Replace keyboard trigger with pvporcupine:

```bash
cd client/
source venv/bin/activate
pip install pvporcupine
```

Edit `voice_client.py`:
```python
import pvporcupine

def detect_wake_word(self, audio_chunk):
    # Use pvporcupine for real wake word detection
    keyword_index = porcupine.process(audio_chunk)
    if keyword_index >= 0:
        return True
    return False
```

## Performance

### Expected Latency

- Wake word detection: <100ms
- Audio streaming: Real-time
- STT (GPU): 1-2 seconds
- AI processing: <100ms
- TTS: 0.5-1 second
- **Total**: 2-4 seconds end-to-end

### Resource Usage

**Client:**
- CPU: <5%
- RAM: <100 MB
- Network: Minimal (audio streaming only)

**Voice Server:**
- CPU: 10-20% (idle), 50-80% (transcribing)
- GPU: 20-40% (large-v3 model)
- RAM: 4-6 GB (model + buffers)
- Disk: 10 GB (model storage)

**AI Server:**
- CPU: <5%
- RAM: OpenQM process memory
- Disk: Minimal (logs and sessions)

## Security

### Current Implementation
- No authentication (trusted network only)
- Plain WebSocket (no TLS/SSL)
- Suitable for private network only

### Production Recommendations
1. Use WSS (WebSocket Secure) with TLS certificates
2. Add authentication tokens
3. Implement rate limiting
4. Add VPN or firewall rules
5. Encrypt sensitive data in transit and at rest

## License

See LICENSE file

## Authors

Voice Assistant System v2
Created: 2025-12-03

## Support

For issues or questions, refer to the troubleshooting section above.

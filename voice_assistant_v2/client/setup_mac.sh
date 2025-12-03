#!/bin/bash
#
# Setup script for HAL Voice Client - Unified System (Mac)
# Sets up Python environment and copies sound files
#

set -e

echo "============================================"
echo "HAL Voice Client - Unified Setup (Mac)"
echo "============================================"
echo ""

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Check Python version
echo "[1/8] Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 not found. Please install Python 3.8 or later."
    exit 1
fi

PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
echo "Found Python $PYTHON_VERSION"

# Create virtual environment
echo ""
echo "[2/8] Creating virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "Virtual environment created"
else
    echo "Virtual environment already exists"
fi

# Activate virtual environment
echo ""
echo "[3/8] Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo ""
echo "[4/8] Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo ""
echo "[5/8] Installing Python dependencies..."
pip install numpy sounddevice webrtcvad simpleaudio websockets openwakeword

# Install PortAudio (required for pyaudio on Mac)
echo ""
echo "[6/8] Checking PortAudio..."
if ! brew list portaudio &> /dev/null; then
    echo "Installing PortAudio via Homebrew..."
    if ! command -v brew &> /dev/null; then
        echo "WARNING: Homebrew not found. Please install Homebrew first:"
        echo "  /bin/bash -c \"\$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\""
        echo ""
        echo "Then run: brew install portaudio"
        echo ""
    else
        brew install portaudio
    fi
else
    echo "PortAudio already installed"
fi

# Copy config file if it doesn't exist
echo ""
echo "[7/8] Setting up configuration..."
if [ ! -f "voice_client.config" ]; then
    echo "ERROR: voice_client.config not found!"
    echo "Please ensure voice_client.config is in the same directory as this script"
    exit 1
fi

# Copy sound files from existing clients directory
echo ""
echo "[8/8] Setting up sound files..."

# Determine the path to the clients directory
# Assume it's at ../../clients relative to voice_assistant_v2/client
CLIENTS_DIR="$SCRIPT_DIR/../../clients"

if [ -d "$CLIENTS_DIR" ]; then
    # Copy activation sound (TNG Star Trek sound)
    if [ -f "$CLIENTS_DIR/activation.mp3" ]; then
        cp "$CLIENTS_DIR/activation.mp3" activation.mp3
        echo "✓ Copied activation.mp3 (TNG Star Trek sound)"
    else
        echo "⚠ WARNING: activation.mp3 not found in clients directory"
        echo "  Expected at: $CLIENTS_DIR/activation.mp3"
    fi
    
    # Copy acknowledgement sound
    if [ -f "$CLIENTS_DIR/acknowledgement.wav" ]; then
        cp "$CLIENTS_DIR/acknowledgement.wav" acknowledgement.wav
        echo "✓ Copied acknowledgement.wav"
    elif [ -f "$CLIENTS_DIR/ack.wav" ]; then
        cp "$CLIENTS_DIR/ack.wav" acknowledgement.wav
        echo "✓ Copied ack.wav → acknowledgement.wav"
    else
        echo "⚠ WARNING: acknowledgement.wav not found in clients directory"
    fi
else
    echo "⚠ WARNING: Clients directory not found at $CLIENTS_DIR"
    echo "  Attempting to use generate_sounds.py if available..."
    
    # Try to use generate_sounds.py from clients
    if [ -f "$CLIENTS_DIR/generate_sounds.py" ]; then
        python3 "$CLIENTS_DIR/generate_sounds.py"
    else
        echo "  Generating basic placeholder sounds..."
        python3 -c "
import wave
import struct
import math

def generate_beep(filename, frequency, duration, sample_rate=16000):
    with wave.open(filename, 'w') as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(sample_rate)
        
        for i in range(int(duration * sample_rate)):
            value = int(32767 * 0.3 * math.sin(2 * math.pi * frequency * i / sample_rate))
            data = struct.pack('<h', value)
            wav_file.writeframes(data)

# Create basic beep as WAV (not MP3)
generate_beep('activation.wav', 800, 0.1)
generate_beep('acknowledgement.wav', 600, 0.1)
print('Generated basic placeholder sound files')
"
        # Update config to use .wav instead of .mp3
        sed -i.bak 's/activation.mp3/activation.wav/' voice_client.config
    fi
fi

echo ""
echo "============================================"
echo "Setup Complete!"
echo "============================================"
echo ""
echo "Configuration file: voice_client.config"
echo "Python script: voice_client.py"
echo ""
echo "To start the client:"
echo "  source venv/bin/activate"
echo "  python voice_client.py"
echo ""
echo "To run at system boot, create a LaunchAgent:"
echo "  See setup_launchagent.sh"
echo ""

# Create LaunchAgent setup script
cat > setup_launchagent.sh << 'EOF'
#!/bin/bash
# Setup LaunchAgent for auto-start at login

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PLIST_FILE="$HOME/Library/LaunchAgents/com.voice.assistant.client.plist"

cat > "$PLIST_FILE" << PLIST
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.voice.assistant.client</string>
    <key>ProgramArguments</key>
    <array>
        <string>$SCRIPT_DIR/venv/bin/python</string>
        <string>$SCRIPT_DIR/voice_client.py</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
    <key>WorkingDirectory</key>
    <string>$SCRIPT_DIR</string>
    <key>StandardOutPath</key>
    <string>$HOME/Library/Logs/voice_client.log</string>
    <key>StandardErrorPath</key>
    <string>$HOME/Library/Logs/voice_client_error.log</string>
</dict>
</plist>
PLIST

launchctl load "$PLIST_FILE"

echo "LaunchAgent installed and loaded"
echo "The client will now start automatically at login"
echo ""
echo "To stop: launchctl stop com.voice.assistant.client"
echo "To unload: launchctl unload $PLIST_FILE"
EOF

chmod +x setup_launchagent.sh

echo "Run ./setup_launchagent.sh to enable auto-start at login"
echo ""

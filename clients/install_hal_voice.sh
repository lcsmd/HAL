#!/bin/bash
# HAL Voice Client Installer - One-line installation
# Usage: curl -fsSL http://10.1.34.103:8080/install_hal_voice.sh | HAL_SERVER_URL=http://10.1.34.103:8768 bash

set -e

# Get server URL from environment or prompt
HAL_SERVER_URL="${HAL_SERVER_URL:-}"
PORCUPINE_KEY="${PORCUPINE_ACCESS_KEY:-}"

if [ -z "$HAL_SERVER_URL" ]; then
    echo -n "Enter HAL Server URL (e.g., http://10.1.34.103:8768): "
    read HAL_SERVER_URL
fi

# Convert to WebSocket URL
GATEWAY_URL=$(echo "$HAL_SERVER_URL" | sed 's|^http://|ws://|' | sed 's|^https://|wss://|')

# Get installer server from HAL_SERVER_URL
INSTALLER_HOST=$(echo "$HAL_SERVER_URL" | sed 's|http://||' | sed 's|https://||' | cut -d: -f1)
INSTALLER_URL="http://${INSTALLER_HOST}:8080"

echo "=========================================="
echo "HAL Voice Client Installation"
echo "=========================================="
echo ""
echo "Server: $HAL_SERVER_URL"
echo "Gateway: $GATEWAY_URL"
echo ""

# Check Python
echo "[1/6] Checking Python..."
if ! command -v python3 &> /dev/null; then
    echo "✗ Python 3 required: https://www.python.org/downloads/"
    exit 1
fi
echo "  ✓ $(python3 --version)"

# Install dependencies
echo ""
echo "[2/6] Installing dependencies..."
echo "  (This may take a few minutes on first install)"

# Check for PortAudio on Mac
if [[ "$OSTYPE" == "darwin"* ]]; then
    if ! command -v brew &> /dev/null; then
        echo "  ⚠ Homebrew not found. Install from: https://brew.sh"
        echo "  ⚠ Then run: brew install portaudio"
    else
        if ! brew list portaudio &> /dev/null; then
            echo "  Installing portaudio..."
            brew install portaudio
        fi
    fi
fi

pip3 install --user --quiet pyaudio pvporcupine openai-whisper 2>&1 | grep -v "already satisfied" || true
echo "  ✓ Dependencies installed"

# Create installation directory
echo ""
echo "[3/6] Setting up directories..."
INSTALL_DIR="$HOME/.hal-voice"
mkdir -p "$INSTALL_DIR/VOICE/SOUNDS"
echo "  ✓ $INSTALL_DIR"

# Download voice client
echo ""
echo "[4/6] Downloading voice client..."
curl -fsSL "$INSTALLER_URL/hal_voice_client.py" -o "$INSTALL_DIR/hal_voice_client.py"
chmod +x "$INSTALL_DIR/hal_voice_client.py"
echo "  ✓ Voice client downloaded"

# Download TNG activation sound
echo ""
echo "[5/6] Downloading TNG activation sound..."
curl -fsSL "$INSTALLER_URL/ack.wav" -o "$INSTALL_DIR/VOICE/SOUNDS/ack.wav"
echo "  ✓ TNG sound installed (ack.wav)"

# Create configuration
echo ""
echo "[6/6] Creating configuration..."

cat > "$INSTALL_DIR/.env" << EOF
HAL_GATEWAY_URL=$GATEWAY_URL
HAL_SERVER_URL=$HAL_SERVER_URL
PORCUPINE_ACCESS_KEY=$PORCUPINE_KEY
WHISPER_MODEL=base
EOF

# Create launcher script
cat > "$INSTALL_DIR/hal-voice" << 'LAUNCHEREOF'
#!/bin/bash
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"
source "$SCRIPT_DIR/.env"
export HAL_GATEWAY_URL
export PORCUPINE_ACCESS_KEY
export WHISPER_MODEL
python3 "$SCRIPT_DIR/hal_voice_client.py" "$@"
LAUNCHEREOF

chmod +x "$INSTALL_DIR/hal-voice"

# Add to PATH if not already there
SHELL_RC=""
if [ -f "$HOME/.zshrc" ]; then
    SHELL_RC="$HOME/.zshrc"
elif [ -f "$HOME/.bashrc" ]; then
    SHELL_RC="$HOME/.bashrc"
elif [ -f "$HOME/.bash_profile" ]; then
    SHELL_RC="$HOME/.bash_profile"
fi

if [ -n "$SHELL_RC" ]; then
    if ! grep -q ".hal-voice" "$SHELL_RC"; then
        echo "" >> "$SHELL_RC"
        echo "# HAL Voice Client" >> "$SHELL_RC"
        echo "export PATH=\"\$HOME/.hal-voice:\$PATH\"" >> "$SHELL_RC"
        echo "  ✓ Added to PATH in $SHELL_RC"
    fi
fi

echo "  ✓ Configuration saved"

echo ""
echo "=========================================="
echo "Installation Complete!"
echo "=========================================="
echo ""

# Check if Porcupine key is set
if [ -z "$PORCUPINE_KEY" ]; then
    echo "⚠ PORCUPINE_ACCESS_KEY not set"
    echo ""
    echo "To enable wake word detection:"
    echo "  1. Get free key: https://console.picovoice.ai/"
    echo "  2. Add to ~/.hal-voice/.env:"
    echo "     PORCUPINE_ACCESS_KEY=your-key-here"
    echo ""
    echo "Without this key, you'll use keyboard mode (press ENTER to record)"
    echo ""
fi

echo "To start HAL Voice Client:"
echo "  1. Restart your terminal (or run: source $SHELL_RC)"
echo "  2. Type: hal-voice"
echo ""
echo "Or run directly:"
echo "  $INSTALL_DIR/hal-voice"
echo ""
echo "Voice Mode:"
echo "  - Say 'Computer' to activate"
echo "  - 🔊 Hear TNG activation sound"
echo "  - Speak your query"
echo "  - Get HAL's response"
echo ""
echo "Text Mode (testing):"
echo "  hal-voice --query \"What medications am I taking?\""
echo ""
echo "Configuration: $INSTALL_DIR/.env"
echo ""
echo "Live long and prosper! 🖖"
echo ""

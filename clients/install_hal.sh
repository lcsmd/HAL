#!/bin/bash
# HAL Client Installer - Unified (Voice + Text)
# One-line: curl -fsSL http://10.1.34.103:8080/install_hal.sh -o /tmp/hal_install.sh && HAL_SERVER_URL=http://10.1.34.103:8768 bash /tmp/hal_install.sh

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
echo "HAL Client Installation (Voice + Text)"
echo "=========================================="
echo ""
echo "Server: $HAL_SERVER_URL"
echo "Gateway: $GATEWAY_URL"
echo ""

# Check Python
echo "[1/7] Checking Python..."
if ! command -v python3 &> /dev/null; then
    echo "✗ Python 3 required: https://www.python.org/downloads/"
    exit 1
fi
echo "  ✓ $(python3 --version)"

# Install base dependencies
echo ""
echo "[2/7] Installing base dependencies..."
pip3 install --user --quiet websockets 2>&1 | grep -v "already satisfied" || true
echo "  ✓ websockets installed"

# Install voice dependencies (optional)
echo ""
echo "[3/7] Installing voice dependencies..."
echo "  (This may take a few minutes on first install)"

# Check for PortAudio on Mac
VOICE_AVAILABLE=true
if [[ "$OSTYPE" == "darwin"* ]]; then
    if command -v brew &> /dev/null; then
        if ! brew list portaudio &> /dev/null 2>&1; then
            echo "  Installing portaudio..."
            brew install portaudio 2>&1 | tail -1
        fi
    else
        echo "  ⚠ Homebrew not found. Skipping voice dependencies."
        echo "    For voice support: install Homebrew, then run: brew install portaudio"
        VOICE_AVAILABLE=false
    fi
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    if ! dpkg -l | grep -q portaudio19-dev 2>&1; then
        echo "  ⚠ portaudio19-dev not found."
        echo "    For voice support: sudo apt-get install portaudio19-dev"
        VOICE_AVAILABLE=false
    fi
fi

if [ "$VOICE_AVAILABLE" = true ]; then
    if pip3 install --user --quiet pyaudio openwakeword openai-whisper numpy 2>&1 | grep -v "already satisfied"; then
        echo "  ✓ Voice dependencies installed (pyaudio, openwakeword, whisper)"
    else
        echo "  ⚠ Voice dependencies may have failed. Voice mode may not work."
        VOICE_AVAILABLE=false
    fi
else
    echo "  ⚠ Skipping voice dependencies (optional)"
fi

# Create installation directory
echo ""
echo "[4/7] Setting up directories..."
INSTALL_DIR="$HOME/.hal-client"
mkdir -p "$INSTALL_DIR/VOICE/SOUNDS"
echo "  ✓ $INSTALL_DIR"

# Download text client
echo ""
echo "[5/7] Downloading text client..."
cat > "$INSTALL_DIR/hal_text_client.py" << 'TEXTCLIENTEOF'
#!/usr/bin/env python3
"""HAL Text Client"""
import asyncio
import websockets
import json
import sys
import os

GATEWAY_URL = os.getenv('HAL_GATEWAY_URL', 'ws://localhost:8768')

class HALClient:
    def __init__(self, gateway_url):
        self.gateway_url = gateway_url
        self.session_id = None
        self.websocket = None
        
    async def connect(self):
        try:
            self.websocket = await websockets.connect(self.gateway_url)
            response = await self.websocket.recv()
            data = json.loads(response)
            if data.get('type') == 'connected':
                self.session_id = data.get('session_id')
                return True
            return False
        except Exception as e:
            print(f"✗ Connection failed: {e}")
            return False
    
    async def send_text_query(self, text):
        if not self.websocket:
            return None
        try:
            message = {'type': 'text_input', 'text': text, 'session_id': self.session_id}
            await self.websocket.send(json.dumps(message))
            while True:
                response = await asyncio.wait_for(self.websocket.recv(), timeout=30.0)
                data = json.loads(response)
                if data.get('type') == 'response':
                    print(f"\n{data.get('text', '')}")
                    return data.get('text')
                elif data.get('type') == 'processing':
                    pass
        except Exception as e:
            print(f"✗ Error: {e}")
            return None
    
    async def interactive_mode(self):
        print("\nHAL Text Client - Interactive Mode")
        print("(Type 'quit' to exit)\n")
        while True:
            try:
                query = input("You: ").strip()
                if not query:
                    continue
                if query.lower() in ['quit', 'exit', 'q']:
                    break
                await self.send_text_query(query)
            except KeyboardInterrupt:
                break
    
    async def close(self):
        if self.websocket:
            await self.websocket.close()

async def main():
    import argparse
    parser = argparse.ArgumentParser(description='HAL Text Client')
    parser.add_argument('--url', default=GATEWAY_URL, help='Gateway URL')
    parser.add_argument('--query', help='Single query')
    args = parser.parse_args()
    
    client = HALClient(args.url)
    if not await client.connect():
        return 1
    try:
        if args.query:
            await client.send_text_query(args.query)
        else:
            await client.interactive_mode()
    finally:
        await client.close()
    return 0

if __name__ == '__main__':
    try:
        sys.exit(asyncio.run(main()))
    except KeyboardInterrupt:
        sys.exit(0)
TEXTCLIENTEOF

chmod +x "$INSTALL_DIR/hal_text_client.py"
echo "  ✓ Text client installed"

# Download voice client
echo ""
echo "[6/7] Downloading voice client..."
if curl -fsSL "$INSTALLER_URL/hal_voice_client.py" -o "$INSTALL_DIR/hal_voice_client.py" 2>/dev/null; then
    chmod +x "$INSTALL_DIR/hal_voice_client.py"
    echo "  ✓ Voice client installed"
    
    # Download TNG activation sound
    if curl -fsSL "$INSTALLER_URL/ack.wav" -o "$INSTALL_DIR/VOICE/SOUNDS/ack.wav" 2>/dev/null; then
        echo "  ✓ TNG activation sound installed"
    else
        echo "  ⚠ Could not download TNG sound (will use fallback)"
    fi
else
    echo "  ⚠ Could not download voice client (text mode will still work)"
    VOICE_AVAILABLE=false
fi

# Create configuration
echo ""
echo "[7/7] Creating configuration..."

cat > "$INSTALL_DIR/.env" << EOF
HAL_GATEWAY_URL=$GATEWAY_URL
HAL_SERVER_URL=$HAL_SERVER_URL
WAKE_WORD_MODEL=hey_jarvis
WHISPER_MODEL=base
EOF

# Create unified launcher script
cat > "$INSTALL_DIR/hal" << 'LAUNCHEREOF'
#!/bin/bash
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"
source "$SCRIPT_DIR/.env"
export HAL_GATEWAY_URL
export WAKE_WORD_MODEL
export WHISPER_MODEL

# Check if voice mode requested
USE_VOICE=false
for arg in "$@"; do
    if [ "$arg" = "--voice" ] || [ "$arg" = "-v" ]; then
        USE_VOICE=true
    fi
done

if [ "$USE_VOICE" = true ]; then
    if [ -f "$SCRIPT_DIR/hal_voice_client.py" ]; then
        # Remove --voice flag from args
        ARGS=()
        for arg in "$@"; do
            if [ "$arg" != "--voice" ] && [ "$arg" != "-v" ]; then
                ARGS+=("$arg")
            fi
        done
        python3 "$SCRIPT_DIR/hal_voice_client.py" "${ARGS[@]}"
    else
        echo "✗ Voice client not installed. Run text mode instead."
        python3 "$SCRIPT_DIR/hal_text_client.py" "$@"
    fi
else
    python3 "$SCRIPT_DIR/hal_text_client.py" "$@"
fi
LAUNCHEREOF

chmod +x "$INSTALL_DIR/hal"

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
    if ! grep -q ".hal-client" "$SHELL_RC"; then
        echo "" >> "$SHELL_RC"
        echo "# HAL Client" >> "$SHELL_RC"
        echo "export PATH=\"\$HOME/.hal-client:\$PATH\"" >> "$SHELL_RC"
        echo "  ✓ Added to PATH in $SHELL_RC"
    fi
fi

echo "  ✓ Configuration saved"

echo ""
echo "=========================================="
echo "Installation Complete!"
echo "=========================================="
echo ""

# Show what's available
echo "Installed Modes:"
echo "  ✓ Text mode (always available)"
if [ "$VOICE_AVAILABLE" = true ] && [ -f "$INSTALL_DIR/hal_voice_client.py" ]; then
    echo "  ✓ Voice mode (with wake word support)"
else
    echo "  ✗ Voice mode (not available)"
fi
echo ""

# Wake word info
if [ "$VOICE_AVAILABLE" = true ]; then
    echo "Wake Word: Free & Open Source (OpenWakeWord)"
    echo "  No API key needed!"
    echo "  Say: 'Hey Jarvis' or 'Computer'"
    echo ""
fi

echo "Usage:"
echo ""
echo "Text Mode (default):"
echo "  hal --query \"What medications am I taking?\""
echo "  hal  # Interactive mode"
echo ""
if [ "$VOICE_AVAILABLE" = true ]; then
    echo "Voice Mode:"
    echo "  hal --voice"
    echo "  # Say 'Computer' → 🔊 TNG beep → speak query"
    echo ""
fi
echo "Configuration: $INSTALL_DIR/.env"
echo ""
echo "Restart your terminal, then type: hal"
echo ""
echo "Live long and prosper! 🖖"
echo ""

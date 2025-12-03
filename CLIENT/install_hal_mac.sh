#!/bin/bash
# HAL Voice Client - Mac Installer
# Auto-downloads and installs everything needed
# Usage: curl -fsSL http://YOUR_SERVER:8080/install_hal_mac.sh | bash

set -e

echo "=========================================="
echo "HAL Voice Client - Mac Installation"
echo "=========================================="
echo ""

# Detect server from curl URL or prompt
if [ -z "$HAL_SERVER_URL" ]; then
    echo "Enter your HAL server URL:"
    echo "  Local network: http://192.168.1.100:8768"
    echo "  External: https://hal.yourdomain.com"
    read -p "URL: " HAL_SERVER_URL
    
    if [ -z "$HAL_SERVER_URL" ]; then
        echo "Error: Server URL is required"
        exit 1
    fi
fi

# Convert HTTP URL to WebSocket URL
if [[ "$HAL_SERVER_URL" == https://* ]]; then
    GATEWAY_URL="wss://${HAL_SERVER_URL#https://}"
elif [[ "$HAL_SERVER_URL" == http://* ]]; then
    GATEWAY_URL="ws://${HAL_SERVER_URL#http://}"
elif [[ "$HAL_SERVER_URL" == wss://* ]] || [[ "$HAL_SERVER_URL" == ws://* ]]; then
    GATEWAY_URL="$HAL_SERVER_URL"
else
    # Assume it's just hostname:port
    GATEWAY_URL="ws://${HAL_SERVER_URL}"
fi

echo ""
echo "Configuration:"
echo "  Server URL: $HAL_SERVER_URL"
echo "  Gateway URL: $GATEWAY_URL"
echo ""

# Check Python
echo "[1/5] Checking Python..."
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is required but not installed."
    echo "Install from: https://www.python.org/downloads/"
    exit 1
fi
PYTHON_VERSION=$(python3 --version)
echo "  ✓ Found: $PYTHON_VERSION"

# Install dependencies
echo ""
echo "[2/5] Installing Python dependencies..."
pip3 install --user --quiet websockets 2>/dev/null || pip3 install --user websockets
echo "  ✓ websockets installed"

# Create installation directory
echo ""
echo "[3/5] Setting up installation directory..."
INSTALL_DIR="$HOME/.hal-client"
mkdir -p "$INSTALL_DIR"
cd "$INSTALL_DIR"
echo "  ✓ Directory: $INSTALL_DIR"

# Download client
echo ""
echo "[4/5] Downloading HAL client..."
cat > "$INSTALL_DIR/hal_client.py" << 'CLIENTEOF'
#!/usr/bin/env python3
"""HAL Voice Client for Mac"""
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
        print(f"Connecting to HAL at {self.gateway_url}...")
        try:
            self.websocket = await websockets.connect(self.gateway_url)
            print("✓ Connected to HAL")
            response = await self.websocket.recv()
            data = json.loads(response)
            if data.get('type') == 'connected':
                self.session_id = data.get('session_id')
                print(f"✓ Session: {self.session_id}")
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
            print("  Waiting for response...", flush=True)
            while True:
                response = await asyncio.wait_for(self.websocket.recv(), timeout=30.0)
                data = json.loads(response)
                msg_type = data.get('type')
                print(f"  Got message type: {msg_type}", flush=True)
                if msg_type == 'response':
                    response_text = data.get('text', '')
                    intent = data.get('intent', 'unknown')
                    action = data.get('action', 'unknown')
                    print(f"\n[HAL Response]")
                    print(f"Intent: {intent}")
                    print(f"Action: {action}")
                    print(f"Text: {response_text}")
                    return response_text
                elif msg_type == 'processing':
                    print("  (HAL is thinking...)")
        except asyncio.TimeoutError:
            print("✗ Timeout")
            return None
        except Exception as e:
            print(f"✗ Error: {e}")
            return None
    
    async def interactive_mode(self):
        print("\n" + "="*60)
        print("HAL Voice Client - Type your queries")
        print("="*60)
        print("(Type 'quit' to exit)\n")
        while True:
            try:
                query = input("You: ").strip()
                if not query:
                    continue
                if query.lower() in ['quit', 'exit', 'q']:
                    print("Goodbye!")
                    break
                await self.send_text_query(query)
                print()
            except KeyboardInterrupt:
                print("\nGoodbye!")
                break
            except Exception as e:
                print(f"Error: {e}")
    
    async def close(self):
        if self.websocket:
            await self.websocket.close()

async def main():
    import argparse
    parser = argparse.ArgumentParser(description='HAL Voice Client')
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
CLIENTEOF

chmod +x "$INSTALL_DIR/hal_client.py"
echo "  ✓ Client downloaded"

# Create configuration
echo ""
echo "[5/5] Creating configuration..."
cat > "$INSTALL_DIR/.env" << ENVEOF
HAL_GATEWAY_URL=$GATEWAY_URL
HAL_SERVER_URL=$HAL_SERVER_URL
ENVEOF

# Create launcher script
cat > "$INSTALL_DIR/hal" << 'LAUNCHEREOF'
#!/bin/bash
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
source "$SCRIPT_DIR/.env"
export HAL_GATEWAY_URL
python3 "$SCRIPT_DIR/hal_client.py" "$@"
LAUNCHEREOF

chmod +x "$INSTALL_DIR/hal"

# Add to PATH if not already there
if [[ ":$PATH:" != *":$HOME/.hal-client:"* ]]; then
    SHELL_RC=""
    if [ -f "$HOME/.zshrc" ]; then
        SHELL_RC="$HOME/.zshrc"
    elif [ -f "$HOME/.bashrc" ]; then
        SHELL_RC="$HOME/.bashrc"
    elif [ -f "$HOME/.bash_profile" ]; then
        SHELL_RC="$HOME/.bash_profile"
    fi
    
    if [ -n "$SHELL_RC" ]; then
        echo "" >> "$SHELL_RC"
        echo "# HAL Voice Client" >> "$SHELL_RC"
        echo "export PATH=\"\$HOME/.hal-client:\$PATH\"" >> "$SHELL_RC"
        echo "  ✓ Added to PATH in $SHELL_RC"
    fi
fi

echo "  ✓ Configuration saved"

# Test connection
echo ""
echo "Testing connection to HAL..."
export HAL_GATEWAY_URL="$GATEWAY_URL"
if timeout 5 python3 "$INSTALL_DIR/hal_client.py" --query "test" 2>&1 | grep -q "Connected"; then
    echo "  ✓ Connection successful!"
else
    echo "  ⚠ Could not connect to HAL server"
    echo "    Make sure the Voice Gateway is running at $HAL_SERVER_URL"
    echo "    For external access, ensure HAProxy is configured"
fi

echo ""
echo "=========================================="
echo "Installation Complete!"
echo "=========================================="
echo ""
echo "To start HAL client:"
echo "  1. Restart your terminal (or run: source ~/.zshrc)"
echo "  2. Type: hal"
echo ""
echo "Or run directly:"
echo "  $INSTALL_DIR/hal"
echo ""
echo "Single query:"
echo "  hal --query \"What medications am I taking?\""
echo ""
echo "Configuration: $INSTALL_DIR/.env"
echo ""

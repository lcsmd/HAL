#!/bin/bash
# Start HAL Web Voice Client Servers
# Run this on Windows Server (10.1.34.103)

echo "Starting HAL Web Voice Client Servers..."
echo ""

# Get the script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Check if Python3 is available
if ! command -v python3 &> /dev/null; then
    echo "ERROR: python3 not found. Please install Python 3.7+."
    exit 1
fi

# Check if required Python packages are installed
echo "Checking Python dependencies..."
python3 -c "import websockets, aiohttp" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "Installing required Python packages..."
    python3 -m pip install websockets aiohttp
fi

echo ""
echo "Starting services..."
echo ""

# Start HTTP server for static files (port 8080)
echo "[1/2] Starting HTTP server on port 8080..."
cd voice_assistant_v2/web_client
python3 -m http.server 8080 > ../../logs/http_server.log 2>&1 &
HTTP_PID=$!
echo "HTTP server started with PID $HTTP_PID"
cd ../..

# Wait a moment
sleep 2

# Start Voice Gateway WebSocket server (port 8768)
echo "[2/2] Starting Voice Gateway on port 8768..."
cd PY
python3 voice_gateway_web.py > ../logs/voice_gateway.log 2>&1 &
VOICE_PID=$!
echo "Voice Gateway started with PID $VOICE_PID"
cd ..

echo ""
echo "======================================"
echo "HAL Web Voice Client is running!"
echo "======================================"
echo ""
echo "HTTP Server (static files): http://10.1.34.103:8080"
echo "  - PID: $HTTP_PID"
echo "  - Log: logs/http_server.log"
echo ""
echo "Voice Gateway (WebSocket): ws://10.1.34.103:8768"
echo "  - PID: $VOICE_PID"
echo "  - Log: logs/voice_gateway.log"
echo ""
echo "Public URL: https://hal2.lcs.ai"
echo ""
echo "To stop servers:"
echo "  kill $HTTP_PID $VOICE_PID"
echo ""
echo "To view logs:"
echo "  tail -f logs/http_server.log"
echo "  tail -f logs/voice_gateway.log"
echo ""

# Save PIDs for easy stopping
echo "$HTTP_PID" > logs/http_server.pid
echo "$VOICE_PID" > logs/voice_gateway.pid

echo "PIDs saved to logs/*.pid"

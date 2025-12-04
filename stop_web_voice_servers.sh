#!/bin/bash
# Stop HAL Web Voice Client Servers

echo "Stopping HAL Web Voice Client Servers..."

# Get the script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Check if PID files exist
if [ -f logs/http_server.pid ]; then
    HTTP_PID=$(cat logs/http_server.pid)
    echo "Stopping HTTP server (PID: $HTTP_PID)..."
    kill $HTTP_PID 2>/dev/null && echo "  Stopped." || echo "  Process not found."
    rm logs/http_server.pid
else
    echo "HTTP server PID file not found. Attempting to find process..."
    pkill -f "python.*http.server 8080" && echo "  Stopped." || echo "  Process not found."
fi

if [ -f logs/voice_gateway.pid ]; then
    VOICE_PID=$(cat logs/voice_gateway.pid)
    echo "Stopping Voice Gateway (PID: $VOICE_PID)..."
    kill $VOICE_PID 2>/dev/null && echo "  Stopped." || echo "  Process not found."
    rm logs/voice_gateway.pid
else
    echo "Voice Gateway PID file not found. Attempting to find process..."
    pkill -f "python.*voice_gateway_web.py" && echo "  Stopped." || echo "  Process not found."
fi

echo ""
echo "Servers stopped."

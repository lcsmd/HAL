#!/bin/bash
# HAL Mac Client Connection Test
# Run this to verify connectivity to HAL Voice Gateway

echo "============================================================"
echo "HAL Connection Test"
echo "============================================================"
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Get gateway URL from environment or use configured default
GATEWAY_URL=${HAL_GATEWAY_URL:-"ws://10.1.34.103:8768"}

# Extract host and port from WebSocket URL
HOST=$(echo $GATEWAY_URL | sed -E 's/ws:\/\/([^:]+):([0-9]+)/\1/')
PORT=$(echo $GATEWAY_URL | sed -E 's/ws:\/\/([^:]+):([0-9]+)/\2/')

echo "Gateway URL: $GATEWAY_URL"
echo "Host: $HOST"
echo "Port: $PORT"
echo ""

# Test 1: Network connectivity
echo "Test 1: Network Connectivity"
echo "─────────────────────────────"
if ping -c 1 -W 2 $HOST > /dev/null 2>&1; then
    echo -e "${GREEN}✓${NC} Host $HOST is reachable"
else
    echo -e "${RED}✗${NC} Cannot reach host $HOST"
    echo "  Check: Are both machines on the same network?"
    echo "  Check: Is the IP address correct?"
    exit 1
fi
echo ""

# Test 2: Port connectivity
echo "Test 2: Port Connectivity"
echo "─────────────────────────────"
if command -v nc &> /dev/null; then
    if nc -z -w 2 $HOST $PORT 2>/dev/null; then
        echo -e "${GREEN}✓${NC} Port $PORT is open on $HOST"
    else
        echo -e "${RED}✗${NC} Port $PORT is not accessible on $HOST"
        echo "  Check: Is Voice Gateway running? (python PY/voice_gateway.py)"
        echo "  Check: Is Windows firewall blocking port $PORT?"
        echo "  Run on Windows: New-NetFirewallRule -DisplayName \"HAL Voice Gateway\" -Direction Inbound -LocalPort $PORT -Protocol TCP -Action Allow"
        exit 1
    fi
else
    echo -e "${YELLOW}⚠${NC} 'nc' command not found, skipping port test"
    echo "  Install with: brew install netcat"
fi
echo ""

# Test 3: WebSocket connection
echo "Test 3: WebSocket Connection"
echo "─────────────────────────────"
if [ -f "venv/bin/python3" ]; then
    source venv/bin/activate
    echo "Testing connection with HAL client..."
    echo ""
    
    # Try a simple query
    python3 hal_text_client.py --query "Hello HAL" 2>&1 | head -20
    
    if [ $? -eq 0 ]; then
        echo ""
        echo -e "${GREEN}✓${NC} WebSocket connection successful!"
    else
        echo ""
        echo -e "${RED}✗${NC} WebSocket connection failed"
        echo "  Check: Is Voice Gateway running?"
        echo "  Check: Is QM Voice Listener running?"
        exit 1
    fi
else
    echo -e "${YELLOW}⚠${NC} Virtual environment not found"
    echo "  Run: bash setup_mac.sh"
    exit 1
fi

echo ""
echo "============================================================"
echo "All Tests Passed! ✓"
echo "============================================================"
echo ""
echo "Your Mac can successfully connect to HAL!"
echo ""
echo "To start using HAL:"
echo "  python3 hal_text_client.py"
echo ""

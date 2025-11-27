#!/bin/bash
# HAL Mac Client Setup Script
# Run this on your MacBook Pro to set up the HAL text client

set -e  # Exit on error

echo "============================================================"
echo "HAL Mac Client Setup"
echo "============================================================"
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Check Python version
echo "Checking Python version..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
    echo -e "${GREEN}✓${NC} Found Python $PYTHON_VERSION"
    
    # Check if version is 3.8+
    MAJOR=$(echo $PYTHON_VERSION | cut -d. -f1)
    MINOR=$(echo $PYTHON_VERSION | cut -d. -f2)
    
    if [ "$MAJOR" -lt 3 ] || ([ "$MAJOR" -eq 3 ] && [ "$MINOR" -lt 8 ]); then
        echo -e "${RED}✗${NC} Python 3.8 or higher required"
        echo "  Install with: brew install python@3.11"
        exit 1
    fi
else
    echo -e "${RED}✗${NC} Python 3 not found"
    echo "  Install with: brew install python@3.11"
    exit 1
fi

# Check if in deployment package directory
if [ ! -f "hal_text_client.py" ]; then
    echo -e "${RED}✗${NC} Please run this script from the mac_deployment_package directory"
    exit 1
fi

echo ""
echo "Creating Python virtual environment..."
if [ -d "venv" ]; then
    echo -e "${YELLOW}⚠${NC} Virtual environment already exists, skipping creation"
else
    python3 -m venv venv
    echo -e "${GREEN}✓${NC} Virtual environment created"
fi

echo ""
echo "Activating virtual environment..."
source venv/bin/activate
echo -e "${GREEN}✓${NC} Virtual environment activated"

echo ""
echo "Installing Python dependencies..."
pip install --upgrade pip > /dev/null 2>&1
pip install -r requirements.txt
echo -e "${GREEN}✓${NC} Dependencies installed"

echo ""
echo "============================================================"
echo "Setup Complete!"
echo "============================================================"
echo ""
echo "Next steps:"
echo ""
echo "1. Set network configuration:"
echo "   source network_config.sh"
echo "   (Already configured for your network)"
echo ""
echo "2. Or set manually:"
echo "   export HAL_GATEWAY_URL=ws://10.1.34.103:8768"
echo ""
echo "3. Make sure Voice Gateway is running on Windows:"
echo "   python PY/voice_gateway.py"
echo ""
echo "4. Run the test script:"
echo "   bash test_connection.sh"
echo ""
echo "5. Start using HAL:"
echo "   python3 hal_text_client.py"
echo ""
echo "============================================================"
echo ""

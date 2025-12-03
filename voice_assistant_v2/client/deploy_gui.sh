#!/bin/bash
#
# HAL Voice Assistant - GUI Client Deployment (Mac/Linux)
#

set -e

echo "========================================"
echo "HAL Voice Assistant GUI - Deploy"
echo "========================================"
echo ""

GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

print_status() {
    echo -e "${GREEN}✓${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

# Check Python 3
echo "Checking Python 3..."
if ! command -v python3 &> /dev/null; then
    print_error "Python 3 not found!"
    echo "Install with: brew install python3 (Mac) or apt install python3 (Linux)"
    exit 1
fi
PYTHON_VERSION=$(python3 --version)
print_status "Found: $PYTHON_VERSION"
echo ""

# Create virtual environment
echo "Setting up virtual environment..."
if [ -d "venv" ]; then
    print_status "Virtual environment exists"
else:
    python3 -m venv venv
    print_status "Virtual environment created"
fi
echo ""

# Install packages
echo "Installing Python packages..."
source venv/bin/activate
pip install --upgrade pip > /dev/null 2>&1
pip install -r requirements.txt
print_status "Python packages installed"
echo ""

# Check sound files
echo "Checking sound files..."
if [ -f "sounds/activation.mp3" ]; then
    print_status "Sound files found"
else
    print_warning "Sound files not found (optional for GUI)"
fi
echo ""

# Display info
echo "========================================"
echo "✓ Deployment Complete!"
echo "========================================"
echo ""
echo "Starting HAL Voice Assistant GUI..."
echo ""
echo "Features:"
echo "  • Type messages and press Enter"
echo "  • Say wake word for voice input"
echo "  • Toggle TTS on/off (button)"
echo "  • Voice auto-enables TTS"
echo "  • Text keeps current TTS state"
echo ""
echo "========================================"
echo ""

# Start GUI
python3 hal_voice_client_gui.py

deactivate

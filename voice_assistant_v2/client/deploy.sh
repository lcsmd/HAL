#!/bin/bash
#
# HAL Voice Client - One-Command Deployment (Mac)
#
# Usage:
#   ./deploy.sh
#
# This script will:
# 1. Check for required tools (Python 3, brew)
# 2. Install system dependencies (portaudio, ffmpeg)
# 3. Create virtual environment
# 4. Install Python packages
# 5. Copy sound files from CLIENT/ directory
# 6. Start the voice client
#

set -e  # Exit on error

echo "========================================"
echo "HAL Voice Client - One-Command Deploy"
echo "========================================"
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print status
print_status() {
    echo -e "${GREEN}✓${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

# Step 1: Check Python 3
echo "Checking Python 3..."
if ! command -v python3 &> /dev/null; then
    print_error "Python 3 not found!"
    echo "Install with: brew install python3"
    exit 1
fi
PYTHON_VERSION=$(python3 --version)
print_status "Found: $PYTHON_VERSION"
echo ""

# Step 2: Check Homebrew
echo "Checking Homebrew..."
if ! command -v brew &> /dev/null; then
    print_warning "Homebrew not found - will skip optional dependencies"
    echo "Install from: https://brew.sh"
    HAVE_BREW=false
else
    print_status "Homebrew found"
    HAVE_BREW=true
fi
echo ""

# Step 3: Install system dependencies
if [ "$HAVE_BREW" = true ]; then
    echo "Installing system dependencies..."
    
    # Check and install portaudio
    if brew list portaudio &> /dev/null; then
        print_status "portaudio already installed"
    else
        echo "  Installing portaudio..."
        brew install portaudio
        print_status "portaudio installed"
    fi
    
    # Check and install ffmpeg
    if brew list ffmpeg &> /dev/null; then
        print_status "ffmpeg already installed"
    else
        echo "  Installing ffmpeg..."
        brew install ffmpeg
        print_status "ffmpeg installed"
    fi
    echo ""
fi

# Step 4: Create virtual environment
echo "Setting up virtual environment..."
if [ -d "venv" ]; then
    print_status "Virtual environment exists"
else
    python3 -m venv venv
    print_status "Virtual environment created"
fi
echo ""

# Step 5: Install Python packages
echo "Installing Python packages..."
source venv/bin/activate
pip install --upgrade pip > /dev/null 2>&1
pip install -r requirements.txt
print_status "Python packages installed"
echo ""

# Step 6: Copy sound files
echo "Copying sound files..."

# Determine CLIENT directory location
if [ -d "../../CLIENT" ]; then
    CLIENT_DIR="../../CLIENT"
elif [ -d "../../../CLIENT" ]; then
    CLIENT_DIR="../../../CLIENT"
else
    print_warning "CLIENT directory not found at ../../CLIENT"
    print_warning "Sound files must be copied manually"
    CLIENT_DIR=""
fi

if [ -n "$CLIENT_DIR" ]; then
    # Create sounds directory
    mkdir -p sounds
    
    # Copy activation sound
    if [ -f "$CLIENT_DIR/activation.mp3" ]; then
        cp "$CLIENT_DIR/activation.mp3" sounds/
        print_status "Copied activation.mp3"
    else
        print_warning "activation.mp3 not found in $CLIENT_DIR"
    fi
    
    # Copy acknowledgement sound
    if [ -f "$CLIENT_DIR/acknowledgement.wav" ]; then
        cp "$CLIENT_DIR/acknowledgement.wav" sounds/
        print_status "Copied acknowledgement.wav"
    elif [ -f "$CLIENT_DIR/ack.wav" ]; then
        cp "$CLIENT_DIR/ack.wav" sounds/acknowledgement.wav
        print_status "Copied ack.wav -> acknowledgement.wav"
    else
        print_warning "acknowledgement.wav not found in $CLIENT_DIR"
    fi
    echo ""
fi

# Step 7: Check configuration
echo "Checking configuration..."
if [ -f "voice_client.config" ]; then
    print_status "Configuration file found"
else
    print_warning "voice_client.config not found (will use defaults)"
fi
echo ""

# Step 8: Display startup info
echo "========================================"
echo "✓ Deployment Complete!"
echo "========================================"
echo ""
echo "Voice Server: ws://10.1.10.20:8585"
echo "Wake Word: HEY JARVIS"
echo ""
echo "Starting HAL Voice Client..."
echo ""
echo "Say: \"HEY JARVIS, what time is it?\""
echo ""
echo "Press Ctrl+C to exit"
echo ""
echo "========================================"
echo ""

# Step 9: Start the client
python hal_voice_client.py

# If client exits, deactivate venv
deactivate

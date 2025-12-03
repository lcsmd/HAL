#!/bin/bash
# Setup HAL Voice Client Audio Feedback Sounds
# Copies existing TNG activation sound and ack.wav from VOICE/SOUNDS

set -e

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
VOICE_SOUNDS="../VOICE/SOUNDS"

echo "Setting up HAL voice client audio feedback sounds..."
echo ""

# Check if we're in the right directory
if [ ! -f "hal_voice_client_full.py" ]; then
    echo "❌ Error: Run this script from the clients/ directory"
    exit 1
fi

# Function to copy sound file
copy_sound() {
    local source="$1"
    local dest="$2"
    local desc="$3"
    
    if [ -f "$source" ]; then
        cp "$source" "$dest"
        echo "✓ $desc"
    else
        echo "⚠ Warning: $source not found"
    fi
}

# Copy TNG activation sound (MP3)
copy_sound "$VOICE_SOUNDS/TNG_activation.mp3" "activation.mp3" "Activation sound (TNG chirp)"

# Copy acknowledgement sound (WAV)
copy_sound "$VOICE_SOUNDS/ack.wav" "acknowledgement.wav" "Acknowledgement sound"

# Use ack.wav as error sound too (fallback)
if [ -f "acknowledgement.wav" ] && [ ! -f "error.wav" ]; then
    cp "acknowledgement.wav" "error.wav"
    echo "✓ Error sound (using ack.wav as fallback)"
fi

echo ""
echo "✅ Audio feedback sounds setup complete!"
echo ""
echo "Files created:"
ls -lh activation.mp3 acknowledgement.wav error.wav 2>/dev/null || echo "Some files missing - check warnings above"

echo ""
echo "You can now run: python3 hal_voice_client_full.py"

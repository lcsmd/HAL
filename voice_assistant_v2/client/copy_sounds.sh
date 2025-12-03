#!/bin/bash
#
# Copy sound files from existing HAL clients directory
# Run this if sound files are missing or need to be updated
#

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Path to existing clients directory
CLIENTS_DIR="../../clients"

echo "============================================"
echo "Copying Sound Files"
echo "============================================"
echo ""

if [ ! -d "$CLIENTS_DIR" ]; then
    echo "ERROR: Clients directory not found at: $CLIENTS_DIR"
    echo "Please adjust the path in this script or copy files manually"
    exit 1
fi

echo "Source directory: $CLIENTS_DIR"
echo "Target directory: $SCRIPT_DIR"
echo ""

# Copy activation sound
if [ -f "$CLIENTS_DIR/activation.mp3" ]; then
    cp "$CLIENTS_DIR/activation.mp3" activation.mp3
    echo "✓ Copied activation.mp3 (TNG Star Trek sound)"
else
    echo "✗ activation.mp3 not found"
fi

# Copy acknowledgement sound
if [ -f "$CLIENTS_DIR/acknowledgement.wav" ]; then
    cp "$CLIENTS_DIR/acknowledgement.wav" acknowledgement.wav
    echo "✓ Copied acknowledgement.wav"
elif [ -f "$CLIENTS_DIR/ack.wav" ]; then
    cp "$CLIENTS_DIR/ack.wav" acknowledgement.wav
    echo "✓ Copied ack.wav → acknowledgement.wav"
else
    echo "✗ acknowledgement.wav not found"
fi

# Optional: Copy error sound if it exists
if [ -f "$CLIENTS_DIR/error.wav" ]; then
    cp "$CLIENTS_DIR/error.wav" error.wav
    echo "✓ Copied error.wav"
fi

echo ""
echo "Sound files copied successfully!"
echo ""
echo "Files in current directory:"
ls -lh *.wav *.mp3 2>/dev/null || echo "No sound files found"
echo ""

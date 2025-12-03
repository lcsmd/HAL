#!/bin/bash
#
# Setup script for Voice Server (Ubuntu with GPU)
# This script installs dependencies and sets up the voice server
#

set -e

echo "============================================"
echo "Voice Assistant Server Setup (Ubuntu)"
echo "============================================"
echo ""

# Check if running as root
if [ "$EUID" -ne 0 ]; then
    echo "Please run as root or with sudo"
    exit 1
fi

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Detect user who called sudo
if [ -n "$SUDO_USER" ]; then
    ACTUAL_USER=$SUDO_USER
else
    ACTUAL_USER=$USER
fi

echo "Installing for user: $ACTUAL_USER"

# Update system
echo ""
echo "[1/10] Updating system packages..."
apt-get update
apt-get upgrade -y

# Install Python and dependencies
echo ""
echo "[2/10] Installing Python and build tools..."
apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    build-essential \
    ffmpeg \
    git

# Check for NVIDIA GPU and CUDA
echo ""
echo "[3/10] Checking GPU..."
if command -v nvidia-smi &> /dev/null; then
    echo "NVIDIA GPU detected:"
    nvidia-smi --query-gpu=name,driver_version,memory.total --format=csv,noheader
    
    HAS_CUDA=1
    
    # Check CUDA version
    if command -v nvcc &> /dev/null; then
        CUDA_VERSION=$(nvcc --version | grep "release" | awk '{print $6}' | cut -c2-)
        echo "CUDA version: $CUDA_VERSION"
    else
        echo "WARNING: CUDA toolkit not found"
        echo "Install CUDA toolkit from: https://developer.nvidia.com/cuda-downloads"
        read -p "Continue anyway? (y/n) " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            exit 1
        fi
    fi
else
    echo "WARNING: No NVIDIA GPU detected"
    echo "Faster-Whisper will run on CPU (slower)"
    HAS_CUDA=0
    read -p "Continue? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Create project directory
echo ""
echo "[4/10] Setting up project directory..."
PROJECT_DIR="/opt/voice_assistant"
mkdir -p "$PROJECT_DIR"
cp voice_server.py "$PROJECT_DIR/"
chown -R "$ACTUAL_USER:$ACTUAL_USER" "$PROJECT_DIR"

# Create virtual environment as actual user
echo ""
echo "[5/10] Creating Python virtual environment..."
su - "$ACTUAL_USER" -c "cd $PROJECT_DIR && python3 -m venv venv"

# Install Python packages
echo ""
echo "[6/10] Installing Python packages..."
if [ $HAS_CUDA -eq 1 ]; then
    # Install with GPU support
    su - "$ACTUAL_USER" -c "cd $PROJECT_DIR && source venv/bin/activate && \
        pip install --upgrade pip && \
        pip install websockets faster-whisper torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118"
else
    # Install CPU-only version
    su - "$ACTUAL_USER" -c "cd $PROJECT_DIR && source venv/bin/activate && \
        pip install --upgrade pip && \
        pip install websockets faster-whisper torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu"
fi

# Download Whisper model
echo ""
echo "[7/10] Downloading Whisper model..."
echo "This may take several minutes..."
su - "$ACTUAL_USER" -c "cd $PROJECT_DIR && source venv/bin/activate && python3 << 'EOF'
from faster_whisper import WhisperModel
import os

model_name = 'large-v3'
device = 'cuda' if os.path.exists('/usr/bin/nvidia-smi') else 'cpu'
compute_type = 'float16' if device == 'cuda' else 'int8'

print(f'Loading {model_name} model on {device}...')
model = WhisperModel(model_name, device=device, compute_type=compute_type)
print('Model downloaded and ready!')
EOF
"

# Create systemd service
echo ""
echo "[8/10] Creating systemd service..."
cat > /etc/systemd/system/voice-server.service << EOF
[Unit]
Description=Voice Assistant Server
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
User=$ACTUAL_USER
WorkingDirectory=$PROJECT_DIR
ExecStart=$PROJECT_DIR/venv/bin/python $PROJECT_DIR/voice_server.py
Restart=always
RestartSec=3
StandardOutput=journal
StandardError=journal

# Environment
Environment="PYTHONUNBUFFERED=1"

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload

# Configure firewall
echo ""
echo "[9/10] Configuring firewall..."
if command -v ufw &> /dev/null; then
    ufw allow 8585/tcp comment "Voice Assistant Client Port"
    echo "Firewall rule added for port 8585"
else
    echo "UFW not found, skipping firewall configuration"
fi

# Create helper scripts
echo ""
echo "[10/10] Creating helper scripts..."

# Start script
cat > /usr/local/bin/voice-server-start << EOF
#!/bin/bash
systemctl start voice-server
systemctl status voice-server
EOF
chmod +x /usr/local/bin/voice-server-start

# Stop script
cat > /usr/local/bin/voice-server-stop << EOF
#!/bin/bash
systemctl stop voice-server
EOF
chmod +x /usr/local/bin/voice-server-stop

# Status script
cat > /usr/local/bin/voice-server-status << EOF
#!/bin/bash
systemctl status voice-server
EOF
chmod +x /usr/local/bin/voice-server-status

# Logs script
cat > /usr/local/bin/voice-server-logs << EOF
#!/bin/bash
journalctl -u voice-server -f
EOF
chmod +x /usr/local/bin/voice-server-logs

echo ""
echo "============================================"
echo "Setup Complete!"
echo "============================================"
echo ""
echo "Voice server installed at: $PROJECT_DIR"
echo ""
echo "Commands:"
echo "  sudo systemctl start voice-server    - Start the server"
echo "  sudo systemctl stop voice-server     - Stop the server"
echo "  sudo systemctl enable voice-server   - Enable auto-start at boot"
echo "  sudo systemctl status voice-server   - Check status"
echo "  journalctl -u voice-server -f        - View logs"
echo ""
echo "Or use helper commands:"
echo "  voice-server-start"
echo "  voice-server-stop"
echo "  voice-server-status"
echo "  voice-server-logs"
echo ""
echo "To enable auto-start at boot:"
echo "  sudo systemctl enable voice-server"
echo ""
echo "Port 8585 is now open for client connections"
echo ""

# Ask to start now
read -p "Start the voice server now? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    systemctl start voice-server
    sleep 2
    systemctl status voice-server
fi

echo ""
echo "Setup complete!"

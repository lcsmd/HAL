#!/bin/bash
#
# Install HAL AI Services on Ubuntu (ubuai)
# Run as root: sudo bash install_services.sh
#

set -e

if [ "$EUID" -ne 0 ]; then
    echo "Please run as root: sudo bash install_services.sh"
    exit 1
fi

echo "============================================"
echo "Installing HAL AI Services on ubuai"
echo "============================================"
echo ""

# Detect actual user
if [ -n "$SUDO_USER" ]; then
    ACTUAL_USER=$SUDO_USER
else
    ACTUAL_USER=$USER
fi

echo "Installing for user: $ACTUAL_USER"
echo ""

# Update system
echo "[1/8] Updating system..."
apt-get update
apt-get upgrade -y

# Install dependencies
echo ""
echo "[2/8] Installing dependencies..."
apt-get install -y python3 python3-pip python3-venv ffmpeg git curl

# Install Faster-Whisper
echo ""
echo "[3/8] Setting up Faster-Whisper..."

# Create directory
mkdir -p /opt/faster-whisper/models
cd /opt/faster-whisper

# Copy whisper server script
if [ -f "../whisper_server.py" ]; then
    cp ../whisper_server.py .
else
    echo "ERROR: whisper_server.py not found"
    echo "Please ensure whisper_server.py is in the same directory as this script"
    exit 1
fi

# Create virtual environment
python3 -m venv venv

# Install packages
source venv/bin/activate
pip install --upgrade pip
pip install fastapi uvicorn faster-whisper torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
deactivate

# Download model
echo ""
echo "[4/8] Downloading Whisper model (this may take several minutes)..."
source venv/bin/activate
python3 << 'EOF'
from faster_whisper import WhisperModel
import logging
logging.basicConfig(level=logging.INFO)

model = WhisperModel(
    "large-v3",
    device="cuda",
    compute_type="float16",
    download_root="/opt/faster-whisper/models"
)
print("Model downloaded successfully!")
EOF
deactivate

# Install Ollama
echo ""
echo "[5/8] Installing Ollama..."

if command -v ollama &> /dev/null; then
    echo "Ollama already installed"
else
    curl -fsSL https://ollama.com/install.sh | sh
fi

# Pull Ollama model
echo ""
echo "[6/8] Pulling Ollama models..."
su - $ACTUAL_USER -c "ollama pull llama3.2:latest" || true

# Install systemd services
echo ""
echo "[7/8] Installing systemd services..."

# Faster-Whisper service
if [ -f "../faster-whisper.service" ]; then
    cp ../faster-whisper.service /etc/systemd/system/
    echo "Installed faster-whisper.service"
else
    echo "WARNING: faster-whisper.service not found, creating default..."
    cat > /etc/systemd/system/faster-whisper.service << 'EOFSVC'
[Unit]
Description=Faster-Whisper STT Service
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
User=root
WorkingDirectory=/opt/faster-whisper
ExecStart=/opt/faster-whisper/venv/bin/python /opt/faster-whisper/whisper_server.py
Restart=always
RestartSec=5
StandardOutput=journal
StandardError=journal
Environment="PYTHONUNBUFFERED=1"
Environment="CUDA_VISIBLE_DEVICES=0"

[Install]
WantedBy=multi-user.target
EOFSVC
fi

# Ollama service
if [ -f "../ollama.service" ]; then
    cp ../ollama.service /etc/systemd/system/
    echo "Installed ollama.service"
else
    echo "WARNING: ollama.service not found, creating default..."
    cat > /etc/systemd/system/ollama.service << 'EOFSVC'
[Unit]
Description=Ollama LLM Service
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
User=root
ExecStart=/usr/local/bin/ollama serve
Restart=always
RestartSec=5
StandardOutput=journal
StandardError=journal
Environment="OLLAMA_HOST=0.0.0.0:11434"
Environment="OLLAMA_ORIGINS=*"

[Install]
WantedBy=multi-user.target
EOFSVC
fi

# Reload systemd
systemctl daemon-reload

# Configure firewall
echo ""
echo "[8/8] Configuring firewall..."
if command -v ufw &> /dev/null; then
    ufw allow 9000/tcp comment "Faster-Whisper STT"
    ufw allow 11434/tcp comment "Ollama LLM"
    echo "Firewall rules added"
else
    echo "UFW not found, skipping firewall configuration"
fi

# Set permissions
chown -R $ACTUAL_USER:$ACTUAL_USER /opt/faster-whisper

echo ""
echo "============================================"
echo "Installation Complete!"
echo "============================================"
echo ""
echo "Services installed:"
echo "  1. faster-whisper.service (port 9000)"
echo "  2. ollama.service (port 11434)"
echo ""
echo "To enable auto-start at boot:"
echo "  sudo systemctl enable faster-whisper"
echo "  sudo systemctl enable ollama"
echo ""
echo "To start services now:"
echo "  sudo systemctl start faster-whisper"
echo "  sudo systemctl start ollama"
echo ""
echo "To check status:"
echo "  sudo systemctl status faster-whisper"
echo "  sudo systemctl status ollama"
echo ""
echo "To view logs:"
echo "  sudo journalctl -u faster-whisper -f"
echo "  sudo journalctl -u ollama -f"
echo ""

# Ask to enable auto-start
read -p "Enable auto-start at boot? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    systemctl enable faster-whisper
    systemctl enable ollama
    echo "Auto-start enabled"
fi

# Ask to start now
echo ""
read -p "Start services now? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "Starting faster-whisper..."
    systemctl start faster-whisper
    sleep 3
    
    echo "Starting ollama..."
    systemctl start ollama
    sleep 3
    
    echo ""
    echo "Service Status:"
    systemctl status faster-whisper --no-pager
    echo ""
    systemctl status ollama --no-pager
fi

echo ""
echo "Setup complete!"

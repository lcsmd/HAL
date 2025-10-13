#!/bin/bash

echo "HAL AI Server Deployment Script"
echo "============================="

# Check if running as root
if [ "$EUID" -ne 0 ]; then 
    echo "Please run as root"
    exit 1
fi

# Install system dependencies
echo "Installing system dependencies..."
apt-get update
apt-get install -y python3-pip python3-venv nvidia-cuda-toolkit

# Create directory structure
mkdir -p /opt/hal/ai_server
mkdir -p /opt/hal/ai_server/logs

# Copy files
echo "Copying files..."
cp server.py /opt/hal/ai_server/
cp server_requirements.txt /opt/hal/ai_server/requirements.txt

# Create virtual environment
cd /opt/hal/ai_server
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt

# Install Ollama if not present
if ! command -v ollama &> /dev/null; then
    echo "Installing Ollama..."
    curl -fsSL https://ollama.ai/install.sh | sh
fi

# Pull Mistral model
echo "Pulling Mistral model..."
ollama pull mistral

# Create systemd service
echo "Creating systemd service..."
cat > /etc/systemd/system/hal-ai-server.service << EOL
[Unit]
Description=HAL AI Server
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/opt/hal/ai_server
Environment=PATH=/opt/hal/ai_server/venv/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
ExecStart=/opt/hal/ai_server/venv/bin/python server.py
Restart=always

[Install]
WantedBy=multi-user.target
EOL

# Reload systemd and enable service
systemctl daemon-reload
systemctl enable hal-ai-server
systemctl start hal-ai-server

echo
echo "AI Server deployment complete!"
echo "Check status with: systemctl status hal-ai-server"
echo

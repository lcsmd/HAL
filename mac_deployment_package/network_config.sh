#!/bin/bash
# HAL Network Configuration
# Source this file to set environment variables for your network

# Network Architecture:
# - QM Server (Windows/OpenQM): 10.1.34.103 (user: lawr)
# - AI Server (Ollama/Faster-Whisper): 10.1.10.20 (user: lawr)
# - HAProxy Load Balancer: 10.1.50.100 (user: lawr, SSH port 2222)
# - Proxmox: 10.1.33.1 (user: root)

# HAL Voice Gateway (runs on QM Server)
export HAL_GATEWAY_URL="ws://10.1.34.103:8768"

# Alternative: Use HAProxy if configured for voice gateway
# export HAL_GATEWAY_URL="ws://10.1.50.100:8768"

# AI Services (GPU-accelerated on ubuai)
export OLLAMA_HOST="10.1.10.20"
export OLLAMA_PORT="11434"
export OLLAMA_URL="http://10.1.10.20:11434"
export WHISPER_URL="http://10.1.10.20:9000/transcribe"
export UBUAI_HOST="10.1.10.20"

# HAProxy SSH access (for administration)
export HAPROXY_HOST="10.1.50.100"
export HAPROXY_SSH_PORT="2222"
export HAPROXY_USER="lawr"

# Proxmox
export PROXMOX_HOST="10.1.33.1"
export PROXMOX_USER="root"

# QM Server
export QM_HOST="10.1.34.103"
export QM_VOICE_PORT="8767"
export QM_GATEWAY_PORT="8768"

echo "HAL Network Configuration Loaded:"
echo "  Voice Gateway: $HAL_GATEWAY_URL"
echo "  QM Server: $QM_HOST (user: lawr)"
echo "  AI Server: $OLLAMA_HOST (user: lawr)"
echo "  HAProxy: $HAPROXY_USER@$HAPROXY_HOST:$HAPROXY_SSH_PORT"
echo "  Proxmox: $PROXMOX_USER@$PROXMOX_HOST"
echo ""
echo "Credentials: See CREDENTIALS.txt (secure file)"

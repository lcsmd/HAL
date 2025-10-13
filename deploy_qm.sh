#!/bin/bash

echo "HAL OpenQM Deployment Script"
echo "=========================="

# Check if running as root
if [ "$EUID" -ne 0 ]; then 
    echo "Please run as root"
    exit 1
fi

# Variables
QM_ACCOUNT="hal"
QM_BP_DIR="/usr/qmsys/bp"
QM_VOC_DIR="/usr/qmsys/VOC"

# Create HAL account if it doesn't exist
echo "Setting up QM account..."
if ! grep -q "^$QM_ACCOUNT:" /etc/passwd; then
    useradd -m -s /bin/bash $QM_ACCOUNT
fi

# Copy BASIC programs
echo "Copying BASIC programs..."
cp BP/HAL.* $QM_BP_DIR/

# Compile BASIC programs
echo "Compiling BASIC programs..."
qm << EOL
BASIC BP HAL.PROCESS
BASIC BP HAL.SCHEDULE
BASIC BP HAL.TASK
BASIC BP HAL.QUERY
BASIC BP HAL.SYSTEM
BASIC BP HAL.HTTP.SERVICE
EOL

# Set up HTTP service
echo "Configuring HTTP service..."
qm << EOL
ED VOC HTTP.SERVICE
INSERT
HAL /hal/ HAL.HTTP.SERVICE
FILE
EOL

# Create necessary files
echo "Creating QM files..."
qm << EOL
CREATE.FILE HAL.SCHEDULE
CREATE.FILE HAL.TASKS
CREATE.FILE HAL.CHAT.HISTORY
EOL

# Set up permissions
echo "Setting permissions..."
chown -R qmsys:qmusers $QM_BP_DIR/HAL.*
chmod 644 $QM_BP_DIR/HAL.*

# Restart QM HTTP service
echo "Restarting QM HTTP service..."
systemctl restart qm-http

echo
echo "OpenQM deployment complete!"
echo "Test the service with: curl http://localhost:4243/hal/health"
echo

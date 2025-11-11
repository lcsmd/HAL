#!/bin/bash
# Add HAL REST command to Home Assistant configuration

echo "Adding HAL REST command to Home Assistant..."

# Backup config
cp /config/configuration.yaml /config/configuration.yaml.backup.$(date +%Y%m%d_%H%M%S)

# Check if already exists
if grep -q "ask_hal" /config/configuration.yaml; then
    echo "HAL REST command already exists!"
    exit 0
fi

# Add REST command
cat >> /config/configuration.yaml << 'EOF'

# HAL Voice Interface
rest_command:
  ask_hal:
    url: "http://10.1.34.103:8766/ask"
    method: POST
    payload: '{"text": "{{ text }}"}'
    content_type: "application/json"
EOF

echo "Configuration added!"
echo "Now restart Home Assistant from the web UI"
echo "Developer Tools -> YAML -> Restart"

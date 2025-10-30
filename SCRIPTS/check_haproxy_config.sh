#!/bin/bash
# Check HAProxy configuration and add voice.lcs.ai backend

echo "=== Checking HAProxy Configuration ==="
echo ""

# Check speech backend
echo "1. Checking speech.lcs.ai backend:"
sudo grep -A 15 "backend.*speech" /etc/haproxy/haproxy.cfg || echo "  No speech backend found"
echo ""

# Check existing backends
echo "2. All backends:"
sudo grep "^backend " /etc/haproxy/haproxy.cfg
echo ""

# Check frontend ACLs
echo "3. Frontend ACLs:"
sudo grep "acl is_" /etc/haproxy/haproxy.cfg | head -20
echo ""

# Check if voice backend exists
echo "4. Checking for voice backend:"
sudo grep -i "voice" /etc/haproxy/haproxy.cfg || echo "  No voice backend found - needs to be added"
echo ""

echo "=== Ready to add voice.lcs.ai backend ==="

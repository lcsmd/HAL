#!/bin/bash

# HAL Network Diagnostics Script
# Checks connectivity to QM server

echo "============================================================"
echo "HAL Network Diagnostics"
echo "============================================================"
echo ""

# Load network config if exists
if [ -f network_config.sh ]; then
    source network_config.sh
fi

# Default to configured server or fallback
QM_IP=${QM_SERVER:-10.1.34.103}
QM_PORT=${QM_WEBSOCKET_PORT:-8768}
HAPROXY_IP=${HAPROXY_SERVER:-10.1.50.100}
HAPROXY_PORT=${HAPROXY_SSH_PORT:-2222}

echo "Target Server: $QM_IP"
echo "Target Port: $QM_PORT"
echo ""

# Check 1: Mac IP addresses
echo "Test 1: Your Mac's Network Configuration"
echo "─────────────────────────────────────────"
MAC_IPS=$(ifconfig | grep "inet " | grep -v 127.0.0.1 | awk '{print $2}')
if [ -z "$MAC_IPS" ]; then
    echo "✗ No network interfaces found"
    echo ""
else
    echo "IP addresses on this Mac:"
    ifconfig | grep "inet " | grep -v 127.0.0.1 | while read line; do
        IP=$(echo $line | awk '{print $2}')
        INTERFACE=$(echo $line | awk '{print $1}')
        echo "  $IP"
    done
    echo ""
    
    # Check if on same network
    SAME_NETWORK=$(echo "$MAC_IPS" | grep -c "^10\.1\.34\.")
    if [ "$SAME_NETWORK" -gt 0 ]; then
        echo "✓ Mac is on 10.1.34.x network (same as server)"
    else
        echo "⚠ Mac is NOT on 10.1.34.x network"
        echo "  You may need VPN or SSH tunnel"
    fi
fi
echo ""

# Check 2: Ping QM Server
echo "Test 2: Network Connectivity to QM Server"
echo "─────────────────────────────────────────"
if ping -c 2 -W 2 $QM_IP > /dev/null 2>&1; then
    RTT=$(ping -c 1 $QM_IP | grep "time=" | awk -F'time=' '{print $2}' | awk '{print $1}')
    echo "✓ Can reach $QM_IP"
    echo "  Round-trip time: $RTT"
else
    echo "✗ Cannot reach $QM_IP"
    echo "  Possible reasons:"
    echo "  - Server is offline"
    echo "  - You're on a different network"
    echo "  - Firewall blocking ICMP"
fi
echo ""

# Check 3: Test WebSocket port
echo "Test 3: WebSocket Port ($QM_PORT)"
echo "─────────────────────────────────────────"
if command -v nc > /dev/null 2>&1; then
    if nc -z -w 2 $QM_IP $QM_PORT > /dev/null 2>&1; then
        echo "✓ Port $QM_PORT is open on $QM_IP"
        echo "  WebSocket listener appears to be running"
    else
        echo "✗ Port $QM_PORT is not reachable"
        echo "  Possible reasons:"
        echo "  - QM listener not running"
        echo "  - Firewall blocking port"
        echo "  - Server not accessible"
    fi
else
    echo "⚠ 'nc' command not available, skipping port test"
    echo "  Install with: brew install netcat"
fi
echo ""

# Check 4: HAProxy accessibility (alternate route)
echo "Test 4: HAProxy SSH Tunnel (Alternate Route)"
echo "─────────────────────────────────────────"
if command -v nc > /dev/null 2>&1; then
    if nc -z -w 2 $HAPROXY_IP $HAPROXY_PORT > /dev/null 2>&1; then
        echo "✓ HAProxy is reachable at $HAPROXY_IP:$HAPROXY_PORT"
        echo "  You can use SSH tunnel as alternate connection:"
        echo "  ssh -p $HAPROXY_PORT -L $QM_PORT:$QM_IP:$QM_PORT lawr@$HAPROXY_IP -N"
    else
        echo "✗ HAProxy not reachable"
    fi
else
    echo "⚠ Skipping HAProxy test (nc not available)"
fi
echo ""

# Check 5: DNS resolution
echo "Test 5: Network Route"
echo "─────────────────────────────────────────"
if command -v route > /dev/null 2>&1; then
    echo "Route to $QM_IP:"
    route -n get $QM_IP 2>/dev/null | grep -E "(gateway|interface)" || echo "No route found"
else
    echo "⚠ Route command not available"
fi
echo ""

# Summary
echo "============================================================"
echo "Summary & Recommendations"
echo "============================================================"
echo ""

# Determine issue
CAN_PING=$(ping -c 1 -W 2 $QM_IP > /dev/null 2>&1 && echo "yes" || echo "no")
CAN_CONNECT=$(nc -z -w 2 $QM_IP $QM_PORT > /dev/null 2>&1 && echo "yes" || echo "no")
SAME_NET=$(ifconfig | grep "inet " | grep -c "10\.1\.34\.")

if [ "$CAN_CONNECT" = "yes" ]; then
    echo "✓ Everything looks good!"
    echo "  You should be able to connect to HAL"
    echo ""
    echo "Try: python3 hal_text_client.py"
elif [ "$CAN_PING" = "yes" ]; then
    echo "⚠ Server is reachable but port $QM_PORT is not open"
    echo ""
    echo "Next steps:"
    echo "1. Check if QM WebSocket listener is running on server"
    echo "   On server: netstat -an | findstr $QM_PORT"
    echo ""
    echo "2. Check Windows firewall on server"
    echo "   On server: Get-NetFirewallRule | Where-Object {$_.LocalPort -eq $QM_PORT}"
elif [ "$SAME_NET" -eq 0 ]; then
    echo "⚠ You're not on the 10.1.34.x network"
    echo ""
    echo "Solutions:"
    echo ""
    echo "Option 1: Connect to same network"
    echo "  Check System Preferences → Network"
    echo "  Connect to the same WiFi/network as the server"
    echo ""
    echo "Option 2: Use SSH Tunnel (Recommended)"
    echo "  Terminal 1: ssh -p $HAPROXY_PORT -L $QM_PORT:$QM_IP:$QM_PORT lawr@$HAPROXY_IP -N"
    echo "  Terminal 2: export WEBSOCKET_URL=\"ws://localhost:$QM_PORT\""
    echo "  Terminal 2: python3 hal_text_client.py"
else
    echo "✗ Server not reachable"
    echo ""
    echo "Possible causes:"
    echo "1. Server is offline or sleeping"
    echo "2. Network firewall blocking access"
    echo "3. VPN required"
    echo ""
    echo "Try SSH tunnel through HAProxy as alternate:"
    echo "  ssh -p $HAPROXY_PORT -L $QM_PORT:$QM_IP:$QM_PORT lawr@$HAPROXY_IP -N"
fi

echo ""
echo "============================================================"
echo ""

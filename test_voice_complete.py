#!/usr/bin/env python
"""Test complete voice system"""
import socket
import json

print("Testing Voice Listener on port 8767...")

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(5)
    s.connect(('localhost', 8767))
    
    # Send test request
    request = {"text": "test voice system", "intent": "GENERAL"}
    s.send(json.dumps(request).encode() + b'\n')
    
    # Read response
    response = b""
    while True:
        chunk = s.recv(4096)
        if not chunk:
            break
        response += chunk
        if b'\n' in chunk:
            break
    
    s.close()
    
    print(f"Response: {response.decode()}")
    print("\nVoice Listener is WORKING!")
    
except Exception as e:
    print(f"Error: {e}")
    print("Voice Listener may not be responding correctly")

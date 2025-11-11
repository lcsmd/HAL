#!/usr/bin/env python
"""Debug the full voice system using COMMAND.EXECUTOR"""
from qm_exec import execute_qm_commands
import socket
import json
import time

print("="*70)
print("FULL SYSTEM DEBUG")
print("="*70)

# Step 1: Check QM processes
print("\n1. Checking QM processes...")
results = execute_qm_commands(['WHO', 'LIST.READU'])
for r in results:
    print(f"{r['command']}: {r['output'][:200]}")

# Step 2: Check port 8767
print("\n2. Checking port 8767...")
try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(2)
    sock.connect(('localhost', 8767))
    print("  [OK] Port 8767 is listening")
    sock.close()
except Exception as e:
    print(f"  [ERROR] Port 8767: {e}")

# Step 3: Test direct QM connection
print("\n3. Testing direct QM connection...")
try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(5)
    sock.connect(('localhost', 8767))
    
    message = {
        "session_id": "debug-test",
        "transcription": "What medications am I taking?",
        "timestamp": "2025-11-07T03:00:00Z",
        "client_type": "test",
        "context": []
    }
    data = json.dumps(message).encode() + b'\n'
    sock.sendall(data)
    print(f"  Sent {len(data)} bytes")
    
    response = b""
    start = time.time()
    while time.time() - start < 5:
        chunk = sock.recv(4096)
        if not chunk:
            break
        response += chunk
        if b'}' in response:
            break
    
    sock.close()
    print(f"  Received {len(response)} bytes")
    if response:
        result = json.loads(response.decode())
        print(f"  Intent: {result.get('intent')}")
        print(f"  Status: {result.get('status')}")
    else:
        print("  [ERROR] No response received")
except Exception as e:
    print(f"  [ERROR] {e}")

# Step 4: Check Voice Gateway
print("\n4. Checking Voice Gateway on port 8768...")
try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(2)
    sock.connect(('localhost', 8768))
    print("  [OK] Port 8768 is listening")
    sock.close()
except Exception as e:
    print(f"  [ERROR] Port 8768: {e}")

# Step 5: Check latest COMO
print("\n5. Checking latest COMO...")
import os
como_dir = "C:\\qmsys\\hal\\$COMO"
files = sorted([f for f in os.listdir(como_dir) if f.startswith('PH')], reverse=True)
if files:
    latest = files[0]
    print(f"  Latest: {latest}")
    with open(os.path.join(como_dir, latest), 'r', errors='ignore') as f:
        lines = f.readlines()
        print("  Last 10 lines:")
        for line in lines[-10:]:
            print(f"    {line.rstrip()}")

print("\n" + "="*70)

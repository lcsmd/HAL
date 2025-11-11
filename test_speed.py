#!/usr/bin/env python
"""Test individual request speed"""
import socket
import json
import time

def test_single_request():
    start = time.time()
    
    # Connect
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('localhost', 8767))
    connect_time = time.time()
    
    # Send
    message = {
        "session_id": "speed-test",
        "transcription": "What medications am I taking?",
        "timestamp": "2025-11-07T03:00:00Z",
        "client_type": "test",
        "context": []
    }
    data = json.dumps(message).encode() + b'\n'
    sock.sendall(data)
    send_time = time.time()
    
    # Receive
    response = b""
    while True:
        chunk = sock.recv(4096)
        if not chunk:
            break
        response += chunk
        if b'}' in response:
            break
    recv_time = time.time()
    
    sock.close()
    end_time = time.time()
    
    result = json.loads(response.decode())
    
    print(f"Total time: {(end_time - start)*1000:.1f}ms")
    print(f"  Connect: {(connect_time - start)*1000:.1f}ms")
    print(f"  Send: {(send_time - connect_time)*1000:.1f}ms")
    print(f"  Receive: {(recv_time - send_time)*1000:.1f}ms")
    print(f"  Close: {(end_time - recv_time)*1000:.1f}ms")
    print(f"Intent: {result['intent']}")
    print(f"Status: {result['status']}")

if __name__ == "__main__":
    for i in range(3):
        print(f"\n=== Request {i+1} ===")
        test_single_request()

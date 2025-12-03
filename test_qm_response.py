#!/usr/bin/env python3
"""Test what AI.SERVER actually returns"""
import socket
import json

def test_query(text):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(5.0)
        s.connect(('localhost', 8745))
        
        message = {
            'type': 'text_input',
            'text': text,
            'session_id': 'test123'
        }
        
        msg_bytes = json.dumps(message).encode() + b'\n'
        s.sendall(msg_bytes)
        
        response_data = b""
        while True:
            chunk = s.recv(4096)
            if not chunk:
                break
            response_data += chunk
            if b'}' in chunk:
                break
        
        s.close()
        
        print(f"\n=== Query: {text} ===")
        print(f"Raw response: {response_data}")
        print(f"Decoded: {response_data.decode()}")
        
        try:
            parsed = json.loads(response_data.decode())
            print(f"Parsed JSON: {json.dumps(parsed, indent=2)}")
            print(f"Text field: {parsed.get('text', 'NO TEXT FIELD!')}")
        except Exception as e:
            print(f"Parse error: {e}")
            
    except Exception as e:
        print(f"Error: {e}")

# Test different queries
test_query("what time is it")
test_query("tell me a joke")
test_query("hello")
test_query("what is 2+2")

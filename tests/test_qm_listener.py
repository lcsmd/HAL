"""Test QM Voice Listener on port 8767"""
import socket
import json
import time

print("Testing QM Voice Listener on localhost:8767...")
print("")

try:
    # Connect to QM listener
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(5)
    sock.connect(('localhost', 8767))
    print("[OK] Connected to QM Voice Listener!")
    print("")
    
    # Send test message
    test_message = {
        'type': 'voice_message',
        'session_id': 'test-123',
        'transcription': 'What medications am I taking?',
        'timestamp': '2025-11-04T12:00:00Z'
    }
    
    message_json = json.dumps(test_message)
    print(f"Sending: {message_json}")
    sock.sendall(message_json.encode('utf-8'))
    print("")
    
    # Receive response
    print("Waiting for response...")
    response = sock.recv(4096).decode('utf-8')
    print(f"Received: {response}")
    print("")
    
    # Parse response
    try:
        response_data = json.loads(response)
        print("[OK] Valid JSON response!")
        print(f"Response text: {response_data.get('response_text')}")
        print(f"Status: {response_data.get('status')}")
    except json.JSONDecodeError:
        print("Response is not JSON")
    
    sock.close()
    
    print("")
    print("=" * 60)
    print("SUCCESS! QM Voice Listener is working!")
    print("=" * 60)
    
except ConnectionRefusedError:
    print("[ERROR] Connection refused - QM Listener not running on port 8767")
except socket.timeout:
    print("[ERROR] Connection timeout")
except Exception as e:
    print(f"[ERROR] Error: {e}")

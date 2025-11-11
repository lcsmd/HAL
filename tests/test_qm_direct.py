"""Test QM Listener directly (bypass Voice Gateway)"""
import socket
import json

def test_qm_direct():
    print("Connecting directly to QM Listener on localhost:8767...")
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('localhost', 8767))
    print("[OK] Connected!")
    
    # Send message
    message = {
        'session_id': 'test-123',
        'transcription': 'What medications am I taking?',
        'timestamp': '2025-11-06T00:00:00',
        'client_type': 'test',
        'context': []
    }
    
    print(f"\nSending: {json.dumps(message)}")
    sock.sendall(json.dumps(message).encode() + b'\n')
    print("Message sent with newline")
    
    # Read response until newline
    print("\nWaiting for response...")
    response_data = b''
    while True:
        chunk = sock.recv(1024)
        if not chunk:
            break
        response_data += chunk
        if b'\n' in response_data:
            break
    
    print(f"Received {len(response_data)} bytes")
    print(f"Raw: {response_data}")
    
    if response_data:
        response = json.loads(response_data.decode())
        print(f"\nResponse: {json.dumps(response, indent=2)}")
        print(f"\nText: {response.get('response_text')}")
        print(f"Intent: {response.get('intent')}")
        print(f"Action: {response.get('action_taken')}")
    
    sock.close()
    print("\n[SUCCESS] Direct QM test passed!")

if __name__ == "__main__":
    test_qm_direct()

"""Test QM listener with exact message format"""
import socket
import json
import time

def test_qm():
    print("Connecting to QM listener on localhost:8767...")
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('localhost', 8767))
    print("[OK] Connected!")
    
    # Create message exactly as gateway does
    message = {
        'session_id': 'test-12345',
        'transcription': 'What medications am I taking?',
        'timestamp': '2025-11-07T01:50:00Z',
        'client_type': 'test',
        'context': []
    }
    
    message_json = json.dumps(message)
    message_bytes = message_json.encode() + b'\n'
    
    print(f"\nSending {len(message_bytes)} bytes:")
    print(f"Message: {message_json}")
    print(f"With newline: {repr(message_bytes)}")
    
    sock.sendall(message_bytes)
    print("[OK] Message sent")
    
    print("\nWaiting for response...")
    sock.settimeout(5.0)
    
    try:
        # Read all data - might come in multiple chunks
        response_data = b''
        while True:
            chunk = sock.recv(4096)
            if not chunk:
                break
            response_data += chunk
            # If we got a complete JSON (has closing brace), stop
            if b'}' in chunk:
                break
        
        print(f"[OK] Received {len(response_data)} bytes:")
        print(response_data.decode('utf-8', errors='ignore'))
        
        # Try to parse as JSON
        response = json.loads(response_data.decode())
        print(f"\n[SUCCESS] Parsed response:")
        print(f"  Response text: {response.get('response_text')}")
        print(f"  Intent: {response.get('intent')}")
        print(f"  Status: {response.get('status')}")
        
    except socket.timeout:
        print("[ERROR] Timeout waiting for response")
    except Exception as e:
        print(f"[ERROR] {e}")
        import traceback
        traceback.print_exc()
    finally:
        sock.close()

if __name__ == "__main__":
    test_qm()

"""Test medication query through QM Voice Listener"""
import socket
import json

print("Testing Medication Query...")
print("")

try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(5)
    sock.connect(('localhost', 8767))
    print("[OK] Connected to QM Voice Listener")
    print("")
    
    # Send medication query
    message = {
        'type': 'voice_message',
        'session_id': 'test-456',
        'transcription': 'What medications am I taking?',
        'timestamp': '2025-11-04T13:00:00Z'
    }
    
    message_json = json.dumps(message)
    print(f"Sending: {message_json}")
    sock.sendall(message_json.encode('utf-8'))
    print("")
    
    # Receive response
    print("Waiting for response...")
    response = sock.recv(4096).decode('utf-8')
    print(f"Received: {response}")
    print("")
    
    # Parse response
    response_data = json.loads(response)
    print("=" * 60)
    print("Response Details:")
    print("=" * 60)
    print(f"Intent: {response_data.get('intent')}")
    print(f"Status: {response_data.get('status')}")
    print(f"Response: {response_data.get('response_text')}")
    print("")
    
    if response_data.get('intent') == 'MEDICATION':
        print("[SUCCESS] Medication intent recognized!")
        print("[SUCCESS] Response includes medication information!")
    else:
        print("[WARNING] Intent not recognized as MEDICATION")
    
    sock.close()
    
except Exception as e:
    print(f"[ERROR] {e}")

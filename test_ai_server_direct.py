#!/usr/bin/env python3
"""
Quick Test Client - Direct connection to AI.SERVER on port 8745
Tests the AI.SERVER phantom we just started
"""

import socket
import json
import time

def test_ai_server():
    """Test direct connection to AI.SERVER"""
    
    print("="*60)
    print("Testing AI.SERVER on 10.1.34.103:8745")
    print("="*60)
    
    # Connect
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(("10.1.34.103", 8745))
        print("[OK] Connected!")
    except Exception as e:
        print(f"[ERROR] Connection failed: {e}")
        return
    
    # Test queries
    queries = [
        "what time is it",
        "what is the date",
        "hello",
        "how are you"
    ]
    
    for query in queries:
        print(f"\n>> Sending: {query}")
        
        # Build message
        msg = {
            "type": "text_input",
            "text": query,
            "user_id": "test_user",
            "session_id": f"test_{int(time.time())}"
        }
        
        # Send
        s.send((json.dumps(msg) + "\n").encode())
        
        # Receive response
        time.sleep(0.5)
        try:
            response = s.recv(4096).decode().strip()
            data = json.loads(response)
            print(f"<< Response: {data.get('text', 'No text')}")
            print(f"   Status: {data.get('status', 'unknown')}")
        except Exception as e:
            print(f"[ERROR] Error receiving: {e}")
            break
        
        time.sleep(0.5)
    
    s.close()
    print("\n" + "="*60)
    print("Test complete!")
    print("="*60)

if __name__ == "__main__":
    test_ai_server()

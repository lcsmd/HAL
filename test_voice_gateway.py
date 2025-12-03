#!/usr/bin/env python3
"""
Test Voice Gateway Connection
"""

import asyncio
import websockets
import json

async def test_gateway():
    """Test connection to Voice Gateway"""
    
    print("="*60)
    print("Testing Voice Gateway on localhost:8768")
    print("="*60)
    
    try:
        # Connect
        print("\n[1] Connecting...")
        async with websockets.connect("ws://localhost:8768") as ws:
            print("[OK] Connected!")
            
            # Receive initial state
            print("\n[2] Waiting for initial state...")
            response = await asyncio.wait_for(ws.recv(), timeout=5.0)
            data = json.loads(response)
            print(f"[OK] Received: {data.get('type')}")
            print(f"     Session ID: {data.get('session_id')}")
            print(f"     State: {data.get('state')}")
            
            session_id = data.get('session_id')
            
            # Send text input
            print("\n[3] Sending text query...")
            query = {
                "type": "text_input",
                "session_id": session_id,
                "text": "what time is it"
            }
            await ws.send(json.dumps(query))
            print("[OK] Query sent")
            
            # Wait for responses
            print("\n[4] Waiting for responses...")
            responses = []
            for i in range(5):  # Collect up to 5 messages
                try:
                    msg = await asyncio.wait_for(ws.recv(), timeout=10.0)
                    data = json.loads(msg)
                    responses.append(data)
                    print(f"     [{i+1}] {data.get('type')}: {str(data)[:80]}")
                    
                    # Stop if we get the final response
                    if data.get('type') == 'response':
                        print(f"\n[SUCCESS] Response: {data.get('text')}")
                        break
                except asyncio.TimeoutError:
                    print(f"     [{i+1}] Timeout waiting for message")
                    break
            
            print("\n" + "="*60)
            print("Test Complete!")
            print("="*60)
            
    except Exception as e:
        print(f"\n[ERROR] {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_gateway())

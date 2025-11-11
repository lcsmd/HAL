#!/usr/bin/env python
"""Test QM listener WITHOUT sending EOF"""
import asyncio
import json

async def test_qm():
    print("Testing QM listener without EOF...")
    
    try:
        # Connect
        reader, writer = await asyncio.open_connection('localhost', 8767)
        print("Connected!")
        
        # Send message
        message = {
            'transcription': 'What medications am I taking?',
            'session_id': 'test-session-123'
        }
        
        message_bytes = json.dumps(message).encode() + b'\n'
        print(f"Sending {len(message_bytes)} bytes...")
        writer.write(message_bytes)
        await writer.drain()
        
        # DON'T send EOF - just wait for response
        print("Waiting for response (no EOF sent)...")
        
        # Read response with timeout
        try:
            response_data = await asyncio.wait_for(reader.read(4096), timeout=3.0)
            print(f"Received: {len(response_data)} bytes")
            print(f"Response: {response_data.decode()}")
            
            response = json.loads(response_data.decode())
            print(f"\nSuccess!")
            print(f"  Text: {response.get('response_text')}")
            print(f"  Intent: {response.get('intent')}")
        except asyncio.TimeoutError:
            print("Timeout - no response")
        
        writer.close()
        await writer.wait_closed()
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_qm())

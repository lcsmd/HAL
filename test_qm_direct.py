#!/usr/bin/env python
"""Test QM listener exactly as gateway does"""
import asyncio
import json

async def test_qm():
    print("Testing QM listener connection...")
    
    try:
        # Connect
        reader, writer = await asyncio.open_connection('localhost', 8767)
        print("Connected!")
        
        # Send message
        message = {
            'transcription': 'What medications am I taking?',
            'session_id': 'test-session-123',
            'timestamp': '2025-11-07T00:00:00',
            'client_type': 'test',
            'context': []
        }
        
        message_bytes = json.dumps(message).encode() + b'\n'
        print(f"Sending {len(message_bytes)} bytes...")
        writer.write(message_bytes)
        await writer.drain()
        
        # Send EOF
        try:
            writer.write_eof()
        except:
            pass
        
        print("Waiting for response...")
        
        # Read response
        response_data = b""
        while True:
            try:
                chunk = await asyncio.wait_for(reader.read(4096), timeout=5.0)
                if not chunk:
                    break
                response_data += chunk
                print(f"  Got chunk: {len(chunk)} bytes")
            except asyncio.TimeoutError:
                print("  Timeout waiting for more data")
                break
        
        print(f"\nTotal received: {len(response_data)} bytes")
        print(f"Response: {response_data.decode()}")
        
        writer.close()
        await writer.wait_closed()
        
        # Parse
        response = json.loads(response_data.decode())
        print(f"\nParsed successfully:")
        print(f"  Text: {response.get('response_text')}")
        print(f"  Action: {response.get('action_taken')}")
        print(f"  Intent: {response.get('intent')}")
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_qm())

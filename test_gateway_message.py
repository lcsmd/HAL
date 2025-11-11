#!/usr/bin/env python
"""Test with exact gateway message format"""
import asyncio
import json

async def test():
    print("Testing with exact gateway format...")
    r, w = await asyncio.open_connection('localhost', 8767)
    
    # Exact format gateway sends
    message = {
        'session_id': 'test-123',
        'transcription': 'What medications am I taking?',
        'timestamp': '2025-11-07T04:00:00.000000',
        'client_type': 'test',
        'context': []
    }
    
    msg_bytes = json.dumps(message).encode() + b'\n'
    print(f"Sending {len(msg_bytes)} bytes...")
    print(f"Message: {message}")
    
    w.write(msg_bytes)
    await w.drain()
    
    print("Waiting for response...")
    try:
        resp = await asyncio.wait_for(r.read(4096), timeout=3.0)
        print(f"Response ({len(resp)} bytes): {resp.decode()}")
    except asyncio.TimeoutError:
        print("TIMEOUT - no response")
    
    w.close()
    await w.wait_closed()

asyncio.run(test())

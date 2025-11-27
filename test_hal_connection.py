#!/usr/bin/env python3
"""Test connection to HAL server"""
import asyncio
import websockets
import sys

async def test_connection():
    uri = 'ws://10.1.34.103:8768'
    try:
        async with websockets.connect(uri, ping_interval=None) as ws:
            await ws.send('{"command":"ping"}')
            response = await asyncio.wait_for(ws.recv(), timeout=5)
            print('SUCCESS')
            return True
    except Exception as e:
        print(f'FAILED: {e}')
        return False

if __name__ == '__main__':
    result = asyncio.run(test_connection())
    sys.exit(0 if result else 1)

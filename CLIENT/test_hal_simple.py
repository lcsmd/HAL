#!/usr/bin/env python3
import asyncio
import websockets
import json

async def test():
    ws = await websockets.connect('ws://10.1.34.103:8768')
    print("Connected!")
    msg = await ws.recv()
    print(f"State: {msg}")
    data = json.loads(msg)
    session_id = data.get('session_id')
    print(f"Session ID: {session_id}")
    query = {'type': 'text_input', 'text': 'test query', 'session_id': session_id}
    await ws.send(json.dumps(query))
    print("Query sent!")
    for i in range(5):
        msg = await asyncio.wait_for(ws.recv(), timeout=5.0)
        print(f"Response {i+1}: {msg}")
        data = json.loads(msg)
        if data.get('type') == 'response':
            break
    await ws.close()

asyncio.run(test())

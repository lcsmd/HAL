"""
Simple Voice Interface Test
Tests WebSocket connection and basic message flow
"""

import asyncio
import websockets
import json
import uuid
from datetime import datetime

# Configuration
GATEWAY_URL = "ws://localhost:8765"  # Change to your QM server IP if testing remotely
SESSION_ID = str(uuid.uuid4())

async def test_connection():
    """Test basic WebSocket connection"""
    print(f"[{datetime.now()}] Connecting to {GATEWAY_URL}...")
    
    try:
        async with websockets.connect(GATEWAY_URL) as websocket:
            print(f"[{datetime.now()}] Connected!")
            
            # Wait for connection acknowledgment
            message = await websocket.recv()
            data = json.loads(message)
            print(f"[{datetime.now()}] Received: {data}")
            
            if data.get('type') == 'connected':
                print(f"[{datetime.now()}] ✓ Connection successful")
                print(f"[{datetime.now()}] Session ID: {data.get('session_id')}")
                return data.get('session_id')
            else:
                print(f"[{datetime.now()}] ✗ Unexpected message type: {data.get('type')}")
                return None
                
    except Exception as e:
        print(f"[{datetime.now()}] ✗ Connection failed: {e}")
        return None

async def test_wake_word(session_id):
    """Test wake word detection flow"""
    print(f"\n[{datetime.now()}] Testing wake word detection...")
    
    async with websockets.connect(GATEWAY_URL) as websocket:
        # Wait for connection
        await websocket.recv()
        
        # Send wake word detected message
        message = {
            'type': 'wake_word_detected',
            'session_id': session_id,
            'wake_word': 'hey hal',
            'confidence': 0.95,
            'timestamp': datetime.now().isoformat()
        }
        
        print(f"[{datetime.now()}] Sending wake word message...")
        await websocket.send(json.dumps(message))
        
        # Wait for acknowledgment
        response = await websocket.recv()
        data = json.loads(response)
        print(f"[{datetime.now()}] Received: {data}")
        
        if data.get('type') == 'ack':
            print(f"[{datetime.now()}] ✓ Acknowledgment received")
        else:
            print(f"[{datetime.now()}] ✗ Expected 'ack', got: {data.get('type')}")
        
        # Wait for state change
        response = await websocket.recv()
        data = json.loads(response)
        print(f"[{datetime.now()}] Received: {data}")
        
        if data.get('type') == 'state_change' and data.get('new_state') == 'active_listening':
            print(f"[{datetime.now()}] ✓ State changed to active listening")
            return True
        else:
            print(f"[{datetime.now()}] ✗ Expected state change to active_listening")
            return False

async def test_command(session_id, command):
    """Test interrupt commands"""
    print(f"\n[{datetime.now()}] Testing command: {command}")
    
    async with websockets.connect(GATEWAY_URL) as websocket:
        # Wait for connection
        await websocket.recv()
        
        # Send command
        message = {
            'type': 'command',
            'session_id': session_id,
            'command': command,
            'timestamp': datetime.now().isoformat()
        }
        
        print(f"[{datetime.now()}] Sending command...")
        await websocket.send(json.dumps(message))
        
        # Wait for response
        response = await websocket.recv()
        data = json.loads(response)
        print(f"[{datetime.now()}] Received: {data}")
        
        return data

async def test_heartbeat(session_id):
    """Test heartbeat/keepalive"""
    print(f"\n[{datetime.now()}] Testing heartbeat...")
    
    async with websockets.connect(GATEWAY_URL) as websocket:
        # Wait for connection
        await websocket.recv()
        
        # Send heartbeat
        message = {
            'type': 'heartbeat',
            'session_id': session_id,
            'timestamp': datetime.now().isoformat()
        }
        
        print(f"[{datetime.now()}] Sending heartbeat...")
        await websocket.send(json.dumps(message))
        
        # No response expected, just checking it doesn't error
        await asyncio.sleep(0.5)
        print(f"[{datetime.now()}] ✓ Heartbeat sent successfully")

async def run_tests():
    """Run all tests"""
    print("=" * 60)
    print("HAL Voice Interface - Simple Test Suite")
    print("=" * 60)
    
    # Test 1: Connection
    session_id = await test_connection()
    if not session_id:
        print("\n✗ Connection test failed. Is the Voice Gateway running?")
        print("  Start it with: python PY/voice_gateway.py")
        return
    
    # Test 2: Wake word
    success = await test_wake_word(session_id)
    if not success:
        print("\n✗ Wake word test failed")
    
    # Test 3: Heartbeat
    await test_heartbeat(session_id)
    
    # Test 4: Commands
    await test_command(session_id, 'hold')
    await asyncio.sleep(0.5)
    await test_command(session_id, 'stop')
    await asyncio.sleep(0.5)
    await test_command(session_id, 'goodbye')
    
    print("\n" + "=" * 60)
    print("Test suite complete!")
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(run_tests())

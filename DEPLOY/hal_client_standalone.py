#!/usr/bin/env python3
"""
HAL Voice Assistant - Standalone Windows Client
Copy this file to any Windows PC and run it
No installation required (except Python 3.x and websockets)
"""

import asyncio
import sys
import os

# Try to import websockets
try:
    import websockets
except ImportError:
    print("="*60)
    print("FIRST TIME SETUP")
    print("="*60)
    print("\nInstalling websockets library...")
    print("Run this command:")
    print("  pip install websockets")
    print("\nOr:")
    print("  python -m pip install websockets")
    print("\nThen run this script again.\n")
    input("Press ENTER to exit...")
    sys.exit(1)

import json
from datetime import datetime

# CONFIGURATION - Change this to your HAL server IP
GATEWAY_URL = 'ws://10.1.34.103:8768'

class HALClient:
    def __init__(self, gateway_url):
        self.gateway_url = gateway_url
        self.session_id = None
        self.websocket = None
        
    async def connect(self):
        """Connect to HAL Voice Gateway"""
        print("\n" + "="*60)
        print(f"Connecting to HAL at {self.gateway_url}")
        print("="*60 + "\n")
        
        try:
            self.websocket = await websockets.connect(self.gateway_url)
            
            # Wait for initial state message
            response = await asyncio.wait_for(self.websocket.recv(), timeout=5.0)
            data = json.loads(response)
            
            if data.get('type') == 'connected':
                self.session_id = data.get('session_id')
                print("[OK] Connected to HAL")
                print(f"Session ID: {self.session_id}\n")
                return True
            
            print(f"[ERROR] Unexpected response: {data}")
            return False
            
        except asyncio.TimeoutError:
            print("[ERROR] Connection timeout")
            print("\nTroubleshooting:")
            print("  1. Is HAL server running?")
            print("  2. Is Voice Gateway running on server?")
            print("  3. Check IP address in script (currently: 10.1.34.103)")
            print("  4. Check firewall settings")
            return False
        except ConnectionRefusedError:
            print("[ERROR] Connection refused")
            print("\nTroubleshooting:")
            print("  1. Voice Gateway not running on server")
            print("  2. Wrong IP address (check GATEWAY_URL in script)")
            print("  3. Firewall blocking port 8768")
            return False
        except Exception as e:
            print(f"[ERROR] Connection failed: {e}")
            return False
    
    async def send_query(self, text):
        """Send text query to HAL"""
        if not self.websocket:
            print("[ERROR] Not connected!")
            return None
            
        try:
            # Send text input message
            message = {
                'type': 'text_input',
                'text': text,
                'session_id': self.session_id
            }
            
            await self.websocket.send(json.dumps(message))
            
            # Wait for response
            while True:
                response = await asyncio.wait_for(
                    self.websocket.recv(),
                    timeout=30.0
                )
                
                data = json.loads(response)
                msg_type = data.get('type')
                
                if msg_type == 'processing':
                    print("  [Processing...]")
                    
                elif msg_type == 'response':
                    response_text = data.get('text', '')
                    print("\n" + "="*60)
                    print(f"HAL: {response_text}")
                    print("="*60 + "\n")
                    return response_text
                    
                elif msg_type == 'error':
                    print(f"  [ERROR] {data.get('message')}")
                    return None
                    
        except asyncio.TimeoutError:
            print("[ERROR] Timeout waiting for response")
        except Exception as e:
            print(f"[ERROR] {e}")
            
        return None
    
    async def interactive(self):
        """Interactive mode"""
        print("="*60)
        print("HAL Voice Assistant - Interactive Mode")
        print("="*60)
        print("\nCommands:")
        print("  - Type your question and press ENTER")
        print("  - Type 'quit' or 'exit' to close")
        print("  - Type 'help' for examples\n")
        print("="*60 + "\n")
        
        while True:
            try:
                query = input("You: ").strip()
                
                if not query:
                    continue
                    
                if query.lower() in ['quit', 'exit', 'bye', 'q']:
                    print("\nGoodbye!\n")
                    break
                    
                if query.lower() == 'help':
                    print("\nExample queries:")
                    print("  - what time is it")
                    print("  - what is the date")
                    print("  - hello")
                    print("  - test")
                    print()
                    continue
                
                await self.send_query(query)
                
            except (KeyboardInterrupt, EOFError):
                print("\n\nGoodbye!\n")
                break
            except Exception as e:
                print(f"[ERROR] {e}")
    
    async def close(self):
        """Close connection"""
        if self.websocket:
            await self.websocket.close()

async def main():
    """Main function"""
    print("="*60)
    print("HAL Voice Assistant - Standalone Client")
    print("="*60)
    print(f"Server: {GATEWAY_URL}")
    print("="*60 + "\n")
    
    # Create client
    client = HALClient(GATEWAY_URL)
    
    # Connect
    if not await client.connect():
        print("\nConnection failed. Press ENTER to exit...")
        input()
        return 1
    
    # Run interactive mode
    try:
        await client.interactive()
    finally:
        await client.close()
    
    return 0

if __name__ == "__main__":
    try:
        exit_code = asyncio.run(main())
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n\nInterrupted. Goodbye!\n")
        sys.exit(0)
    except Exception as e:
        print(f"\n[FATAL ERROR] {e}\n")
        input("Press ENTER to exit...")
        sys.exit(1)

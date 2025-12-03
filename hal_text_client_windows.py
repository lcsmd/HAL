#!/usr/bin/env python3
"""
HAL Text Client for Windows
Simple text interface - Windows console compatible (no Unicode emoji)
"""

import asyncio
import websockets
import json
import sys

# Configuration
GATEWAY_URL = 'ws://10.1.34.103:8768'

class HALTextClient:
    def __init__(self, gateway_url):
        self.gateway_url = gateway_url
        self.session_id = None
        self.websocket = None
        
    async def connect(self):
        """Connect to HAL Voice Gateway"""
        print("\n" + "="*60)
        print(f"Connecting to HAL at {self.gateway_url}...")
        print("="*60 + "\n")
        
        try:
            self.websocket = await websockets.connect(self.gateway_url)
            
            # Wait for initial state message
            response = await asyncio.wait_for(self.websocket.recv(), timeout=5.0)
            data = json.loads(response)
            
            if data.get('type') == 'connected':
                self.session_id = data.get('session_id')
                print("[OK] Connected to HAL Voice Gateway")
                print(f"   Session ID: {self.session_id}")
                print(f"   State: {data.get('state')}\n")
                return True
            
            print(f"[ERROR] Unexpected response: {data}")
            return False
            
        except asyncio.TimeoutError:
            print("[ERROR] Connection timeout. Is Voice Gateway running?")
            print("   Run: cd C:\\qmsys\\hal && python PY\\voice_gateway.py")
            return False
        except ConnectionRefusedError:
            print("[ERROR] Connection refused. Possible issues:")
            print("   1. Voice Gateway not running")
            print("   2. Wrong IP address")
            print("   3. Firewall blocking port 8768")
            return False
        except Exception as e:
            print(f"[ERROR] Connection failed: {e}")
            return False
    
    async def send_text_query(self, text):
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
            print("   [SENT] Query sent to HAL...")
            
            # Wait for responses
            response_text = None
            
            while True:
                response = await asyncio.wait_for(
                    self.websocket.recv(),
                    timeout=30.0
                )
                
                data = json.loads(response)
                msg_type = data.get('type')
                
                if msg_type == 'processing':
                    print("   [PROCESSING] HAL is thinking...")
                    
                elif msg_type == 'response':
                    response_text = data.get('text', '')
                    
                    print("\n" + "="*60)
                    print(f"HAL: {response_text}")
                    print("="*60 + "\n")
                    break
                    
                elif msg_type == 'error':
                    print(f"   [ERROR] {data.get('message')}")
                    break
                    
        except asyncio.TimeoutError:
            print("[ERROR] Timeout waiting for response (30 seconds)")
        except Exception as e:
            print(f"[ERROR] {e}")
            
        return response_text
    
    async def interactive_mode(self):
        """Interactive query mode"""
        print("="*60)
        print("HAL Text Client - Interactive Mode")
        print("="*60)
        print("\nCommands:")
        print("  - Type your question and press ENTER")
        print("  - Type 'quit' or 'exit' to close")
        print("  - Type 'help' for example queries\n")
        print("="*60 + "\n")
        
        while True:
            try:
                query = input("You: ").strip()
                
                if not query:
                    continue
                    
                if query.lower() in ['quit', 'exit', 'bye']:
                    print("\nGoodbye!\n")
                    break
                    
                if query.lower() == 'help':
                    print("\nExample queries:")
                    print("  - what time is it")
                    print("  - what is the date")
                    print("  - hello")
                    print("  - how are you")
                    print()
                    continue
                
                await self.send_text_query(query)
                
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
    # Parse command line arguments
    import argparse
    parser = argparse.ArgumentParser(description='HAL Text Client for Windows')
    parser.add_argument('--server', default=GATEWAY_URL, help='Gateway URL (default: ws://10.1.34.103:8768)')
    parser.add_argument('--query', help='Single query mode (instead of interactive)')
    args = parser.parse_args()
    
    # Create client
    client = HALTextClient(args.server)
    
    # Connect
    if not await client.connect():
        return 1
    
    # Run query or interactive mode
    try:
        if args.query:
            # Single query mode
            print(f"Query: {args.query}\n")
            await client.send_text_query(args.query)
        else:
            # Interactive mode
            await client.interactive_mode()
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

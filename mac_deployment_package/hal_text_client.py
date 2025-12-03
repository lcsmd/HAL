#!/usr/bin/env python3
"""
HAL Text Client for MacBook Pro
Simple text interface to HAL Voice Gateway
No audio dependencies - pure text mode for testing and basic usage
"""

import asyncio
import websockets
import json
import sys
import os
from datetime import datetime

# Configuration - Your HAL Network
# QM Server: 10.1.34.103 (Windows with OpenQM)
# Voice Gateway runs on QM Server port 8768
GATEWAY_URL = os.getenv('HAL_GATEWAY_URL', 'ws://10.1.34.103:8768')

class HALTextClient:
    def __init__(self, gateway_url):
        self.gateway_url = gateway_url
        self.session_id = None
        self.websocket = None
        
    async def connect(self):
        """Connect to HAL Voice Gateway"""
        print(f"\n{'='*60}")
        print(f"Connecting to HAL at {self.gateway_url}...")
        print(f"{'='*60}\n")
        
        try:
            self.websocket = await websockets.connect(self.gateway_url)
            
            # Wait for initial state message
            response = await asyncio.wait_for(self.websocket.recv(), timeout=5.0)
            data = json.loads(response)
            
            if data.get('type') == 'connected':
                self.session_id = data.get('session_id')
                print(f"[OK] Connected to HAL Voice Gateway")
                print(f"   Session ID: {self.session_id}")
                print(f"   State: {data.get('state')}\n")
                return True
            
            print(f"[ERROR] Unexpected response: {data}")
            return False
            
        except asyncio.TimeoutError:
            print(f"[ERROR] Connection timeout. Is Voice Gateway running?")
            return False
        except ConnectionRefusedError:
            print(f"[ERROR] Connection refused. Possible issues:")
            print(f"   1. Voice Gateway not running on Windows")
            print(f"   2. Wrong IP address in GATEWAY_URL")
            print(f"   3. Firewall blocking port 8768")
            return False
        except Exception as e:
            print(f"[ERROR] Connection failed: {e}")
            return False
    
    async def send_text_query(self, text):
        """Send text query to HAL"""
        if not self.websocket:
            print("❌ Not connected!")
            return None
            
        try:
            # Send text input message
            message = {
                'type': 'text_input',
                'text': text,
                'session_id': self.session_id,
                'timestamp': datetime.now().isoformat()
            }
            
            await self.websocket.send(json.dumps(message))
            
            # Wait for responses
            response_text = None
            
            while True:
                response = await asyncio.wait_for(
                    self.websocket.recv(),
                    timeout=30.0
                )
                
                data = json.loads(response)
                msg_type = data.get('type')
                
                if msg_type == 'response':
                    response_text = data.get('text', '')
                    intent = data.get('intent', 'unknown')
                    action = data.get('action_taken', 'unknown')
                    
                    print(f"\n{'='*60}")
                    print(f"HAL: {response_text}")
                    print(f"{'='*60}")
                    print(f"   Intent: {intent}")
                    print(f"   Action: {action}")
                    print(f"{'─'*60}\n")
                    
                    return response_text
                    
                elif msg_type == 'processing':
                    print("   ⏳ HAL is processing...")
                    
                elif msg_type == 'state_change':
                    new_state = data.get('new_state')
                    print(f"   → State: {new_state}")
                    
                elif msg_type == 'error':
                    print(f"   ❌ Error: {data.get('message')}")
                    return None
                    
        except asyncio.TimeoutError:
            print("❌ Timeout waiting for response (30 seconds)")
            return None
        except Exception as e:
            print(f"❌ Error: {e}")
            return None
    
    async def interactive_mode(self):
        """Interactive text chat with HAL"""
        print(f"\n{'='*60}")
        print("HAL Text Client - Interactive Mode")
        print(f"{'='*60}")
        print("\nCommands:")
        print("  • Type your question and press ENTER")
        print("  • Type 'quit' or 'exit' to close")
        print("  • Type 'help' for example queries")
        print(f"\n{'='*60}\n")
        
        while True:
            try:
                # Get user input
                query = input("You: ").strip()
                
                if not query:
                    continue
                    
                if query.lower() in ['quit', 'exit', 'q', 'bye']:
                    print("\n👋 Goodbye!\n")
                    break
                
                if query.lower() == 'help':
                    self.show_help()
                    continue
                
                # Send to HAL
                await self.send_text_query(query)
                
            except KeyboardInterrupt:
                print("\n\n👋 Goodbye!\n")
                break
            except EOFError:
                print("\n\n👋 Goodbye!\n")
                break
            except Exception as e:
                print(f"❌ Error: {e}")
    
    def show_help(self):
        """Show example queries"""
        print(f"\n{'='*60}")
        print("Example Queries:")
        print(f"{'='*60}")
        print("\n📋 Medical:")
        print("  • What medications am I taking?")
        print("  • Show my allergy list")
        print("  • When is my next doctor appointment?")
        print("  • What were my last vital signs?")
        print("\n💰 Financial:")
        print("  • Show recent transactions")
        print("  • What did I spend at Starbucks?")
        print("  • List my reimbursable expenses")
        print("\n📝 General:")
        print("  • Hello HAL")
        print("  • What can you do?")
        print("  • Tell me about yourself")
        print(f"\n{'='*60}\n")
    
    async def close(self):
        """Close connection"""
        if self.websocket:
            await self.websocket.close()

async def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='HAL Text Client for MacBook Pro',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Interactive mode
  python3 hal_text_client.py
  
  # Single query
  python3 hal_text_client.py --query "What medications am I taking?"
  
  # Custom server
  python3 hal_text_client.py --url ws://192.168.1.100:8768
  
Environment Variables:
  HAL_GATEWAY_URL - Voice Gateway URL (default: ws://localhost:8768)
        """
    )
    
    parser.add_argument('--url', default=GATEWAY_URL, 
                       help='Voice Gateway URL (ws://ip:port)')
    parser.add_argument('--query', help='Single query mode')
    
    args = parser.parse_args()
    
    # Create client
    client = HALTextClient(args.url)
    
    # Connect
    if not await client.connect():
        print("\n⚠️  Connection failed. Check:")
        print("   1. Voice Gateway is running: python PY/voice_gateway.py")
        print("   2. Windows server IP is correct")
        print("   3. Firewall allows port 8768")
        print("   4. Both machines on same network\n")
        return 1
    
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

if __name__ == '__main__':
    try:
        exit_code = asyncio.run(main())
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!\n")
        sys.exit(0)

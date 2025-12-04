#!/usr/bin/env python3
"""
Simple HTTPS server to serve HAL web client
"""

import http.server
import socketserver
import ssl
import os

PORT = 8443  # Standard HTTPS port (or use 8443)
DIRECTORY = os.path.dirname(os.path.abspath(__file__))

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)
    
    def end_headers(self):
        # Enable CORS
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

if __name__ == '__main__':
    os.chdir(DIRECTORY)
    
    with socketserver.TCPServer(("", PORT), MyHTTPRequestHandler) as httpd:
        # Add SSL
        cert_file = os.path.join(DIRECTORY, 'cert.pem')
        key_file = os.path.join(DIRECTORY, 'key.pem')
        
        if os.path.exists(cert_file) and os.path.exists(key_file):
            context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
            context.load_cert_chain(cert_file, key_file)
            httpd.socket = context.wrap_socket(httpd.socket, server_side=True)
            protocol = "https"
        else:
            protocol = "http"
            print(f"[WARN] SSL certificates not found - running without HTTPS")
            print(f"[WARN] Microphone will not work without HTTPS!")
        
        print(f"=" * 60)
        print(f"HAL Web Client Server (HTTPS)")
        print(f"=" * 60)
        print(f"")
        print(f"Server running at: {protocol}://10.1.34.103:{PORT}")
        print(f"")
        print(f"From ANY computer on your network:")
        print(f"  1. Open a web browser")
        print(f"  2. Go to: {protocol}://10.1.34.103:{PORT}")
        print(f"  3. Accept the security warning (self-signed cert)")
        print(f"  4. Allow microphone access")
        print(f"  5. Click 🎤 and say 'Hey Jarvis'")
        print(f"")
        print(f"Press Ctrl+C to stop")
        print(f"=" * 60)
        print()
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServer stopped")

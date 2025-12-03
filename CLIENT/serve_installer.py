#!/usr/bin/env python
"""
Simple HTTP server to serve HAL Mac installer
Run this on Windows to allow Mac to download installer
Usage: python serve_installer.py
"""

import http.server
import socketserver
import os

PORT = 8080
DIRECTORY = os.path.dirname(os.path.abspath(__file__))

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)
    
    def end_headers(self):
        # Allow CORS
        self.send_header('Access-Control-Allow-Origin', '*')
        super().end_headers()

if __name__ == '__main__':
    os.chdir(DIRECTORY)
    
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        import socket
        
        # Get all IP addresses
        hostname = socket.gethostname()
        
        # Try to get the actual network IP (not localhost)
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            # Connect to external address to find local IP
            s.connect(('8.8.8.8', 80))
            local_ip = s.getsockname()[0]
            s.close()
        except:
            # Fallback to hostname lookup
            local_ip = socket.gethostbyname(hostname)
        
        print("="*60)
        print("HAL Mac Installer Server")
        print("="*60)
        print(f"\nYour Windows Server IP: {local_ip}")
        print(f"Serving installer at: http://{local_ip}:{PORT}/")
        print(f"\n" + "="*60)
        print(f"INSTALLATION COMMANDS:")
        print(f"="*60)
        
        print(f"\nMAC CLIENTS:")
        print(f"-" * 60)
        print(f"\n1. LOCAL NETWORK:")
        print(f"   curl -fsSL http://{local_ip}:{PORT}/install_hal_mac.sh | \\")
        print(f"   HAL_SERVER_URL=http://{local_ip}:8768 bash")
        
        print(f"\n2. INTERACTIVE (will prompt for URL):")
        print(f"   curl -fsSL http://{local_ip}:{PORT}/install_hal_mac.sh | bash")
        
        print(f"\n\nWINDOWS CLIENTS:")
        print(f"-" * 60)
        print(f"\n1. LOCAL NETWORK (PowerShell as Administrator):")
        print(f"   $env:HAL_SERVER_URL=\"http://{local_ip}:8768\"; iex (irm http://{local_ip}:{PORT}/install_hal_windows.ps1)")
        
        print(f"\n2. INTERACTIVE (will prompt for URL):")
        print(f"   iex (irm http://{local_ip}:{PORT}/install_hal_windows.ps1)")
        
        print(f"\n" + "="*60)
        print(f"NOTE: For external access, configure HAProxy to route:")
        print(f"  https://your-domain/ -> localhost:8768 (Voice Gateway)")
        print(f"="*60)
        print(f"\nPress Ctrl+C to stop the installer server...")
        print("="*60)
        print()
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n\nShutting down...")

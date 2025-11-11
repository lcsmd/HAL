#!/usr/bin/env python
"""Extract socket documentation from QM_HELP directory"""
from datetime import datetime
import os
import re

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
base_dir = "C:\\qmsys\\hal\\COM"
help_dir = "C:\\qmsys\\hal\\QM_HELP"

# Socket-related help files to extract
socket_files = [
    "qmb_accept_socket_connection.htm",
    "qmb_close_socket.htm",
    "qmb_create_server_socket.htm",
    "qmb_open_socket.htm",
    "qmb_read_socket.htm",
    "qmb_write_socket.htm",
    "qmb_server_socket.htm",
    "qmb_socket_info.htm"
]

output_filename = f"SOCKET_DOCS_{timestamp}.txt"
output_path = os.path.join(base_dir, output_filename)

with open(output_path, 'w', encoding='utf-8', errors='ignore') as out:
    out.write("="*70 + "\n")
    out.write("QM SOCKET FUNCTION DOCUMENTATION\n")
    out.write(f"Extracted: {timestamp}\n")
    out.write("="*70 + "\n\n")
    
    for filename in socket_files:
        filepath = os.path.join(help_dir, filename)
        if os.path.exists(filepath):
            out.write("\n" + "="*70 + "\n")
            out.write(f"FILE: {filename}\n")
            out.write("="*70 + "\n")
            
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                
                # Extract text from HTML (simple extraction)
                # Remove HTML tags
                text = re.sub(r'<[^>]+>', ' ', content)
                # Remove multiple spaces
                text = re.sub(r'\s+', ' ', text)
                # Remove special chars
                text = text.replace('&nbsp;', ' ')
                text = text.replace('&quot;', '"')
                text = text.replace('&lt;', '<')
                text = text.replace('&gt;', '>')
                
                out.write(text)
                out.write("\n\n")
        else:
            out.write(f"\n[NOT FOUND: {filename}]\n")

print(f"Created: {output_filename}")
print(f"Location: {base_dir}")
print(f"\nExtracted documentation for {len(socket_files)} socket functions")

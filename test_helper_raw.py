"""Test QM helper with raw bytes"""
import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(('localhost', 8766))

# Send simple command
sock.sendall(b"LIST.READU\n")

# Read raw response
response = b""
while len(response) < 1000:
    chunk = sock.recv(1024)
    if not chunk:
        break
    response += chunk
    if b"}" in response:
        break

sock.close()

print(f"Received {len(response)} bytes")
print(f"Raw bytes (first 300): {response[:300]}")
print(f"\nHex dump (first 200):")
for i in range(0, min(200, len(response)), 16):
    hex_str = ' '.join(f'{b:02x}' for b in response[i:i+16])
    ascii_str = ''.join(chr(b) if 32 <= b < 127 else '.' for b in response[i:i+16])
    print(f"{i:04x}: {hex_str:<48} {ascii_str}")

print(f"\nTrying UTF-8: ", end="")
try:
    decoded = response.decode('utf-8')
    print(f"Success! Length: {len(decoded)}")
    print(f"Content: {repr(decoded[:200])}")
except Exception as e:
    print(f"Failed: {e}")

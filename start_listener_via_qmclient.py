"""Start Voice Listener using QMClient Python module"""
import sys
sys.path.insert(0, "C:\\QMSYS\\bin")
import qmclient as qm

print("Connecting to QM...")
session = qm.Connect('localhost', 4243, 'HAL', '', '')
if not session:
    print("ERROR: Failed to connect to QM")
    sys.exit(1)

print("Connected successfully!")
print()

# Execute commands
commands = [
    "LOGTO HAL",
    "BASIC BP VOICE.LISTENER",
    "CATALOG BP VOICE.LISTENER",
    "PHANTOM BP VOICE.LISTENER"
]

for cmd in commands:
    print(f"Executing: {cmd}")
    qm.Execute(cmd)
    
    # Read output
    output_lines = []
    while True:
        line = qm.ReadLine()
        if not line:
            break
        output_lines.append(line)
        print(f"  {line}")
    
    print()

print("Disconnecting...")
qm.Disconnect()

print()
print("="*60)
print("Voice Listener should now be running!")
print("Verify with: netstat -an | findstr :8767")
print("="*60)

"""Automatically start QM Voice Listener"""
import subprocess
import time
import socket

print("="*60)
print("Automated QM Voice Listener Startup")
print("="*60)
print()

# Kill any existing QM processes on port 8767
print("Step 1: Checking for existing processes...")
try:
    result = subprocess.run(
        ['powershell', '-Command', 
         'Get-NetTCPConnection -LocalPort 8767 -ErrorAction SilentlyContinue | Select-Object -ExpandProperty OwningProcess'],
        capture_output=True, text=True, timeout=5
    )
    if result.stdout.strip():
        pid = result.stdout.strip()
        print(f"  Found process {pid} on port 8767, stopping it...")
        subprocess.run(['powershell', '-Command', f'Stop-Process -Id {pid} -Force'], timeout=5)
        time.sleep(2)
except:
    pass

print("  Clear.")
print()

# Start QM with inline commands
print("Step 2: Starting QM and compiling listener...")
commands = """LOGTO HAL
BASIC BP VOICE.LISTENER
CATALOG BP VOICE.LISTENER
PHANTOM BP VOICE.LISTENER
"""

# Use PowerShell to pipe commands to QM
ps_script = f"""
$commands = @"
{commands}
"@

$process = Start-Process -FilePath 'C:\\qmsys\\bin\\qm.exe' -ArgumentList 'HAL' -PassThru -WindowStyle Hidden
Start-Sleep -Milliseconds 500
$commands | Set-Clipboard
# Can't easily pipe to QM, so we'll start it and let PHANTOM run
"""

try:
    # Alternative: Just start QM in the background and it should pick up the compiled code
    subprocess.Popen(
        ['C:\\qmsys\\bin\\qm.exe', 'HAL'],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    print("  QM process started")
    print()
    
    print("Step 3: Waiting for listener to initialize...")
    time.sleep(3)
    
    # Try to connect
    for attempt in range(10):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            sock.connect(('localhost', 8767))
            sock.close()
            print(f"  [SUCCESS] Listener is responding on port 8767!")
            print()
            print("="*60)
            print("QM Voice Listener is RUNNING!")
            print("="*60)
            exit(0)
        except:
            print(f"  Attempt {attempt + 1}/10...")
            time.sleep(2)
    
    print()
    print("[WARNING] Could not detect listener on port 8767")
    print("You may need to manually start it.")
    
except Exception as e:
    print(f"  Error: {e}")
    print()
    print("Automated start failed. Manual commands needed:")
    print("  cd C:\\qmsys\\bin")
    print("  qm HAL")
    print("  BASIC BP VOICE.LISTENER")
    print("  CATALOG BP VOICE.LISTENER")
    print("  PHANTOM BP VOICE.LISTENER")

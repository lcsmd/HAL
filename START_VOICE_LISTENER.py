"""Start Voice Listener - Clean automated startup"""
import sys
import time
import subprocess

sys.path.insert(0, "C:\\QMSYS\\SYSCOM")
import ctypes
qm_dll = ctypes.cdll.LoadLibrary("C:\\QMSYS\\bin\\qmclilib.dll")
import qmclient as qm
qm.__qm_lib = qm_dll
qm.__LoadQMCliLib = lambda: None

print("Connecting to QM...")
session = qm.ConnectLocal('HAL')
if not session:
    print("[ERROR] Connection failed")
    sys.exit(1)
print("[OK] Connected")

# Get current phantoms
print("\nChecking for existing VOICE.LISTENER phantoms...")
result = subprocess.run("C:\\QMSYS\\bin\\qm.exe -aHAL -u lawr -p apgar-66 LIST.READU", 
                       shell=True, capture_output=True, text=True)
uids_to_logout = []
for line in result.stdout.split('\n'):
    if 'VOICE.LISTENER' in line:
        # Extract UID from the line
        parts = line.strip().split()
        if parts and parts[0].isdigit():
            uids_to_logout.append(int(parts[0]))

if uids_to_logout:
    print(f"Found UIDs to logout: {uids_to_logout}")
    for uid in uids_to_logout:
        try:
            qm.Execute(f"LOGOUT {uid}")
            print(f"  Logged out UID {uid}")
            time.sleep(0.5)
        except:
            print(f"  Could not logout {uid}")
    time.sleep(3)
else:
    print("No existing phantoms found")

# Don't copy - assume VOICE.LISTENER is already the correct version
print("\nUsing existing BP/VOICE.LISTENER file...")
print("[OK] Ready")

# Compile and catalog with LOCAL
print("\nCompiling and cataloging...")
try:
    qm.Execute("LOGTO HAL")
    time.sleep(0.5)
except:
    pass

try:
    qm.Execute("BASIC BP VOICE.LISTENER")
    time.sleep(1)
    print("[OK] Compiled")
except Exception as e:
    print(f"  Compile error: {e}")

try:
    qm.Execute("CATALOG BP VOICE.LISTENER LOCAL")
    time.sleep(1)
    print("[OK] Cataloged with LOCAL")
except Exception as e:
    print(f"  Catalog error: {e}")

# Start PHANTOM
print("\nStarting PHANTOM VOICE.LISTENER...")
try:
    qm.Execute("PHANTOM VOICE.LISTENER")
    time.sleep(3)
    print("[OK] PHANTOM command sent")
except Exception as e:
    print(f"  PHANTOM error: {e}")

qm.Disconnect()

# Verify
print("\n" + "="*60)
print("Verifying...")
print("="*60)

time.sleep(2)

result = subprocess.run("netstat -an | findstr :8767", shell=True, capture_output=True, text=True)
if "LISTENING" in result.stdout:
    print("[SUCCESS] Port 8767 is LISTENING")
    
    # Test it
    print("\nTesting QM Listener...")
    test_result = subprocess.run("python test_qm_direct_newline.py", shell=True, cwd="C:\\qmsys\\hal")
    
    if test_result.returncode == 0:
        print("\n[SUCCESS] QM Listener is working!")
        print("\nNow test the full system:")
        print("  python tests\\test_text_input.py")
    else:
        print("\n[WARNING] QM Listener test failed")
else:
    print("[ERROR] Port 8767 not listening")
    print("Check COMO logs for errors")

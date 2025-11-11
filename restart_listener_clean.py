"""Kill all listeners, recompile with LOCAL, and start fresh"""
import sys
import time
import subprocess

sys.path.insert(0, "C:\\QMSYS\\SYSCOM")

# Load 64-bit QM DLL
import ctypes
qm_dll = ctypes.cdll.LoadLibrary("C:\\QMSYS\\bin\\qmclilib.dll")

# Import and patch qmclient
import qmclient as qm
qm.__qm_lib = qm_dll
qm.__LoadQMCliLib = lambda: None
print("[OK] QMClient ready")

# Connect
print("Connecting to QM...")
session = qm.ConnectLocal('HAL')
if not session:
    print("[ERROR] Connection failed")
    sys.exit(1)
print("[OK] Connected")

# Kill ALL VOICE.LISTENER phantoms
print("\nKilling all VOICE.LISTENER phantoms...")
for phantom_id in [14, 16]:
    try:
        qm.Execute(f"KILL.PHANTOM {phantom_id}")
        print(f"  Killed phantom {phantom_id}")
        time.sleep(0.5)
    except:
        pass

time.sleep(2)

# Recompile
print("\nRecompiling VOICE.LISTENER...")
try:
    qm.Execute("LOGTO HAL")
    time.sleep(0.5)
    qm.Execute("BASIC BP VOICE.LISTENER")
    time.sleep(1)
    print("[OK] Compiled")
except Exception as e:
    print(f"  Error: {e}")

# Catalog with LOCAL
print("\nCataloging with LOCAL...")
try:
    qm.Execute("CATALOG BP VOICE.LISTENER LOCAL")
    time.sleep(1)
    print("[OK] Cataloged")
except Exception as e:
    print(f"  Error: {e}")

# Start new phantom
print("\nStarting PHANTOM...")
try:
    qm.Execute("PHANTOM VOICE.LISTENER")
    time.sleep(2)
    print("[OK] Started")
except Exception as e:
    print(f"  Error: {e}")

# Disconnect
qm.Disconnect()

# Verify
print("\n" + "="*60)
time.sleep(3)

result = subprocess.run("netstat -an | findstr :8767", shell=True, capture_output=True, text=True)
if result.returncode == 0 and "LISTENING" in result.stdout:
    print("[SUCCESS] Listener is running!")
    
    # Test it
    print("\nTesting listener...")
    subprocess.run("python C:\\qmsys\\hal\\test_qm_direct_newline.py", shell=True)
else:
    print("[ERROR] Listener not running")

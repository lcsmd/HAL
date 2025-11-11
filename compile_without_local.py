"""Compile and catalog WITHOUT LOCAL option"""
import sys
import time
import subprocess

sys.path.insert(0, "C:\\QMSYS\\SYSCOM")
import ctypes
qm_dll = ctypes.cdll.LoadLibrary("C:\\QMSYS\\bin\\qmclilib.dll")
import qmclient as qm
qm.__qm_lib = qm_dll
qm.__LoadQMCliLib = lambda: None

session = qm.ConnectLocal('HAL')
if not session:
    print("[ERROR] Connection failed")
    sys.exit(1)
print("[OK] Connected to QM")

# Logout existing phantoms
print("\nLogging out existing VOICE.LISTENER phantoms...")
result = subprocess.run("C:\\QMSYS\\bin\\qm.exe -aHAL -u lawr -p apgar-66 LIST.READU", 
                       shell=True, capture_output=True, text=True)
for line in result.stdout.split('\n'):
    if 'VOICE.LISTENER' in line:
        parts = line.strip().split()
        if parts and parts[0].isdigit():
            uid = int(parts[0])
            print(f"  Logging out UID {uid}...")
            qm.Execute(f"LOGOUT {uid}")
            time.sleep(0.5)

time.sleep(3)

# Compile
print("\nCompiling BP VOICE.LISTENER...")
qm.Execute("LOGTO HAL")
time.sleep(0.5)
qm.Execute("BASIC BP VOICE.LISTENER")
time.sleep(1)
print("[OK] Compiled")

# Catalog WITHOUT LOCAL
print("\nCataloging BP VOICE.LISTENER (no LOCAL)...")
qm.Execute("CATALOG BP VOICE.LISTENER")
time.sleep(1)
print("[OK] Cataloged")

# Start PHANTOM
print("\nStarting PHANTOM VOICE.LISTENER...")
qm.Execute("PHANTOM VOICE.LISTENER")
time.sleep(3)
print("[OK] PHANTOM started")

qm.Disconnect()

# Verify
print("\n" + "="*60)
time.sleep(2)

result2 = subprocess.run("netstat -an | findstr :8767", shell=True, capture_output=True, text=True)
if "LISTENING" in result2.stdout:
    print("[SUCCESS] Port 8767 is LISTENING")
    print("\nTesting...")
    subprocess.run("python test_qm_direct_newline.py", shell=True, cwd="C:\\qmsys\\hal")
else:
    print("[ERROR] Port not listening")

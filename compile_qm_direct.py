"""Use qm.exe directly for compilation since qmclient.Execute has bugs"""
import subprocess
import time

print("Logging out existing phantoms...")
result = subprocess.run("C:\\QMSYS\\bin\\qm.exe -aHAL -u lawr -p apgar-66 LIST.READU", 
                       shell=True, capture_output=True, text=True)
uids = []
for line in result.stdout.split('\n'):
    if 'VOICE.LISTENER' in line:
        parts = line.strip().split()
        if parts and parts[0].isdigit():
            uids.append(parts[0])

for uid in uids:
    print(f"  LOGOUT {uid}")
    subprocess.run(f"C:\\QMSYS\\bin\\qm.exe -aHAL -u lawr -p apgar-66 \"LOGOUT {uid}\"", shell=True)
    time.sleep(0.5)

print("\nWaiting for port to be free...")
time.sleep(5)

print("\nCompiling and cataloging...")
# Use echo to pipe commands
subprocess.run('echo LOGTO HAL & echo BASIC BP VOICE.LISTENER & echo CATALOG BP VOICE.LISTENER & echo PHANTOM VOICE.LISTENER & echo QUIT | C:\\qmsys\\bin\\qm.exe HAL', shell=True, timeout=30)

print("\nWaiting for PHANTOM to start...")
time.sleep(3)

# Verify
result2 = subprocess.run("netstat -an | findstr :8767", shell=True, capture_output=True, text=True)
if "LISTENING" in result2.stdout:
    print("[SUCCESS] Port 8767 is LISTENING!")
    print("\nTesting...")
    subprocess.run("python test_qm_direct_newline.py", shell=True, cwd="C:\\qmsys\\hal")
else:
    print("[ERROR] Port not listening")

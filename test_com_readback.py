#!/usr/bin/env python
"""Test that COMMAND.EXECUTOR writes to COM and we can read it back"""
import subprocess
import time

print("Step 1: Write commands to COM INPUT record...")
write_cmd = 'OPEN "COM" TO F ELSE STOP; WRITE "WHO":CHAR(254):"TIME":CHAR(254):"COUNT COM" TO F, "INPUT"; CLOSE F'
subprocess.run(['C:\\qmsys\\bin\\qm.exe', '-aHAL', write_cmd], timeout=5)
print("  Written INPUT record")

print("\nStep 2: Run COMMAND.EXECUTOR...")
result = subprocess.run(
    'C:\\qmsys\\bin\\qm.exe -aHAL "RUN BP COMMAND.EXECUTOR"',
    shell=True,
    timeout=10
)
print("  Executor completed")

time.sleep(0.5)

print("\nStep 3: Read back the output record...")
date_prefix = "20251107"
for seq in range(1, 10):
    output_id = f"{date_prefix}-{seq:03d}O"
    read_cmd = f'OPEN "COM" TO F ELSE STOP; READ REC FROM F, "{output_id}" THEN CRT REC'
    result = subprocess.run(
        ['C:\\qmsys\\bin\\qm.exe', '-aHAL', read_cmd],
        capture_output=True,
        text=True,
        timeout=5
    )
    if result.stdout.strip():
        print(f"\n{output_id}:")
        print(result.stdout)
        break
else:
    print("  No output records found")

print("\nStep 4: Count total COM records...")
result = subprocess.run(
    'C:\\qmsys\\bin\\qm.exe -aHAL "COUNT COM"',
    shell=True,
    capture_output=True,
    text=True,
    timeout=5
)
print(f"  {result.stdout.strip()}")

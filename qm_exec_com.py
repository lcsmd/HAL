#!/usr/bin/env python
"""Execute QM commands and store results in COM hashed file"""
from datetime import datetime
import subprocess
import time

date_prefix = datetime.now().strftime("%Y%m%d")
sequence_file = "C:\\qmsys\\hal\\.sequence"

# Get next sequence number
try:
    with open(sequence_file, 'r') as f:
        sequence = int(f.read().strip())
except:
    sequence = 1

def execute_to_com(commands, description=""):
    """Execute commands and store in COM file"""
    global sequence
    
    input_id = f"{date_prefix}-{sequence:03d}I"
    output_id = f"{date_prefix}-{sequence:03d}O"
    
    print(f"\n{description}")
    print(f"  IDs: {input_id} / {output_id}")
    
    # Join commands with field mark (char 254)
    commands_text = chr(254).join(commands)
    
    # Write commands to COM INPUT record using QM
    qm_cmd = f'''
OPEN "","COM" TO F ELSE STOP
WRITE "{commands_text}" TO F, "INPUT"
CLOSE F
'''
    subprocess.run(
        ['C:\\qmsys\\bin\\qm.exe', '-aHAL', qm_cmd],
        timeout=5
    )
    
    # Run COMMAND.EXECUTOR
    result = subprocess.run(
        'C:\\qmsys\\bin\\qm.exe -aHAL "RUN BP COMMAND.EXECUTOR"',
        shell=True,
        capture_output=True,
        text=True,
        timeout=10
    )
    
    print(f"  Output: {result.stdout}")
    if result.stderr:
        print(f"  Error: {result.stderr}")
    
    # Save sequence
    with open(sequence_file, 'w') as f:
        f.write(str(sequence + 1))
    
    sequence += 1

# Test
print("="*70)
print("TESTING COM STORAGE")
print("="*70)

execute_to_com(
    ["WHO", "LIST.READU"],
    "Test 1: Basic commands"
)

print("\n" + "="*70)
print(f"Records stored with prefix: {date_prefix}")
print("="*70)

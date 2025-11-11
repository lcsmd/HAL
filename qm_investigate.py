#!/usr/bin/env python
"""Execute QM commands using COMMAND.EXECUTOR and store in COM hashed file"""
from datetime import datetime
import subprocess
import os
import time

# Get current date for record IDs
date_prefix = datetime.now().strftime("%Y%m%d")
sequence = 1

def execute_and_store_commands(commands, description=""):
    """Execute commands and store in COM file with sequential numbering"""
    global sequence
    
    input_id = f"{date_prefix}-I{sequence:03d}"
    output_id = f"{date_prefix}-O{sequence:03d}"
    
    print(f"\n{description}")
    print(f"  Input ID: {input_id}")
    print(f"  Output ID: {output_id}")
    
    # Write commands to COM file using QM
    commands_text = '\n'.join(commands)
    
    # Use QM to write to COM file
    qm_write_cmd = f'''
OPEN "COM" TO COM.FILE ELSE STOP
WRITE "{commands_text}" TO COM.FILE, "{input_id}"
'''
    
    # Write input commands
    result = subprocess.run(
        ['C:\\qmsys\\bin\\qm.exe', '-aHAL', '-q', qm_write_cmd],
        capture_output=True,
        text=True,
        timeout=5
    )
    
    # Execute commands via COMMAND.EXECUTOR
    # Create temp input file
    with open("C:\\qmsys\\hal\\COM\\input.txt", 'w') as f:
        f.write(commands_text)
    
    # Execute
    result = subprocess.run(
        'C:\\qmsys\\bin\\qm.exe -aHAL "RUN BP COMMAND.EXECUTOR"',
        shell=True,
        capture_output=True,
        text=True,
        timeout=30
    )
    
    time.sleep(0.5)
    
    # Read output file
    output_path = "C:\\qmsys\\hal\\COM\\output.txt"
    if os.path.exists(output_path):
        with open(output_path, 'r') as f:
            output_text = f.read()
        
        # Write output to COM file using QM
        # Escape quotes in output
        safe_output = output_text.replace('"', '""')
        qm_write_out = f'''
OPEN "COM" TO COM.FILE ELSE STOP  
WRITE "{safe_output}" TO COM.FILE, "{output_id}"
'''
        
        result = subprocess.run(
            ['C:\\qmsys\\bin\\qm.exe', '-aHAL', '-q', qm_write_out],
            capture_output=True,
            text=True,
            timeout=5
        )
        
        print(f"  Stored: {len(output_text)} bytes")
    else:
        print(f"  ERROR: No output file")
    
    sequence += 1

# Investigation commands
print("="*70)
print("QM SYSTEM INVESTIGATION")
print("="*70)

execute_and_store_commands(
    ["WHO", "LIST.READU"],
    "1. Check phantom status"
)

execute_and_store_commands(
    ["LISTF BP.OUT VOICE.LISTENER"],
    "2. Check compiled voice listener"
)

execute_and_store_commands(
    ["LIST BP VOICE.LISTENER 1 50"],
    "3. List first 50 lines of voice listener source"
)

execute_and_store_commands(
    ["LIST BP VOICE.LISTENER 51 100"],
    "4. List lines 51-100 of voice listener source"
)

print("\n" + "="*70)
print(f"All commands stored in COM file with date prefix: {date_prefix}")
print("View with: LIST COM")
print("="*70)

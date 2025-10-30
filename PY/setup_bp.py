#!/usr/bin/env python3
"""
Setup BP file in HAL0 and copy programs from BP directory
"""
import sys
import os
import glob

# Add SYSCOM to Python path for QMClient module
sys.path.insert(0, r'C:\QMSYS\SYSCOM')

import qmclient as qm

def main():
    # Connect to local QM
    print("Connecting to local QM...")
    status = qm.ConnectLocal("HAL")
    if not status:
        print(f"QM Connection Error: {qm.Error()}")
        return 1
    
    print("Connected to HAL")
    
    # Create BP file if it doesn't exist
    print("\nCreating BP file...")
    result = qm.Execute("CREATE.FILE BP DYNAMIC")
    print(f"CREATE.FILE result: {result}")
    
    # Open BP file
    print("\nOpening BP file...")
    bp_fno = qm.Open("BP")
    if bp_fno == 0:
        print(f"Failed to open BP: {qm.Error()}")
        qm.Disconnect()
        return 1
    
    print(f"BP file opened (handle: {bp_fno})")
    
    # Read all programs from BP directory and write to BP file
    bp_dir = r"C:\QMSYS\HAL\BP"
    programs = glob.glob(os.path.join(bp_dir, "*"))
    
    for prog_path in programs:
        if os.path.isfile(prog_path):
            prog_name = os.path.basename(prog_path)
            print(f"\nCopying {prog_name}...")
            
            # Read program from file
            with open(prog_path, 'r') as f:
                content = f.read()
            
            # Write to BP file
            # Convert line endings to QM format (field marks)
            lines = content.split('\n')
            qm_record = '\xfe'.join(lines)  # \xfe is field mark
            
            try:
                qm.Write(bp_fno, prog_name, qm_record)
                print(f"  ✓ {prog_name} copied successfully")
            except Exception as e:
                print(f"  ✗ Failed to write {prog_name}: {e}")
                print(f"     QM Error: {qm.Error()}")
    
    print("\n*** BP file setup complete ***")
    
    # Disconnect
    qm.Disconnect()
    return 0

if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""
Verify BP file type - should be a directory file
"""
import sys
import os

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
    
    # Check what BP actually is
    print("\nChecking BP file type...")
    result = qm.Execute("LIST.FILES BP")
    output = result[0] if isinstance(result, tuple) else result
    
    print("\nLIST.FILES BP output:")
    if isinstance(output, str):
        lines = output.split('\xfe')
        for line in lines:
            print(line)
    
    # Check filesystem
    print("\n" + "="*60)
    print("Checking filesystem...")
    print("="*60)
    bp_path = r"C:\QMSYS\HAL\BP"
    if os.path.isdir(bp_path):
        print(f"✓ {bp_path} exists as filesystem directory")
        files = os.listdir(bp_path)
        print(f"  Contains {len(files)} files:")
        for f in files[:5]:
            print(f"    - {f}")
        if len(files) > 5:
            print(f"    ... and {len(files)-5} more")
    else:
        print(f"✗ {bp_path} does NOT exist as filesystem directory")
    
    # Disconnect
    qm.Disconnect()
    return 0

if __name__ == "__main__":
    sys.exit(main())

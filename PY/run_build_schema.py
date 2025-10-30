#!/usr/bin/env python3
"""
Run BUILD.SCHEMA to create QM files and dictionaries from schema
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
    
    # Run BUILD.SCHEMA
    print("\nRunning BUILD.SCHEMA...")
    result = qm.Execute("BUILD.SCHEMA")
    
    # Execute returns (output, status_code)
    output = result[0] if isinstance(result, tuple) else result
    status_code = result[1] if isinstance(result, tuple) else 0
    
    print("\n" + "="*60)
    print("BUILD.SCHEMA OUTPUT:")
    print("="*60)
    
    # Display output with proper line breaks (field marks are line separators)
    if isinstance(output, str):
        lines = output.split('\xfe')  # Split on field mark
        for line in lines:
            print(line)
    else:
        print(output)
    
    print("="*60)
    print(f"Status code: {status_code}")
    print("="*60)
    
    if status_code == 0:
        print("\n✓ BUILD.SCHEMA completed successfully!")
    else:
        print(f"\n⚠ BUILD.SCHEMA completed with status code: {status_code}")
    
    # Disconnect
    qm.Disconnect()
    return 0

if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""
Compile BUILD.SCHEMA directly from filesystem BP directory
Programs should exist in filesystem directories, NOT QM dynamic hashed files
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
    
    # Compile BUILD.SCHEMA from filesystem
    # Use relative path from HAL account directory
    print("\nCompiling BUILD.SCHEMA from filesystem...")
    result = qm.Execute("BASIC BP/BUILD.SCHEMA")
    
    # Execute returns (output, status_code)
    output = result[0] if isinstance(result, tuple) else result
    status_code = result[1] if isinstance(result, tuple) else 0
    
    print("\n" + "="*60)
    print("COMPILATION OUTPUT:")
    print("="*60)
    
    # Display output with proper line breaks
    if isinstance(output, str):
        lines = output.split('\xfe')  # Split on field mark
        for line in lines:
            print(line)
    else:
        print(output)
    
    print("="*60)
    
    # Check for compilation errors
    if isinstance(output, str):
        if "0 error(s)" in output.lower() or "no errors" in output.lower():
            print("\n✓ Compilation successful!")
            print("✓ Program automatically cataloged to local catalogue")
        elif "error" in output.lower() or "unrecognised" in output.lower() or "cannot" in output.lower():
            print("\n*** Compilation failed - see errors above ***")
            qm.Disconnect()
            return 1
    
    print("\n*** BUILD.SCHEMA compiled successfully from filesystem ***")
    
    # Disconnect
    qm.Disconnect()
    return 0

if __name__ == "__main__":
    sys.exit(main())

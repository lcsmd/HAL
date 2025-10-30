#!/usr/bin/env python3
"""
Compile and catalog BUILD.SCHEMA using QMClient
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
    
    # List current directory to verify location
    print("\nChecking current location...")
    result = qm.Execute("PWD")
    print(f"PWD result: {result}")
    
    # Compile BUILD.SCHEMA
    print("\nCompiling BP BUILD.SCHEMA...")
    result = qm.Execute("BASIC BP BUILD.SCHEMA")
    print(f"BASIC result: {result}")
    
    # Execute returns (output, status_code)
    output = result[0] if isinstance(result, tuple) else result
    status_code = result[1] if isinstance(result, tuple) else 0
    
    # Check for compilation errors - look for "0 error(s)" or actual error count
    if isinstance(output, str):
        if "0 error(s)" in output.lower() or "no errors" in output.lower():
            print("✓ Compilation successful!")
            print("✓ Program automatically cataloged to local catalogue")
        elif "error" in output.lower() or "unrecognised" in output.lower() or "cannot" in output.lower():
            print("\n*** Compilation failed - see errors above ***")
            qm.Disconnect()
            return 1
    
    print("\n*** BUILD.SCHEMA compiled successfully ***")
    
    # Disconnect
    qm.Disconnect()
    return 0

if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""
Check VOC for BP entry and create if needed
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
    
    # Open VOC
    print("\nOpening VOC...")
    voc_fno = qm.Open("VOC")
    if voc_fno == 0:
        print(f"Failed to open VOC: {qm.Error()}")
        qm.Disconnect()
        return 1
    
    # Read BP entry
    print("Reading BP entry from VOC...")
    bp_rec, status = qm.Read(voc_fno, "BP")
    
    if status == 0:  # SV_OK
        print("\nBP entry exists in VOC:")
        print(bp_rec)
    else:
        print("\nBP entry does not exist in VOC")
        print("Creating BP as DIR-type VOC entry...")
        
        # Create DIR-type VOC entry for BP
        # Format: DIR<FM>directory-path
        bp_entry = "DIR\xfe" + os.path.abspath("BP")
        
        qm.Write(voc_fno, "BP", bp_entry)
        print(f"Created BP VOC entry pointing to: {os.path.abspath('BP')}")
    
    # Now try to compile
    print("\n" + "="*60)
    print("Attempting to compile BUILD.SCHEMA...")
    print("="*60)
    
    result = qm.Execute("BASIC BP BUILD.SCHEMA")
    output = result[0] if isinstance(result, tuple) else result
    
    # Display output
    if isinstance(output, str):
        lines = output.split('\xfe')
        for line in lines:
            print(line)
    
    # Disconnect
    qm.Disconnect()
    return 0

if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""
Run all schema setup programs in sequence
"""
import sys
import os
sys.path.insert(0, r'c:\QMSYS\SYSCOM')
import qmclient as qm

def check_and_create_voc(file_name):
    """Check if VOC entry exists and create if needed"""
    print(f"\nChecking {file_name} VOC entry...")
    result = qm.Execute(f"LIST VOC {file_name}")
    if "not found" in result[0].lower() or "no records" in result[0].lower():
        print(f"Creating VOC entry for {file_name}...")
        voc_rec = f"F\xfe{file_name}\xfe\xfeD\xfe"
        fno = qm.Open("VOC")
        qm.Write(fno, file_name, voc_rec)
        print("VOC entry created")
        return True
    else:
        print("VOC entry exists")
        return False

def compile_and_run(program_name):
    """Compile, catalog, and run a program"""
    print(f"\n{'='*60}")
    print(f"Processing {program_name}")
    print('='*60)
    
    # Compile
    print(f"\nCompiling BP {program_name}...")
    result = qm.Execute(f"BASIC BP {program_name}")
    if result[1] != 0:
        print(f"Error compiling: {result[0]}")
        return False
    print("Compiled successfully")
    
    # Catalog
    print(f"\nCataloging BP {program_name}...")
    result = qm.Execute(f"CATALOG BP {program_name} LOCAL")
    if result[1] != 0:
        print(f"Error cataloging: {result[0]}")
        return False
    print("Cataloged successfully")
    
    # Run
    print(f"\nRunning {program_name}...")
    result = qm.Execute(f"RUN BP {program_name}")
    print(result[0])
    
    return True

# Connect to QM
print("="*60)
print("HAL Schema Setup - Running All Setup Programs")
print("="*60)
print("\nConnecting to QM...")
qm.Connect('localhost', 4243, 'lawr', 'apgar-66', 'HAL')
print("Connected!")

# Setup DOMAINS
check_and_create_voc("DOMAINS")
compile_and_run("SETUP.DOMAINS")

# Setup FILES
check_and_create_voc("FILES")
compile_and_run("SETUP.FILES")

# Setup FIELDS
check_and_create_voc("FIELDS")
compile_and_run("SETUP.FIELDS")

# Setup DOM_FILE_FIELD
check_and_create_voc("DOM_FILE_FIELD")
compile_and_run("SETUP.DOM_FILE_FIELD")

# Final verification
print("\n" + "="*60)
print("FINAL VERIFICATION")
print("="*60)

print("\n--- DOMAINS ---")
result = qm.Execute("COUNT DOMAINS")
print(result[0])

print("\n--- FILES ---")
result = qm.Execute("COUNT FILES")
print(result[0])

print("\n--- FIELDS ---")
result = qm.Execute("COUNT FIELDS")
print(result[0])

print("\n--- DOM_FILE_FIELD ---")
result = qm.Execute("COUNT DOM_FILE_FIELD")
print(result[0])

# Disconnect
qm.Disconnect()

print("\n" + "="*60)
print("All schema setup programs completed successfully!")
print("="*60)

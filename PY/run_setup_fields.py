#!/usr/bin/env python3
"""
Compile and run SETUP.FIELDS program
"""
import sys
import os
sys.path.insert(0, r'c:\QMSYS\SYSCOM')
import qmclient as qm

# Connect to QM
print("Connecting to QM...")
qm.Connect('localhost', 4243, 'lawr', 'apgar-66', 'HAL')
print("Connected!")

# Check if FIELDS VOC entry exists, if not create it
print("\nChecking FIELDS VOC entry...")
result = qm.Execute("LIST VOC FIELDS")
if "not found" in result[0].lower() or "no records" in result[0].lower():
    print("Creating VOC entry for FIELDS...")
    voc_rec = "F\xfeFIELDS\xfe\xfeD\xfe"
    fno = qm.Open("VOC")
    qm.Write(fno, "FIELDS", voc_rec)
    print("VOC entry created")
else:
    print("VOC entry exists")

# Compile SETUP.FIELDS
print("\nCompiling BP SETUP.FIELDS...")
result = qm.Execute("BASIC BP SETUP.FIELDS")
print(result)

# Catalog it to local catalog
print("\nCataloging BP SETUP.FIELDS...")
result = qm.Execute("CATALOG BP SETUP.FIELDS LOCAL")
print(result)

# Run it
print("\nRunning SETUP.FIELDS...")
result = qm.Execute("RUN BP SETUP.FIELDS")
print(result)

# Verify the data
print("\n" + "="*50)
print("Verifying FIELDS file...")
print("="*50)
result = qm.Execute("LIST FIELDS DISPLAY_DESC CONV LEN_JUST")
print(result[0])

# Disconnect
qm.Disconnect()
print("\nDone!")

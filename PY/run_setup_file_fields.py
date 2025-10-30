#!/usr/bin/env python3
"""
Compile and run SETUP.DOM_FILE_FIELD program
"""
import sys
import os
sys.path.insert(0, r'c:\QMSYS\SYSCOM')
import qmclient as qm

# Connect to QM
print("Connecting to QM...")
qm.Connect('localhost', 4243, 'lawr', 'apgar-66', 'HAL')
print("Connected!")

# Check if DOM_FILE_FIELD VOC entry exists, if not create it
print("\nChecking DOM_FILE_FIELD VOC entry...")
result = qm.Execute("LIST VOC DOM_FILE_FIELD")
if "not found" in result[0].lower() or "no records" in result[0].lower():
    print("Creating VOC entry for DOM_FILE_FIELD...")
    voc_rec = "F\xfeDOM_FILE_FIELD\xfe\xfeD\xfe"
    fno = qm.Open("VOC")
    qm.Write(fno, "DOM_FILE_FIELD", voc_rec)
    print("VOC entry created")
else:
    print("VOC entry exists")

# Compile SETUP.DOM_FILE_FIELD
print("\nCompiling BP SETUP.DOM_FILE_FIELD...")
result = qm.Execute("BASIC BP SETUP.DOM_FILE_FIELD")
print(result)

# Catalog it to local catalog
print("\nCataloging BP SETUP.DOM_FILE_FIELD...")
result = qm.Execute("CATALOG BP SETUP.DOM_FILE_FIELD LOCAL")
print(result)

# Run it
print("\nRunning SETUP.DOM_FILE_FIELD...")
result = qm.Execute("RUN BP SETUP.DOM_FILE_FIELD")
print(result)

# Verify the data
print("\n" + "="*50)
print("Verifying DOM_FILE_FIELD file...")
print("="*50)
result = qm.Execute("LIST DOM_FILE_FIELD M_S ASSOCIATION INDEX REQUIRED")
print(result[0])

# Disconnect
qm.Disconnect()
print("\nDone!")

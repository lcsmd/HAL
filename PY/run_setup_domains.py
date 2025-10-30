#!/usr/bin/env python3
"""
Compile and run SETUP.DOMAINS program
"""
import sys
import os
sys.path.insert(0, r'c:\QMSYS\SYSCOM')
import qmclient as qm

# Connect to QM
print("Connecting to QM...")
qm.Connect('localhost', 4243, 'lawr', 'apgar-66', 'HAL')
print("Connected!")

# Check if DOMAINS VOC entry exists, if not create it
print("\nChecking DOMAINS VOC entry...")
result = qm.Execute("LIST VOC DOMAINS")
if "not found" in result[0].lower() or "no records" in result[0].lower():
    print("Creating VOC entry for DOMAINS...")
    # Create F-type VOC entry for DOMAINS file
    voc_rec = "F\xfeDOMAINS\xfe\xfeD\xfe"  # F-type, pathname DOMAINS, dict DOMAINS.DIC
    fno = qm.Open("VOC")
    qm.Write(fno, "DOMAINS", voc_rec)
    print("VOC entry created")
else:
    print("VOC entry exists")

# Compile SETUP.DOMAINS
print("\nCompiling BP SETUP.DOMAINS...")
result = qm.Execute("BASIC BP SETUP.DOMAINS")
print(result)

# Catalog it to local catalog
print("\nCataloging BP SETUP.DOMAINS...")
result = qm.Execute("CATALOG BP SETUP.DOMAINS LOCAL")
print(result)

# Run it
print("\nRunning SETUP.DOMAINS...")
result = qm.Execute("RUN BP SETUP.DOMAINS")
print(result)

# Verify the data
print("\n" + "="*50)
print("Verifying DOMAINS file...")
print("="*50)
result = qm.Execute("LIST DOMAINS DOMAIN_ABB DOMAIN_DESC")
print(result[0])

# Disconnect
qm.Disconnect()
print("\nDone!")

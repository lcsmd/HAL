#!/usr/bin/env python3
import sys
sys.path.insert(0, r'c:\QMSYS\SYSCOM')
import qmclient as qm

qm.Connect('localhost', 4243, 'lawr', 'apgar-66', 'HAL')

print("Running SETUP.FIELDS...")
r = qm.Execute('RUN BP SETUP.FIELDS')
print(r[0])

print("\n" + "="*60)
print("Running SETUP.DOM_FILE_FIELD...")
print("="*60)
r = qm.Execute('RUN BP SETUP.DOM_FILE_FIELD')
print(r[0])

qm.Disconnect()

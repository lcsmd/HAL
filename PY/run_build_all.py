#!/usr/bin/env python3
"""
Compile and run BUILD.ALL.SETUPS program
"""
import sys
sys.path.insert(0, r'c:\QMSYS\SYSCOM')
import qmclient as qm

print("Connecting to QM...")
qm.Connect('localhost', 4243, 'lawr', 'apgar-66', 'HAL')
print("Connected!\n")

print("Compiling BP BUILD.ALL.SETUPS...")
result = qm.Execute("BASIC BP BUILD.ALL.SETUPS")
print(result[0])

print("\nCataloging BP BUILD.ALL.SETUPS...")
result = qm.Execute("CATALOG BP BUILD.ALL.SETUPS LOCAL")
print(result[0])

print("\nRunning BUILD.ALL.SETUPS...\n")
result = qm.Execute("RUN BP BUILD.ALL.SETUPS")
print(result[0])

qm.Disconnect()
print("\nDone!")

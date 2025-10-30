#!/usr/bin/env python3
"""
Move AI infrastructure files from sys domain to ai domain
"""
import sys
sys.path.insert(0, r'c:\QMSYS\SYSCOM')
import qmclient as qm

print("Connecting to QM...")
qm.Connect('localhost', 4243, 'lawr', 'apgar-66', 'HAL')

files_fno = qm.Open("FILES")
dff_fno = qm.Open("DOM_FILE_FIELD")

print("\nMoving AI files from sys to ai domain...")
print("="*60)

# AI files to move
ai_files = [
    "prompt_template",
    "persona", 
    "voice",
    "wake_word",
    "mood",
    "conversation",
    "conversation_message",
    "memory"
]

for filename in ai_files:
    # Update FILES record - change domain from sys to ai
    try:
        rec = qm.Read(files_fno, filename)
        parts = rec.split('\xfe')
        old_domain = parts[2]
        parts[2] = "ai"  # Change domain to ai
        new_rec = '\xfe'.join(parts)
        qm.Write(files_fno, filename, new_rec)
        print(f"  Updated {filename}: {old_domain} -> ai")
    except:
        print(f"  Warning: {filename} not found in FILES")
        continue
    
    # Update DOM_FILE_FIELD records - change keys from sys:file:field to ai:file:field
    # Select all fields for this file
    select_cmd = f"SELECT DOM_FILE_FIELD WITH @ID LIKE 'sys:{filename}:...'"
    qm.Execute(select_cmd)
    
    fields_moved = 0
    while True:
        try:
            old_key = qm.ReadNext(1)
            if not old_key:
                break
            
            # Read the record
            rec = qm.Read(dff_fno, old_key)
            
            # Create new key with ai domain
            new_key = old_key.replace(f"sys:{filename}:", f"ai:{filename}:")
            
            # Write with new key
            qm.Write(dff_fno, new_key, rec)
            
            # Delete old key
            qm.Delete(dff_fno, old_key)
            
            fields_moved += 1
        except:
            break
    
    print(f"    Moved {fields_moved} fields")

print("\n" + "="*60)
print("AI domain migration complete!")
print("="*60)

# Verify
print("\nVerifying domain distribution...")
result = qm.Execute("SSELECT FILES BY DOMAIN")
result = qm.Execute("LIST FILES DOMAIN")
print(result[0])

qm.Disconnect()
print("\nDone!")

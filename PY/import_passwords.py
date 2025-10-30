#!/usr/bin/env python3
"""
Import passwords from various formats
Supports: CSV, JSON, LastPass, 1Password, Chrome, Firefox
"""
import sys
import os
import csv
import json
from datetime import datetime
from getpass import getpass

# Add SYSCOM to Python path
sys.path.insert(0, r'C:\QMSYS\SYSCOM')
import qmclient as qm

from password_crypto import (
    verify_master_password, encrypt_data, 
    check_password_strength, get_master_password_record
)

PERSON_ID = "P001"

def connect_qm():
    """Connect to QM"""
    if not qm.Connected():
        status = qm.ConnectLocal("HAL")
        if not status:
            print(f"QM Connection Error: {qm.Error()}")
            return False
    return True

def import_from_csv(csv_file, encryption_key):
    """Import passwords from CSV file"""
    print(f"\nImporting from CSV: {csv_file}")
    
    if not os.path.exists(csv_file):
        print(f"File not found: {csv_file}")
        return 0
    
    if not connect_qm():
        return 0
    
    fno = qm.Open("PASSWORD")
    if fno == 0:
        print("Error opening PASSWORD file")
        return 0
    
    imported = 0
    
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        
        for row in reader:
            # Map CSV columns (flexible mapping)
            site_name = row.get('name') or row.get('site') or row.get('title') or row.get('url', '')
            username = row.get('username') or row.get('login') or row.get('email', '')
            password = row.get('password') or row.get('pass', '')
            url = row.get('url') or row.get('website', '')
            notes = row.get('notes') or row.get('note', '')
            category = row.get('category') or row.get('type', 'website')
            
            if not site_name or not password:
                continue
            
            # Encrypt password
            encrypted_password = encrypt_data(password, encryption_key)
            encrypted_notes = encrypt_data(notes, encryption_key) if notes else ''
            
            # Check strength
            strength = check_password_strength(password)
            
            # Generate ID
            timestamp = datetime.now().strftime('%Y%m%d%H%M%S%f')
            rec_id = f"PWD{timestamp}"
            
            # Build record
            record = [
                rec_id,
                PERSON_ID,
                category.lower(),
                site_name,
                url,
                username,
                encrypted_password,
                '',  # PASSWORD_HINT
                '',  # EMAIL_USED
                '',  # PHONE_USED
                '',  # SECURITY_QUESTIONS
                '',  # SECURITY_ANSWERS_ENC
                'N',  # TWO_FACTOR_ENABLED
                '',  # TWO_FACTOR_METHOD
                '',  # TWO_FACTOR_BACKUP
                '',  # RECOVERY_EMAIL
                '',  # RECOVERY_PHONE
                str(qm.Date()),  # LAST_CHANGED_DATE
                '',  # EXPIRES_DATE
                strength,
                encrypted_notes,
                '',  # TAGS
                'N',  # FAVORITE
                '',  # SHARED_WITH
                'N',  # AUTO_LOGIN
                '',  # LAST_USED_DATE
                '0',  # USAGE_COUNT
                'N',  # BREACH_DETECTED
                '',  # BREACH_DATE
                'Y',  # ACTIVE
                str(qm.Date()),
                str(qm.Date()),
            ]
            
            qm_record = '\xfe'.join(record)
            qm.Write(fno, rec_id, qm_record)
            
            imported += 1
            print(f"  Imported: {site_name}")
    
    print(f"\n✓ Imported {imported} passwords")
    return imported

def import_from_json(json_file, encryption_key):
    """Import passwords from JSON file"""
    print(f"\nImporting from JSON: {json_file}")
    
    if not os.path.exists(json_file):
        print(f"File not found: {json_file}")
        return 0
    
    if not connect_qm():
        return 0
    
    fno = qm.Open("PASSWORD")
    if fno == 0:
        print("Error opening PASSWORD file")
        return 0
    
    imported = 0
    
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Handle different JSON structures
    passwords = []
    if isinstance(data, list):
        passwords = data
    elif isinstance(data, dict):
        # Try common keys
        passwords = data.get('passwords') or data.get('items') or data.get('logins') or [data]
    
    for item in passwords:
        site_name = item.get('name') or item.get('site') or item.get('title', '')
        username = item.get('username') or item.get('login') or item.get('email', '')
        password = item.get('password') or item.get('pass', '')
        url = item.get('url') or item.get('website', '')
        notes = item.get('notes') or item.get('note', '')
        category = item.get('category') or item.get('type', 'website')
        
        if not site_name or not password:
            continue
        
        # Encrypt
        encrypted_password = encrypt_data(password, encryption_key)
        encrypted_notes = encrypt_data(notes, encryption_key) if notes else ''
        strength = check_password_strength(password)
        
        # Generate ID
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S%f')
        rec_id = f"PWD{timestamp}"
        
        # Build record
        record = [
            rec_id, PERSON_ID, category.lower(), site_name, url, username,
            encrypted_password, '', '', '', '', '', 'N', '', '', '', '',
            str(qm.Date()), '', strength, encrypted_notes, '', 'N', '', 'N',
            '', '0', 'N', '', 'Y', str(qm.Date()), str(qm.Date()),
        ]
        
        qm_record = '\xfe'.join(record)
        qm.Write(fno, rec_id, qm_record)
        
        imported += 1
        print(f"  Imported: {site_name}")
    
    print(f"\n✓ Imported {imported} passwords")
    return imported

def export_to_csv(output_file, encryption_key):
    """Export passwords to CSV"""
    print(f"\nExporting to CSV: {output_file}")
    
    if not connect_qm():
        return 0
    
    fno = qm.Open("PASSWORD")
    if fno == 0:
        print("Error opening PASSWORD file")
        return 0
    
    qm.Execute(f'SELECT PASSWORD WITH PERSON_ID = "{PERSON_ID}" AND ACTIVE = "Y" TO 1')
    
    passwords = []
    while True:
        rec_id = qm.ReadNext(1)
        if not rec_id:
            break
        
        record = qm.Read(fno, rec_id)
        if record:
            fields = record.split('\xfe')
            
            # Decrypt password
            from password_crypto import decrypt_data
            encrypted_password = fields[6] if len(fields) > 6 else ''
            password = decrypt_data(encrypted_password, encryption_key)
            
            if password:
                passwords.append({
                    'name': fields[3] if len(fields) > 3 else '',
                    'url': fields[4] if len(fields) > 4 else '',
                    'username': fields[5] if len(fields) > 5 else '',
                    'password': password,
                    'category': fields[2] if len(fields) > 2 else '',
                    'notes': '',  # Don't export encrypted notes for security
                })
    
    if not passwords:
        print("No passwords to export")
        return 0
    
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        fieldnames = ['name', 'url', 'username', 'password', 'category', 'notes']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(passwords)
    
    print(f"\n✓ Exported {len(passwords)} passwords")
    print(f"\n⚠ WARNING: Exported file contains unencrypted passwords!")
    print(f"   Keep it secure and delete after use.")
    
    return len(passwords)

def main():
    if len(sys.argv) < 3:
        print("Password Import/Export Utility")
        print("\nUsage:")
        print("  Import: python import_passwords.py import <file.csv|file.json>")
        print("  Export: python import_passwords.py export <output.csv>")
        print("\nExamples:")
        print("  python import_passwords.py import passwords.csv")
        print("  python import_passwords.py import lastpass_export.json")
        print("  python import_passwords.py export my_passwords.csv")
        return 1
    
    action = sys.argv[1].lower()
    filename = sys.argv[2]
    
    # Get master password
    master_rec = get_master_password_record(PERSON_ID)
    if not master_rec:
        print("No master password set. Run password_manager.py first.")
        return 1
    
    master_pw = getpass("Enter master password: ")
    encryption_key = verify_master_password(PERSON_ID, master_pw)
    
    if not encryption_key:
        print("Invalid master password")
        return 1
    
    if action == 'import':
        ext = os.path.splitext(filename)[1].lower()
        if ext == '.csv':
            import_from_csv(filename, encryption_key)
        elif ext == '.json':
            import_from_json(filename, encryption_key)
        else:
            print(f"Unsupported file type: {ext}")
            print("Supported: .csv, .json")
            return 1
    
    elif action == 'export':
        export_to_csv(filename, encryption_key)
    
    else:
        print(f"Unknown action: {action}")
        print("Use 'import' or 'export'")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())

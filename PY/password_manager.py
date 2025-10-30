#!/usr/bin/env python3
"""
Password Manager - Secure Password Vault
"""
import sys
import os
from getpass import getpass
from datetime import datetime

# Add SYSCOM to Python path
sys.path.insert(0, r'C:\QMSYS\SYSCOM')
import qmclient as qm

# Import crypto module
from password_crypto import (
    verify_master_password, create_master_password,
    encrypt_data, decrypt_data, check_password_strength,
    generate_password, get_master_password_record
)

PERSON_ID = "P001"  # Default person ID
encryption_key = None

def connect_qm():
    """Connect to QM"""
    if not qm.Connected():
        status = qm.ConnectLocal("HAL")
        if not status:
            print(f"QM Connection Error: {qm.Error()}")
            return False
    return True

def setup_master_password():
    """Set up master password for first time"""
    print("\n" + "="*60)
    print("Master Password Setup")
    print("="*60)
    print("\nYou need to create a master password to protect your vault.")
    print("This password will encrypt all your stored passwords.")
    print("\nIMPORTANT:")
    print("- Use a strong, unique password")
    print("- DO NOT forget this password")
    print("- There is NO way to recover if you forget it")
    
    while True:
        master_pw = getpass("\nEnter master password: ")
        if len(master_pw) < 8:
            print("Password must be at least 8 characters")
            continue
        
        confirm_pw = getpass("Confirm master password: ")
        if master_pw != confirm_pw:
            print("Passwords do not match")
            continue
        
        strength = check_password_strength(master_pw)
        print(f"\nPassword strength: {strength}")
        
        if strength == "weak":
            choice = input("Weak password. Continue anyway? (y/n): ")
            if choice.lower() != 'y':
                continue
        
        break
    
    hint = input("\nPassword hint (optional): ")
    
    if create_master_password(PERSON_ID, master_pw):
        print("\n✓ Master password created successfully!")
        return master_pw
    else:
        print("\n✗ Failed to create master password")
        return None

def login():
    """Login with master password"""
    global encryption_key
    
    # Check if master password exists
    master_rec = get_master_password_record(PERSON_ID)
    
    if not master_rec:
        print("\nNo master password found. Setting up...")
        master_pw = setup_master_password()
        if not master_pw:
            return False
    else:
        print("\n" + "="*60)
        print("Password Vault Login")
        print("="*60)
        master_pw = getpass("\nEnter master password: ")
    
    # Verify and get encryption key
    encryption_key = verify_master_password(PERSON_ID, master_pw)
    
    if encryption_key:
        print("✓ Login successful!")
        return True
    else:
        print("✗ Invalid master password")
        return False

def list_passwords(category=None):
    """List all passwords"""
    if not connect_qm():
        return
    
    fno = qm.Open("PASSWORD")
    if fno == 0:
        print("Error opening PASSWORD file")
        return
    
    # Build query
    if category:
        qm.Execute(f'SELECT PASSWORD WITH PERSON_ID = "{PERSON_ID}" AND CATEGORY = "{category}" AND ACTIVE = "Y" TO 1')
    else:
        qm.Execute(f'SELECT PASSWORD WITH PERSON_ID = "{PERSON_ID}" AND ACTIVE = "Y" TO 1')
    
    passwords = []
    while True:
        rec_id = qm.ReadNext(1)
        if not rec_id:
            break
        
        record = qm.Read(fno, rec_id)
        if record:
            fields = record.split('\xfe')
            passwords.append({
                'id': rec_id,
                'category': fields[2] if len(fields) > 2 else '',
                'site_name': fields[3] if len(fields) > 3 else '',
                'username': fields[5] if len(fields) > 5 else '',
                'favorite': fields[22] if len(fields) > 22 else 'N',
            })
    
    if not passwords:
        print("\nNo passwords found")
        return
    
    print("\n" + "="*60)
    print(f"{'ID':<15} {'Site':<25} {'Username':<20} {'Category':<12}")
    print("="*60)
    
    for pwd in passwords:
        fav = "★ " if pwd['favorite'] == 'Y' else "  "
        print(f"{fav}{pwd['id']:<13} {pwd['site_name']:<25} {pwd['username']:<20} {pwd['category']:<12}")

def add_password():
    """Add new password"""
    if not encryption_key:
        print("Not logged in")
        return
    
    if not connect_qm():
        return
    
    print("\n" + "="*60)
    print("Add New Password")
    print("="*60)
    
    # Get details
    site_name = input("\nSite/Service name: ")
    if not site_name:
        print("Site name required")
        return
    
    site_url = input("Website URL (optional): ")
    
    print("\nCategory:")
    print("1. Website")
    print("2. App")
    print("3. Email")
    print("4. Bank")
    print("5. System")
    print("6. Other")
    cat_choice = input("Select (1-6): ")
    
    categories = {
        '1': 'website',
        '2': 'app',
        '3': 'email',
        '4': 'bank',
        '5': 'system',
        '6': 'other'
    }
    category = categories.get(cat_choice, 'other')
    
    username = input("\nUsername/Email: ")
    if not username:
        print("Username required")
        return
    
    print("\nPassword:")
    print("1. Enter manually")
    print("2. Generate random password")
    pwd_choice = input("Select (1-2): ")
    
    if pwd_choice == '2':
        length = input("Length (default 16): ")
        length = int(length) if length.isdigit() else 16
        password = generate_password(length)
        print(f"\nGenerated password: {password}")
        input("Press ENTER to continue (password will be hidden)...")
    else:
        password = getpass("Enter password: ")
        if not password:
            print("Password required")
            return
    
    # Encrypt password
    encrypted_password = encrypt_data(password, encryption_key)
    
    # Additional details
    email_used = input("\nEmail used for account (optional): ")
    phone_used = input("Phone used for account (optional): ")
    two_factor = input("Two-factor authentication enabled? (y/n): ")
    notes = input("Notes (optional): ")
    
    # Encrypt notes if provided
    encrypted_notes = encrypt_data(notes, encryption_key) if notes else ''
    
    # Check password strength
    strength = check_password_strength(password)
    
    # Generate ID
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    rec_id = f"PWD{timestamp}"
    
    # Build record
    record = [
        rec_id,  # ID
        PERSON_ID,  # PERSON_ID
        category,  # CATEGORY
        site_name,  # SITE_NAME
        site_url,  # SITE_URL
        username,  # USERNAME
        encrypted_password,  # PASSWORD_ENCRYPTED
        '',  # PASSWORD_HINT
        email_used,  # EMAIL_USED
        phone_used,  # PHONE_USED
        '',  # SECURITY_QUESTIONS
        '',  # SECURITY_ANSWERS_ENC
        'Y' if two_factor.lower() == 'y' else 'N',  # TWO_FACTOR_ENABLED
        '',  # TWO_FACTOR_METHOD
        '',  # TWO_FACTOR_BACKUP
        '',  # RECOVERY_EMAIL
        '',  # RECOVERY_PHONE
        str(qm.Date()),  # LAST_CHANGED_DATE
        '',  # EXPIRES_DATE
        strength,  # STRENGTH
        encrypted_notes,  # NOTES_ENCRYPTED
        '',  # TAGS
        'N',  # FAVORITE
        '',  # SHARED_WITH
        'N',  # AUTO_LOGIN
        '',  # LAST_USED_DATE
        '0',  # USAGE_COUNT
        'N',  # BREACH_DETECTED
        '',  # BREACH_DATE
        'Y',  # ACTIVE
        str(qm.Date()),  # CREATED_DATE
        str(qm.Date()),  # UPDATED_DATE
    ]
    
    qm_record = '\xfe'.join(record)
    
    fno = qm.Open("PASSWORD")
    if fno == 0:
        print("Error opening PASSWORD file")
        return
    
    qm.Write(fno, rec_id, qm_record)
    
    print(f"\n✓ Password saved successfully! ID: {rec_id}")

def view_password():
    """View password details"""
    if not encryption_key:
        print("Not logged in")
        return
    
    if not connect_qm():
        return
    
    pwd_id = input("\nEnter password ID: ")
    if not pwd_id:
        return
    
    fno = qm.Open("PASSWORD")
    if fno == 0:
        print("Error opening PASSWORD file")
        return
    
    record = qm.Read(fno, pwd_id)
    if not record:
        print("Password not found")
        return
    
    fields = record.split('\xfe')
    
    # Decrypt password
    encrypted_password = fields[6] if len(fields) > 6 else ''
    password = decrypt_data(encrypted_password, encryption_key)
    
    if not password:
        print("Error decrypting password")
        return
    
    # Decrypt notes
    encrypted_notes = fields[20] if len(fields) > 20 else ''
    notes = decrypt_data(encrypted_notes, encryption_key) if encrypted_notes else ''
    
    print("\n" + "="*60)
    print("Password Details")
    print("="*60)
    print(f"ID: {pwd_id}")
    print(f"Site: {fields[3] if len(fields) > 3 else ''}")
    print(f"URL: {fields[4] if len(fields) > 4 else ''}")
    print(f"Category: {fields[2] if len(fields) > 2 else ''}")
    print(f"Username: {fields[5] if len(fields) > 5 else ''}")
    print(f"Password: {password}")
    print(f"Strength: {fields[19] if len(fields) > 19 else ''}")
    print(f"2FA Enabled: {fields[12] if len(fields) > 12 else 'N'}")
    if notes:
        print(f"Notes: {notes}")
    
    # Update usage
    usage_count = int(fields[26]) if len(fields) > 26 and fields[26].isdigit() else 0
    fields[26] = str(usage_count + 1)
    fields[25] = str(qm.Date())  # LAST_USED_DATE
    fields[31] = str(qm.Date())  # UPDATED_DATE
    
    qm_record = '\xfe'.join(fields)
    qm.Write(fno, pwd_id, qm_record)

def delete_password():
    """Delete password"""
    if not connect_qm():
        return
    
    pwd_id = input("\nEnter password ID to delete: ")
    if not pwd_id:
        return
    
    fno = qm.Open("PASSWORD")
    if fno == 0:
        print("Error opening PASSWORD file")
        return
    
    record = qm.Read(fno, pwd_id)
    if not record:
        print("Password not found")
        return
    
    fields = record.split('\xfe')
    site_name = fields[3] if len(fields) > 3 else ''
    
    confirm = input(f"\nDelete password for '{site_name}'? (yes/no): ")
    if confirm.lower() != 'yes':
        print("Cancelled")
        return
    
    # Mark as inactive instead of deleting
    fields[29] = 'N'  # ACTIVE
    fields[31] = str(qm.Date())  # UPDATED_DATE
    
    qm_record = '\xfe'.join(fields)
    qm.Write(fno, pwd_id, qm_record)
    
    print("✓ Password deleted")

def search_passwords():
    """Search passwords"""
    search_term = input("\nSearch term: ")
    if not search_term:
        return
    
    if not connect_qm():
        return
    
    fno = qm.Open("PASSWORD")
    if fno == 0:
        print("Error opening PASSWORD file")
        return
    
    qm.Execute(f'SELECT PASSWORD WITH PERSON_ID = "{PERSON_ID}" AND ACTIVE = "Y" TO 1')
    
    results = []
    while True:
        rec_id = qm.ReadNext(1)
        if not rec_id:
            break
        
        record = qm.Read(fno, rec_id)
        if record:
            fields = record.split('\xfe')
            site_name = fields[3] if len(fields) > 3 else ''
            username = fields[5] if len(fields) > 5 else ''
            
            if search_term.lower() in site_name.lower() or search_term.lower() in username.lower():
                results.append({
                    'id': rec_id,
                    'site_name': site_name,
                    'username': username,
                    'category': fields[2] if len(fields) > 2 else '',
                })
    
    if not results:
        print("\nNo matches found")
        return
    
    print("\n" + "="*60)
    print(f"{'ID':<15} {'Site':<25} {'Username':<20}")
    print("="*60)
    
    for pwd in results:
        print(f"{pwd['id']:<15} {pwd['site_name']:<25} {pwd['username']:<20}")

def main_menu():
    """Main menu"""
    if not connect_qm():
        return 1
    
    # Login
    if not login():
        return 1
    
    while True:
        print("\n" + "="*60)
        print("Password Manager")
        print("="*60)
        print("1. List All Passwords")
        print("2. List by Category")
        print("3. Add Password")
        print("4. View Password")
        print("5. Search Passwords")
        print("6. Delete Password")
        print("7. Change Master Password")
        print("Q. Quit")
        
        choice = input("\nSelect option: ").upper()
        
        if choice == '1':
            list_passwords()
        elif choice == '2':
            print("\nCategories: website, app, email, bank, system, other")
            category = input("Enter category: ")
            list_passwords(category)
        elif choice == '3':
            add_password()
        elif choice == '4':
            view_password()
        elif choice == '5':
            search_passwords()
        elif choice == '6':
            delete_password()
        elif choice == '7':
            print("Change master password not yet implemented")
        elif choice == 'Q':
            break
        else:
            print("Invalid choice")
    
    qm.Disconnect()
    return 0

if __name__ == "__main__":
    sys.exit(main_menu())

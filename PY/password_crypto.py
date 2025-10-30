#!/usr/bin/env python3
"""
Password Encryption/Decryption Module
Uses Fernet (symmetric encryption) from cryptography library
"""
import sys
import os
import base64
import hashlib
from getpass import getpass

try:
    from cryptography.fernet import Fernet
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2
except ImportError:
    print("cryptography library not installed")
    print("Install with: pip install cryptography")
    sys.exit(1)

def generate_key_from_password(master_password, salt):
    """Generate encryption key from master password"""
    kdf = PBKDF2(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(master_password.encode()))
    return key

def hash_password(password, salt):
    """Hash a password with salt"""
    return hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000).hex()

def generate_salt():
    """Generate a random salt"""
    return os.urandom(16)

def encrypt_data(data, key):
    """Encrypt data with key"""
    f = Fernet(key)
    return f.encrypt(data.encode()).decode()

def decrypt_data(encrypted_data, key):
    """Decrypt data with key"""
    try:
        f = Fernet(key)
        return f.decrypt(encrypted_data.encode()).decode()
    except Exception as e:
        return None

def check_password_strength(password):
    """Check password strength"""
    length = len(password)
    has_upper = any(c.isupper() for c in password)
    has_lower = any(c.islower() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_special = any(c in '!@#$%^&*()_+-=[]{}|;:,.<>?' for c in password)
    
    score = 0
    if length >= 8: score += 1
    if length >= 12: score += 1
    if length >= 16: score += 1
    if has_upper: score += 1
    if has_lower: score += 1
    if has_digit: score += 1
    if has_special: score += 1
    
    if score <= 2:
        return "weak"
    elif score <= 4:
        return "medium"
    elif score <= 6:
        return "strong"
    else:
        return "very-strong"

def generate_password(length=16, use_special=True):
    """Generate a random password"""
    import random
    import string
    
    chars = string.ascii_letters + string.digits
    if use_special:
        chars += '!@#$%^&*()_+-='
    
    password = ''.join(random.choice(chars) for _ in range(length))
    return password

# QM Integration
sys.path.insert(0, r'C:\QMSYS\SYSCOM')
import qmclient as qm

def get_master_password_record(person_id):
    """Get master password record from QM"""
    if not qm.Connected():
        status = qm.ConnectLocal("HAL")
        if not status:
            return None
    
    fno = qm.Open("MASTER_PASSWORD")
    if fno == 0:
        return None
    
    # Find master password record for person
    qm.Execute(f'SELECT MASTER_PASSWORD WITH PERSON_ID = "{person_id}" TO 1')
    
    rec_id = qm.ReadNext(1)
    if not rec_id:
        return None
    
    record = qm.Read(fno, rec_id)
    if not record:
        return None
    
    # Parse record
    fields = record.split('\xfe')  # Field mark
    
    return {
        'id': rec_id,
        'password_hash': fields[2] if len(fields) > 2 else '',
        'salt': fields[3] if len(fields) > 3 else '',
        'encryption_key_enc': fields[4] if len(fields) > 4 else '',
    }

def verify_master_password(person_id, master_password):
    """Verify master password and return encryption key"""
    master_rec = get_master_password_record(person_id)
    
    if not master_rec:
        print("No master password set for this person")
        return None
    
    # Get salt
    salt = bytes.fromhex(master_rec['salt'])
    
    # Hash provided password
    password_hash = hash_password(master_password, salt)
    
    # Compare with stored hash
    if password_hash != master_rec['password_hash']:
        print("Invalid master password")
        return None
    
    # Generate encryption key from master password
    encryption_key = generate_key_from_password(master_password, salt)
    
    return encryption_key

def create_master_password(person_id, master_password):
    """Create master password record"""
    if not qm.Connected():
        status = qm.ConnectLocal("HAL")
        if not status:
            return False
    
    # Generate salt
    salt = generate_salt()
    
    # Hash master password
    password_hash = hash_password(master_password, salt)
    
    # Generate encryption key
    encryption_key = generate_key_from_password(master_password, salt)
    
    # Create record
    rec_id = f"MST{person_id}"
    
    record = [
        rec_id,  # ID
        person_id,  # PERSON_ID
        password_hash,  # PASSWORD_HASH
        salt.hex(),  # SALT
        '',  # ENCRYPTION_KEY_ENC (not storing, derived from master password)
        '',  # HINT
        '',  # RECOVERY_KEY
        '0',  # FAILED_ATTEMPTS
        '',  # LOCKED_UNTIL
        '',  # LAST_LOGIN_DATE
        str(qm.Date()),  # LAST_CHANGED_DATE
        '',  # EXPIRES_DATE
        'N',  # REQUIRE_CHANGE
        '30',  # SESSION_TIMEOUT
        'N',  # BIOMETRIC_ENABLED
        'Y',  # ACTIVE
        str(qm.Date()),  # CREATED_DATE
        str(qm.Date()),  # UPDATED_DATE
    ]
    
    qm_record = '\xfe'.join(record)
    
    fno = qm.Open("MASTER_PASSWORD")
    if fno == 0:
        return False
    
    qm.Write(fno, rec_id, qm_record)
    
    return True

if __name__ == "__main__":
    # Test encryption
    print("Password Encryption Test")
    print("="*60)
    
    master_pw = "TestMasterPassword123!"
    salt = generate_salt()
    key = generate_key_from_password(master_pw, salt)
    
    test_data = "MySecretPassword456"
    encrypted = encrypt_data(test_data, key)
    decrypted = decrypt_data(encrypted, key)
    
    print(f"Original: {test_data}")
    print(f"Encrypted: {encrypted}")
    print(f"Decrypted: {decrypted}")
    print(f"Match: {test_data == decrypted}")
    
    print(f"\nPassword strength: {check_password_strength(test_data)}")
    print(f"Generated password: {generate_password()}")

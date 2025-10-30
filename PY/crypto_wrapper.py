#!/usr/bin/env python3
"""
Minimal Crypto Wrapper for QMBasic
Called from QMBasic programs for encryption/decryption only
"""
import sys
import os
import base64
import hashlib

try:
    from cryptography.fernet import Fernet
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2
except ImportError:
    print("ERROR:cryptography library not installed")
    sys.exit(1)

def generate_key_from_password(master_password, salt_hex):
    """Generate encryption key from master password and salt"""
    salt = bytes.fromhex(salt_hex)
    kdf = PBKDF2(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(master_password.encode()))
    return key

def hash_password(password, salt_hex):
    """Hash a password with salt"""
    salt = bytes.fromhex(salt_hex)
    return hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000).hex()

def generate_salt():
    """Generate a random salt"""
    return os.urandom(16).hex()

def encrypt_data(data, key):
    """Encrypt data with key"""
    f = Fernet(key)
    return f.encrypt(data.encode()).decode()

def decrypt_data(encrypted_data, key):
    """Decrypt data with key"""
    try:
        f = Fernet(key)
        return f.decrypt(encrypted_data.encode()).decode()
    except Exception:
        return "ERROR:Decryption failed"

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

def generate_password(length=16):
    """Generate a random password"""
    import random
    import string
    chars = string.ascii_letters + string.digits + '!@#$%^&*()_+-='
    return ''.join(random.choice(chars) for _ in range(length))

def main():
    if len(sys.argv) < 2:
        print("ERROR:Invalid arguments")
        return 1
    
    command = sys.argv[1].upper()
    
    try:
        if command == "GENERATE_SALT":
            # Generate random salt
            print(generate_salt())
        
        elif command == "HASH_PASSWORD":
            # Hash password with salt
            # Args: password salt_hex
            if len(sys.argv) < 4:
                print("ERROR:Missing arguments")
                return 1
            password = sys.argv[2]
            salt_hex = sys.argv[3]
            print(hash_password(password, salt_hex))
        
        elif command == "GENERATE_KEY":
            # Generate encryption key from master password
            # Args: master_password salt_hex
            if len(sys.argv) < 4:
                print("ERROR:Missing arguments")
                return 1
            master_password = sys.argv[2]
            salt_hex = sys.argv[3]
            key = generate_key_from_password(master_password, salt_hex)
            print(key.decode())
        
        elif command == "ENCRYPT":
            # Encrypt data
            # Args: data encryption_key
            if len(sys.argv) < 4:
                print("ERROR:Missing arguments")
                return 1
            data = sys.argv[2]
            key = sys.argv[3].encode()
            print(encrypt_data(data, key))
        
        elif command == "DECRYPT":
            # Decrypt data
            # Args: encrypted_data encryption_key
            if len(sys.argv) < 4:
                print("ERROR:Missing arguments")
                return 1
            encrypted_data = sys.argv[2]
            key = sys.argv[3].encode()
            result = decrypt_data(encrypted_data, key)
            print(result)
        
        elif command == "CHECK_STRENGTH":
            # Check password strength
            # Args: password
            if len(sys.argv) < 3:
                print("ERROR:Missing arguments")
                return 1
            password = sys.argv[2]
            print(check_password_strength(password))
        
        elif command == "GENERATE_PASSWORD":
            # Generate random password
            # Args: [length]
            length = int(sys.argv[2]) if len(sys.argv) > 2 else 16
            print(generate_password(length))
        
        else:
            print(f"ERROR:Unknown command: {command}")
            return 1
    
    except Exception as e:
        print(f"ERROR:{str(e)}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())

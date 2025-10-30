# Password Manager - Complete Guide

## Overview

Secure password vault with military-grade encryption for storing and managing all your passwords.

## Features

✅ **Military-Grade Encryption** - AES-256 via Fernet (cryptography library)  
✅ **Master Password Protection** - Single password to access all stored passwords  
✅ **Password Generator** - Create strong random passwords  
✅ **Password Strength Checker** - Analyzes password security  
✅ **Category Organization** - Website, App, Email, Bank, System, Other  
✅ **Search & Filter** - Find passwords quickly  
✅ **Import/Export** - CSV and JSON support  
✅ **Usage Tracking** - Track when passwords were last used  
✅ **Secure Notes** - Encrypted notes for each password  
✅ **Two-Factor Tracking** - Track 2FA status  

## Security Features

- **PBKDF2** password hashing with 100,000 iterations
- **Random salt** generation for each master password
- **Fernet symmetric encryption** (AES-128 in CBC mode)
- **No plaintext storage** - All passwords encrypted at rest
- **Master password never stored** - Only hash stored
- **Encryption key derived** from master password (not stored)

---

## Quick Start

### 1. First Time Setup

```bash
cd C:\QMSYS\HAL
python PY\password_manager.py
```

**You'll be prompted to create a master password:**
- Use a strong, unique password
- At least 8 characters (longer is better)
- Mix of uppercase, lowercase, numbers, symbols
- **DO NOT FORGET THIS PASSWORD** - Cannot be recovered!

### 2. Add Your First Password

After login, select option **3. Add Password**

```
Site/Service name: Gmail
Website URL: https://gmail.com
Category: 3 (Email)
Username/Email: your.email@gmail.com
Password: 
  1. Enter manually
  2. Generate random password
Select (1-2): 2
Length (default 16): 20

Generated password: aB3$xK9#mP2@qL7&vN5!

Email used for account: your.email@gmail.com
Two-factor authentication enabled? (y/n): y
Notes: Personal email account

✓ Password saved successfully! ID: PWD20251023033800
```

### 3. View Your Passwords

Select option **1. List All Passwords**

```
============================================================
ID              Site                      Username             Category    
============================================================
★ PWD20251023   Gmail                     your.email@gmail.com email       
  PWD20251024   Facebook                  user@email.com       website     
  PWD20251025   Bank of America           john.doe             bank        
```

### 4. Retrieve a Password

Select option **4. View Password**

```
Enter password ID: PWD20251023

============================================================
Password Details
============================================================
ID: PWD20251023
Site: Gmail
URL: https://gmail.com
Category: email
Username: your.email@gmail.com
Password: aB3$xK9#mP2@qL7&vN5!
Strength: very-strong
2FA Enabled: Y
Notes: Personal email account
```

---

## Menu Options

### 1. List All Passwords
Shows all active passwords with ID, site name, username, and category.

### 2. List by Category
Filter passwords by category:
- `website` - General websites
- `app` - Mobile/desktop apps
- `email` - Email accounts
- `bank` - Banking and financial
- `system` - System/server logins
- `other` - Miscellaneous

### 3. Add Password
Add new password with:
- Site name and URL
- Username/email
- Password (manual or generated)
- Category
- 2FA status
- Encrypted notes

### 4. View Password
View complete password details including:
- Decrypted password
- All metadata
- Usage tracking updated

### 5. Search Passwords
Search by site name or username.

### 6. Delete Password
Mark password as inactive (soft delete).

### 7. Change Master Password
Change your master password (coming soon).

---

## Import/Export

### Import from CSV

**CSV Format:**
```csv
name,url,username,password,category,notes
Gmail,https://gmail.com,user@gmail.com,MyPassword123,email,Personal email
Facebook,https://facebook.com,user@email.com,Pass456,website,Social media
```

**Import command:**
```bash
python PY\import_passwords.py import passwords.csv
```

### Import from JSON

**JSON Format:**
```json
[
  {
    "name": "Gmail",
    "url": "https://gmail.com",
    "username": "user@gmail.com",
    "password": "MyPassword123",
    "category": "email",
    "notes": "Personal email"
  }
]
```

**Import command:**
```bash
python PY\import_passwords.py import passwords.json
```

### Export to CSV

```bash
python PY\import_passwords.py export my_passwords.csv
```

**⚠️ WARNING:** Exported file contains unencrypted passwords! Keep secure and delete after use.

---

## Password Generator

The built-in generator creates strong random passwords:

```python
# Default: 16 characters with special characters
Generated: aB3$xK9#mP2@qL7&

# Custom length
Length: 20
Generated: aB3$xK9#mP2@qL7&vN5!

# Includes:
- Uppercase letters (A-Z)
- Lowercase letters (a-z)
- Numbers (0-9)
- Special characters (!@#$%^&*()_+-=)
```

---

## Password Strength Checker

Automatically evaluates password strength:

**Criteria:**
- Length (8+, 12+, 16+ characters)
- Uppercase letters
- Lowercase letters
- Numbers
- Special characters

**Ratings:**
- **weak** - Basic password, easily cracked
- **medium** - Decent password, could be stronger
- **strong** - Good password, hard to crack
- **very-strong** - Excellent password, very hard to crack

---

## Database Schema

### PASSWORD File (pwd)
- ID - Unique password record ID
- PERSON_ID - Owner reference
- CATEGORY - Type of password
- SITE_NAME - Website/service name
- SITE_URL - Website URL
- USERNAME - Username or email
- PASSWORD_ENCRYPTED - Encrypted password
- PASSWORD_HINT - Password hint (not the password!)
- EMAIL_USED - Email for account
- PHONE_USED - Phone for account
- SECURITY_QUESTIONS - Security questions (multivalued)
- SECURITY_ANSWERS_ENC - Encrypted answers (multivalued)
- TWO_FACTOR_ENABLED - 2FA enabled flag
- TWO_FACTOR_METHOD - 2FA method (app/sms/email/hardware)
- TWO_FACTOR_BACKUP - Backup codes (encrypted, multivalued)
- RECOVERY_EMAIL - Recovery email
- RECOVERY_PHONE - Recovery phone
- LAST_CHANGED_DATE - Password last changed
- EXPIRES_DATE - Password expiration
- STRENGTH - Password strength rating
- NOTES_ENCRYPTED - Encrypted notes
- TAGS - Tags (multivalued)
- FAVORITE - Favorite flag
- SHARED_WITH - Shared with person IDs (multivalued)
- AUTO_LOGIN - Auto-login enabled
- LAST_USED_DATE - Last used date
- USAGE_COUNT - Number of times used
- BREACH_DETECTED - Breach detected flag
- BREACH_DATE - Breach detection date
- ACTIVE - Active status
- CREATED_DATE - Record creation
- UPDATED_DATE - Last update

### MASTER_PASSWORD File (mst)
- ID - Master password record ID
- PERSON_ID - Owner reference
- PASSWORD_HASH - Hashed master password
- SALT - Salt for hashing
- ENCRYPTION_KEY_ENC - Encrypted encryption key
- HINT - Password hint
- RECOVERY_KEY - Recovery key
- FAILED_ATTEMPTS - Failed login attempts
- LOCKED_UNTIL - Account lock date
- LAST_LOGIN_DATE - Last successful login
- LAST_CHANGED_DATE - Password last changed
- EXPIRES_DATE - Password expiration
- REQUIRE_CHANGE - Require password change flag
- SESSION_TIMEOUT - Session timeout (minutes)
- BIOMETRIC_ENABLED - Biometric auth enabled
- ACTIVE - Active status
- CREATED_DATE - Record creation
- UPDATED_DATE - Last update

---

## Security Best Practices

### Master Password
- ✅ Use 16+ characters
- ✅ Mix uppercase, lowercase, numbers, symbols
- ✅ Make it memorable but unique
- ✅ Never share it
- ✅ Don't write it down
- ❌ Don't use personal information
- ❌ Don't reuse from other services

### Stored Passwords
- ✅ Use generated passwords when possible
- ✅ Unique password for each site
- ✅ Enable 2FA when available
- ✅ Change passwords periodically
- ✅ Update immediately if breach detected

### File Security
- ✅ Keep QM database backed up
- ✅ Secure your computer with password/encryption
- ✅ Use antivirus software
- ✅ Keep system updated
- ❌ Don't share your master password
- ❌ Don't export passwords unless necessary

---

## Troubleshooting

### "Invalid master password"
- Check caps lock
- Verify you're using correct master password
- If forgotten, cannot be recovered (no backdoor)

### "Error opening PASSWORD file"
- Ensure QM is running
- Check schema was built: `python PY\run_build_schema.py`
- Verify PASSWORD file exists in QM

### "Error decrypting password"
- Master password may have changed
- Database corruption (restore from backup)
- Encryption key mismatch

### Import fails
- Check CSV/JSON format matches expected structure
- Verify file encoding is UTF-8
- Ensure all required fields present

---

## Command Reference

```bash
# Start password manager
python PY\password_manager.py

# Import passwords from CSV
python PY\import_passwords.py import passwords.csv

# Import passwords from JSON
python PY\import_passwords.py import passwords.json

# Export passwords to CSV
python PY\import_passwords.py export output.csv

# Test encryption
python PY\password_crypto.py

# View passwords in QM
LIST PASSWORD
LIST PASSWORD WITH CATEGORY = "bank"
LIST PASSWORD WITH SITE_NAME LIKE "...gmail..."
```

---

## Technical Details

### Encryption Algorithm
- **Algorithm**: Fernet (symmetric encryption)
- **Cipher**: AES-128 in CBC mode
- **Authentication**: HMAC with SHA-256
- **Key Derivation**: PBKDF2-HMAC-SHA256
- **Iterations**: 100,000
- **Salt**: 16 bytes random

### Password Hashing
- **Algorithm**: PBKDF2-HMAC-SHA256
- **Iterations**: 100,000
- **Salt**: 16 bytes random per user
- **Output**: 256-bit hash

### Data Flow
```
Master Password
    ↓
PBKDF2 (100k iterations)
    ↓
Encryption Key (derived, not stored)
    ↓
Fernet Encryption
    ↓
Encrypted Password (stored in QM)
```

---

## Future Enhancements

- [ ] Password expiration reminders
- [ ] Breach detection integration (Have I Been Pwned API)
- [ ] Password sharing with other users
- [ ] Browser extension integration
- [ ] Mobile app sync
- [ ] Biometric authentication
- [ ] Password history tracking
- [ ] Automatic password rotation
- [ ] Security audit reports
- [ ] Cloud backup/sync

---

## Files Created

```
SCHEMA/
├── PASSWORD.csv              - Password vault schema
└── MASTER_PASSWORD.csv       - Master password schema

PY/
├── password_crypto.py        - Encryption/decryption
├── password_manager.py       - Main password manager
└── import_passwords.py       - Import/export utility

EQU/
├── pwd.equ                   - Password field equates
└── mst.equ                   - Master password equates
```

---

## Support

For issues or questions:
1. Check this guide
2. Review error messages
3. Verify QM is running
4. Check schema is built
5. Ensure cryptography library installed: `pip install cryptography`

---

**Your passwords are now secure!** 🔐

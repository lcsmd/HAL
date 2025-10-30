# 🔐 Password Manager - QMBasic Version

## ✅ REBUILT IN QMBASIC!

Password vault now runs natively in QM with QMBasic programs. Python is used ONLY for encryption.

---

## 🏗️ **Architecture**

```
QMBasic Programs (UI & Business Logic)
    ↓
Python Crypto Module (Encryption ONLY)
    ↓
QM Database (Storage)
```

### **Why This is Better:**
- ✅ **Native QM integration** - Direct file access
- ✅ **Consistent with HAL** - All programs in QMBasic
- ✅ **Better performance** - No QMClient overhead
- ✅ **Easier maintenance** - One language for logic
- ✅ **Direct DICT access** - Native field handling

### **Python Used ONLY For:**
- Encryption/Decryption (AES-256 Fernet)
- Password hashing (PBKDF2)
- Password generation
- Password strength checking

---

## 🚀 **HOW TO RUN**

### **From QM Command Line:**
```
qm -kHAL -c"PASSWORD.MENU"
```

### **Or from Windows:**
```bash
cd C:\QMSYS\HAL
qm -kHAL -c"PASSWORD.MENU"
```

---

## 📦 **QMBasic Programs Created**

### **Main Programs:**
1. **PASSWORD.MENU** - Main menu (interactive)
2. **PASSWORD.MASTER.SETUP** - Create master password
3. **PASSWORD.LOGIN** - Login with master password

### **Password Management:**
4. **PASSWORD.ADD** - Add new password
5. **PASSWORD.VIEW** - View/decrypt password
6. **PASSWORD.LIST** - List all passwords
7. **PASSWORD.SEARCH** - Search passwords
8. **PASSWORD.DELETE** - Delete password

### **Python Module (Minimal):**
- **crypto_wrapper.py** - Encryption functions only

---

## 🎯 **Menu Options**

```
============================================================
Password Manager
============================================================
1. List All Passwords
2. List by Category
3. Add Password
4. View Password
5. Search Passwords
6. Delete Password
7. Generate Password
8. Import Passwords
9. Export Passwords
Q. Quit
```

---

## 💡 **Usage Examples**

### **First Time - Setup Master Password:**
```
qm -kHAL -c"PASSWORD.MENU"

Master Password Setup
============================================================
Enter master password: ****************
Confirm master password: ****************
Password strength: very-strong
✓ Master password created successfully!
```

### **Login:**
```
Password Vault Login
============================================================
Enter master password: ****************
✓ Login successful!
```

### **Add Password:**
```
Select option: 3

Site/Service name: Gmail
Website URL: https://gmail.com
Category: 3 (Email)
Username/Email: your.email@gmail.com
Password: 2 (Generate)
Length: 20

Generated password: aB3$xK9#mP2@qL7&vN5!
✓ Password saved successfully!
```

### **View Password:**
```
Select option: 4
Enter password ID: PWD20251023040000

Password Details
============================================================
Site: Gmail
Username: your.email@gmail.com
Password: aB3$xK9#mP2@qL7&vN5!
Strength: very-strong
```

---

## 🔧 **Python Crypto Wrapper Commands**

The Python module is called from QMBasic using `EXECUTE`:

```basic
* Generate salt
EXECUTE 'python PY/crypto_wrapper.py GENERATE_SALT' CAPTURING SALT

* Hash password
CMD = 'python PY/crypto_wrapper.py HASH_PASSWORD "' : PASSWORD : '" "' : SALT : '"'
EXECUTE CMD CAPTURING HASH

* Generate encryption key
CMD = 'python PY/crypto_wrapper.py GENERATE_KEY "' : MASTER.PW : '" "' : SALT : '"'
EXECUTE CMD CAPTURING KEY

* Encrypt data
CMD = 'python PY/crypto_wrapper.py ENCRYPT "' : DATA : '" "' : KEY : '"'
EXECUTE CMD CAPTURING ENCRYPTED

* Decrypt data
CMD = 'python PY/crypto_wrapper.py DECRYPT "' : ENCRYPTED : '" "' : KEY : '"'
EXECUTE CMD CAPTURING DECRYPTED

* Check password strength
EXECUTE 'python PY/crypto_wrapper.py CHECK_STRENGTH "' : PASSWORD : '"' CAPTURING STRENGTH

* Generate password
EXECUTE 'python PY/crypto_wrapper.py GENERATE_PASSWORD 16' CAPTURING PASSWORD
```

---

## 📊 **Database Files**

### **PASSWORD File (pwd):**
- 32 fields
- Stores encrypted passwords
- Indexed on: ID, PERSON_ID, ACTIVE

### **MASTER_PASSWORD File (mst):**
- 18 fields
- Stores master password hash
- One record per person

---

## 🔐 **Security**

### **Encryption:**
- AES-256 via Fernet
- PBKDF2-HMAC-SHA256 (100,000 iterations)
- Random salt per user
- Master password never stored (only hash)
- Encryption key derived from master password

### **Features:**
- Account lockout after 5 failed attempts
- Usage tracking
- Password strength checking
- Soft delete (mark inactive)

---

## 📁 **Files Structure**

```
C:\QMSYS\HAL\
├── BP\
│   ├── PASSWORD.MENU              ← Main menu
│   ├── PASSWORD.MASTER.SETUP      ← Master password setup
│   ├── PASSWORD.LOGIN             ← Login
│   ├── PASSWORD.ADD               ← Add password
│   ├── PASSWORD.VIEW              ← View password
│   ├── PASSWORD.LIST              ← List passwords
│   ├── PASSWORD.SEARCH            ← Search
│   └── PASSWORD.DELETE            ← Delete
├── PY\
│   ├── crypto_wrapper.py          ← Encryption only
│   ├── password_manager.py        ← Old Python version (deprecated)
│   └── import_passwords.py        ← Import/export utility
├── SCHEMA\
│   ├── PASSWORD.csv               ← Password schema
│   └── MASTER_PASSWORD.csv        ← Master password schema
└── compile_password_programs.cmd  ← Compile script
```

---

## 🛠️ **Compilation**

Programs are already compiled. To recompile:

```bash
cd C:\QMSYS\HAL
.\compile_password_programs.cmd
```

Or manually:
```
qm -kHAL -c"BASIC BP PASSWORD.MENU"
qm -kHAL -c"CATALOG BP PASSWORD.MENU"
```

---

## 🔄 **Import/Export**

### **Import from CSV:**
```bash
python PY\import_passwords.py import passwords.csv
```

**CSV Format:**
```csv
name,url,username,password,category,notes
Gmail,https://gmail.com,user@gmail.com,Pass123,email,Personal
```

### **Export to CSV:**
```bash
python PY\import_passwords.py export output.csv
```

⚠️ **WARNING:** Exported files contain unencrypted passwords!

---

## 📋 **QM Queries**

```
* List all passwords
LIST PASSWORD

* List active passwords
LIST PASSWORD WITH ACTIVE = "Y"

* List by category
LIST PASSWORD WITH CATEGORY = "bank"

* List by person
LIST PASSWORD WITH PERSON.ID = "P001"

* Search by site name
LIST PASSWORD WITH SITE.NAME LIKE "...gmail..."

* Count passwords
COUNT PASSWORD WITH ACTIVE = "Y"

* List weak passwords
LIST PASSWORD WITH STRENGTH = "weak"
```

---

## 🎯 **Quick Commands**

```bash
# Run password manager
qm -kHAL -c"PASSWORD.MENU"

# Run with specific person ID
qm -kHAL -c"PASSWORD.MENU P002"

# Compile programs
.\compile_password_programs.cmd

# Import passwords
python PY\import_passwords.py import file.csv

# Export passwords
python PY\import_passwords.py export output.csv
```

---

## 🆚 **Comparison: QMBasic vs Python**

### **QMBasic Version (Current):**
- ✅ Native QM integration
- ✅ Direct file access
- ✅ Faster performance
- ✅ Consistent with HAL architecture
- ✅ Easier to maintain
- ✅ No QMClient overhead
- ✅ Better error handling
- ✅ Transaction control

### **Python Version (Old):**
- ❌ Requires QMClient API
- ❌ Slower (Python startup + QMClient)
- ❌ Awkward field mark handling
- ❌ Separate runtime environment
- ✅ Good for external APIs only

---

## 🐛 **Troubleshooting**

### **"Error: PASSWORD file not found"**
→ Run: `python PY\run_build_schema.py`

### **"Invalid master password"**
→ Check caps lock, verify correct password

### **"Account locked"**
→ Wait until tomorrow or edit MASTER_PASSWORD record

### **Python errors**
→ Ensure cryptography installed: `pip install cryptography`

### **Compilation errors**
→ Check $INCLUDE paths in programs

---

## ✨ **Benefits of QMBasic Approach**

1. **Performance** - No Python/QMClient overhead
2. **Simplicity** - One language for business logic
3. **Integration** - Native QM file access
4. **Maintenance** - Easier to debug and modify
5. **Consistency** - Matches HAL architecture
6. **Security** - Python only for crypto (minimal attack surface)

---

## 📚 **Going Forward**

**ALL future HAL programs will be QMBasic unless:**
- External API integration required
- Cryptography needed
- Complex parsing (JSON/XML) is easier in Python
- Web scraping needed
- Machine learning required

**Everything else = QMBasic!**

---

**Run it now:** `qm -kHAL -c"PASSWORD.MENU"` 🔐

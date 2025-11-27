# HAL Code Organization - REVISED PROPOSAL

## Critical Issue: QM Catalog Behavior

**IMPORTANT:** QM's catalog is **global**. If you have:
- `FIN.BP/MENU`
- `MED.BP/MENU`
- `SEC.BP/MENU`

And catalog all three, **only the last one cataloged will run** when you type `MENU`.

This means:
- ❌ Cannot have duplicate program names across directories
- ❌ Domain directories alone don't prevent collisions
- ✅ Must use domain prefixes in program names

## Revised Recommendation: Domain Prefixes + Domain Directories

**Combine both approaches for maximum organization and safety:**

### Structure

```
BP/                    # Core system programs (no prefix needed)
  BUILD.SCHEMA
  BUILD.INDEX
  BUILD.DICT
  OPEN.FILES
  SCHEMA.MANAGER
  SCHEMA.ADD.DOMAIN
  SCHEMA.ADD.FILE
  SCHEMA.ADD.FIELD
  SCHEMA.VALIDATE
  SCHEMA.SUMMARY

PY/                    # Core system Python
  hal_service.py
  hal_agent.py
  hal_chat.py
  compile_schema.py
  create_all_schema.py

FIN.BP/                # Financial domain QMBasic
  FIN.IMPORT.QUICKEN
  FIN.STANDARDIZE.PAYEES
  FIN.TAG.REIMBURSABLE
  FIN.REPORT.REIMBURSABLE
  FIN.MANAGE.RULES
  FIN.MENU              # Safe - prefixed with FIN.

FIN.PY/                # Financial domain Python
  fin_ai_rule_learner.py
  fin_ai_classifier.py

MED.BP/                # Medical domain QMBasic
  MED.IMPORT.EPIC
  MED.MEDICAL.MENU
  MED.MEDICATION.MENU
  MED.APPOINTMENT.REMINDER
  MED.MENU              # Safe - prefixed with MED.

MED.PY/                # Medical domain Python
  med_epic_api_sync.py
  med_epic_parser.py
  med_epic_scheduler.py
  med_epic_api_setup.py
  med_analyze_epic_pdf.py

SEC.BP/                # Security domain QMBasic
  SEC.PASSWORD.MENU
  SEC.PASSWORD.ADD
  SEC.PASSWORD.VIEW
  SEC.PASSWORD.SEARCH
  SEC.PASSWORD.DELETE
  SEC.PASSWORD.LOGIN
  SEC.PASSWORD.MASTER.SETUP
  SEC.MENU              # Safe - prefixed with SEC.

SEC.PY/                # Security domain Python
  sec_password_manager.py
  sec_password_crypto.py
  sec_crypto_wrapper.py
  sec_import_passwords.py

COM.BP/                # Communication domain QMBasic
  COM.GMAIL.IMPORT
  COM.EMAIL.MENU
  COM.MENU              # Safe - prefixed with COM.

COM.PY/                # Communication domain Python
  com_gmail_import.py
  com_create_email_file.py
  com_setup_email_file.py

UTIL.BP/               # Utilities (prefixed to avoid conflicts)
  UTIL.TEST.DICT
  UTIL.TEST.OPEN.FILES
  UTIL.TEST.PATH
  UTIL.CRUD.TEMPLATE
  UTIL.STR
  UTIL.DATA.FILTER

UTIL.PY/               # Utility scripts
  util_verify_setup.py
  util_verify_bp_type.py
  util_test_system.py
  util_check_voc.py
```

## Naming Convention

### QMBasic Programs

**Format:** `[DOMAIN].[FUNCTION].[DETAIL]`

**Examples:**
```
FIN.IMPORT.QUICKEN           # Financial import from Quicken
FIN.STANDARDIZE.PAYEES       # Financial payee standardization
FIN.TAG.REIMBURSABLE         # Financial reimbursement tagging
FIN.REPORT.REIMBURSABLE      # Financial reimbursement report
FIN.MENU                     # Financial menu

MED.IMPORT.EPIC              # Medical import from Epic
MED.MEDICAL.MENU             # Medical records menu
MED.MEDICATION.MENU          # Medication management menu
MED.APPOINTMENT.REMINDER     # Medical appointment reminders
MED.MENU                     # Medical main menu

SEC.PASSWORD.MENU            # Security password menu
SEC.PASSWORD.ADD             # Security password add
SEC.PASSWORD.VIEW            # Security password view
SEC.PASSWORD.SEARCH          # Security password search
SEC.MENU                     # Security main menu

BUILD.SCHEMA                 # Core - no prefix needed
BUILD.INDEX                  # Core - no prefix needed
OPEN.FILES                   # Core - no prefix needed
```

### Python Programs

**Format:** `[domain]_[function]_[detail].py`

**Examples:**
```
fin_ai_rule_learner.py       # Financial AI rule learner
fin_ai_classifier.py         # Financial AI classifier
med_epic_api_sync.py         # Medical Epic API sync
med_epic_parser.py           # Medical Epic parser
sec_password_manager.py      # Security password manager
sec_password_crypto.py       # Security password crypto
com_gmail_import.py          # Communication Gmail import
util_verify_setup.py         # Utility verification
```

## Benefits of This Approach

### 1. **No Catalog Collisions**
Every program has a unique name:
- `FIN.MENU` ≠ `MED.MENU` ≠ `SEC.MENU`
- Safe to catalog all programs

### 2. **Clear Domain Ownership**
Program name tells you which domain it belongs to:
- `FIN.*` = Financial
- `MED.*` = Medical
- `SEC.*` = Security

### 3. **Physical Organization**
Related programs grouped in directories:
- All financial programs in `FIN.BP/` and `FIN.PY/`
- All medical programs in `MED.BP/` and `MED.PY/`

### 4. **Easy to Find**
Two ways to locate programs:
- By name: `FIN.IMPORT.QUICKEN`
- By directory: Look in `FIN.BP/`

### 5. **Scalable**
Add new domains easily:
- Create `WOR.BP/` for work programs
- Create `PER.BP/` for personal programs
- No conflicts with existing programs

### 6. **Self-Documenting**
Program name tells you:
- Domain: `FIN`
- Function: `IMPORT`
- Detail: `QUICKEN`

## Migration Plan

### Phase 1: Rename Programs with Domain Prefixes

**Financial Programs:**
```
BP/IMPORT.QUICKEN           → FIN.BP/FIN.IMPORT.QUICKEN
BP/STANDARDIZE.PAYEES       → FIN.BP/FIN.STANDARDIZE.PAYEES
BP/TAG.REIMBURSABLE         → FIN.BP/FIN.TAG.REIMBURSABLE
BP/REPORT.REIMBURSABLE      → FIN.BP/FIN.REPORT.REIMBURSABLE
BP/MANAGE.RULES             → FIN.BP/FIN.MANAGE.RULES

PY/ai_rule_learner.py       → FIN.PY/fin_ai_rule_learner.py
PY/ai_classifier.py         → FIN.PY/fin_ai_classifier.py
```

**Medical Programs:**
```
BP/IMPORT.EPIC              → MED.BP/MED.IMPORT.EPIC
BP/MEDICAL.MENU             → MED.BP/MED.MEDICAL.MENU
BP/MEDICATION.MENU          → MED.BP/MED.MEDICATION.MENU
BP/APPOINTMENT.REMINDER     → MED.BP/MED.APPOINTMENT.REMINDER

PY/epic_api_sync.py         → MED.PY/med_epic_api_sync.py
PY/epic_parser.py           → MED.PY/med_epic_parser.py
PY/epic_scheduler.py        → MED.PY/med_epic_scheduler.py
```

**Security Programs:**
```
BP/PASSWORD.MENU            → SEC.BP/SEC.PASSWORD.MENU
BP/PASSWORD.ADD             → SEC.BP/SEC.PASSWORD.ADD
BP/PASSWORD.VIEW            → SEC.BP/SEC.PASSWORD.VIEW
BP/PASSWORD.SEARCH          → SEC.BP/SEC.PASSWORD.SEARCH
BP/PASSWORD.DELETE          → SEC.BP/SEC.PASSWORD.DELETE
BP/PASSWORD.LOGIN           → SEC.BP/SEC.PASSWORD.LOGIN
BP/PASSWORD.MASTER.SETUP    → SEC.BP/SEC.PASSWORD.MASTER.SETUP

PY/password_manager.py      → SEC.PY/sec_password_manager.py
PY/password_crypto.py       → SEC.PY/sec_password_crypto.py
```

### Phase 2: Create Domain Directories

```bash
mkdir FIN.BP FIN.PY
mkdir MED.BP MED.PY
mkdir SEC.BP SEC.PY
mkdir COM.BP COM.PY
mkdir UTIL.BP UTIL.PY
```

### Phase 3: Copy and Rename Programs

```bash
# Financial
copy BP\IMPORT.QUICKEN FIN.BP\FIN.IMPORT.QUICKEN
copy BP\STANDARDIZE.PAYEES FIN.BP\FIN.STANDARDIZE.PAYEES
copy BP\TAG.REIMBURSABLE FIN.BP\FIN.TAG.REIMBURSABLE
copy BP\REPORT.REIMBURSABLE FIN.BP\FIN.REPORT.REIMBURSABLE
copy BP\MANAGE.RULES FIN.BP\FIN.MANAGE.RULES

copy PY\ai_rule_learner.py FIN.PY\fin_ai_rule_learner.py
copy PY\ai_classifier.py FIN.PY\fin_ai_classifier.py

# Medical
copy BP\IMPORT.EPIC MED.BP\MED.IMPORT.EPIC
copy BP\MEDICAL.MENU MED.BP\MED.MEDICAL.MENU
copy BP\MEDICATION.MENU MED.BP\MED.MEDICATION.MENU
copy BP\APPOINTMENT.REMINDER MED.BP\MED.APPOINTMENT.REMINDER

copy PY\epic_api_sync.py MED.PY\med_epic_api_sync.py
copy PY\epic_parser.py MED.PY\med_epic_parser.py
copy PY\epic_scheduler.py MED.PY\med_epic_scheduler.py

# Security
copy BP\PASSWORD.MENU SEC.BP\SEC.PASSWORD.MENU
copy BP\PASSWORD.ADD SEC.BP\SEC.PASSWORD.ADD
copy BP\PASSWORD.VIEW SEC.BP\SEC.PASSWORD.VIEW
copy BP\PASSWORD.SEARCH SEC.BP\SEC.PASSWORD.SEARCH
copy BP\PASSWORD.DELETE SEC.BP\SEC.PASSWORD.DELETE
copy BP\PASSWORD.LOGIN SEC.BP\SEC.PASSWORD.LOGIN
copy BP\PASSWORD.MASTER.SETUP SEC.BP\SEC.PASSWORD.MASTER.SETUP

copy PY\password_manager.py SEC.PY\sec_password_manager.py
copy PY\password_crypto.py SEC.PY\sec_password_crypto.py
```

### Phase 4: Update Internal References

Programs that call other programs need updating:

**Example: FIN.MENU might call:**
```qmbasic
* Old
EXECUTE "IMPORT.QUICKEN"

* New
EXECUTE "FIN.IMPORT.QUICKEN"
```

**Example: Python imports:**
```python
# Old
from ai_rule_learner import AIRuleLearner

# New
from fin_ai_rule_learner import AIRuleLearner
```

### Phase 5: Compile and Catalog

```
# Compile from new locations
BASIC FIN.BP FIN.IMPORT.QUICKEN
BASIC FIN.BP FIN.STANDARDIZE.PAYEES
BASIC FIN.BP FIN.TAG.REIMBURSABLE
BASIC FIN.BP FIN.REPORT.REIMBURSABLE
BASIC FIN.BP FIN.MANAGE.RULES

BASIC MED.BP MED.IMPORT.EPIC
BASIC MED.BP MED.MEDICAL.MENU
BASIC MED.BP MED.MEDICATION.MENU

BASIC SEC.BP SEC.PASSWORD.MENU
BASIC SEC.BP SEC.PASSWORD.ADD
BASIC SEC.BP SEC.PASSWORD.VIEW

# Catalog with new names
CATALOG FIN.BP FIN.IMPORT.QUICKEN
CATALOG FIN.BP FIN.STANDARDIZE.PAYEES
CATALOG FIN.BP FIN.TAG.REIMBURSABLE
CATALOG FIN.BP FIN.REPORT.REIMBURSABLE
CATALOG FIN.BP FIN.MANAGE.RULES

CATALOG MED.BP MED.IMPORT.EPIC
CATALOG MED.BP MED.MEDICAL.MENU
CATALOG MED.BP MED.MEDICATION.MENU

CATALOG SEC.BP SEC.PASSWORD.MENU
CATALOG SEC.BP SEC.PASSWORD.ADD
CATALOG SEC.BP SEC.PASSWORD.VIEW
```

### Phase 6: Update Documentation

Update all README files to use new program names:
- `README_TRANSACTION_SYSTEM.md` → Use `FIN.*` names
- `README_PASSWORD_MANAGER.md` → Use `SEC.*` names
- `README_EPIC_API.md` → Use `MED.*` names

### Phase 7: Test Thoroughly

```
# Test financial programs
:FIN.IMPORT.QUICKEN C:/test.csv
:FIN.STANDARDIZE.PAYEES
:FIN.TAG.REIMBURSABLE
:FIN.REPORT.REIMBURSABLE SUMMARY

# Test medical programs
:MED.IMPORT.EPIC
:MED.MEDICAL.MENU

# Test security programs
:SEC.PASSWORD.MENU
```

### Phase 8: Remove Old Programs

After verification, delete old programs from BP/ and PY/.

## Core Programs (No Prefix Needed)

These stay in BP/ and PY/ without domain prefixes:

**System/Schema Programs:**
```
BUILD.SCHEMA
BUILD.INDEX
BUILD.DICT
OPEN.FILES
SCHEMA.MANAGER
SCHEMA.ADD.DOMAIN
SCHEMA.ADD.FILE
SCHEMA.ADD.FIELD
SCHEMA.VALIDATE
SCHEMA.SUMMARY
SCHEMA.VIEW.FILE
SCHEMA.LIST.DOMAINS
SCHEMA.LIST.FILES
SCHEMA.EXPORT.DOCS
```

**Core Python:**
```
hal_service.py
hal_agent.py
hal_chat.py
compile_schema.py
create_all_schema.py
```

These are system-level and won't conflict because they're unique.

## Special Cases

### Menu Programs

Each domain can have its own MENU:
```
FIN.MENU        # Financial menu
MED.MENU        # Medical menu
SEC.MENU        # Security menu
COM.MENU        # Communication menu
```

No conflicts because of domain prefix.

### Setup Programs

Each domain can have SETUP:
```
FIN.SETUP       # Financial setup
MED.SETUP       # Medical setup
SEC.SETUP       # Security setup
```

### Test Programs

```
UTIL.TEST.DICT
UTIL.TEST.OPEN.FILES
UTIL.TEST.PATH
```

## Advantages Over Flat Structure

### Without Domain Prefixes (PROBLEM):
```
BP/MENU         # Which menu?
BP/SETUP        # Which setup?
BP/IMPORT       # Import what?
```
Last cataloged wins - **DANGEROUS**

### With Domain Prefixes (SOLUTION):
```
FIN.MENU        # Financial menu - clear
MED.MENU        # Medical menu - clear
SEC.MENU        # Security menu - clear
```
No conflicts - **SAFE**

## Summary

**Recommended Structure:**
- ✅ Domain prefixes in program names (prevents catalog collisions)
- ✅ Domain directories for organization (easy to find related programs)
- ✅ Core programs in BP/PY without prefix (system-level, unique names)
- ✅ Utilities in UTIL.BP/UTIL.PY with UTIL prefix

**Format:**
- QMBasic: `[DOMAIN].[FUNCTION].[DETAIL]`
- Python: `[domain]_[function]_[detail].py`

**Result:**
- No catalog collisions
- Clear organization
- Self-documenting names
- Scalable architecture
- Professional structure

This approach gives you **both safety and organization**.

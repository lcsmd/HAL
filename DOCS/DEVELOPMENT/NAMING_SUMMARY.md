# HAL Naming Conventions - Quick Reference

## Program Type Indicators

### `.S.` = Subroutine (requires arguments, cannot run from command line)
### `.F.` = Function (requires arguments, cannot run from command line)
### No indicator = Regular program (can run from command line)

## QMBasic Naming Patterns

### Regular Programs (User-Facing, Command Line)
**Format:** `[DOMAIN].[ACTION].[OBJECT]`

```
FIN.IMPORT.QUICKEN          # Import Quicken data
FIN.STANDARDIZE.PAYEES      # Standardize payee names
FIN.TAG.REIMBURSABLE        # Tag reimbursable transactions
FIN.REPORT.REIMBURSABLE     # Generate reimbursement report
FIN.MENU                    # Financial menu

MED.IMPORT.EPIC             # Import Epic data
MED.MEDICATION.MENU         # Medication management menu
MED.APPOINTMENT.REMINDER    # Appointment reminders

SEC.PASSWORD.MENU           # Password menu
SEC.PASSWORD.ADD            # Add password
SEC.PASSWORD.VIEW           # View password
```

**Can be run from command line:**
```
:FIN.IMPORT.QUICKEN C:/data.csv
:FIN.MENU
:SEC.PASSWORD.ADD
```

### Subroutines (Require Arguments)
**Format:** `[DOMAIN].[CATEGORY].S.[SUBROUTINE]`

**The `.S.` indicates this is a SUBROUTINE that requires arguments and cannot be run from command line.**

```
FIN.PARSE.S.CSV.LINE        # Parse CSV line subroutine
FIN.CONVERT.S.DATE          # Convert date format subroutine
FIN.VALIDATE.S.AMOUNT       # Validate amount subroutine
FIN.CALC.S.TOTAL            # Calculate total subroutine

MED.PARSE.S.FHIR            # Parse FHIR data subroutine
MED.CALC.S.BMI              # Calculate BMI subroutine
MED.VALIDATE.S.DOSAGE       # Validate dosage subroutine

SEC.CRYPTO.S.ENCRYPT        # Encryption subroutine
SEC.CRYPTO.S.DECRYPT        # Decryption subroutine
SEC.HASH.S.PASSWORD         # Hash password subroutine
```

**Usage in code:**
```qmbasic
* Call subroutine
CALL FIN.PARSE.S.CSV.LINE(LINE, FIELDS)
CALL FIN.CONVERT.S.DATE(DATE.STR, INTERNAL.DATE)
CALL MED.CALC.S.BMI(HEIGHT, WEIGHT, BMI)
```

**Cannot be run from command line** (will error if attempted)

### Functions (Require Arguments, Return Values)
**Format:** `[DOMAIN].[CATEGORY].F.[FUNCTION]`

**The `.F.` indicates this is a FUNCTION that requires arguments and cannot be run from command line.**

```
FIN.CALC.F.TAX              # Calculate tax function
FIN.CALC.F.INTEREST         # Calculate interest function
FIN.VALIDATE.F.AMOUNT       # Validate amount function
FIN.FORMAT.F.CURRENCY       # Format currency function

MED.CALC.F.BMI              # Calculate BMI function
MED.CALC.F.DOSAGE           # Calculate dosage function
MED.VALIDATE.F.DATE         # Validate date function

SEC.CRYPTO.F.ENCRYPT        # Encrypt data function
SEC.CRYPTO.F.DECRYPT        # Decrypt data function
SEC.CRYPTO.F.HASH           # Hash data function
```

**Usage in code:**
```qmbasic
* Call function
CALL FIN.CALC.F.TAX(AMOUNT, RATE, TAX)
CALL MED.CALC.F.BMI(HEIGHT, WEIGHT, BMI)
CALL SEC.CRYPTO.F.HASH(DATA, HASH)
```

**Cannot be run from command line** (will error if attempted)

### Core System Programs (No Domain Prefix)
**Format:** `[ACTION].[OBJECT]`

```
BUILD.SCHEMA                # Build schema structures
BUILD.INDEX                 # Build indexes
BUILD.DICT                  # Build dictionaries
SCHEMA.MANAGER              # Manage schemas
OPEN.FILES                  # Open all system files
```

**These are system-level, no domain needed**

## Python Naming Patterns

### Regular Programs
**Format:** `[domain]_[action]_[object].py`

```
fin_import_quicken.py       # Import Quicken data
fin_ai_rule_learner.py      # AI rule learner
med_epic_api_sync.py        # Epic API sync
sec_password_manager.py     # Password manager
```

### Modules/Libraries (Subroutines/Functions)
**Format:** `[domain]_[category]_lib.py` or `[domain]_[purpose].py`

```
fin_calc_lib.py             # Financial calculation library
fin_validation_lib.py       # Financial validation library
med_fhir_parser.py          # FHIR parser module
sec_crypto_lib.py           # Cryptography library
```

**Functions within these modules:**
```python
# In fin_calc_lib.py
def calculate_tax(amount, rate):
def calculate_interest(principal, rate, years):

# In med_fhir_parser.py
def parse_patient(fhir_data):
def parse_observation(fhir_data):
```

## Quick Decision Tree

### "Can users run this from the command line?"
- **YES** → Regular program: `FIN.IMPORT.QUICKEN`
- **NO** → Continue...

### "Does it require arguments?"
- **YES** → Continue...
- **NO** → Regular program (but why can't users run it?)

### "Is it a subroutine (CALL/GOSUB) or function (returns value)?"
- **Subroutine** → Use `.S.`: `FIN.PARSE.S.CSV.LINE`
- **Function** → Use `.F.`: `FIN.CALC.F.TAX`

## Examples by Type

### User-Facing Programs (No Indicator)
```
FIN.IMPORT.QUICKEN          # User runs: :FIN.IMPORT.QUICKEN file.csv
FIN.MENU                    # User runs: :FIN.MENU
MED.IMPORT.EPIC             # User runs: :MED.IMPORT.EPIC
SEC.PASSWORD.ADD            # User runs: :SEC.PASSWORD.ADD
```

### Subroutines (.S. Indicator)
```
FIN.PARSE.S.CSV.LINE        # Called by: CALL FIN.PARSE.S.CSV.LINE(LINE, FIELDS)
FIN.CONVERT.S.DATE          # Called by: CALL FIN.CONVERT.S.DATE(STR, DATE)
MED.CALC.S.BMI              # Called by: CALL MED.CALC.S.BMI(H, W, BMI)
SEC.CRYPTO.S.ENCRYPT        # Called by: CALL SEC.CRYPTO.S.ENCRYPT(TEXT, KEY, CIPHER)
```

### Functions (.F. Indicator)
```
FIN.CALC.F.TAX              # Called by: CALL FIN.CALC.F.TAX(AMT, RATE, TAX)
FIN.VALIDATE.F.AMOUNT       # Called by: CALL FIN.VALIDATE.F.AMOUNT(AMT, RESULT)
MED.CALC.F.DOSAGE           # Called by: CALL MED.CALC.F.DOSAGE(WT, MG, DOSE)
SEC.CRYPTO.F.HASH           # Called by: CALL SEC.CRYPTO.F.HASH(DATA, HASH)
```

## Directory Organization

```
BP/                         # Core system programs (no domain)
  BUILD.SCHEMA
  BUILD.INDEX
  OPEN.FILES

FIN.BP/                     # Financial programs
  FIN.IMPORT.QUICKEN        # Regular program
  FIN.STANDARDIZE.PAYEES    # Regular program
  FIN.PARSE.S.CSV.LINE      # Subroutine
  FIN.CALC.F.TAX            # Function

MED.BP/                     # Medical programs
  MED.IMPORT.EPIC           # Regular program
  MED.MEDICATION.MENU       # Regular program
  MED.PARSE.S.FHIR          # Subroutine
  MED.CALC.F.BMI            # Function

SEC.BP/                     # Security programs
  SEC.PASSWORD.MENU         # Regular program
  SEC.PASSWORD.ADD          # Regular program
  SEC.CRYPTO.S.ENCRYPT      # Subroutine
  SEC.CRYPTO.F.HASH         # Function

UTIL.BP/                    # Utility programs
  UTIL.TEST.DICT            # Regular program
  UTIL.VERIFY.SETUP         # Regular program
```

## Benefits of This System

### ✅ Clear Intent
- See `.S.` → Know it's a subroutine, needs arguments
- See `.F.` → Know it's a function, needs arguments
- No indicator → Know it's a regular program, can run from command line

### ✅ Prevents Errors
- Users won't try to run `FIN.PARSE.S.CSV.LINE` from command line
- Developers know which programs require arguments
- Clear distinction between user-facing and internal code

### ✅ Better Organization
- Subroutines grouped together (`.S.` programs)
- Functions grouped together (`.F.` programs)
- User programs easy to identify (no indicator)

### ✅ Self-Documenting
- Name tells you: Domain, Category, Type, Purpose
- `FIN.CALC.F.TAX` = Financial calculation function for tax
- `MED.PARSE.S.FHIR` = Medical parsing subroutine for FHIR

### ✅ Manageable Length
- Not too long: `FIN.CALC.F.TAX` (4 segments)
- Not too short: `FIN.TAX` (unclear what it does)
- Just right: Clear, concise, informative

## Summary

| Type | Format | Example | Can Run from CLI? |
|------|--------|---------|-------------------|
| **Regular Program** | `[DOMAIN].[ACTION].[OBJECT]` | `FIN.IMPORT.QUICKEN` | ✅ YES |
| **Subroutine** | `[DOMAIN].[CATEGORY].S.[NAME]` | `FIN.PARSE.S.CSV.LINE` | ❌ NO |
| **Function** | `[DOMAIN].[CATEGORY].F.[NAME]` | `FIN.CALC.F.TAX` | ❌ NO |
| **Core System** | `[ACTION].[OBJECT]` | `BUILD.SCHEMA` | ✅ YES |

**Key Principle:** The `.S.` and `.F.` indicators make it immediately clear that these programs require arguments and cannot be run directly from the command line, keeping names manageable while providing essential information.

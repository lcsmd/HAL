# HAL Naming Conventions - FINAL

## Program Type Indicators (Suffixes)

### `.S` = Subroutine (requires arguments, cannot run from command line)
### `.F` = Function (requires arguments, cannot run from command line)  
### No suffix = Regular program (can run from command line)

**Key principle:** The suffix comes at the END, preserving the semantic meaning of the name.

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
**Format:** `[DOMAIN].[ACTION].[OBJECT].S`

**The `.S` suffix indicates this is a SUBROUTINE that requires arguments.**

```
FIN.PARSE.CSV.LINE.S        # Parse CSV line subroutine
FIN.CONVERT.DATE.S          # Convert date format subroutine
FIN.VALIDATE.AMOUNT.S       # Validate amount subroutine
FIN.CALCULATE.TOTAL.S       # Calculate total subroutine
FIN.FORMAT.CURRENCY.S       # Format currency subroutine

MED.PARSE.FHIR.S            # Parse FHIR data subroutine
MED.CALCULATE.BMI.S         # Calculate BMI subroutine
MED.VALIDATE.DOSAGE.S       # Validate dosage subroutine
MED.FORMAT.DATE.S           # Format date subroutine

SEC.ENCRYPT.DATA.S          # Encryption subroutine
SEC.DECRYPT.DATA.S          # Decryption subroutine
SEC.HASH.PASSWORD.S         # Hash password subroutine
SEC.VALIDATE.TOKEN.S        # Validate token subroutine
```

**Usage in code:**
```qmbasic
* Call subroutine
CALL FIN.PARSE.CSV.LINE.S(LINE, FIELDS)
CALL FIN.CONVERT.DATE.S(DATE.STR, INTERNAL.DATE)
CALL MED.CALCULATE.BMI.S(HEIGHT, WEIGHT, BMI)
CALL SEC.ENCRYPT.DATA.S(PLAINTEXT, KEY, CIPHERTEXT)
```

**Cannot be run from command line** (will error if attempted)

### Functions (Require Arguments, Return Values)
**Format:** `[DOMAIN].[ACTION].[OBJECT].F`

**The `.F` suffix indicates this is a FUNCTION that requires arguments.**

```
FIN.CALCULATE.TAX.F         # Calculate tax function
FIN.CALCULATE.INTEREST.F    # Calculate interest function
FIN.VALIDATE.AMOUNT.F       # Validate amount function
FIN.FORMAT.CURRENCY.F       # Format currency function

MED.CALCULATE.BMI.F         # Calculate BMI function
MED.CALCULATE.DOSAGE.F      # Calculate dosage function
MED.VALIDATE.DATE.F         # Validate date function
MED.PARSE.FHIR.F            # Parse FHIR function

SEC.ENCRYPT.DATA.F          # Encrypt data function
SEC.DECRYPT.DATA.F          # Decrypt data function
SEC.HASH.DATA.F             # Hash data function
SEC.GENERATE.TOKEN.F        # Generate token function
```

**Usage in code:**
```qmbasic
* Call function
CALL FIN.CALCULATE.TAX.F(AMOUNT, RATE, TAX)
CALL MED.CALCULATE.BMI.F(HEIGHT, WEIGHT, BMI)
CALL SEC.HASH.DATA.F(DATA, HASH)
```

**Cannot be run from command line** (will error if attempted)

### Core System Programs (No Domain Prefix)
**Format:** `[ACTION].[OBJECT]` or `[ACTION].[OBJECT].S` or `[ACTION].[OBJECT].F`

```
BUILD.SCHEMA                # Build schema structures (regular)
BUILD.INDEX                 # Build indexes (regular)
OPEN.FILES                  # Open all system files (regular)

PARSE.CSV.S                 # Parse CSV subroutine (core utility)
FORMAT.DATE.S               # Format date subroutine (core utility)
VALIDATE.FIELD.F            # Validate field function (core utility)
```

## Python Naming Patterns

### Regular Programs
**Format:** `[domain]_[action]_[object].py`

```
fin_import_quicken.py       # Import Quicken data
fin_standardize_payees.py   # Standardize payee names
fin_ai_rule_learner.py      # AI rule learner

med_import_epic.py          # Import Epic data
med_epic_api_sync.py        # Epic API sync
med_analyze_vitals.py       # Analyze vital signs

sec_password_manager.py     # Password manager
sec_encrypt_file.py         # Encrypt file
```

### Python Subroutines/Modules
**Format:** `[domain]_[action]_[object].s.py`

**The `.s.py` suffix indicates this is a MODULE with subroutines/functions.**

```
fin_parse_csv.s.py          # CSV parsing module
fin_calculate_tax.s.py      # Tax calculation module
fin_validate_amount.s.py    # Amount validation module

med_parse_fhir.s.py         # FHIR parsing module
med_calculate_bmi.s.py      # BMI calculation module
med_format_date.s.py        # Date formatting module

sec_crypto_functions.s.py   # Cryptography functions module
sec_hash_functions.s.py     # Hashing functions module
```

**Usage:**
```python
# Import and use
from fin_parse_csv.s import parse_csv_line
from med_calculate_bmi.s import calculate_bmi
from sec_crypto_functions.s import encrypt_data
```

## Comparison: Before vs After

### ❌ BEFORE (Breaking Up Semantic Meaning)
```
FIN.PARSE.S.CSV.LINE        # Hard to read, .S. breaks the flow
FIN.CALC.F.TAX              # What is CALC? Calculate? Calculation?
MED.CRYPTO.S.ENCRYPT        # Confusing structure
```

### ✅ AFTER (Suffix Preserves Meaning)
```
FIN.PARSE.CSV.LINE.S        # Clear: Parse CSV line, it's a subroutine
FIN.CALCULATE.TAX.F         # Clear: Calculate tax, it's a function
SEC.ENCRYPT.DATA.S          # Clear: Encrypt data, it's a subroutine
```

## Quick Decision Tree

### "Can users run this from the command line?"
- **YES** → No suffix: `FIN.IMPORT.QUICKEN`
- **NO** → Continue...

### "Does it require arguments?"
- **YES** → Continue...
- **NO** → No suffix (but why can't users run it?)

### "Is it a subroutine or function?"
- **Subroutine** → Add `.S`: `FIN.PARSE.CSV.LINE.S`
- **Function** → Add `.F`: `FIN.CALCULATE.TAX.F`

## Examples by Type

### User-Facing Programs (No Suffix)
```
FIN.IMPORT.QUICKEN          # User runs: :FIN.IMPORT.QUICKEN file.csv
FIN.STANDARDIZE.PAYEES      # User runs: :FIN.STANDARDIZE.PAYEES
FIN.MENU                    # User runs: :FIN.MENU
MED.IMPORT.EPIC             # User runs: :MED.IMPORT.EPIC
SEC.PASSWORD.ADD            # User runs: :SEC.PASSWORD.ADD
```

### Subroutines (.S Suffix)
```
FIN.PARSE.CSV.LINE.S        # Called: CALL FIN.PARSE.CSV.LINE.S(LINE, FIELDS)
FIN.CONVERT.DATE.S          # Called: CALL FIN.CONVERT.DATE.S(STR, DATE)
MED.CALCULATE.BMI.S         # Called: CALL MED.CALCULATE.BMI.S(H, W, BMI)
SEC.ENCRYPT.DATA.S          # Called: CALL SEC.ENCRYPT.DATA.S(TEXT, KEY, CIPHER)
```

### Functions (.F Suffix)
```
FIN.CALCULATE.TAX.F         # Called: CALL FIN.CALCULATE.TAX.F(AMT, RATE, TAX)
FIN.VALIDATE.AMOUNT.F       # Called: CALL FIN.VALIDATE.AMOUNT.F(AMT, RESULT)
MED.CALCULATE.DOSAGE.F      # Called: CALL MED.CALCULATE.DOSAGE.F(WT, MG, DOSE)
SEC.HASH.DATA.F             # Called: CALL SEC.HASH.DATA.F(DATA, HASH)
```

## Directory Organization

```
BP/                         # Core system programs
  BUILD.SCHEMA              # Regular program
  BUILD.INDEX               # Regular program
  PARSE.CSV.S               # Core subroutine
  FORMAT.DATE.S             # Core subroutine

FIN.BP/                     # Financial programs
  FIN.IMPORT.QUICKEN        # Regular program
  FIN.STANDARDIZE.PAYEES    # Regular program
  FIN.PARSE.CSV.LINE.S      # Subroutine
  FIN.CALCULATE.TAX.F       # Function

FIN.PY/                     # Financial Python
  fin_import_quicken.py     # Regular program
  fin_parse_csv.s.py        # Module with functions

MED.BP/                     # Medical programs
  MED.IMPORT.EPIC           # Regular program
  MED.MEDICATION.MENU       # Regular program
  MED.PARSE.FHIR.S          # Subroutine
  MED.CALCULATE.BMI.F       # Function

MED.PY/                     # Medical Python
  med_import_epic.py        # Regular program
  med_parse_fhir.s.py       # Module with functions

SEC.BP/                     # Security programs
  SEC.PASSWORD.MENU         # Regular program
  SEC.PASSWORD.ADD          # Regular program
  SEC.ENCRYPT.DATA.S        # Subroutine
  SEC.HASH.DATA.F           # Function

SEC.PY/                     # Security Python
  sec_password_manager.py   # Regular program
  sec_crypto_functions.s.py # Module with functions
```

## Benefits of Suffix Approach

### ✅ Preserves Semantic Meaning
- `FIN.PARSE.CSV.LINE.S` - Clear what it does (parse CSV line)
- Not `FIN.PARSE.S.CSV.LINE` - Breaks up the meaning

### ✅ Natural Reading Flow
- Read left to right: Domain → Action → Object → Type
- `FIN.CALCULATE.TAX.F` = Financial, Calculate, Tax, Function
- Natural, logical progression

### ✅ Easy to Scan
- All subroutines end with `.S`
- All functions end with `.F`
- Quick visual identification in file lists

### ✅ Consistent with File Extensions
- Python: `module_name.s.py` (suffix before file extension)
- QMBasic: `PROGRAM.NAME.S` (suffix at end)
- Same pattern across languages

### ✅ Grouping in Listings
- Programs sort together: `FIN.IMPORT.*`
- Subroutines sort together: `*.S`
- Functions sort together: `*.F`

## Python File Extension Pattern

### Regular Programs
```
fin_import_quicken.py       # Regular program
med_import_epic.py          # Regular program
sec_password_manager.py     # Regular program
```

### Module/Library Files
```
fin_parse_csv.s.py          # Module with functions (suffix before .py)
med_calculate_bmi.s.py      # Module with functions
sec_crypto_functions.s.py   # Module with functions
```

**Pattern:** `[name].s.py` - The `.s` comes before the `.py` extension

## Summary Table

| Type | QMBasic Format | Python Format | Example |
|------|----------------|---------------|---------|
| **Regular Program** | `[DOMAIN].[ACTION].[OBJECT]` | `[domain]_[action]_[object].py` | `FIN.IMPORT.QUICKEN` |
| **Subroutine** | `[DOMAIN].[ACTION].[OBJECT].S` | `[domain]_[action]_[object].s.py` | `FIN.PARSE.CSV.LINE.S` |
| **Function** | `[DOMAIN].[ACTION].[OBJECT].F` | `[domain]_[action]_[object].f.py` | `FIN.CALCULATE.TAX.F` |

## Key Principles

1. ✅ **Suffix, not infix** - Type indicator at the END
2. ✅ **Preserve semantics** - Don't break up the meaning
3. ✅ **Natural flow** - Domain → Action → Object → Type
4. ✅ **Consistent pattern** - Same approach across languages
5. ✅ **Easy to identify** - Visual pattern for program types

**The suffix approach keeps names readable while clearly indicating the program type!**

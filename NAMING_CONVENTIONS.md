# HAL Naming Conventions

## Philosophy

Good names should be:
1. **Self-documenting** - Tell you what it does without comments
2. **Consistent** - Follow predictable patterns
3. **Hierarchical** - Show relationships and scope
4. **Unambiguous** - No confusion about purpose
5. **Scannable** - Easy to find in lists

## Program Naming

### Main Programs (User-Facing)

**Format:** `[DOMAIN].[ACTION].[OBJECT]`

**Examples:**
```
FIN.IMPORT.QUICKEN          # Import Quicken data
FIN.STANDARDIZE.PAYEES      # Standardize payee names
FIN.TAG.REIMBURSABLE        # Tag reimbursable transactions
FIN.REPORT.REIMBURSABLE     # Generate reimbursement report
FIN.MANAGE.RULES            # Manage processing rules

MED.IMPORT.EPIC             # Import Epic data
MED.SCHEDULE.APPOINTMENT    # Schedule medical appointment
MED.TRACK.MEDICATION        # Track medication adherence
MED.ANALYZE.VITALS          # Analyze vital signs

SEC.PASSWORD.ADD            # Add password
SEC.PASSWORD.VIEW           # View password
SEC.PASSWORD.SEARCH         # Search passwords
SEC.ENCRYPT.DATA            # Encrypt data
SEC.DECRYPT.DATA            # Decrypt data
```

**Pattern Rules:**
- **DOMAIN** - 3-letter domain code (FIN, MED, SEC, etc.)
- **ACTION** - Verb describing what it does (IMPORT, EXPORT, MANAGE, REPORT, etc.)
- **OBJECT** - What it acts on (QUICKEN, PAYEES, RULES, etc.)
- Use **periods** as separators (QM standard)
- Use **UPPERCASE** for QMBasic programs
- Maximum 3 segments to keep names manageable

### Menu Programs

**Format:** `[DOMAIN].MENU.[CONTEXT]`

**Examples:**
```
FIN.MENU                    # Main financial menu
FIN.MENU.TRANSACTIONS       # Transaction submenu
FIN.MENU.REPORTS            # Reports submenu

MED.MENU                    # Main medical menu
MED.MENU.MEDICATIONS        # Medication submenu
MED.MENU.APPOINTMENTS       # Appointments submenu

SEC.MENU                    # Main security menu
SEC.MENU.PASSWORDS          # Password submenu
```

**Special case:** If only one menu per domain, just use `[DOMAIN].MENU`

### System/Core Programs (No Domain)

**Format:** `[ACTION].[OBJECT]`

**Examples:**
```
BUILD.SCHEMA                # Build schema structures
BUILD.INDEX                 # Build indexes
BUILD.DICT                  # Build dictionaries

SCHEMA.MANAGER              # Manage schemas
SCHEMA.ADD.DOMAIN           # Add domain to schema
SCHEMA.ADD.FILE             # Add file to schema
SCHEMA.ADD.FIELD            # Add field to schema
SCHEMA.VALIDATE             # Validate schema

OPEN.FILES                  # Open all system files
```

**Why no domain?**
- These are system-level utilities
- Used across all domains
- No risk of collision (unique names)

### Utility Programs

**Format:** `UTIL.[PURPOSE].[DETAIL]`

**Examples:**
```
UTIL.TEST.DICT              # Test dictionary access
UTIL.TEST.FILES             # Test file operations
UTIL.VERIFY.SETUP           # Verify system setup
UTIL.CRUD.TEMPLATE          # CRUD operation template
UTIL.BENCHMARK.QUERY        # Benchmark query performance
```

## Subroutine/Function Naming

### Internal Subroutines (GOSUB)

**Format:** `[ACTION]_[OBJECT]` or `[ACTION].[OBJECT]`

**Examples:**
```qmbasic
* Processing subroutines
GOSUB PARSE_CSV_LINE
GOSUB CONVERT_DATE
GOSUB VALIDATE_AMOUNT
GOSUB CALCULATE_TOTAL
GOSUB FORMAT_OUTPUT

* Data access subroutines
GOSUB READ_TRANSACTION
GOSUB WRITE_PAYEE
GOSUB UPDATE_RULE
GOSUB DELETE_RECORD

* Business logic subroutines
GOSUB APPLY_RULES
GOSUB MATCH_PATTERN
GOSUB CHECK_DUPLICATE
GOSUB SEND_NOTIFICATION
```

**Pattern Rules:**
- Use **UPPERCASE** with **underscores** or **periods**
- Start with **verb** (action-oriented)
- Be **specific** about what it does
- Group related subroutines with common prefixes:
  - `PARSE_*` - Parsing operations
  - `CONVERT_*` - Conversion operations
  - `VALIDATE_*` - Validation operations
  - `CALCULATE_*` - Calculation operations
  - `FORMAT_*` - Formatting operations

### External Functions (CALL)

**Format:** `[DOMAIN].[CATEGORY].F.[FUNCTION]`

**The `.F.` indicates this is a FUNCTION that requires arguments and cannot be run from command line.**

**Examples:**
```qmbasic
CALL FIN.CALC.F.TAX(AMOUNT, RATE, TAX)
CALL FIN.CALC.F.INTEREST(PRINCIPAL, RATE, YEARS, INTEREST)
CALL FIN.VALIDATE.F.AMOUNT(AMOUNT, RESULT)

CALL MED.CALC.F.BMI(HEIGHT, WEIGHT, BMI)
CALL MED.CALC.F.DOSAGE(WEIGHT, MG.PER.KG, DOSAGE)
CALL MED.VALIDATE.F.DATE(DATE.STR, RESULT)

CALL SEC.CRYPTO.F.ENCRYPT(PLAINTEXT, KEY, CIPHERTEXT)
CALL SEC.CRYPTO.F.DECRYPT(CIPHERTEXT, KEY, PLAINTEXT)
CALL SEC.CRYPTO.F.HASH(DATA, HASH)
```

**Pattern Rules:**
- Use **domain prefix** for reusable functions
- Add **.F.** before function name to indicate it's a function
- Group by **category** (CALC, VALIDATE, FORMAT, etc.)
- Use **descriptive names**
- Document parameters clearly

### Utility Functions (No Domain)

**Format:** `[CATEGORY].F.[FUNCTION]`

**Examples:**
```qmbasic
CALL STRING.F.TRIM(INPUT, OUTPUT)
CALL STRING.F.UPPER(INPUT, OUTPUT)
CALL STRING.F.SPLIT(INPUT, DELIMITER, ARRAY)

CALL DATE.F.FORMAT(INTERNAL, FORMAT, DISPLAY)
CALL DATE.F.PARSE(INPUT, FORMAT, INTERNAL)
CALL DATE.F.DIFF(DATE1, DATE2, DAYS)

CALL ARRAY.F.SORT(ARRAY, SORTED)
CALL ARRAY.F.UNIQUE(ARRAY, UNIQUE)
CALL ARRAY.F.SEARCH(ARRAY, VALUE, INDEX)
```

## Python Naming

### Python Programs

**Format:** `[domain]_[action]_[object].py`

**Examples:**
```python
fin_ai_rule_learner.py          # Financial AI rule learner
fin_ai_classifier.py            # Financial AI classifier
fin_import_quicken.py           # Import Quicken data

med_epic_api_sync.py            # Medical Epic API sync
med_epic_parser.py              # Medical Epic parser
med_analyze_vitals.py           # Analyze vital signs

sec_password_manager.py         # Security password manager
sec_crypto_wrapper.py           # Security crypto wrapper
sec_encrypt_file.py             # Encrypt file
```

**Pattern Rules:**
- Use **lowercase** with **underscores** (Python convention)
- Domain prefix for domain-specific programs
- No prefix for core utilities

### Python Classes

**Format:** `[Domain][Purpose][Type]`

**Examples:**
```python
class FinRuleLearner:           # Financial rule learner
class FinClassifier:            # Financial classifier
class FinTransactionImporter:   # Financial transaction importer

class MedEpicParser:            # Medical Epic parser
class MedAppointmentScheduler:  # Medical appointment scheduler
class MedVitalAnalyzer:         # Medical vital analyzer

class SecPasswordManager:       # Security password manager
class SecCryptoWrapper:         # Security crypto wrapper
class SecHashGenerator:         # Security hash generator

# Core classes (no domain prefix)
class SchemaBuilder:            # Schema builder
class DatabaseConnector:        # Database connector
class ConfigManager:            # Configuration manager
```

**Pattern Rules:**
- Use **PascalCase** (Python convention)
- Domain prefix for domain-specific classes
- Descriptive, noun-based names
- Avoid abbreviations unless well-known

### Python Functions

**Format:** `[action]_[object]` or `[verb]_[noun]`

**Examples:**
```python
def parse_csv_line(line):
def convert_date(date_str):
def validate_amount(amount):
def calculate_total(items):
def format_currency(amount):

def read_transaction(trans_id):
def write_payee(payee_id, data):
def update_rule(rule_id, changes):
def delete_record(file, record_id):

def apply_rules(transaction):
def match_pattern(text, pattern):
def check_duplicate(transaction):
def send_notification(message):
```

**Pattern Rules:**
- Use **lowercase** with **underscores** (Python convention)
- Start with **verb** (action-oriented)
- Be **specific** and **descriptive**
- Avoid abbreviations

### Python Methods

**Format:** Same as functions, but consider context

**Examples:**
```python
class FinRuleLearner:
    def analyze_unmatched_transactions(self, batch_id=None):
    def extract_patterns(self, trans_list):
    def generate_rule_proposal(self, pattern_group):
    def save_proposals(self, proposals):
    def apply_proposal(self, proposal_index):
    
    # Private methods (internal use)
    def _clean_payee_name(self, payee):
    def _calculate_confidence(self, pattern):
    def _create_rule_from_proposal(self, proposal):
```

**Pattern Rules:**
- Public methods: descriptive, action-oriented
- Private methods: prefix with underscore
- Property methods: noun-based (no verb)

## Variable Naming

### QMBasic Variables

**Local Variables:**
```qmbasic
* Use descriptive names
trans_id = ""
payee_name = ""
amount = 0
date_str = ""
is_valid = @FALSE

* Use prefixes for type clarity
num_records = 0
str_category = ""
flag_processed = @FALSE
arr_transactions = ""

* Loop counters (short names OK)
i = 0
j = 0
idx = 0
```

**Common Variables:**
```qmbasic
COMMON /SYSTEM/ FILES(50)       # File handles
COMMON /CONFIG/ CFG.PARAMS      # Configuration
COMMON /SESSION/ USER.ID        # Session data
```

**Pattern Rules:**
- Use **lowercase** with **underscores**
- Be **descriptive** (avoid single letters except loops)
- Use **prefixes** for clarity (num_, str_, flag_, arr_)
- Use **@TRUE/@FALSE** for boolean values

### Python Variables

**Local Variables:**
```python
# Descriptive names
trans_id = ""
payee_name = ""
amount = 0.0
date_str = ""
is_valid = False

# Type hints (recommended)
trans_id: str = ""
amount: float = 0.0
is_valid: bool = False
transactions: List[Dict] = []
```

**Constants:**
```python
# UPPERCASE with underscores
MAX_RETRIES = 3
DEFAULT_TIMEOUT = 30
API_BASE_URL = "https://api.example.com"
CONFIDENCE_THRESHOLD = 0.90
```

**Pattern Rules:**
- Use **lowercase** with **underscores**
- Constants in **UPPERCASE**
- Be **descriptive**
- Use **type hints** when helpful

## File and Directory Naming

### QMBasic Directories

**Format:** `[DOMAIN].BP`

**Examples:**
```
BP/             # Core system programs
FIN.BP/         # Financial programs
MED.BP/         # Medical programs
SEC.BP/         # Security programs
COM.BP/         # Communication programs
UTIL.BP/        # Utility programs
```

### Python Directories

**Format:** `[DOMAIN].PY`

**Examples:**
```
PY/             # Core system Python
FIN.PY/         # Financial Python
MED.PY/         # Medical Python
SEC.PY/         # Security Python
COM.PY/         # Communication Python
UTIL.PY/        # Utility Python
```

### Data Files

**Format:** `[FILENAME]` (from schema)

**Examples:**
```
TRANSACTION     # Transaction data
PAYEE           # Payee master
RULE            # Processing rules
PASSWORD        # Password vault
MEDICATION      # Medication records
APPOINTMENT     # Appointments
```

**Pattern Rules:**
- Use **UPPERCASE** (QM convention)
- Use **singular** nouns (TRANSACTION not TRANSACTIONS)
- Be **descriptive**
- Avoid abbreviations

## Special Naming Patterns

### CRUD Operations

**Format:** `[DOMAIN].[OBJECT].[OPERATION]`

**Examples:**
```
FIN.TRANSACTION.ADD         # Add transaction
FIN.TRANSACTION.VIEW        # View transaction
FIN.TRANSACTION.EDIT        # Edit transaction
FIN.TRANSACTION.DELETE      # Delete transaction
FIN.TRANSACTION.LIST        # List transactions

MED.MEDICATION.ADD
MED.MEDICATION.VIEW
MED.MEDICATION.EDIT
MED.MEDICATION.DELETE
MED.MEDICATION.LIST
```

### Report Programs

**Format:** `[DOMAIN].REPORT.[TYPE]`

**Examples:**
```
FIN.REPORT.REIMBURSABLE     # Reimbursable transactions report
FIN.REPORT.SUMMARY          # Financial summary report
FIN.REPORT.CATEGORY         # Category breakdown report

MED.REPORT.MEDICATIONS      # Medication report
MED.REPORT.APPOINTMENTS     # Appointment report
MED.REPORT.VITALS           # Vital signs report
```

### Import/Export Programs

**Format:** `[DOMAIN].[IMPORT|EXPORT].[SOURCE]`

**Examples:**
```
FIN.IMPORT.QUICKEN          # Import from Quicken
FIN.IMPORT.CSV              # Import from CSV
FIN.EXPORT.EXCEL            # Export to Excel
FIN.EXPORT.PDF              # Export to PDF

MED.IMPORT.EPIC             # Import from Epic
MED.IMPORT.FHIR             # Import FHIR data
MED.EXPORT.CCD              # Export CCD document
```

### Setup/Configuration Programs

**Format:** `[DOMAIN].SETUP.[COMPONENT]`

**Examples:**
```
FIN.SETUP.ACCOUNTS          # Setup financial accounts
FIN.SETUP.CATEGORIES        # Setup categories
FIN.SETUP.RULES             # Setup processing rules

MED.SETUP.PROVIDERS         # Setup healthcare providers
MED.SETUP.PHARMACIES        # Setup pharmacies
MED.SETUP.INSURANCE         # Setup insurance

SYS.SETUP.DATABASE          # Setup database
SYS.SETUP.SCHEMA            # Setup schema
SYS.SETUP.USERS             # Setup users
```

## Anti-Patterns (What to Avoid)

### ❌ Avoid Abbreviations
```
BAD:  FIN.IMP.QKN           # What is QKN?
GOOD: FIN.IMPORT.QUICKEN    # Clear and obvious

BAD:  MED.APPT.SCH          # Confusing
GOOD: MED.APPOINTMENT.SCHEDULE

BAD:  SEC.PWD.MGR           # Unclear
GOOD: SEC.PASSWORD.MANAGER
```

### ❌ Avoid Generic Names
```
BAD:  PROCESS               # Process what?
GOOD: FIN.PROCESS.TRANSACTIONS

BAD:  MANAGER               # Manage what?
GOOD: SEC.PASSWORD.MANAGER

BAD:  UTILITY               # What utility?
GOOD: UTIL.VERIFY.SETUP
```

### ❌ Avoid Ambiguous Names
```
BAD:  FIN.DATA              # What data?
GOOD: FIN.IMPORT.QUICKEN

BAD:  MED.SYSTEM            # What system?
GOOD: MED.IMPORT.EPIC

BAD:  SEC.TOOL              # What tool?
GOOD: SEC.PASSWORD.MANAGER
```

### ❌ Avoid Inconsistent Patterns
```
BAD:  FIN.IMPORT.QUICKEN
      FIN.QUICKEN_IMPORT    # Different pattern
      
GOOD: FIN.IMPORT.QUICKEN
      FIN.IMPORT.CSV        # Consistent pattern

BAD:  MED.IMPORT.EPIC
      MED.EPIC_PARSER       # Inconsistent
      
GOOD: MED.IMPORT.EPIC
      MED.PARSE.EPIC        # Consistent
```

### ❌ Avoid Overly Long Names
```
BAD:  FIN.IMPORT.QUICKEN.CSV.FILE.PROCESSOR.WITH.VALIDATION
      # Too long, hard to type

GOOD: FIN.IMPORT.QUICKEN
      # Concise, clear

BAD:  MED.SCHEDULE.APPOINTMENT.WITH.PROVIDER.AND.INSURANCE.VERIFICATION
      # Way too long

GOOD: MED.SCHEDULE.APPOINTMENT
      # Clear, manageable
```

## Summary

### QMBasic Programs
- **Format:** `[DOMAIN].[ACTION].[OBJECT]`
- **Case:** UPPERCASE
- **Separator:** Periods
- **Example:** `FIN.IMPORT.QUICKEN`

### Python Programs
- **Format:** `[domain]_[action]_[object].py`
- **Case:** lowercase
- **Separator:** Underscores
- **Example:** `fin_import_quicken.py`

### Subroutines/Functions
- **Format:** `[ACTION]_[OBJECT]`
- **Case:** UPPERCASE (QMBasic), lowercase (Python)
- **Example:** `PARSE_CSV_LINE`, `parse_csv_line()`

### Classes
- **Format:** `[Domain][Purpose][Type]`
- **Case:** PascalCase
- **Example:** `FinRuleLearner`

### Variables
- **Format:** `[descriptor]_[name]`
- **Case:** lowercase
- **Example:** `trans_id`, `payee_name`

### Key Principles
1. ✅ Be descriptive and specific
2. ✅ Follow consistent patterns
3. ✅ Use domain prefixes to prevent collisions
4. ✅ Make names self-documenting
5. ✅ Avoid abbreviations and ambiguity

Good naming is an investment in maintainability!

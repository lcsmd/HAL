# HAL Code Organization - FINAL STRUCTURE

## Directory Structure

```
BP/                         # Core system programs (no domain prefix)
PY/                         # Core system Python (no domain prefix)

FIN.BP/                     # Financial QMBasic programs
FIN.PY/                     # Financial Python programs

MED.BP/                     # Medical QMBasic programs
MED.PY/                     # Medical Python programs

SEC.BP/                     # Security QMBasic programs
SEC.PY/                     # Security Python programs

COM.BP/                     # Communication QMBasic programs
COM.PY/                     # Communication Python programs

UTIL.BP/                    # Utility QMBasic programs
UTIL.PY/                    # Utility Python programs

ONCE.BP/                    # One-time QMBasic programs (migrations, setup)
ONCE.PY/                    # One-time Python programs (migrations, setup)
```

## ONCE Directories - Critical Concept

### Purpose
**ONCE.BP/** and **ONCE.PY/** contain programs that should **only be run once** and could have unintended consequences if run again.

### What Goes in ONCE Directories

**Migration Programs:**
```
ONCE.BP/MIGRATE.RENAME.PROGRAMS     # Rename programs to new nomenclature
ONCE.BP/MIGRATE.MOVE.TO.DOMAINS     # Move programs to domain directories
ONCE.BP/MIGRATE.UPDATE.CATALOGS     # Update catalog entries
```

**Setup Programs:**
```
ONCE.BP/SETUP.INITIAL.SCHEMA        # Initial schema setup
ONCE.BP/SETUP.CREATE.DIRECTORIES    # Create directory structure
ONCE.BP/SETUP.IMPORT.LEGACY.DATA    # Import legacy data (one-time)
```

**Data Conversion:**
```
ONCE.PY/convert_old_format.py       # Convert old data format to new
ONCE.PY/migrate_passwords.py        # Migrate passwords (one-time)
ONCE.PY/rebuild_indexes.py          # Rebuild all indexes (one-time)
```

### What Does NOT Go in ONCE

**Regular maintenance programs** - These go in UTIL:
```
UTIL.BP/REBUILD.INDEX               # Can be run anytime
UTIL.BP/VERIFY.SETUP                # Can be run anytime
UTIL.BP/BACKUP.DATA                 # Can be run anytime
```

**Repeatable utilities** - These go in UTIL:
```
UTIL.PY/verify_schema.py            # Safe to run multiple times
UTIL.PY/test_connections.py         # Safe to run multiple times
UTIL.PY/generate_report.py          # Safe to run multiple times
```

### Naming Convention for ONCE Programs

**Format:** `[ACTION].[WHAT].[DETAIL]`

**Examples:**
```
MIGRATE.RENAME.PROGRAMS             # Migrate: rename programs
MIGRATE.MOVE.TO.DOMAINS             # Migrate: move to domain dirs
MIGRATE.UPDATE.REFERENCES           # Migrate: update internal references
SETUP.INITIAL.SCHEMA                # Setup: initial schema
SETUP.CREATE.DIRECTORIES            # Setup: create directories
CONVERT.OLD.FORMAT                  # Convert: old format to new
IMPORT.LEGACY.DATA                  # Import: legacy data
```

**No domain prefix needed** - These are system-level, one-time operations

### Safety Features

**Documentation:**
Every ONCE program should have:
```qmbasic
* WARNING: This program should only be run ONCE
* Purpose: [What it does]
* Date: [When it was created]
* Run by: [Who should run it]
* Consequences if run again: [What could go wrong]
```

**Confirmation Prompts:**
```qmbasic
CRT "WARNING: This program should only be run ONCE!"
CRT "Have you already run this program? (Y/N): "
INPUT ANSWER
IF UPCASE(ANSWER) = "Y" THEN
   CRT "Aborting. Do not run this program again."
   STOP
END

CRT "Are you SURE you want to proceed? (Y/N): "
INPUT ANSWER
IF UPCASE(ANSWER) # "Y" THEN
   CRT "Aborting."
   STOP
END
```

**Execution Log:**
```qmbasic
* Create log file to track execution
LOG.FILE = "ONCE.EXECUTION.LOG"
OPEN LOG.FILE TO F.LOG ELSE
   EXECUTE "CREATE-FILE " : LOG.FILE
   OPEN LOG.FILE TO F.LOG ELSE STOP
END

* Check if already run
READ LOG.REC FROM F.LOG, PROGRAM.NAME THEN
   CRT "ERROR: This program was already run on ": LOG.REC<1>
   CRT "By user: ": LOG.REC<2>
   CRT "Aborting to prevent duplicate execution."
   STOP
END

* ... do the work ...

* Record execution
LOG.REC = ""
LOG.REC<1> = DATE()
LOG.REC<2> = @LOGNAME
LOG.REC<3> = TIME()
WRITE LOG.REC TO F.LOG, PROGRAM.NAME
```

## Migration Program Example

Here's what the migration program would look like:

```qmbasic
PROGRAM MIGRATE.RENAME.PROGRAMS
*
* WARNING: This program should only be run ONCE
* Purpose: Rename programs to new nomenclature with domain prefixes
* Date: 2025-01-24
* Run by: System administrator during reorganization
* Consequences if run again: Could rename already-renamed programs incorrectly
*

PROMPT ""

* Safety check
CRT
CRT STR("=",70)
CRT "WARNING: ONE-TIME MIGRATION PROGRAM"
CRT STR("=",70)
CRT
CRT "This program will:"
CRT "  1. Rename programs to new nomenclature"
CRT "  2. Add domain prefixes"
CRT "  3. Add .S and .F suffixes where appropriate"
CRT
CRT "This should ONLY be run ONCE during the reorganization."
CRT
CRT "Have you already run this program? (Y/N): "
INPUT ANSWER
IF UPCASE(ANSWER) = "Y" THEN
   CRT "Aborting. Do not run this program again."
   STOP
END

CRT
CRT "Are you ABSOLUTELY SURE you want to proceed? (YES/NO): "
INPUT ANSWER
IF UPCASE(ANSWER) # "YES" THEN
   CRT "Aborting. Type YES to proceed."
   STOP
END

* Check execution log
GOSUB CHECK.EXECUTION.LOG

CRT
CRT "Starting migration..."
CRT

* Perform migration
GOSUB MIGRATE.FINANCIAL.PROGRAMS
GOSUB MIGRATE.MEDICAL.PROGRAMS
GOSUB MIGRATE.SECURITY.PROGRAMS
GOSUB MIGRATE.UTILITY.PROGRAMS

* Record execution
GOSUB RECORD.EXECUTION

CRT
CRT "Migration complete!"
CRT "This program should not be run again."
CRT

STOP

* ... subroutines ...

END
```

## Complete Directory Structure with Examples

```
HAL/
├── BP/                             # Core system
│   ├── BUILD.SCHEMA
│   ├── BUILD.INDEX
│   ├── BUILD.DICT
│   ├── OPEN.FILES
│   └── SCHEMA.MANAGER
│
├── PY/                             # Core Python
│   ├── hal_service.py
│   ├── hal_agent.py
│   ├── hal_chat.py
│   └── compile_schema.py
│
├── FIN.BP/                         # Financial QMBasic
│   ├── FIN.IMPORT.QUICKEN
│   ├── FIN.STANDARDIZE.PAYEES
│   ├── FIN.TAG.REIMBURSABLE
│   ├── FIN.REPORT.REIMBURSABLE
│   ├── FIN.MANAGE.RULES
│   ├── FIN.MENU
│   ├── FIN.PARSE.CSV.LINE.S       # Subroutine
│   └── FIN.CALCULATE.TAX.F        # Function
│
├── FIN.PY/                         # Financial Python
│   ├── fin_import_quicken.py
│   ├── fin_ai_rule_learner.py
│   ├── fin_ai_classifier.py
│   └── fin_parse_csv.s.py         # Module
│
├── MED.BP/                         # Medical QMBasic
│   ├── MED.IMPORT.EPIC
│   ├── MED.MEDICAL.MENU
│   ├── MED.MEDICATION.MENU
│   ├── MED.APPOINTMENT.REMINDER
│   ├── MED.MENU
│   ├── MED.PARSE.FHIR.S           # Subroutine
│   └── MED.CALCULATE.BMI.F        # Function
│
├── MED.PY/                         # Medical Python
│   ├── med_import_epic.py
│   ├── med_epic_api_sync.py
│   ├── med_epic_parser.py
│   ├── med_epic_scheduler.py
│   └── med_parse_fhir.s.py        # Module
│
├── SEC.BP/                         # Security QMBasic
│   ├── SEC.PASSWORD.MENU
│   ├── SEC.PASSWORD.ADD
│   ├── SEC.PASSWORD.VIEW
│   ├── SEC.PASSWORD.SEARCH
│   ├── SEC.PASSWORD.DELETE
│   ├── SEC.PASSWORD.LOGIN
│   ├── SEC.PASSWORD.MASTER.SETUP
│   ├── SEC.MENU
│   ├── SEC.ENCRYPT.DATA.S         # Subroutine
│   └── SEC.HASH.DATA.F            # Function
│
├── SEC.PY/                         # Security Python
│   ├── sec_password_manager.py
│   ├── sec_password_crypto.py
│   ├── sec_crypto_wrapper.py
│   ├── sec_import_passwords.py
│   └── sec_crypto_functions.s.py  # Module
│
├── COM.BP/                         # Communication QMBasic
│   ├── COM.GMAIL.IMPORT
│   ├── COM.EMAIL.MENU
│   └── COM.MENU
│
├── COM.PY/                         # Communication Python
│   ├── com_gmail_import.py
│   ├── com_create_email_file.py
│   └── com_setup_email_file.py
│
├── UTIL.BP/                        # Utilities (repeatable)
│   ├── UTIL.TEST.DICT
│   ├── UTIL.TEST.FILES
│   ├── UTIL.VERIFY.SETUP
│   ├── UTIL.CRUD.TEMPLATE
│   └── UTIL.BENCHMARK.QUERY
│
├── UTIL.PY/                        # Utility Python (repeatable)
│   ├── util_verify_setup.py
│   ├── util_verify_bp_type.py
│   ├── util_test_system.py
│   └── util_check_voc.py
│
├── ONCE.BP/                        # One-time QMBasic (DO NOT RE-RUN)
│   ├── MIGRATE.RENAME.PROGRAMS
│   ├── MIGRATE.MOVE.TO.DOMAINS
│   ├── MIGRATE.UPDATE.CATALOGS
│   ├── MIGRATE.UPDATE.REFERENCES
│   ├── SETUP.INITIAL.SCHEMA
│   ├── SETUP.CREATE.DIRECTORIES
│   ├── CONVERT.OLD.FORMAT
│   └── IMPORT.LEGACY.DATA
│
└── ONCE.PY/                        # One-time Python (DO NOT RE-RUN)
    ├── migrate_rename_programs.py
    ├── migrate_move_to_domains.py
    ├── migrate_update_references.py
    ├── convert_old_password_format.py
    ├── rebuild_all_indexes.py
    └── import_legacy_transactions.py
```

## Benefits of ONCE Directories

### ✅ Clear Separation
- One-time programs physically separated from regular programs
- Obvious that these are special

### ✅ Prevents Accidents
- Users won't accidentally run migration programs
- Clear warning in directory name

### ✅ Historical Record
- Keep migration programs for reference
- Document what was done during reorganization
- Can review logic if issues arise

### ✅ Documentation
- ONCE directory serves as documentation of system evolution
- Shows what migrations were performed
- Helps understand current state

### ✅ Safety
- Programs include safety checks
- Execution logging prevents re-runs
- Clear warnings in code

## Execution Log File

Create a special file to track ONCE program execution:

```
ONCE.EXECUTION.LOG/
  MIGRATE.RENAME.PROGRAMS    -> "20250124|admin|14:30:00"
  MIGRATE.MOVE.TO.DOMAINS    -> "20250124|admin|14:35:00"
  SETUP.INITIAL.SCHEMA       -> "20250120|admin|09:00:00"
```

This prevents accidental re-execution.

## Summary

| Directory | Purpose | Can Re-run? | Examples |
|-----------|---------|-------------|----------|
| **BP/** | Core system | ✅ Yes | BUILD.SCHEMA, OPEN.FILES |
| **[DOMAIN].BP/** | Domain programs | ✅ Yes | FIN.IMPORT.QUICKEN, MED.MENU |
| **UTIL.BP/** | Utilities | ✅ Yes | UTIL.VERIFY.SETUP, UTIL.TEST.DICT |
| **ONCE.BP/** | One-time only | ❌ NO | MIGRATE.RENAME.PROGRAMS |

**Key Principle:** If running a program twice could cause problems, it belongs in ONCE.BP/ or ONCE.PY/

This keeps your system safe and well-organized!

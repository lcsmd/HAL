# HAL System Naming Rules and Conventions

**Version**: 1.0  
**Date**: 2025-12-03  
**Status**: DRAFT - Awaiting Approval  
**Purpose**: Define comprehensive, consistent naming conventions for files, fields, programs, and include files

---

## Table of Contents

1. [Overview](#overview)
2. [Schema Requirements](#schema-requirements)
3. [File Naming Conventions](#file-naming-conventions)
4. [Field Naming Conventions](#field-naming-conventions)
5. [Include File Standards](#include-file-standards)
6. [Program Naming Standards](#program-naming-standards)
7. [Code Standards](#code-standards)
8. [Directory Structure](#directory-structure)
9. [Examples](#examples)
10. [Migration Guidelines](#migration-guidelines)

---

## Overview

These naming rules ensure consistency, maintainability, and clarity across the HAL system. All LLM agents and developers must follow these conventions when:

- Creating new data files
- Defining fields in schemas
- Generating include files
- Writing QM Basic programs
- Referencing data in code

### Design Principles

1. **Schema-Driven**: All files and fields must be defined in CSV schemas first
2. **Self-Documenting**: Names should clearly indicate purpose without comments
3. **Consistent Pattern**: Same conventions apply across all domains
4. **Type Safety**: Use equated names instead of numeric attributes
5. **Human Readable**: Code should read like natural language

---

## Schema Requirements

### Schema Index File

**Location**: `SCHEMA/SCHEMA_INDEX.csv`

**Required Columns**:
```csv
FileName,Abbrev,FileNum,FileType,Priority,Description,FieldCount,Status
```

**Example**:
```csv
MEDICATION,med,20,DYNAMIC,1,Medications and prescriptions,28,active
TRANSACTION,trn,32,DYNAMIC,1,Financial transactions,23,active
```

### Field Definition Files

**Location**: `SCHEMA/<FILENAME>.csv`

**Required Columns**:
```csv
FieldName,FieldNum,Type,Description,Required,Indexed,ConversionCode
```

**Field Types**:
- `K` - Key field (always field 0)
- `A` - Alphanumeric text
- `N` - Numeric
- `D` - Date (must end with .dt suffix)
- `T` - Text (long form)
- `M` - Multivalued

**Example** (`SCHEMA/MEDICATION.csv`):
```csv
FieldName,FieldNum,Type,Description,Required,Indexed,ConversionCode,Format
ID,0,K,Unique medication record ID,Y,Y,,
PERSON_ID,1,A,Reference to PERSON file,Y,Y,,
MEDICATION_NAME,2,A,Medication name,Y,Y,,
START.dt,9,D,Start date,Y,Y,D4-,R10
END.dt,10,D,End date,N,N,D4-,R10
COST,21,N,Cost per fill,N,N,MD2,$,
STATUS,11,A,Status (active/discontinued/completed),Y,Y,,
CREATED.dt,26,D,Record creation date,Y,N,D4-,R10
UPDATED.dt,27,D,Last update date,Y,N,D4-,R10
```

**ConversionCode Column** (column 7 in CSV → DICT attribute 3):
- **Date conversions**: `D4-` (YYYY-MM-DD format) - REQUIRED for all date fields
- **Numeric conversions**: `MD2` (2 decimals), `MD2,$` (currency with 2 decimals), `MD0` (integer)
- **Text conversions**: `T` (text justification)
- Leave blank if no conversion needed

**Format Column** (column 8 in CSV → DICT attribute 5):
- Format specification: `JLength` where J = justification, Length = width
- **Date fields**: `R10` (right-justified, 10 characters for YYYY-MM-DD)
- **Currency/Numeric**: `R12`, `R15` (right-justified with width)
- **Text fields**: `L30`, `L50` (left-justified with width)
- **Long text**: `T50`, `T100` (text-justified with width)
- Leave blank for default formatting
- Examples: `L10`, `R10`, `T50`

**OpenQM Dictionary Structure**:
```
Attribute 1: D (type - always D for data definition, never A or S)
Attribute 2: Field number (0, 1, 2, etc.)
Attribute 3: Conversion code (D4-, MD2,$, etc.)
Attribute 4: Title/Column heading for display
Attribute 5: Format specification (JLength format)
```

**Format Specification (Attribute 5)**:
- Format: `JLength` where:
  - `J` = Justification code (L=left, R=right, T=text)
  - `Length` = Field width in characters
- Examples:
  - `L10` = Left justified, 10 characters
  - `R10` = Right justified, 10 characters (dates in YYYY-MM-DD format)
  - `R12` = Right justified, 12 characters (currency amounts)
  - `L30` = Left justified, 30 characters (names, descriptions)
  - `T50` = Text justified, 50 characters (long text fields)

**IMPORTANT**: All dictionary entries must be type **D** (data definition), not type A (alternative) or S (synonym). This ensures consistent dictionary behavior.

### Rule: All Files Must Be in Schema

**Every data file in the HAL system must have**:
1. Entry in `SCHEMA/SCHEMA_INDEX.csv`
2. Detailed field definition in `SCHEMA/<FILENAME>.csv`
3. Status of "active" in SCHEMA_INDEX.csv

### Rule: Dictionary Entries Must Be Type D

**All dictionary data field entries must be**:
1. Type **D** (data definition) - never type A (alternative) or S (synonym)
2. Attribute 2: Field number
3. Attribute 3: Conversion code (if applicable)
4. Attribute 4: Column heading/title
5. Attribute 5: Format specification (if applicable)

This is critical for BUILD.SCHEMA to generate correct dictionary entries.

---

## File Naming Conventions

### File Name Components

```
<FILENAME> = Full uppercase name (e.g., MEDICATION, TRANSACTION)
<abbrev> = 3-letter lowercase abbreviation (e.g., med, trn)
<FileNum> = Unique integer 1-99 (e.g., 20, 32)
```

### File Abbreviation Rules

1. **Length**: Exactly 3 characters (lowercase)
2. **Uniqueness**: No two files share the same abbreviation
3. **Mnemonic**: Should clearly relate to file name
4. **Consistency**: Use standard abbreviations:
   - `med` - MEDICATION
   - `trn` - TRANSACTION
   - `pwd` - PASSWORD_VAULT
   - `per` - PERSON
   - `doc` - DOCUMENT

### File Number Assignment

- **1-40**: Core data files (person, medical, financial)
- **41-60**: Secondary data files (logs, imports)
- **61-80**: System files (config, schema, temp)
- **81-99**: Reserved for future expansion

---

## Field Naming Conventions

### Field Name Components

```
<FIELDNAME> = Full uppercase field name (e.g., MEDICATION_NAME, START_DATE)
<fieldname> = Full lowercase field name (e.g., medication_name, start_date)
```

### Field Naming Rules

1. **Format**: UPPERCASE with underscores (FIELD_NAME)
2. **Clarity**: Descriptive and unambiguous
3. **Consistency**: Use standard suffixes:
   - `_ID` - Foreign key reference (PERSON_ID, DOCTOR_ID)
   - `.dt` - Date fields (START.dt, CREATED.dt, APPOINTMENT.dt)
   - `_FLAG` - Boolean fields (ACTIVE_FLAG, DELETED_FLAG)
   - `_COUNT` - Numeric counters (REFILLS_COUNT, ITEM_COUNT)
   - `_AMT` or `_AMOUNT` - Currency amounts

4. **Date Field Standards**:
   - **Suffix**: All date fields must end with `.dt` (e.g., START.dt, END.dt)
   - **Conversion Code**: `D4-` (YYYY-MM-DD format)
   - **Format**: `R10` (right-justified, 10 characters)
   - **Type**: `D` in schema CSV
   - Examples: TRANSACTION.dt, APPOINTMENT.dt, CREATED.dt, UPDATED.dt

5. **Reserved Field Names**:
   - `ID` - Always field 0, primary key
   - `ACTIVE` - Standard active/inactive flag
   - `CREATED.dt` - Record creation date (not CREATED_DATE)
   - `UPDATED.dt` - Last update date (not UPDATED_DATE)
   - `TAGS` - Multivalued categorization

### Field Number Assignment

- **0**: Always the ID/key field
- **1-10**: Primary identifying fields
- **11-20**: Core data fields
- **21-30**: Extended/optional fields
- **31+**: Metadata fields (created_date, updated_date, tags, notes)

---

## Include File Standards

### Include File Location

**Current Directory**: `EQU/` (contains 43 .h files and 40 .equ files)  
**Migration Target**: Standardize existing EQU/ files or migrate to `INCLUDE/` (decision pending)

**Current State**:
- **43 .h files** - Full format (e.g., MEDICATION.h, TRANSACTION.h)
- **40 .equ files** - Simplified format (DEPRECATED - to be removed)
- Auto-generated by BUILD.SCHEMA
- Use `.A` suffix for attributes (e.g., MEDICATION.ID.A)
- Use `.R` for record buffer (e.g., med.R<MEDICATION.ID.A>)
- **To be added**: Conversion code equates (.conv) and format equates (.fmt)

**All include files must**:
1. Have `.H` suffix (uppercase H)
2. Reside in `EQU/` directory
3. Be auto-generated by BUILD.SCHEMA
4. **One file per entity**: Consolidate to .h only, remove .equ files
5. Follow the standard template below

### Include File Template

Each data file must have a corresponding include file with these sections:

```basic
* <FILENAME> field equates
* Auto-generated by BUILD.SCHEMA on <date>
* Source: SCHEMA/<FILENAME>.csv

* ============================================================
* SECTION 1: File Reference Equates
* ============================================================

EQU <FILENAME>.FILE.NUM TO <FileNum>
EQU <FILENAME>.F TO FILES(<FILENAME>.FILE.NUM)
EQU <abbrev>.F TO <FILENAME>.F
EQU <abbrev> TO <abbrev>.F

* ============================================================
* SECTION 2: Field Attribute Number Equates
* ============================================================

EQU <FILENAME>.<FIELDNAME>.A TO <FieldNum>
EQU <abbrev>.<FIELDNAME>.A TO <FILENAME>.<FIELDNAME>.A

* (Repeat for all fields)

* ============================================================
* SECTION 3: Field Buffer Equates
* ============================================================

EQU <abbrev>.<FIELDNAME> TO <abbrev>.R<<FILENAME>.<FIELDNAME>.A>

* (Repeat for all fields)

* ============================================================
* SECTION 4: Conversion Code Equates (NEW - to be added)
* ============================================================

EQU <abbrev>.<FIELDNAME>.conv TO "<conversion>"

* (Only for fields with ConversionCode in schema CSV)
* Examples:
*   EQU med.START_DATE.conv TO "D2/"
*   EQU trn.AMOUNT.conv TO "MD2,$"

* ============================================================
* SECTION 5: Convenience Aliases
* ============================================================

EQU <abbrev>.id TO <abbrev>.R<<FILENAME>.ID.A>
EQU <abbrev>.rec TO <abbrev>.R

```

**Note**: Current files use uppercase `.A` suffix and uppercase `.R` for record buffer, matching OpenQM conventions.

### Equate Naming Patterns

#### 1. File Reference Equates (EXISTING)

```basic
EQU MEDICATION.FILE.NUM TO 20
EQU MEDICATION.F TO FILES(MEDICATION.FILE.NUM)
EQU med.F TO MEDICATION.F
EQU med TO med.F
```

**Purpose**: Reference the file handle  
**Status**: ✅ Already implemented in EQU/*.h files  
**Usage**: `OPEN "MEDICATION" TO med ELSE STOP`

#### 2. Field Attribute Equates (EXISTING)

```basic
EQU MEDICATION.MEDICATION_NAME.A TO 2
EQU med.MEDICATION_NAME.A TO MEDICATION.MEDICATION_NAME.A
```

**Purpose**: Reference the attribute number  
**Status**: ✅ Already implemented in EQU/*.h files  
**Usage**: `DICT.REC<med.MEDICATION_NAME.A> = "D"`  
**Note**: Uses `.A` suffix (not `.att`)

#### 3. Field Buffer Equates (EXISTING)

```basic
EQU med.MEDICATION_NAME TO med.R<MEDICATION.MEDICATION_NAME.A>
```

**Purpose**: Access field data from record  
**Status**: ✅ Already implemented in EQU/*.h files  
**Usage**: 
```basic
READ med.R FROM med, med.id ELSE STOP
PRINT "Medication: ":med.MEDICATION_NAME
```
**Note**: Uses uppercase `.R` for record buffer, UPPERCASE field names

#### 4. Conversion Code Equates (NEW - TO BE ADDED)

```basic
EQU med.START_DATE.conv TO "D2/"
EQU med.COST.conv TO "MD2,$"
EQU trn.TRANS_DATE.conv TO "D2/"
EQU trn.AMOUNT.conv TO "MD2,$"
```

**Purpose**: Store dictionary conversion codes for formatting  
**Status**: ❌ Not currently implemented - needs to be added  
**Source**: ConversionCode column in SCHEMA/*.csv (to be added to CSVs)  
**Usage**: 
```basic
PRINT OCONV(med.START_DATE, med.START_DATE.conv)
FORMATTED.AMOUNT = OCONV(trn.AMOUNT, trn.AMOUNT.conv)
```

### Special Equates

```basic
* Primary key equate (always field 0)
EQU <abbrev>.id TO <abbrev>.R<<FILENAME>.ID.A>

* Record holder variable name
* Programs should use: <abbrev>.R (uppercase R)
```

---

## OPEN.FILES Subroutine

### Purpose

Dynamic subroutine that opens data files based on priority settings in schema.

### Location

`BP/OPEN.FILES` (subroutine, not include file)

### Implementation

```basic
SUBROUTINE OPEN.FILES
* Opens data files with PRIORITY=1 from SCHEMA_INDEX.csv
* Dynamically reads schema and opens only priority files
* Source: SCHEMA/SCHEMA_INDEX.csv

COMMON /FILES/ FILES(100)

* Read schema index
INDEX.FILENAME = "SCHEMA/SCHEMA_INDEX.csv"
OPENSEQ INDEX.FILENAME TO f.index ELSE
   PRINT "Error: Cannot open ":INDEX.FILENAME
   STOP
END

* Read all lines
csv.lines = ""
line.count = 0
LOOP
   READSEQ line FROM f.index ELSE EXIT
   line.count += 1
   IF line.count > 1 THEN
      csv.lines<-1> = line
   END
REPEAT
CLOSESEQ f.index

* Parse and open priority 1 files only
files.opened = 0
failed.files = ""

FOR i = 1 TO DCOUNT(csv.lines, @FM)
   line = csv.lines<i>
   IF line = "" THEN CONTINUE
   
   filename = FIELD(line, ",", 1)
   file.num = FIELD(line, ",", 3)
   priority = FIELD(line, ",", 5)
   status = FIELD(line, ",", 8)
   
   * Only open priority 1 active files
   IF status = "active" AND priority = "1" THEN
      OPEN filename TO FILES(file.num) ELSE
         failed.files<-1> = filename
         CONTINUE
      END
      files.opened += 1
   END
NEXT i

* Report failures
IF failed.files # "" THEN
   failed.ct = DCOUNT(failed.files, @FM)
   PRINT "THE FOLLOWING ":failed.ct:" PRIORITY 1 FILES FAILED TO OPEN:"
   FOR x = 1 TO failed.ct
      PRINT "  ":failed.files<x>
   NEXT x
   STOP
END

* Success message (optional)
* PRINT "Opened ":files.opened:" priority 1 files"

RETURN
END
```

### Usage in Programs

```basic
PROGRAM EXAMPLE

* Include common block
$INCLUDE EQU/COMMON.H

* Include file definitions
$INCLUDE EQU/MEDICATION.H
$INCLUDE EQU/TRANSACTION.H

* Open all priority 1 files dynamically
CALL OPEN.FILES

* Now all priority 1 files are open and ready
READ med.R FROM med, "MED001" ELSE STOP
PRINT med.MEDICATION_NAME

END
```

### Benefits

- **Dynamic**: Automatically adapts to schema changes
- **Priority-based**: Opens only files with PRIORITY=1
- **No regeneration**: Changes to SCHEMA_INDEX.csv take effect immediately
- **Error reporting**: Lists files that failed to open
- **Centralized**: Single subroutine for all programs

---

## Program Naming Standards

### Program Name Format

```
<file.abbrev>.<ACTION>.<MODIFIER>
```

Where:
- `<file.abbrev>` - 3-letter file abbreviation (lowercase)
- `<ACTION>` - What the program does (UPPERCASE)
- `<MODIFIER>` - Optional distinguisher (UPPERCASE)

### Standard Actions

| Action | Purpose | Example |
|--------|---------|---------|
| `ADD` | Create new record | `med.ADD` |
| `EDIT` | Modify existing record | `med.EDIT` |
| `DELETE` | Remove record | `med.DELETE` |
| `VIEW` | Display record | `med.VIEW` |
| `LIST` | List multiple records | `med.LIST` |
| `SEARCH` | Find records | `med.SEARCH` |
| `REPORT` | Generate report | `med.REPORT` |
| `IMPORT` | Import data | `med.IMPORT` |
| `EXPORT` | Export data | `med.EXPORT` |
| `MENU` | Menu system | `med.MENU` |
| `PROCESS` | Process/calculate | `trn.PROCESS` |
| `VALIDATE` | Validation routine | `pwd.VALIDATE` |

### Modifier Usage

Use modifiers when:
1. Multiple programs perform same action differently
2. Distinguishing between variants

Examples:
- `med.IMPORT.EPIC` - Import from Epic API
- `med.IMPORT.CSV` - Import from CSV file
- `trn.REPORT.MONTHLY` - Monthly transaction report
- `trn.REPORT.ANNUAL` - Annual transaction report

### Multi-File Programs

For programs that work with multiple files, use domain prefix:

- `fin.RECONCILE` - Financial reconciliation (multiple files)
- `med.SYNC.EPIC` - Medical data sync (multiple medical files)
- `sys.BACKUP.ALL` - System-wide backup

### Utility Programs

For programs that don't act on specific files:

```
<domain>.UTILITY.<NAME>
```

Examples:
- `sys.UTIL.BACKUP`
- `fin.UTIL.CALCULATOR`
- `med.UTIL.CONVERTER`

---

## Code Standards

### Variable Naming in Programs

#### QM Basic Case Conventions

QM Basic is **case-insensitive** for variable names, but we follow these conventions for readability:

**UPPERCASE** (for constants and equates):
```basic
* EQU statements - always UPPERCASE
EQU MEDICATION.FILE.NUM TO 20
EQU MEDICATION.MEDICATION_NAME.A TO 2

* Manifest constants
EQU MAX.RETRIES TO 3
EQU DEFAULT.STATUS TO "ACTIVE"

* System variables
COMMON /FILES/ FILES(100)
```

**lowercase** (for runtime variables):
```basic
* Loop counters
FOR i = 1 TO record.count
FOR x = 1 TO field.count

* Temporary variables
temp.value = ""
line.count = 0
failed.files = ""

* Descriptive variables
user.name = ""
error.message = ""
total.amount = 0
```

**Mixed Case** (field access through equates):
```basic
* File handle (lowercase abbreviation)
OPEN "MEDICATION" TO med ELSE STOP

* Record and ID (lowercase prefix, UPPERCASE field via equate)
med.id = "MED001"
READ med.R FROM med, med.id ELSE STOP

* Field access (resolves to med.R<MEDICATION.MEDICATION_NAME.A>)
PRINT med.MEDICATION_NAME
med.START.dt = "2024-01-15"
```

**Key Principle**: Since case doesn't matter in QM Basic, **consistency** is more important than the specific convention. Use:
- UPPERCASE for compile-time constants (EQUs)
- lowercase for runtime variables
- Follow established patterns in existing code

#### Record Variables

```basic
<abbrev>.R = "Complete record buffer (uppercase R)"
<abbrev>.id = "Record ID/key (lowercase)"
```

Example:
```basic
med.id = "MED001"
READ med.R FROM med, med.id ELSE
   PRINT "Medication not found"
   STOP
END
```

#### Field Access

```basic
* Use equated field names (UPPERCASE from include file)
PRINT med.MEDICATION_NAME
PRINT med.START.dt

* Format dates using .conv equates
PRINT OCONV(med.START.dt, med.START.dt.conv)
```

#### File Handles

```basic
* Use lowercase abbreviation (from schema)
OPEN "MEDICATION" TO med ELSE STOP

* File handle via FILES array
OPEN "MEDICATION" TO FILES(MEDICATION.FILE.NUM) ELSE STOP
```

#### Loop Variables and Counters

```basic
* Standard loop counters (lowercase)
FOR i = 1 TO max.count
FOR x = 1 TO field.count
FOR rec.num = 1 TO total.records

* Descriptive counters
FOR line.count = 1 TO total.lines
FOR file.x = 1 TO file.count
```

### Required Includes

Every program that accesses data files must:

```basic
PROGRAM <name>

* Include all file definitions needed
$INCLUDE INCLUDE/MEDICATION.H
$INCLUDE INCLUDE/DOCTOR.H

* Open files
$INCLUDE INCLUDE/OPEN.FILES.H

* Program logic here

END
```

### Standard Code Pattern

```basic
PROGRAM med.VIEW

* Include definitions
$INCLUDE INCLUDE/MEDICATION.H

* Open files
$INCLUDE INCLUDE/OPEN.FILES.H

* Get record ID
INPUT "Enter Medication ID: ":med.id

* Read record
READ med.rec FROM med, med.id ELSE
   PRINT "Medication ":med.id:" not found"
   STOP
END

* Display fields using named equates
PRINT "ID: ":med.id
PRINT "Name: ":med.medication_name
PRINT "Dosage: ":med.dosage:" ":med.dosage_unit
PRINT "Start Date: ":OCONV(med.start_date, med.start_date.conv)
PRINT "Cost: ":OCONV(med.cost, med.cost.conv)

END
```

---

## Directory Structure

### Schema Files

```
SCHEMA/
├── SCHEMA_INDEX.csv          - Master file registry
├── domains.csv               - Domain definitions
├── MEDICATION.csv            - Field definitions for MEDICATION
├── TRANSACTION.csv           - Field definitions for TRANSACTION
└── <FILENAME>.csv            - One per data file
```

### Include Files

```
INCLUDE/
├── OPEN.FILES.H              - Opens all files
├── COMMON.H                  - Common system equates
├── MEDICATION.H              - MEDICATION field equates
├── TRANSACTION.H             - TRANSACTION field equates
└── <FILENAME>.H              - One per data file
```

### Programs

```
BP/
├── med.ADD                   - Add medication
├── med.EDIT                  - Edit medication
├── med.VIEW                  - View medication
├── med.LIST                  - List medications
├── trn.IMPORT.CSV            - Import transactions
└── <abbrev>.<ACTION>.<MOD>   - Standard naming
```

---

## Examples

### Example 1: MEDICATION File

#### Schema Index Entry
```csv
FileName,Abbrev,FileNum,FileType,Priority,Description,FieldCount,Status
MEDICATION,med,20,DYNAMIC,1,Medications and prescriptions,28,active
```

#### Field Definition (SCHEMA/MEDICATION.csv)
```csv
FieldName,FieldNum,Type,Description,Required,Indexed,ConversionCode,Format
ID,0,K,Unique medication record ID,Y,Y,,
MEDICATION_NAME,2,A,Medication name,Y,Y,,
START.dt,9,D,Start date,Y,Y,D4-,R10
END.dt,10,D,End date,N,N,D4-,R10
COST,21,N,Cost per fill,N,N,MD2,$,R12
CREATED.dt,26,D,Record creation date,Y,N,D4-,R10
UPDATED.dt,27,D,Last update date,Y,N,D4-,R10
```

#### Current Include File (EQU/MEDICATION.h)
```basic
* MEDICATION field equates
* Auto-generated by BUILD.SCHEMA

* File reference equates
EQU MEDICATION.FILE.NUM TO 20
EQU MEDICATION.F TO FILES(MEDICATION.FILE.NUM)
EQU med.F TO MEDICATION.F
EQU med TO med.F

* Field attribute equates (note: .A suffix, not .att)
EQU MEDICATION.ID.A TO 0
EQU MEDICATION.MEDICATION_NAME.A TO 2
EQU MEDICATION.START_DATE.A TO 9
EQU MEDICATION.COST.A TO 21
* ... (all 28 fields)

* Field buffer equates (note: .R for record, UPPERCASE field names)
EQU med.ID TO med.R<MEDICATION.ID.A>
EQU med.MEDICATION_NAME TO med.R<MEDICATION.MEDICATION_NAME.A>
EQU med.START_DATE TO med.R<MEDICATION.START_DATE.A>
EQU med.COST TO med.R<MEDICATION.COST.A>
* ... (all 28 fields)

* Conversion code equates (TO BE ADDED)
EQU med.START_DATE.conv TO "D2/"
EQU med.COST.conv TO "MD2,$"
```

**Changes Needed**:
1. ✅ File equates - Already correct
2. ✅ Attribute equates - Already correct (using .A)
3. ✅ Buffer equates - Already correct (using .R and UPPERCASE)
4. ❌ Conversion equates - Need to be added

#### Sample Program (BP/med.VIEW)
```basic
PROGRAM med.VIEW

* Include file definitions
$INCLUDE EQU/MEDICATION.H

* Open files
CALL OPEN.FILES

* Get medication ID
INPUT "Enter Medication ID: ":med.id

* Read the record (note: med.R is the record buffer)
READ med.R FROM med, med.id ELSE
   PRINT "Medication ":med.id:" not found"
   STOP
END

* Display using named fields (note: UPPERCASE field names)
PRINT "Medication Details:"
PRINT "ID: ":med.ID
PRINT "Name: ":med.MEDICATION_NAME
PRINT "Start Date: ":OCONV(med.START.dt, med.START.dt.conv)
PRINT "Cost: ":OCONV(med.COST, med.COST.conv)

END
```

**Key Points**:
- Use `$INCLUDE EQU/MEDICATION.H` (current location)
- Record buffer is `med.R` (uppercase R)
- Field names are UPPERCASE (med.MEDICATION_NAME, not med.medication_name)
- Use `.conv` equates for formatting (once implemented)

### Example 2: TRANSACTION File

#### Schema Index Entry
```csv
FileName,Abbrev,FileNum,FileType,Priority,Description,FieldCount,Status
TRANSACTION,trn,32,DYNAMIC,1,Financial transactions,23,active
```

#### Field Definition (SCHEMA/TRANSACTION.csv)
```csv
FieldName,FieldNum,Type,Description,Required,Indexed,ConversionCode,Format
ID,0,K,Unique transaction ID,Y,Y,,
TRANSACTION.dt,1,D,Transaction date,Y,Y,D4-,R10
AMOUNT,2,N,Transaction amount,Y,Y,MD2,$,R12
PAYEE_ID,3,A,Reference to PAYEE file,Y,Y,,
DESCRIPTION,4,A,Transaction description,Y,N,,
CREATED.dt,20,D,Record creation date,Y,N,D4-,R10
UPDATED.dt,21,D,Last update date,Y,N,D4-,R10
```

#### Generated Include File (INCLUDE/TRANSACTION.H)
```basic
* TRANSACTION field equates
* Auto-generated by BUILD.SCHEMA on 2025-12-03

* File reference equates
EQU TRANSACTION.FILE.NUM TO 32
EQU TRANSACTION.F TO FILES(TRANSACTION.FILE.NUM)
EQU trn.F TO TRANSACTION.F
EQU trn TO trn.F

* Field attribute equates
EQU TRANSACTION.ID.att TO 0
EQU TRANSACTION.TRANSACTION_DATE.att TO 1
EQU TRANSACTION.AMOUNT.att TO 2
EQU TRANSACTION.PAYEE_ID.att TO 3
EQU TRANSACTION.DESCRIPTION.att TO 4

EQU trn.id.att TO TRANSACTION.ID.att
EQU trn.transaction_date.att TO TRANSACTION.TRANSACTION_DATE.att
EQU trn.amount.att TO TRANSACTION.AMOUNT.att
EQU trn.payee_id.att TO TRANSACTION.PAYEE_ID.att
EQU trn.description.att TO TRANSACTION.DESCRIPTION.att

* Field buffer equates
EQU trn.id.b TO trn.rec<TRANSACTION.ID.att>
EQU trn.transaction_date.b TO trn.rec<TRANSACTION.TRANSACTION_DATE.att>
EQU trn.amount.b TO trn.rec<TRANSACTION.AMOUNT.att>
EQU trn.payee_id.b TO trn.rec<TRANSACTION.PAYEE_ID.att>
EQU trn.description.b TO trn.rec<TRANSACTION.DESCRIPTION.att>

EQU trn.id TO trn.id.b
EQU trn.transaction_date TO trn.transaction_date.b
EQU trn.amount TO trn.amount.b
EQU trn.payee_id TO trn.payee_id.b
EQU trn.description TO trn.description.b

* Conversion code equates
EQU trn.transaction_date.conv TO "D2/"
EQU trn.amount.conv TO "MD2,$"
```

---

## Migration Guidelines

### Current State Assessment

**EQU Directory Status**:
- ✅ 43 .h files exist (full format with UPPERCASE and lowercase equates)
- ✅ 40 .equ files exist (simple format with lowercase only)
- ✅ Files use correct `.A` suffix for attributes
- ✅ Files use correct `.R` for record buffer
- ❌ Missing: `.conv` equates for conversion codes
- ❌ Dual format (.h and .equ) creates redundancy

### Phase 1: Enhance Existing Files

**Immediate Actions** (No breaking changes):

1. **Add ConversionCode and Format columns to schema CSVs**
   - Add column 7 (ConversionCode) to SCHEMA/*.csv files → DICT attribute 3
   - Add column 8 (Format) to SCHEMA/*.csv files → DICT attribute 5
   - Populate date fields with: `D4-` (conversion) and `R10` (format)
   - Populate currency fields with: `MD2,$` (conversion) and `R12` (format)
   - Populate numeric fields with: `MD2` or `MD0` (conversion)

2. **Rename date fields to .dt suffix**
   - All date fields must end with `.dt` (e.g., START_DATE → START.dt)
   - Update all 40 SCHEMA/*.csv files
   - Examples: CREATED_DATE → CREATED.dt, TRANSACTION_DATE → TRANSACTION.dt

3. **Update BUILD.SCHEMA program**
   - Read columns 7 and 8 from CSV: `CONV.CODE = FIELD(FLINE, ",", 7)` and `FORMAT.SPEC = FIELD(FLINE, ",", 8)`
   - Remove automatic conversion detection logic (lines 105-179 in current code)
   - DICT structure already correct: `DICT.REC<3> = CONV.CODE` and `DICT.REC<5> = FORMAT.SPEC`
   - Generate `.conv` equates in .h files
   - Generate `.fmt` equates in .h files
   - Stop generating .equ files
   - Keep existing .A and .R equates unchanged

4. **Regenerate .h files**
   - Run BUILD.SCHEMA
   - Verify all DICT entries are type D (not A or S)
   - Review generated files for accuracy
   - Test with existing programs (should work unchanged)

5. **Remove .equ files**
   - Delete all 40 .equ files from EQU/ directory
   - Single .h format simplifies maintenance

### Phase 2: Standardize Programs (Gradual)

**Update programs to use .conv equates**:

```basic
* OLD (hardcoded conversion)
PRINT OCONV(med.START_DATE, "D2/")

* NEW (using .conv equate)
PRINT OCONV(med.START_DATE, med.START_DATE.conv)
```

**Benefits**:
- Conversion codes maintained in schema, not code
- Easy to change date formats globally
- Self-documenting code

### Phase 3: Consolidate Formats (Optional)

**Decision Point**: Keep or remove .equ files?

**Option A: Keep Both**
- .h files for full development
- .equ files for quick scripts
- Maintain both in BUILD.SCHEMA

**Option B: Remove .equ files**
- Single .h format per file
- Simplify maintenance
- Less redundancy

### For New Development

1. **Always start with schema** - Add to SCHEMA_INDEX.csv and create field CSV
2. **Include ConversionCode** in field definitions
3. **Run BUILD.SCHEMA** to generate include files
4. **Use $INCLUDE EQU/<FILENAME>.H** in programs
5. **Use UPPERCASE field names** (med.MEDICATION_NAME)
6. **Use .R for record buffer** (med.R)
7. **Use .conv for formatting** (med.START_DATE.conv)
8. **Never use numeric attributes** in code

### Validation Checklist

- [ ] File exists in SCHEMA_INDEX.csv
- [ ] File has detailed CSV in SCHEMA/
- [ ] Include file exists in INCLUDE/ with .H suffix
- [ ] OPEN.FILES.H includes the file
- [ ] Programs use $INCLUDE directives
- [ ] Code uses named equates (not numbers)
- [ ] Conversion codes defined for date/numeric fields
- [ ] Program names follow <abbrev>.<ACTION> pattern

---

## Questions and Clarifications

### Resolved Questions (Based on Current Implementation)

### Question 1: Record Variable Naming ✅ RESOLVED

**Current implementation**: `med.R<MEDICATION.ID.A>` (uppercase R, uppercase A)  
**Decision**: Keep existing convention
- ✅ Use `med.R` as the record holder variable (uppercase R)
- ✅ Use `.A` suffix for attribute numbers (not .att)
- ✅ Use UPPERCASE field names in equates
- ❌ No `.b` suffix needed (direct buffer access)

**Rationale**: 43 existing .h files already use this pattern

### Question 2: Directory Location ✅ RESOLVED

**Current**: Include files in `EQU/` directory (43 .h + 40 .equ files)  
**Decision**: Keep EQU/ directory
- ✅ Continue using EQU/ directory
- ✅ Standardize existing files rather than migrate
- ❌ No need to create INCLUDE/ directory

**Rationale**: 83 existing files, programs already use EQU/

### Question 3: Conversion Codes ⚠️ PENDING DECISION

**Implementation needed**: Add `.conv` equates to existing .h files

**Source Options**:
1. **SCHEMA CSV (Recommended)**: Add ConversionCode column to SCHEMA/*.csv
   - Pro: Single source of truth
   - Pro: Easy to maintain and change
   - Con: Requires updating 40 CSV files

2. **Dictionary File**: Read from DICT attribute 3
   - Pro: Uses existing data
   - Pro: No CSV changes needed
   - Con: Requires DICT to exist first
   - Con: Less maintainable

**Questions for user**:
- Add ConversionCode column to SCHEMA/*.csv files?
- What conversion codes for each field type?
  - Dates: D2/ (MM/DD/YY), D4/ (MM/DD/YYYY), D4- (YYYY-MM-DD)?
  - Currency: MD2,$ or MD2,$?
  - Other numeric: MD2, MD0, etc.?

### Question 4: OPEN.FILES Format ⚠️ PENDING DECISION

**Current**: `OPEN.FILES` subroutine (67 lines) that:
- Reads SCHEMA_INDEX.csv dynamically
- Opens all active files
- Reports failures
- Uses COMMON /FILES/ FILES(100)

**Proposed**: `OPEN.FILES.H` include file with static OPEN statements

**Trade-offs**:

| Aspect | Subroutine (Current) | Include File (Proposed) |
|--------|----------------------|-------------------------|
| Maintenance | Updates automatically | Requires regeneration |
| Performance | CSV read overhead | Inline, faster |
| Flexibility | Dynamic, configurable | Static, compiled |
| Error handling | Detailed reporting | Simple ELSE STOP |
| Preferred use | One-time opens | Multiple programs |

**Questions for user**:
- Replace CALL OPEN.FILES with $INCLUDE EQU/OPEN.FILES.H?
- Keep both options available?
- Prefer dynamic (current) or static (proposed)?

---

## Suggestions for Improvement

### 1. Schema Validation Program

Create `SCHEMA.VALIDATE` program to check:
- All files in SCHEMA_INDEX have detail CSVs
- Field numbers are sequential and unique
- File numbers are unique
- Required fields are present
- Conversion codes are valid

### 2. Automated Include Generation

Enhance `BUILD.SCHEMA` to:
- Generate INCLUDE/ files (not EQU/)
- Follow exact template format
- Generate OPEN.FILES.H automatically
- Add generation timestamp and source reference
- Validate before generating

### 3. Code Migration Tool

Create `MIGRATE.NAMING` program to:
- Scan existing programs
- Identify numeric attribute references
- Suggest named equate replacements
- Generate before/after reports

### 4. Naming Convention Checker

Create `CHECK.NAMING` utility to:
- Verify program names follow pattern
- Check for correct include usage
- Identify numeric attributes in code
- Report violations

### 5. Documentation Generator

Enhance schema system to generate:
- Data dictionary documentation
- Field reference guides
- Program usage documentation
- API documentation

---

## Implementation Priority

### Phase 1: Enhance Existing (High Priority)
1. ✅ Create this NAMING.RULES.MD document
2. ❌ Add ConversionCode column to SCHEMA/*.csv files (40 files)
3. ❌ Update BUILD.SCHEMA to generate .conv equates
4. ❌ Regenerate EQU/*.h files with .conv equates
5. ⚠️ Decision: OPEN.FILES subroutine vs OPEN.FILES.H include?

### Phase 2: Test and Validate (High Priority)
6. Test .conv equates in sample programs
7. Verify existing programs still work
8. Document conversion code standards
9. Update HAL_SYSTEM_MASTER.MD reference

### Phase 3: Program Updates (Medium Priority)
10. Update programs to use .conv equates
11. Replace hardcoded conversions with equated conversions
12. Standardize program naming (ensure <abbrev>.<ACTION> pattern)
13. Update all programs to use UPPERCASE field names consistently

### Phase 4: Cleanup (Medium Priority)
14. Decide: Keep or remove .equ files?
15. If removing: Update BUILD.SCHEMA, remove .equ generation
16. If keeping: Document when to use .h vs .equ
17. Clean up any inconsistent patterns

### Phase 5: Tooling (Low Priority)
18. Create SCHEMA.VALIDATE program
19. Create CHECK.NAMING utility
20. Create MIGRATE.NAMING tool
21. Establish automated checks

---

## Approval and Next Steps

**Status**: DRAFT - Awaiting User Approval

**User Decisions - APPROVED**:

1. **Conversion Codes**: ✅ APPROVED
   - Add ConversionCode column (column 7) to all SCHEMA/*.csv files
   - Add Format column (column 8) to all SCHEMA/*.csv files
   - **Date fields**: Use `D4-` conversion (YYYY-MM-DD format)
   - **Date fields**: Use `R10` format (right-justified, 10 characters)
   - **Date field names**: Must end with `.dt` suffix
   - **Currency**: Use `MD2,$` conversion
   - **Numeric**: Use `MD2` for decimals, `MD0` for integers

2. **OPEN.FILES Format**: ✅ APPROVED
   - Keep and enhance OPEN.FILES subroutine (dynamic)
   - Read files from SCHEMA/SCHEMA_INDEX.csv
   - Open only files with **PRIORITY=1**
   - No static include file needed

3. **Dual Format Files**: ✅ APPROVED
   - **Remove .equ files** (40 files to be deleted)
   - **Keep only .h files** (43 files, one per entity)
   - Update BUILD.SCHEMA to stop generating .equ files
   - Single format simplifies maintenance

4. **Variable Naming Conventions**: ✅ DOCUMENTED
   - **UPPERCASE**: EQU statements, constants, system variables
   - **lowercase**: Runtime variables, loop counters, temporary values
   - **Mixed**: Field access (med.MEDICATION_NAME uses equate → UPPERCASE)
   - **Consistency** is key in case-insensitive QM Basic

**Implementation Steps**:

### Phase 0: Backup (CRITICAL - Do First!)
0a. ⏳ Backup all affected files before making ANY changes
0b. ⏳ Commit backup to GitHub with tag: `backup-before-naming-rules-2025-12-03`
0c. ⏳ Verify backup is pushed to remote

### Phase 1: Documentation
1. ✅ Create NAMING.RULES.MD document
2. ✅ Document approved decisions with correct format specs (JLength)
3. ⏳ Update HAL_SYSTEM_MASTER.MD to reference this document

### Phase 2: Schema Updates
4. ⏳ Add ConversionCode (column 7 → DICT attr 3) to all 40 SCHEMA/*.csv files
5. ⏳ Add Format (column 8 → DICT attr 5) to all 40 SCHEMA/*.csv files
6. ⏳ Rename all date fields to end with `.dt` suffix in all schemas
7. ⏳ Populate date fields: `D4-` conversion, `R10` format
8. ⏳ Populate currency fields: `MD2,$` conversion, `R12` format
9. ⏳ Populate text fields with appropriate format (L30, L50, T100, etc.)

### Phase 3: Code Updates
10. ⏳ Update BUILD.SCHEMA program to:
   - Read column 7: `CONV.CODE = FIELD(FLINE, ",", 7)`
   - Read column 8: `FORMAT.SPEC = FIELD(FLINE, ",", 8)` (JLength format)
   - Remove automatic conversion detection logic (lines 105-179)
   - Generate DICT entries: `<3> = CONV.CODE`, `<5> = FORMAT.SPEC`
   - Generate .conv equates in .h files
   - Generate .fmt equates in .h files
   - Stop generating .equ files
11. ⏳ Update OPEN.FILES subroutine to filter by PRIORITY=1

### Phase 4: Generation and Testing
12. ⏳ Regenerate all 43 EQU/*.h files with new equates
13. ⏳ Verify all DICT entries are type D (not A or S)
14. ⏳ Test with existing programs
15. ⏳ Delete 40 .equ files from EQU/ directory
16. ⏳ Update programs to use .conv and .fmt equates

### Phase 5: Commit
17. ⏳ Commit all changes to GitHub
18. ⏳ Create tag: `naming-rules-implemented-2025-12-03`

---

## References

- **HAL_SYSTEM_MASTER.MD** - System architecture overview
- **DOCUMENTATION_MAINTENANCE.MD** - Documentation rules
- **SCHEMA/SCHEMA_INDEX.csv** - File registry
- **BP/BUILD.SCHEMA** - Schema generation program
- **BP/OPEN.FILES** - Current file opening subroutine

---

**Document Status**: DRAFT  
**Author**: AI Agent following user specifications  
**Reviewers**: User (primary), Development team  
**Last Updated**: 2025-12-03  
**Next Review**: After user approval

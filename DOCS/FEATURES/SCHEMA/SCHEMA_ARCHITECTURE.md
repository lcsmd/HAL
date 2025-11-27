# HAL Schema-Driven Datastore Architecture

## Overview

The HAL datastore is a **schema-driven architecture** where CSV files serve as the **single source of truth** for all data structures. This approach enables dynamic, extensible data management without interruption to existing operations.

## Core Principles

1. **CSV as Source of Truth** - All data structure definitions exist in intelligently designed CSV files
2. **Automated Generation** - Code builds files, dictionaries, and equates from CSV schemas
3. **Human/AI Collaboration** - Schemas are conceived through combined human and AI intelligence
4. **Dynamic Extensibility** - New domains, files, or fields can be added without interruption
5. **Consistent Naming** - Standardized conventions for domains, files, and fields

## Architecture Layers

```
┌─────────────────────────────────────────────────────────┐
│                    CSV SCHEMAS                          │
│  (Single Source of Truth - Human/AI Designed)          │
├─────────────────────────────────────────────────────────┤
│  DOMAINS.CSV → Domain definitions                       │
│  SCHEMA_INDEX.csv → File registry                       │
│  [FILENAME].csv → Field definitions per file            │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│              BUILD.SCHEMA PROGRAM                       │
│  (Reads CSV, Generates All Structures)                  │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│              GENERATED ARTIFACTS                        │
├─────────────────────────────────────────────────────────┤
│  • QM Data Files (DYNAMIC/STATIC)                       │
│  • Dictionary Entries (Type D)                          │
│  • Equate Files (EQU/[abb].equ)                        │
│  • Master Include (EQU/FILES.EQU)                       │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│              APPLICATION PROGRAMS                       │
│  (CRUD Operations, Business Logic)                      │
└─────────────────────────────────────────────────────────┘
```

## Schema Hierarchy

### 1. Domains (DOMAINS_ENHANCED.csv)

Domains are top-level organizational categories that group related files.

**Structure:**
```csv
DomainAbb,DomainName,DomainNum,Description,Tags,Files,Priority,Status
fin,Finance,1,Financial matters...,money|banking,ACCOUNT|TRANSACTION,1,active
med,Medical,2,Health and medical...,health|clinical,MEDICATION|DOCTOR,1,active
```

**Fields:**
- `DomainAbb` - 3-character abbreviation (fin, med, per, sys, sec, etc.)
- `DomainName` - Full domain name
- `DomainNum` - Unique numeric identifier
- `Description` - Domain purpose and scope
- `Tags` - Pipe-separated tags for classification
- `Files` - Pipe-separated list of files in domain
- `Priority` - 1=high, 2=medium, 3=low
- `Status` - active/inactive

**Current Domains:**
- **fin** - Finance (accounts, transactions, investments)
- **med** - Medical (medications, doctors, appointments)
- **sch** - School (education, courses, degrees)
- **wor** - Work (jobs, companies, projects, skills)
- **per** - Personal (people, places, events, relationships)
- **new** - News (media, content, subscriptions)
- **sys** - System (sessions, logs, integrations)
- **sec** - Security (passwords, credentials)
- **com** - Communication (email, messages)
- **doc** - Documents (files, attachments)
- **ai** - AI (models, personas, prompts, memories)

### 2. Files (SCHEMA_INDEX.csv)

Files are the primary data containers within domains.

**Structure:**
```csv
FileName,Abbrev,FileNum,FileType,Priority,Description,FieldCount,Status
PERSON,per,1,DYNAMIC,1,People and contacts,26,active
MEDICATION,med,20,DYNAMIC,1,Medications and prescriptions,28,active
```

**Fields:**
- `FileName` - Full file name (uppercase)
- `Abbrev` - 3-character abbreviation (lowercase)
- `FileNum` - Unique numeric identifier (1-999)
- `FileType` - DYNAMIC (hash) or STATIC (sequential)
- `Priority` - 1=high, 2=medium, 3=low
- `Description` - File purpose
- `FieldCount` - Number of fields defined
- `Status` - active/inactive

### 3. Fields (Individual CSV per file)

Each file has a detailed CSV defining all its fields.

**Structure (e.g., PERSON.csv):**
```csv
FieldName,FieldNum,Type,Description,Required,Indexed
ID,0,K,Unique person identifier,Y,Y
FIRST_NAME,1,A,First name,Y,N
BIRTHDATE,4,D,Date of birth,N,N
TAGS,14,M,Tags for categorization (multivalued),N,N
```

**Fields:**
- `FieldName` - Field name (uppercase with underscores)
- `FieldNum` - Field position (0-based)
- `Type` - Field type (see below)
- `Description` - Field purpose
- `Required` - Y/N (validation flag)
- `Indexed` - Y/N (create secondary index)

**Field Types:**
- **K** - Key field (unique identifier)
- **A** - Alphanumeric (text, single-valued)
- **N** - Numeric (integers, decimals)
- **D** - Date (stored as internal date)
- **T** - Text (long text, notes)
- **M** - Multivalued (array of values)

## Naming Conventions

### Domain Abbreviations
- 3 characters, lowercase
- Mnemonic and intuitive
- Examples: fin, med, per, sys, sec

### File Abbreviations
- 3 characters, lowercase
- Unique across all domains
- Examples: per, med, pwd, mst, evt

### Field Names
- Uppercase with underscores
- Descriptive and clear
- Examples: FIRST_NAME, BIRTHDATE, MEDICATION_NAME

### Equate Files
- Location: `EQU/` directory
- Format: `[fileabb].equ` (lowercase)
- Examples: `EQU/per.equ`, `EQU/med.equ`

### Meaningful Field References
Fields are accessed using meaningful equates:
```basic
per.r<per.FIRST_NAME>     ' PERSON file, FIRST_NAME field
med.r<med.DOSAGE>         ' MEDICATION file, DOSAGE field
pwd.r<pwd.ENCRYPTED_PWD>  ' PASSWORD file, ENCRYPTED_PWD field
```

## Generated Artifacts

### 1. QM Data Files

Created using `CREATE.FILE` command based on `FileType`:
```basic
CREATE.FILE PERSON DYNAMIC
CREATE.FILE LOG STATIC
```

### 2. Dictionary Entries (Type D)

All dictionary entries are Type D (data definition):

**Structure:**
```
Field 1: "D" (type)
Field 2: Field number
Field 3: Conversion code (D4-, MD2, etc.)
Field 4: Description
Field 5: Format specification (10R, 30L, etc.)
Field 6: S/M flag (single/multivalued)
Field 7: (reserved)
Field 8: X for indexed fields
```

**Intelligent Formatting:**
- Date fields: `D4-` conversion, `10R` format
- Currency: `MD2` conversion, `12R` format
- Counts: `MR0` conversion, `8R` format
- Names: `30L` format
- Emails: `35L` format
- URLs: `40L` format

### 3. Equate Files

Each file gets an equate file with field position constants:

**Example (EQU/per.equ):**
```basic
* PERSON field equates
* Auto-generated by BUILD.SCHEMA
* File handle: FILES(1)

EQU per TO FILES(1)

EQU per.ID TO per.r<0>
EQU per.FIRST_NAME TO per.r<1>
EQU per.LAST_NAME TO per.r<2>
EQU per.BIRTHDATE TO per.r<4>
```

### 4. Master Include File

**EQU/FILES.EQU** includes all file equates:
```basic
* Master file equates
* Auto-generated by BUILD.SCHEMA

COMMON FILES(50)

$INCLUDE EQU per.equ
$INCLUDE EQU med.equ
$INCLUDE EQU pwd.equ
```

## Build Process

### 1. Design Schema (Human/AI)

Create or update CSV files:
- Add domain to `DOMAINS_ENHANCED.csv`
- Add file to `SCHEMA_INDEX.csv`
- Create `[FILENAME].csv` with field definitions

### 2. Validate Schema

```
qm -kHAL
SCHEMA.MANAGER
> 5. Validate Schema Files
```

Checks for:
- Duplicate file numbers
- Duplicate abbreviations
- Missing schema files
- Duplicate field numbers/names
- Invalid field types

### 3. Build Schema

```
qm -kHAL
SCHEMA.MANAGER
> 6. Build Schema
```

Or directly:
```
qm -kHAL -c"BUILD.SCHEMA"
```

This creates:
- QM data files
- Dictionary entries (Type D)
- Equate files
- Master FILES.EQU

### 4. Build Indexes (Optional)

```
qm -kHAL
SCHEMA.MANAGER
> 7. Build Indexes
```

Or directly:
```
qm -kHAL -c"BUILD.INDEX PERSON ALL"
qm -kHAL -c"BUILD.INDEX MEDICATION PERSON_ID"
```

## CRUD Operations

### Standard Pattern

All programs follow this pattern:

```basic
PROGRAM EXAMPLE.PROGRAM
$INCLUDE EQU/FILES.EQU

* Open files (automatic via COMMON FILES)

* CREATE
ID = SYSTEM(9)
per.r<per.FIRST_NAME> = "John"
per.r<per.LAST_NAME> = "Smith"
per.r<per.CREATED_DATE> = DATE()
WRITE per.r ON per, ID

* READ
READ per.r FROM per, ID ELSE
   CRT "Not found"
   STOP
END

* UPDATE
per.r<per.EMAIL> = "john@example.com"
per.r<per.UPDATED_DATE> = DATE()
WRITE per.r ON per, ID

* DELETE
DELETE per, ID

* LIST
SELECT per
LOOP
   READNEXT ID ELSE EXIT
   READ per.r FROM per, ID THEN
      CRT per.r<per.FIRST_NAME>:" ":per.r<per.LAST_NAME>
   END
REPEAT

RETURN
END
```

### CRUD Template

Use `BP/CRUD.TEMPLATE` as a starting point for new programs.

## Dynamic Schema Updates

### Adding a New Domain

1. Edit `DOMAINS_ENHANCED.csv`:
```csv
new,NewDomain,12,Description,tags,FILES,1,active
```

2. No rebuild needed unless adding files

### Adding a New File

1. Edit `SCHEMA_INDEX.csv`:
```csv
NEWFILE,nwf,32,DYNAMIC,1,Description,10,active
```

2. Create `SCHEMA/NEWFILE.csv`:
```csv
FieldName,FieldNum,Type,Description,Required,Indexed
ID,0,K,Unique identifier,Y,Y
NAME,1,A,Name,Y,Y
```

3. Run `BUILD.SCHEMA`

### Adding Fields to Existing File

1. Edit `SCHEMA/[FILENAME].csv`:
```csv
NEW_FIELD,26,A,New field description,N,N
```

2. Run `BUILD.SCHEMA` (regenerates dictionary and equates)

3. Existing records automatically have empty values for new fields

### No Interruption

- Existing data is preserved
- New fields appear as empty in old records
- Programs using old equates continue to work
- Recompile programs to use new fields

## Schema Management Tools

### SCHEMA.MANAGER

Interactive menu system:
```
qm -kHAL -c"SCHEMA.MANAGER"
```

**Features:**
1. View Schema Summary
2. List Domains
3. List Files by Domain
4. View File Schema
5. Validate Schema Files
6. Build Schema
7. Build Indexes
8. Add New Domain
9. Add New File
10. Add Field to File
11. Export Schema Documentation

### Command Line Tools

```bash
# Build entire schema
qm -kHAL -c"BUILD.SCHEMA"

# Build all indexes for a file
qm -kHAL -c"BUILD.INDEX PERSON ALL"

# Build specific index
qm -kHAL -c"BUILD.INDEX MEDICATION PERSON_ID"
```

## Best Practices

### Schema Design

1. **Plan Domain Structure** - Group related files logically
2. **Use Meaningful Names** - Clear, descriptive field names
3. **Index Judiciously** - Only index fields used in searches
4. **Document Thoroughly** - Use description fields
5. **Version Control** - Keep CSV files in git

### Field Types

1. **Use K for Keys** - Always field 0
2. **Use D for Dates** - Automatic formatting
3. **Use N for Numbers** - Proper alignment
4. **Use M for Arrays** - Multivalued data
5. **Use T for Long Text** - Notes, descriptions

### Equate Usage

1. **Always Include FILES.EQU** - Gets all file handles
2. **Use Meaningful Names** - `per.FIRST_NAME` not `per.r<1>`
3. **Never Hardcode Numbers** - Always use equates
4. **Consistent Naming** - Follow conventions

### CRUD Operations

1. **Set System Fields** - CREATED_DATE, UPDATED_DATE, ACTIVE
2. **Validate Input** - Check required fields
3. **Handle Errors** - Use ELSE clauses
4. **Use Transactions** - For multi-file updates
5. **Log Changes** - Audit trail

## File Organization

```
c:\QMSYS\HAL\
├── SCHEMA/                    # CSV schema files
│   ├── DOMAINS_ENHANCED.csv   # Domain definitions
│   ├── SCHEMA_INDEX.csv       # File registry
│   ├── PERSON.csv             # Field definitions
│   ├── MEDICATION.csv
│   └── ...
├── EQU/                       # Generated equate files
│   ├── FILES.EQU              # Master include
│   ├── per.equ                # PERSON equates
│   ├── med.equ                # MEDICATION equates
│   └── ...
├── BP/                        # QMBasic programs
│   ├── BUILD.SCHEMA           # Schema builder
│   ├── BUILD.INDEX            # Index builder
│   ├── SCHEMA.MANAGER         # Schema management
│   ├── CRUD.TEMPLATE          # CRUD template
│   └── ...
├── PERSON/                    # Data files
├── MEDICATION/
└── ...
```

## Examples

### Example 1: Create Person Record

```basic
PROGRAM CREATE.PERSON
$INCLUDE EQU/FILES.EQU

ID = SYSTEM(9)
per.r<per.ID> = ID
per.r<per.FIRST_NAME> = "John"
per.r<per.LAST_NAME> = "Smith"
per.r<per.EMAIL> = "john@example.com"
per.r<per.BIRTHDATE> = ICONV("1990-01-15", "D4-")
per.r<per.CREATED_DATE> = DATE()
per.r<per.UPDATED_DATE> = DATE()
per.r<per.ACTIVE> = "Y"

WRITE per.r ON per, ID ELSE
   CRT "Error creating person"
   STOP
END

CRT "Person created: ":ID
RETURN
END
```

### Example 2: Search Medications

```basic
PROGRAM SEARCH.MEDICATIONS
$INCLUDE EQU/FILES.EQU

INPUT PERSON.ID, "Enter person ID: "

SELECT med WITH med.PERSON_ID = PERSON.ID
LOOP
   READNEXT ID ELSE EXIT
   READ med.r FROM med, ID THEN
      CRT med.r<med.MEDICATION_NAME>:" - ":med.r<med.DOSAGE>:" ":med.r<med.DOSAGE_UNIT>
   END
REPEAT

RETURN
END
```

### Example 3: Update Password

```basic
PROGRAM UPDATE.PASSWORD
$INCLUDE EQU/FILES.EQU

INPUT PWD.ID, "Enter password ID: "

READ pwd.r FROM pwd, PWD.ID ELSE
   CRT "Password not found"
   STOP
END

pwd.r<pwd.LAST_USED_DATE> = DATE()
pwd.r<pwd.USE_COUNT> += 1
pwd.r<pwd.UPDATED_DATE> = DATE()

WRITE pwd.r ON pwd, PWD.ID ELSE
   CRT "Error updating password"
   STOP
END

CRT "Password updated"
RETURN
END
```

## Troubleshooting

### Schema Validation Errors

**Duplicate FileNum:**
- Each file must have unique FileNum in SCHEMA_INDEX.csv
- Check for conflicts and reassign

**Duplicate Abbrev:**
- Each file must have unique 3-char abbreviation
- Choose different abbreviation

**Missing Schema File:**
- Create [FILENAME].csv in SCHEMA directory
- Include all field definitions

**Invalid Field Type:**
- Must be K, A, N, D, T, or M
- Check field type in CSV

### Build Errors

**Cannot Open File:**
- Check file permissions
- Verify SCHEMA directory exists
- Ensure CSV files are not locked

**Dictionary Write Error:**
- File may be in use
- Close all QM sessions
- Retry build

**Equate File Error:**
- Check EQU directory exists
- Verify write permissions
- Check disk space

### Runtime Errors

**Variable Not Found:**
- Ensure $INCLUDE EQU/FILES.EQU is present
- Recompile program after schema changes
- Check equate file exists

**File Not Open:**
- COMMON FILES(50) must be declared
- File must exist (run BUILD.SCHEMA)
- Check file name spelling

## Future Enhancements

1. **Schema Versioning** - Track schema changes over time
2. **Migration Tools** - Automated data migration between schema versions
3. **Schema Export/Import** - Share schemas between systems
4. **Visual Schema Designer** - GUI for schema design
5. **Automated Testing** - Validate data against schema rules
6. **Schema Documentation Generator** - Auto-generate technical docs
7. **Field-Level Security** - Access control per field
8. **Data Validation Rules** - Enforce business rules in schema

## Conclusion

The HAL schema-driven architecture provides:

- **Single Source of Truth** - CSV files define everything
- **Automation** - Code generates all structures
- **Flexibility** - Easy to extend and modify
- **Consistency** - Standardized patterns throughout
- **Maintainability** - Clear organization and documentation
- **Scalability** - Supports growth without redesign

This architecture enables rapid development, easy maintenance, and seamless evolution of the HAL datastore.

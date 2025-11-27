# HAL Schema-Driven Datastore System

## Overview

The HAL datastore uses **CSV files as the single source of truth** for all data structures. This schema-driven architecture enables dynamic, extensible data management through human/AI collaboration.

## Quick Start

### View Schema
```bash
qm -kHAL -c"SCHEMA.MANAGER"
> 1. View Schema Summary
```

### Add New File
```bash
qm -kHAL -c"SCHEMA.MANAGER"
> 9. Add New File
```

### Build Schema
```bash
qm -kHAL -c"BUILD.SCHEMA"
```

### Use in Program
```basic
PROGRAM MY.PROGRAM
$INCLUDE EQU/FILES.EQU

per.r<per.FIRST_NAME> = "John"
WRITE per.r ON per, ID

RETURN
END
```

## Architecture

```
CSV Schemas (Source of Truth)
    ↓
BUILD.SCHEMA (Generator)
    ↓
QM Files + Dictionaries + Equates
    ↓
Application Programs (CRUD)
```

## Schema Files

### DOMAINS_ENHANCED.csv
Top-level organizational categories:
```csv
DomainAbb,DomainName,DomainNum,Description,Tags,Files,Priority,Status
fin,Finance,1,Financial matters...,money|banking,ACCOUNT|TRANSACTION,1,active
med,Medical,2,Health and medical...,health|clinical,MEDICATION|DOCTOR,1,active
```

### SCHEMA_INDEX.csv
File registry:
```csv
FileName,Abbrev,FileNum,FileType,Priority,Description,FieldCount,Status
PERSON,per,1,DYNAMIC,1,People and contacts,26,active
MEDICATION,med,20,DYNAMIC,1,Medications and prescriptions,28,active
```

### [FILENAME].csv
Field definitions per file:
```csv
FieldName,FieldNum,Type,Description,Required,Indexed
ID,0,K,Unique identifier,Y,Y
FIRST_NAME,1,A,First name,Y,N
BIRTHDATE,4,D,Date of birth,N,N
```

## Field Types

| Type | Description | Example | Format |
|------|-------------|---------|--------|
| K | Key (unique ID) | ID | 15L |
| A | Alphanumeric | NAME, EMAIL | 20L-40L |
| N | Numeric | COUNT, COST | 10R, MD2 |
| D | Date | BIRTHDATE | D4-, 10R |
| T | Text (long) | NOTES | 50L |
| M | Multivalued | TAGS | varies |

## Programs

### Schema Management
- **SCHEMA.MANAGER** - Interactive menu system
- **BUILD.SCHEMA** - Generate files/dicts/equates from CSV
- **BUILD.INDEX** - Create secondary indexes
- **SCHEMA.VALIDATE** - Validate schema consistency

### Schema Operations
- **SCHEMA.SUMMARY** - Display statistics
- **SCHEMA.LIST.DOMAINS** - List all domains
- **SCHEMA.LIST.FILES** - List all files
- **SCHEMA.VIEW.FILE** - View file schema details
- **SCHEMA.ADD.DOMAIN** - Add new domain
- **SCHEMA.ADD.FILE** - Add new file
- **SCHEMA.ADD.FIELD** - Add field to file
- **SCHEMA.EXPORT.DOCS** - Export markdown documentation

### Templates
- **CRUD.TEMPLATE** - Standard CRUD operations pattern

## Naming Conventions

### Domains
- 3 characters, lowercase
- Examples: `fin`, `med`, `per`, `sys`, `sec`

### Files
- 3 characters, lowercase
- Examples: `per`, `med`, `pwd`, `mst`, `evt`

### Fields
- Uppercase with underscores
- Examples: `FIRST_NAME`, `BIRTHDATE`, `MEDICATION_NAME`

### Equates
- Format: `fileabb.FIELDNAME`
- Examples: `per.FIRST_NAME`, `med.DOSAGE`
- Files: `EQU/[fileabb].equ`

## Workflow

### 1. Design Schema (Human/AI)
Edit CSV files in `SCHEMA/` directory

### 2. Validate
```bash
qm -kHAL -c"SCHEMA.MANAGER"
> 5. Validate Schema Files
```

### 3. Build
```bash
qm -kHAL -c"BUILD.SCHEMA"
```

### 4. Create Indexes (Optional)
```bash
qm -kHAL -c"BUILD.INDEX PERSON ALL"
```

### 5. Write Programs
```basic
PROGRAM EXAMPLE
$INCLUDE EQU/FILES.EQU

* CRUD operations using meaningful field names
per.r<per.FIRST_NAME> = "John"
WRITE per.r ON per, ID

RETURN
END
```

## Generated Artifacts

### 1. QM Data Files
Created via `CREATE.FILE` command

### 2. Dictionary Entries (Type D)
- Field 2: Field number
- Field 3: Conversion code (D4-, MD2, etc.)
- Field 4: Description
- Field 5: Format (10R, 30L, etc.)
- Field 6: S/M flag (single/multivalued)
- Field 8: X for indexed fields

### 3. Equate Files
`EQU/[abb].equ` with field position constants:
```basic
EQU per TO FILES(1)
EQU per.FIRST_NAME TO per.r<1>
EQU per.LAST_NAME TO per.r<2>
```

### 4. Master Include
`EQU/FILES.EQU` includes all file equates:
```basic
COMMON FILES(50)
$INCLUDE EQU per.equ
$INCLUDE EQU med.equ
```

## CRUD Pattern

```basic
PROGRAM EXAMPLE
$INCLUDE EQU/FILES.EQU

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

## Dynamic Updates

### Add New Domain
1. Edit `DOMAINS_ENHANCED.csv`
2. No rebuild needed unless adding files

### Add New File
1. Edit `SCHEMA_INDEX.csv`
2. Create `SCHEMA/[FILENAME].csv`
3. Run `BUILD.SCHEMA`

### Add Field to Existing File
1. Edit `SCHEMA/[FILENAME].csv`
2. Run `BUILD.SCHEMA`
3. Recompile programs using new field

**No interruption to existing data!**

## Current Domains

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

## File Organization

```
c:\QMSYS\HAL\
├── SCHEMA/                    # CSV schemas (source of truth)
│   ├── DOMAINS_ENHANCED.csv
│   ├── SCHEMA_INDEX.csv
│   ├── PERSON.csv
│   └── ...
├── EQU/                       # Generated equates
│   ├── FILES.EQU
│   ├── per.equ
│   └── ...
├── BP/                        # QMBasic programs
│   ├── BUILD.SCHEMA
│   ├── SCHEMA.MANAGER
│   ├── CRUD.TEMPLATE
│   └── ...
├── DOCS/                      # Documentation
│   ├── SCHEMA_ARCHITECTURE.md
│   ├── SCHEMA_QUICK_START.md
│   └── SCHEMA_EXPORT.md
└── [FILENAME]/                # Data files
```

## Best Practices

### Schema Design
1. Plan domain structure logically
2. Use meaningful, descriptive names
3. Index only fields used in searches
4. Document thoroughly
5. Version control CSV files

### Field Types
1. Use K for keys (always field 0)
2. Use D for dates (automatic formatting)
3. Use N for numbers (proper alignment)
4. Use M for arrays (multivalued data)
5. Use T for long text (notes, descriptions)

### Programming
1. Always include `$INCLUDE EQU/FILES.EQU`
2. Use meaningful equate names, not numbers
3. Set system fields (CREATED_DATE, UPDATED_DATE, ACTIVE)
4. Validate input and handle errors
5. Log changes for audit trail

## Documentation

- **SCHEMA_ARCHITECTURE.md** - Complete architecture guide
- **SCHEMA_QUICK_START.md** - 5-minute quick start
- **SCHEMA_EXPORT.md** - Auto-generated schema reference
- **README_SCHEMA_SYSTEM.md** - This file

## Commands Reference

```bash
# Interactive menu
qm -kHAL -c"SCHEMA.MANAGER"

# Build entire schema
qm -kHAL -c"BUILD.SCHEMA"

# Build indexes
qm -kHAL -c"BUILD.INDEX [filename] ALL"
qm -kHAL -c"BUILD.INDEX [filename] [fieldname]"

# Query data
qm -kHAL
LIST [filename]
LIST [filename] WITH [field] = "value"
```

## Examples

See `BP/CRUD.TEMPLATE` for complete CRUD examples.

See `DOCS/SCHEMA_ARCHITECTURE.md` for detailed examples.

## Support

- QM Help: `c:\QMSYS\HAL\QM_HELP\`
- Schema Files: `c:\QMSYS\HAL\SCHEMA\`
- Programs: `c:\QMSYS\HAL\BP\`
- Documentation: `c:\QMSYS\HAL\DOCS\`

## Philosophy

**CSV schemas are the single source of truth.**

All structure generation is automated. Human/AI collaboration designs schemas. Code builds structure, other programs populate data. Dynamic and extensible without interruption.

This is the HAL way.

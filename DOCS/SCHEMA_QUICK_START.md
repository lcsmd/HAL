# HAL Schema Quick Start Guide

## 5-Minute Quick Start

### 1. View Current Schema

```bash
qm -kHAL
SCHEMA.MANAGER
> 1. View Schema Summary
```

### 2. Add a New File

**Step 1: Update SCHEMA_INDEX.csv**

Add line to `c:\QMSYS\HAL\SCHEMA\SCHEMA_INDEX.csv`:
```csv
CONTACT,con,33,DYNAMIC,1,Contact information,15,active
```

**Step 2: Create Field Definition**

Create `c:\QMSYS\HAL\SCHEMA\CONTACT.csv`:
```csv
FieldName,FieldNum,Type,Description,Required,Indexed
ID,0,K,Unique contact ID,Y,Y
PERSON_ID,1,A,Reference to PERSON,Y,Y
CONTACT_TYPE,2,A,Type (phone/email/address),Y,Y
CONTACT_VALUE,3,A,Contact value,Y,N
LABEL,4,A,Label (home/work/mobile),N,N
PREFERRED,5,A,Preferred contact (Y/N),N,N
VERIFIED,6,A,Verified (Y/N),N,N
VERIFIED_DATE,7,D,Verification date,N,N
NOTES,8,T,Notes,N,N
TAGS,9,M,Tags (multivalued),N,N
ACTIVE,10,A,Active status (Y/N),Y,Y
CREATED_DATE,11,D,Created date,Y,N
UPDATED_DATE,12,D,Updated date,Y,N
CREATED_BY,13,A,Created by user,N,N
UPDATED_BY,14,A,Updated by user,N,N
```

**Step 3: Validate**

```bash
qm -kHAL
SCHEMA.MANAGER
> 5. Validate Schema Files
```

**Step 4: Build**

```bash
qm -kHAL
SCHEMA.MANAGER
> 6. Build Schema
```

**Step 5: Use in Program**

```basic
PROGRAM TEST.CONTACT
$INCLUDE EQU/FILES.EQU

* Create contact
ID = SYSTEM(9)
con.r<con.PERSON_ID> = "P001"
con.r<con.CONTACT_TYPE> = "email"
con.r<con.CONTACT_VALUE> = "john@example.com"
con.r<con.LABEL> = "work"
con.r<con.PREFERRED> = "Y"
con.r<con.ACTIVE> = "Y"
con.r<con.CREATED_DATE> = DATE()
con.r<con.UPDATED_DATE> = DATE()

WRITE con.r ON con, ID

CRT "Contact created: ":ID

RETURN
END
```

## Common Tasks

### Add Field to Existing File

1. Edit `SCHEMA/[FILENAME].csv`
2. Add new field at end:
```csv
NEW_FIELD,26,A,Description,N,N
```
3. Run `BUILD.SCHEMA`
4. Recompile programs that need new field

### Create Index

```bash
qm -kHAL -c"BUILD.INDEX CONTACT PERSON_ID"
```

Or build all indexes:
```bash
qm -kHAL -c"BUILD.INDEX CONTACT ALL"
```

### Query Data

```bash
qm -kHAL
LIST CONTACT WITH PERSON_ID = "P001"
LIST CONTACT WITH CONTACT_TYPE = "email"
```

### CRUD Operations

Use `BP/CRUD.TEMPLATE` as starting point:

1. Copy template:
```bash
qm -kHAL
COPY BP CRUD.TEMPLATE CONTACT.MANAGER
```

2. Edit `BP/CONTACT.MANAGER`
3. Replace `per` with `con`
4. Replace field names
5. Compile and catalog:
```bash
qm -kHAL
BASIC BP CONTACT.MANAGER
CATALOG BP CONTACT.MANAGER
```

6. Run:
```bash
qm -kHAL -c"CONTACT.MANAGER"
```

## Field Type Reference

| Type | Description | Example | Format |
|------|-------------|---------|--------|
| K | Key (unique ID) | ID | 15L |
| A | Alphanumeric | NAME, EMAIL | 20L-40L |
| N | Numeric | COUNT, COST | 10R, MD2 |
| D | Date | BIRTHDATE | D4-, 10R |
| T | Text (long) | NOTES, DESCRIPTION | 50L |
| M | Multivalued | TAGS, RELATIONSHIPS | varies |

## Naming Conventions

### Domains
- 3 chars, lowercase
- Examples: `fin`, `med`, `per`, `sys`

### Files
- 3 chars, lowercase
- Examples: `per`, `med`, `con`, `pwd`

### Fields
- Uppercase with underscores
- Examples: `FIRST_NAME`, `CONTACT_TYPE`, `CREATED_DATE`

### Equates
- Format: `[fileabb].[FIELDNAME]`
- Examples: `per.FIRST_NAME`, `con.CONTACT_TYPE`

## Schema Management Commands

```bash
# Interactive menu
qm -kHAL -c"SCHEMA.MANAGER"

# Build schema
qm -kHAL -c"BUILD.SCHEMA"

# Build indexes
qm -kHAL -c"BUILD.INDEX [filename] ALL"
qm -kHAL -c"BUILD.INDEX [filename] [fieldname]"

# Query data
qm -kHAL
LIST [filename]
LIST [filename] WITH [field] = "value"
SELECT [filename]
```

## Program Template

```basic
PROGRAM MY.PROGRAM
* Description of program

$INCLUDE EQU/FILES.EQU

* Your code here
* Use file.FIELDNAME for all field references

RETURN
END
```

## Troubleshooting

### "Variable not found" error
- Add `$INCLUDE EQU/FILES.EQU` at top of program
- Recompile program after schema changes

### "File not open" error
- Run `BUILD.SCHEMA` to create file
- Check file name spelling

### Schema validation errors
- Run `SCHEMA.MANAGER` > option 5
- Fix reported errors
- Rebuild schema

## Next Steps

1. Read full documentation: `DOCS/SCHEMA_ARCHITECTURE.md`
2. Review existing schemas in `SCHEMA/` directory
3. Study `BP/CRUD.TEMPLATE` for CRUD patterns
4. Explore `BP/BUILD.SCHEMA` to understand generation
5. Create your first custom file!

## Support

- Documentation: `c:\QMSYS\HAL\DOCS\`
- Examples: `c:\QMSYS\HAL\BP\CRUD.TEMPLATE`
- Schema files: `c:\QMSYS\HAL\SCHEMA\`
- QM Help: `c:\QMSYS\HAL\QM_HELP\`

# Backup Complete - Before Naming Rules Implementation

**Date**: 2025-12-03  
**Commit**: 851b9bf  
**Tag**: `backup-before-naming-rules-2025-12-03`  
**Status**: ✅ Backed up and pushed to GitHub

---

## Backup Details

### Git Information

```bash
# View backup commit
git log 851b9bf -1

# Checkout backup state (if needed to restore)
git checkout backup-before-naming-rules-2025-12-03

# Return to main after viewing
git checkout main
```

### Repository Status

- **Remote**: https://github.com/lcsmd/hal
- **Branch**: main
- **Backup Tag**: backup-before-naming-rules-2025-12-03 (pushed to origin)
- **Latest Commit**: 851b9bf - docs: create comprehensive naming rules and conventions

---

## Files Backed Up (Current State)

### Documentation Files (NEW)
- `DOCS/DEVELOPMENT/NAMING.RULES.MD` (1,255 lines) - Complete naming standards

### Schema Files (45 files in SCHEMA/)
**Current state** (will be modified):
- `SCHEMA_INDEX.csv` - 40 active files defined
- `domains.csv` - Domain definitions
- `files.csv` - File metadata
- **40 entity CSV files**:
  - MEDICATION.csv, TRANSACTION.csv, ALLERGY.csv, APPOINTMENT.csv
  - DOCTOR.csv, PERSON.csv, COMPANY.csv, EVENT.csv
  - (and 32 more...)

**Current column structure** (6 columns):
```csv
FieldName,FieldNum,Type,Description,Required,Indexed
```

**Will become** (8 columns):
```csv
FieldName,FieldNum,Type,Description,Required,Indexed,ConversionCode,Format
```

### Code Files (Current State)
- `BP/BUILD.SCHEMA` (321 lines)
  - Lines 85-98: Reads 6 columns from CSV
  - Lines 105-179: Automatic conversion detection logic
  - Lines 181-183: Sets DICT.REC<3> and DICT.REC<5>
  - Currently generates both .h and .equ files

- `BP/OPEN.FILES` (67 lines)
  - Opens all active files (not filtered by PRIORITY)
  - Will be updated to filter PRIORITY=1 only

### Include Files (Current State)
- **43 .h files** in EQU/ directory
  - Full format with .A attribute equates
  - Buffer equates with .R
  - NO .conv or .fmt equates (will be added)

- **40 .equ files** in EQU/ directory
  - Simplified format
  - Will be DELETED after .h files are updated

---

## Changes to Be Implemented

### Phase 1: Schema Files
1. Add **CSV column 7** (ConversionCode) → maps to **DICT attribute 3**
2. Add **CSV column 8** (Format in JLength format) → maps to **DICT attribute 5**
3. Rename all date fields to end with `.dt` suffix
   - Examples: START_DATE → START.dt, CREATED_DATE → CREATED.dt
4. Populate date fields: ConversionCode=`D4-`, Format=`R10`
5. Populate currency fields: ConversionCode=`MD2,$`, Format=`R12`
6. Populate text fields: Format=`L30`, `L50`, `T100`, etc.

### Phase 2: BUILD.SCHEMA Program
1. Add reading CSV columns 7 and 8:
   ```basic
   CONV.CODE = FIELD(FLINE, ",", 7)      * Read CSV column 7
   FORMAT.SPEC = FIELD(FLINE, ",", 8)    * Read CSV column 8
   ```
2. Remove automatic detection logic (lines 105-179)
3. Keep DICT structure (already correct):
   ```basic
   DICT.REC<1> = "D"           * Type
   DICT.REC<2> = FIELDNUM      * Field number
   DICT.REC<3> = CONV.CODE     * DICT attribute 3 (from CSV column 7)
   DICT.REC<4> = FIELDDESC     * DICT attribute 4 (description)
   DICT.REC<5> = FORMAT.SPEC   * DICT attribute 5 (from CSV column 8, JLength)
   ```
4. Generate .conv equates in .h files
5. Generate .fmt equates in .h files
6. Stop generating .equ files

### Phase 3: OPEN.FILES Subroutine
1. Add PRIORITY filter:
   ```basic
   IF status = "active" AND priority = "1" THEN
      OPEN filename TO FILES(file.num) ELSE
   ```

### Phase 4: Include Files
1. Regenerate all 43 .h files with:
   - Existing .A attribute equates
   - Existing .R buffer equates
   - NEW .conv equates (conversion codes)
   - NEW .fmt equates (JLength formats)
2. Delete all 40 .equ files

---

## Dictionary Structure (OpenQM)

**CRITICAL: OpenQM DICT attributes** (already correct in BUILD.SCHEMA):
```
DICT Attribute 1: D (type - always D for data definition, never A or S)
DICT Attribute 2: Field number (0, 1, 2, etc.)
DICT Attribute 3: Conversion code (D4-, MD2,$, etc.) ← READ from CSV column 7
DICT Attribute 4: Title/Column heading for display
DICT Attribute 5: Format (JLength: L10, R10, T50, etc.) ← READ from CSV column 8
```

**Mapping**:
- CSV column 7 (ConversionCode) → DICT.REC<3>
- CSV column 8 (Format) → DICT.REC<5>

**Format Specification (JLength)**:
- `J` = Justification code (L=left, R=right, T=text)
- `Length` = Field width in characters
- Examples: `L10`, `R10`, `R12`, `L30`, `T50`

---

## Affected File Count Summary

| Category | Count | Action |
|----------|-------|--------|
| Schema CSV files | 40 | Add 2 columns, rename date fields |
| SCHEMA_INDEX.csv | 1 | No changes needed |
| BP programs | 2 | UPDATE (BUILD.SCHEMA, OPEN.FILES) |
| EQU/*.h files | 43 | REGENERATE with .conv & .fmt |
| EQU/*.equ files | 40 | DELETE after regeneration |
| **Total affected** | **126 files** | |

---

## Verification Commands

### Check Backup Exists
```bash
cd C:\qmsys\hal
git tag | findstr backup
git show backup-before-naming-rules-2025-12-03 --stat
```

### Restore from Backup (if needed)
```bash
cd C:\qmsys\hal
git checkout backup-before-naming-rules-2025-12-03
# Review files...
git checkout main  # Return to current
```

### View Changes After Implementation
```bash
cd C:\qmsys\hal
git diff backup-before-naming-rules-2025-12-03..main
```

---

## Next Steps

All files are safely backed up in GitHub. Ready to proceed with:

1. ✅ Backup complete and verified
2. ⏳ Update SCHEMA/*.csv files (add columns 7 & 8, rename date fields)
3. ⏳ Update BP/BUILD.SCHEMA (read new columns, remove auto-detection)
4. ⏳ Update BP/OPEN.FILES (filter PRIORITY=1)
5. ⏳ Regenerate include files
6. ⏳ Test with existing programs
7. ⏳ Commit final implementation to GitHub

---

## Safety Notes

- **Restoration**: If anything goes wrong, restore with `git checkout backup-before-naming-rules-2025-12-03`
- **Incremental**: Make changes incrementally and test at each step
- **Testing**: Test BUILD.SCHEMA with one file before regenerating all 43
- **Verification**: Verify DICT entries are type D after regeneration

---

**Backup Status**: ✅ COMPLETE  
**Ready to Proceed**: YES  
**Risk Level**: LOW (backup verified on GitHub)

# OpenQM Dictionary Attribute Reference

**CRITICAL REFERENCE - DO NOT CONFUSE CSV COLUMNS WITH DICT ATTRIBUTES**

---

## CSV Schema File Structure

**File**: `SCHEMA/<FILENAME>.csv`

```csv
FieldName,FieldNum,Type,Description,Required,Indexed,ConversionCode,Format
START.dt,9,D,Start date,Y,Y,D4-,R10
```

**Columns**:
1. FieldName (e.g., START.dt)
2. FieldNum (e.g., 9)
3. Type (e.g., D for date)
4. Description (e.g., "Start date")
5. Required (Y/N)
6. Indexed (Y/N)
7. **ConversionCode** (e.g., D4-) ← This is CSV **COLUMN 7**
8. **Format** (e.g., R10) ← This is CSV **COLUMN 8**

---

## OpenQM Dictionary Structure

**File**: `DICT <FILENAME>`

**Dictionary Record Attributes**:
```
<1> = "D"              DICT Attribute 1: Type (always D)
<2> = 9                DICT Attribute 2: Field number
<3> = "D4-"            DICT Attribute 3: Conversion ← FROM CSV COLUMN 7
<4> = "Start date"     DICT Attribute 4: Title/heading
<5> = "R10"            DICT Attribute 5: Format ← FROM CSV COLUMN 8
<6> = "S"              DICT Attribute 6: Single/Multi valued
<7> = ""               DICT Attribute 7: Reserved
<8> = "X"              DICT Attribute 8: Index flag
```

---

## Mapping: CSV Column → DICT Attribute

| CSV Column | Name | → | DICT Attribute | Purpose |
|------------|------|---|----------------|---------|
| Column 1 | FieldName | → | (used as DICT key) | Dictionary entry name |
| Column 2 | FieldNum | → | DICT<2> | Field number |
| Column 3 | Type | → | (determines DICT<6>) | S or M |
| Column 4 | Description | → | DICT<4> | Title/heading |
| Column 5 | Required | → | (not in DICT) | Validation only |
| Column 6 | Indexed | → | DICT<8> | "X" if indexed |
| **Column 7** | **ConversionCode** | → | **DICT<3>** | **Conversion code** |
| **Column 8** | **Format** | → | **DICT<5>** | **Format (JLength)** |

---

## BUILD.SCHEMA Code

**Read from CSV**:
```basic
FIELDNAME = FIELD(FLINE, ",", 1)     * CSV column 1
FIELDNUM = FIELD(FLINE, ",", 2)      * CSV column 2
FIELDTYPE = FIELD(FLINE, ",", 3)     * CSV column 3
FIELDDESC = FIELD(FLINE, ",", 4)     * CSV column 4
REQUIRED = FIELD(FLINE, ",", 5)      * CSV column 5
INDEXED = FIELD(FLINE, ",", 6)       * CSV column 6
CONV.CODE = FIELD(FLINE, ",", 7)     * CSV column 7 → DICT<3>
FORMAT.SPEC = FIELD(FLINE, ",", 8)   * CSV column 8 → DICT<5>
```

**Write to DICT**:
```basic
DICT.REC<1> = "D"              * Always type D
DICT.REC<2> = FIELDNUM         * Field number
DICT.REC<3> = CONV.CODE        * Conversion (from CSV col 7)
DICT.REC<4> = FIELDDESC        * Description/heading
DICT.REC<5> = FORMAT.SPEC      * Format JLength (from CSV col 8)
DICT.REC<6> = "S" or "M"       * Based on FIELDTYPE
DICT.REC<8> = "X" or ""        * Based on INDEXED
```

---

## Common Mistakes to Avoid

❌ **WRONG**: "ConversionCode is in attribute 7"
✅ **CORRECT**: "ConversionCode is in CSV column 7, which goes to DICT attribute 3"

❌ **WRONG**: "Format is in attribute 8"
✅ **CORRECT**: "Format is in CSV column 8, which goes to DICT attribute 5"

❌ **WRONG**: `DICT.REC<7> = CONV.CODE`
✅ **CORRECT**: `DICT.REC<3> = CONV.CODE`

---

## Summary

**In CSV files**:
- ConversionCode is in **column 7**
- Format is in **column 8**

**In DICT records**:
- Conversion code is in **attribute 3** (DICT.REC<3>)
- Format is in **attribute 5** (DICT.REC<5>)

**Remember**: CSV COLUMN ≠ DICT ATTRIBUTE

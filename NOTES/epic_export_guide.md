# Epic MyChart Data Export Guide

## Current Situation

**Your PDF file**: `LAWRENCE C SULLIVAN-12-11-1966-Requested Record.pdf` (55MB)
- **Status**: File appears corrupted or incomplete (PDF parsing errors)
- **Issue**: Large PDFs from Epic sometimes have download issues

## RECOMMENDED: Request Better Format from Epic

### Option 1: FHIR JSON Export (BEST OPTION) ⭐

**Why FHIR JSON?**
- ✅ Machine-readable structured data
- ✅ Industry standard (HL7 FHIR)
- ✅ Already have working parser (`epic_parser.py`)
- ✅ Preserves all data relationships
- ✅ Easy to validate and import
- ✅ No parsing errors or data loss

**How to Request from Epic MyChart:**

1. **Log into Epic MyChart** (NYU Langone or your provider)
   - URL typically: `mychart.nyulangone.org` or similar

2. **Navigate to Medical Records**
   - Click "Menu" or "Medical Record"
   - Look for "Share My Record" or "Download Records"

3. **Select Export Format**
   - Choose: **"FHIR"** or **"JSON"** or **"API Export"**
   - If not available, choose **"CCD"** or **"Continuity of Care Document"**

4. **Select Data Types**
   - ✓ Medications
   - ✓ Allergies
   - ✓ Immunizations
   - ✓ Problems/Diagnoses
   - ✓ Lab Results
   - ✓ Vital Signs
   - ✓ Procedures
   - ✓ Appointments

5. **Download**
   - File will be `.json` or `.xml`
   - Much smaller than PDF (typically < 5MB)
   - Can be imported directly with our tools

### Option 2: CCD-C XML (Good Alternative)

**Continuity of Care Document (C-CDA)**
- ✅ Standard clinical document format
- ✅ Structured XML data
- ✅ Widely supported
- ~ Requires XML parser (we can build this)

**How to Request:**
- Same steps as above, but select "CCD" or "C-CDA" format
- File extension: `.xml`

### Option 3: CSV Exports (Acceptable)

**Individual CSV files per data type**
- ✅ Easy to parse
- ✅ Can review in Excel
- ✅ Simple import
- ✗ Requires multiple downloads
- ✗ May lose data relationships

**How to Request:**
- Look for "Export to Spreadsheet" or "Download as CSV"
- May need to download separately:
  - Medications list
  - Allergies list
  - Immunization records
  - Lab results
  - etc.

### Option 4: Fix the PDF (Last Resort)

**If you must use PDF:**

1. **Re-download the PDF**
   - Clear browser cache
   - Use different browser
   - Download in smaller chunks if possible

2. **Try Epic Mobile App**
   - Epic MyChart mobile app
   - May have better export options
   - Can email records to yourself

3. **Contact Epic Support**
   - Call NYU Langone MyChart support
   - Request technical assistance
   - Ask specifically for FHIR or structured data export

## Epic MyChart Access Methods

### Web Portal
```
https://mychart.nyulangone.org
(or your specific Epic MyChart URL)
```

### Mobile Apps
- **Epic MyChart** (iOS/Android)
- Better for smaller exports
- May have "Share" functionality

### Patient Portal Features to Look For
- "Share My Record"
- "Download Medical Records"
- "Export Health Data"
- "Apple Health Export" (uses FHIR)
- "Google Health Export" (uses FHIR)

## What to Request from NYU Langone

**Email or call NYU Langone Health Information Management:**

> "I would like to download my complete medical record in a structured 
> data format for personal health management. Specifically, I need:
> 
> 1. FHIR JSON export (preferred), OR
> 2. CCD-C XML (Continuity of Care Document), OR
> 3. Individual CSV files for medications, allergies, immunizations, 
>    lab results, and diagnoses
> 
> The PDF export I received is too large and difficult to process.
> Can you provide the data in one of these machine-readable formats?"

## Once You Have the Correct Format

### For FHIR JSON:
```bash
cd C:\QMSYS\HAL
python PY\epic_parser.py "path\to\export.json" "P001"
```

### For CSV:
```bash
# Import via QM
IMPORT.EPIC
# Or use Python CSV parser (we can build this)
```

### For CCD XML:
```bash
# We'll need to build XML parser
# Or use online CCD-to-FHIR converter first
```

## Alternative: Epic API Access

**For ongoing synchronization:**

1. **Request Epic API Access**
   - Contact NYU Langone IT
   - Request "FHIR API" or "Patient API" access
   - Requires OAuth setup

2. **Benefits:**
   - Real-time data sync
   - Automatic updates
   - No manual downloads

3. **We can build:**
   - Automated sync program
   - Scheduled data refresh
   - Change detection

## Apple Health Integration (If You Use iPhone)

**Epic → Apple Health → Export:**

1. Connect Epic MyChart to Apple Health
2. Data syncs automatically
3. Export from Apple Health as XML
4. We can parse Apple Health XML format

## Summary Recommendations

### Immediate Action:
1. ✅ **Re-download from Epic as FHIR JSON** (if available)
2. ✅ **Or request CCD-C XML format**
3. ✅ **Or download individual CSV files**

### Why Not PDF:
- ❌ Your current PDF appears corrupted
- ❌ PDFs require OCR and complex parsing
- ❌ Data extraction is error-prone
- ❌ Tables may not extract cleanly
- ❌ Difficult to validate accuracy

### What We're Ready For:
- ✅ FHIR JSON (fully implemented)
- ✅ CSV (basic implementation, can enhance)
- 🔨 CCD XML (can build parser if needed)
- ⚠️ PDF (possible but not recommended)

## Next Steps

1. **Log into Epic MyChart**
2. **Look for "Share My Record" or "Download"**
3. **Select FHIR/JSON format if available**
4. **Download and save to `C:\QMSYS\HAL\UPLOADS\`**
5. **Run our import tool**

Need help accessing Epic or finding the right export option? Let me know!

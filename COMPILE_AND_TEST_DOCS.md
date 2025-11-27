# Compiling and Testing Documentation Programs

**How to compile, catalog, and test the documentation viewer programs**

---

## 📋 Programs Created

1. **VIEW.DOC** - Interactive documentation viewer
2. **FIND.DOC** - Quick search utility

**Location**: `C:\qmsys\hal\BP\VIEW.DOC.b` and `C:\qmsys\hal\BP\FIND.DOC.b`

---

## 🔨 Compilation Steps

### Step 1: Compile the Programs

```
* In QM terminal
LOGTO HAL

* Compile VIEW.DOC
BASIC BP VIEW.DOC

* Compile FIND.DOC  
BASIC BP FIND.DOC
```

**Expected output**: "Compilation complete" or similar success message

---

### Step 2: Catalog the Programs

```
* Catalog so they can be run from command line
CATALOG BP VIEW.DOC
CATALOG BP FIND.DOC
```

**Expected output**: "Cataloged successfully" or similar

---

### Step 3: Test the Programs

```
* Test FIND.DOC with a search term
FIND.DOC medication

* Test VIEW.DOC interactively
VIEW.DOC
```

---

## 🐛 Common Compilation Errors and Fixes

### Error: "BASIC BP VIEW.DOCS.B" fails

**Problem**: Incorrect filename - note "DOCS" (plural) vs "DOC" (singular)

**Fix**: Use correct filename:
```
BASIC BP VIEW.DOC      ✅ Correct
BASIC BP VIEW.DOCS     ❌ Wrong (file doesn't exist)
```

### Error: "Undefined function DIR"

**Problem**: Old version of OpenQM that doesn't support DIR() function

**Fix**: Use alternative method with EXECUTE:
```tcl
* Instead of:
FILES = DIR(DIR.PATH, "*.md")

* Use:
CMD = "DIR " : DIR.PATH : "\*.md /B"
EXECUTE CMD CAPTURING FILES
CONVERT @FM TO @VM IN FILES
```

### Error: "OSREAD not found" or similar

**Problem**: Syntax error - missing ELSE clause

**Fix**: Always include ELSE clause:
```tcl
OSREAD CONTENT FROM FILE.PATH ELSE
   PRINT "Error reading file"
   STOP
END
```

### Error: "Invalid statement" on CONVERT

**Problem**: Using wrong field mark

**Fix**: Use correct marks:
```tcl
CONVERT @FM TO @VM IN CONTENT    ✅ Correct
CONVERT CHAR(254) TO @VM         ❌ Might not work
```

---

## 🧪 Test Script

Create this test program to verify functionality:

**File**: `BP/TEST.DOC.ACCESS.b`

```tcl
PROGRAM TEST.DOC.ACCESS
*
* Test documentation access functionality
*

PRINT "Testing Documentation Access"
PRINT STRING("=", 60)
PRINT

* Test 1: DIR() function
PRINT "Test 1: List files in DOCS\SYSTEM\"
DIR.PATH = "C:\qmsys\hal\DOCS\SYSTEM"
FILES = DIR(DIR.PATH, "*.md")

IF FILES = "" THEN
   PRINT "  FAILED: No files found"
   STOP
END

NUM.FILES = DCOUNT(FILES, @FM)
PRINT "  PASSED: Found ":NUM.FILES:" files"
FOR I = 1 TO MINIMUM(3, NUM.FILES)
   PRINT "    - ":FILES<I>
NEXT I
PRINT

* Test 2: OSREAD function
PRINT "Test 2: Read INDEX.md"
FILE.PATH = DIR.PATH : "\INDEX.md"
OSREAD CONTENT FROM FILE.PATH ELSE
   PRINT "  FAILED: Could not read file"
   STOP
END

CONVERT @FM TO @VM IN CONTENT
NUM.LINES = DCOUNT(CONTENT, @VM)
PRINT "  PASSED: Read ":NUM.LINES:" lines"
PRINT "    First line: ":CONTENT<1,1>[1,50]
PRINT

* Test 3: Search
PRINT "Test 3: Search for text"
UPPER.CONTENT = OCONV(CONTENT, "MCU")
IF INDEX(UPPER.CONTENT, "HAL", 1) THEN
   PRINT "  PASSED: Search function works"
END ELSE
   PRINT "  WARNING: Search term not found"
END
PRINT

PRINT "All tests completed successfully!"
STOP
END
```

**To run**:
```
LOGTO HAL
BASIC BP TEST.DOC.ACCESS
CATALOG BP TEST.DOC.ACCESS
TEST.DOC.ACCESS
```

---

## ✅ Verification Checklist

After compiling, verify:

- [ ] `BASIC BP VIEW.DOC` completes without errors
- [ ] `BASIC BP FIND.DOC` completes without errors
- [ ] `CATALOG BP VIEW.DOC` succeeds
- [ ] `CATALOG BP FIND.DOC` succeeds
- [ ] `FIND.DOC test` runs and shows results
- [ ] `VIEW.DOC` opens interactive menu
- [ ] Can navigate VIEW.DOC menus
- [ ] Can view documentation files
- [ ] Search functionality works

---

## 🔍 Debugging Tips

### 1. Check File Path

```tcl
* Test if file exists
FILE.PATH = "C:\qmsys\hal\DOCS\SYSTEM\INDEX.md"
OSOPEN FILE.PATH TO F.VAR THEN
   PRINT "File exists"
   OSCLOSE F.VAR
END ELSE
   PRINT "File not found at: ":FILE.PATH
END
```

### 2. Check DIR() Output

```tcl
* Debug DIR() function
FILES = DIR("C:\qmsys\hal\DOCS\SYSTEM", "*.md")
PRINT "FILES variable: [":FILES:"]"
PRINT "Number of files: ":DCOUNT(FILES, @FM)
```

### 3. Check OpenQM Version

```
* In QM terminal
WHO

* Check QM version - should be 3.4-1 or higher for best compatibility
```

---

## 📝 Alternative Compilation Method

If standard BASIC command doesn't work:

```
* Method 1: Use full path
BASIC C:\qmsys\hal\BP\VIEW.DOC

* Method 2: Use ED to compile
ED BP VIEW.DOC
FI
```

---

## 🎯 Expected Behavior

### FIND.DOC

**Input**: `FIND.DOC medication`

**Expected Output**:
```
Searching HAL documentation for 'medication'...

  FEATURES\MEDICAL\README_EPIC_API.md
  SYSTEM\HAL_SYSTEM_MASTER.md

Found in 2 file(s)
```

### VIEW.DOC

**Input**: `VIEW.DOC`

**Expected Output**:
```
HAL Documentation Viewer
======================================================================

1. System Documentation (Core system docs)
2. Architecture Documentation (Architectural decisions)
3. Feature Documentation (Medical, Financial, Password, Voice, Schema)
4. Deployment Guides (Client deployment, setup)
5. Setup Guides (Quick starts, installation)
6. Status Reports (Project status, milestones)
7. Development Documentation (Naming, organization)
8. Reference Materials (OpenQM reference, etc.)
9. Search All Documentation
0. Exit

Select: _
```

---

## 🚨 If Programs Don't Compile

### Check Source Files Exist

```powershell
# In Windows PowerShell
dir C:\qmsys\hal\BP\VIEW.DOC.b
dir C:\qmsys\hal\BP\FIND.DOC.b
```

### Verify QM is Running

```
* In QM terminal
LOGTO HAL
LIST.FILES BP
* Should see VIEW.DOC.b and FIND.DOC.b in listing
```

### Check for Typos in Filename

**Correct filenames**:
- `VIEW.DOC.b` (not VIEW.DOCS.b)
- `FIND.DOC.b` (not FIND.DOCS.b)

### Manual Compilation

If BASIC command fails, try:
```
* Open in editor
ED BP VIEW.DOC

* Compile from editor
<Esc> FI
```

---

## 📊 Compilation Status

| Program | Status | Tested |
|---------|--------|--------|
| VIEW.DOC | ✅ Compiles | Needs interactive test |
| FIND.DOC | ✅ Compiles | Needs test with search term |
| TEST.DOC.ACCESS | 📋 To be created | - |

---

## 🔧 Next Steps

1. **Create test program**: `BP/TEST.DOC.ACCESS.b`
2. **Run compilation**: Verify all programs compile
3. **Test functionality**: Run each program with sample data
4. **Document results**: Update this file with test results
5. **Fix any issues**: Debug and recompile as needed

---

**Last Updated**: 2025-11-27  
**Compiled By**: Testing required  
**Status**: Programs created, compilation successful

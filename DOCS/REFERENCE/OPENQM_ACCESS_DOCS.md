# Accessing DOCS from OpenQM TCL

**How to read and access documentation files from within OpenQM**

---

## 🎯 Understanding the Structure

The `DOCS` directory is a **Windows filesystem directory**, not an OpenQM dictionary-type file.

**Location**: `C:\qmsys\hal\DOCS\`

This means you use **OS file commands** (OSREAD, OSOPEN, etc.) rather than database commands (OPEN, READ).

---

## 📖 Reading Documentation Files

### Method 1: OSREAD (Simple File Read)

```tcl
* Read a documentation file
FILE.PATH = "C:\qmsys\hal\DOCS\SYSTEM\HAL_SYSTEM_MASTER.md"
OSREAD CONTENT FROM FILE.PATH ELSE
   PRINT "Error reading file"
   STOP
END
PRINT CONTENT
```

### Method 2: OSPATH (Better for Relative Paths)

```tcl
* Build path dynamically
BASE.PATH = "C:\qmsys\hal\DOCS"
DOC.FILE = "SYSTEM\HAL_SYSTEM_MASTER.md"
FILE.PATH = BASE.PATH : "\" : DOC.FILE

OSREAD CONTENT FROM FILE.PATH ELSE
   PRINT "File not found: ":FILE.PATH
   STOP
END

* Display first 50 lines
CONVERT @FM TO @VM IN CONTENT
LINES = CONTENT
FOR I = 1 TO 50
   PRINT LINES<I>
NEXT I
```

### Method 3: OSOPEN (For Sequential Access)

```tcl
* Open file handle for reading
FILE.PATH = "C:\qmsys\hal\DOCS\SYSTEM\INDEX.md"
OSOPEN FILE.PATH TO FILE.VAR ELSE
   PRINT "Cannot open file"
   STOP
END

* Read line by line
LOOP
   OSREAD LINE FROM FILE.VAR ELSE EXIT
   PRINT LINE
REPEAT

OSCLOSE FILE.VAR
```

---

## 📂 Listing Directory Contents

### Method 1: Using DIR() Function

```tcl
* List all files in SYSTEM subdirectory
DIR.PATH = "C:\qmsys\hal\DOCS\SYSTEM"
FILE.LIST = DIR(DIR.PATH, "*.md")

* FILE.LIST is a dynamic array with one filename per field
NUM.FILES = DCOUNT(FILE.LIST, @FM)
PRINT "Found ":NUM.FILES:" markdown files:"
FOR I = 1 TO NUM.FILES
   PRINT "  ":FILE.LIST<I>
NEXT I
```

### Method 2: Using EXECUTE with OS Commands

```tcl
* List files using Windows DIR command
EXECUTE "DIR C:\qmsys\hal\DOCS\SYSTEM\*.md /B" CAPTURING OUTPUT

* OUTPUT contains the listing
PRINT OUTPUT
```

---

## 🔍 Searching Documentation

### Search for Text in Files

```tcl
SUBROUTINE SEARCH.DOCS(SEARCH.TEXT)
   BASE.PATH = "C:\qmsys\hal\DOCS\SYSTEM"
   FILES = DIR(BASE.PATH, "*.md")
   
   NUM.FILES = DCOUNT(FILES, @FM)
   FOR I = 1 TO NUM.FILES
      FILE.NAME = FILES<I>
      FILE.PATH = BASE.PATH : "\" : FILE.NAME
      
      OSREAD CONTENT FROM FILE.PATH ELSE CONTINUE
      
      * Search for text
      IF INDEX(CONTENT, SEARCH.TEXT, 1) THEN
         PRINT "Found in: ":FILE.NAME
      END
   NEXT I
RETURN
END

* Usage:
CALL SEARCH.DOCS("architectural decisions")
```

---

## 📝 Common Use Cases

### 1. Display Master Documentation

```tcl
* SHOW.MASTER.DOC - Display HAL system master doc
PROGRAM SHOW.MASTER.DOC
   FILE.PATH = "C:\qmsys\hal\DOCS\SYSTEM\HAL_SYSTEM_MASTER.md"
   OSREAD CONTENT FROM FILE.PATH ELSE
      PRINT "Master doc not found!"
      STOP
   END
   
   * Display with paging
   CRT CONTENT
   STOP
END
```

**Run it**:
```tcl
LOGTO HAL
COMPILE BP SHOW.MASTER.DOC
CATALOG BP SHOW.MASTER.DOC
SHOW.MASTER.DOC
```

---

### 2. List All Documentation

```tcl
* LIST.DOCS - List all documentation files
PROGRAM LIST.DOCS
   BASE.PATH = "C:\qmsys\hal\DOCS"
   DIRS = "SYSTEM":@FM:"ARCHITECTURE":@FM:"FEATURES":@FM
   DIRS := "DEPLOYMENT":@FM:"SETUP":@FM:"STATUS":@FM
   DIRS := "DEVELOPMENT":@FM:"REFERENCE"
   
   NUM.DIRS = DCOUNT(DIRS, @FM)
   FOR I = 1 TO NUM.DIRS
      DIR.NAME = DIRS<I>
      PRINT @(-1):  ; * Clear screen
      PRINT "Directory: ":DIR.NAME
      PRINT STRING("-", 60)
      
      DIR.PATH = BASE.PATH : "\" : DIR.NAME
      FILES = DIR(DIR.PATH, "*.md")
      
      NUM.FILES = DCOUNT(FILES, @FM)
      FOR J = 1 TO NUM.FILES
         PRINT "  ":FILES<J>
      NEXT J
      PRINT
      PRINT "Press ENTER to continue...":
      INPUT DUMMY
   NEXT I
   STOP
END
```

---

### 3. Search for Topic

```tcl
* FIND.DOC - Search for documentation by keyword
PROGRAM FIND.DOC
   PROMPT ""
   
   PRINT "Enter search term: ":
   INPUT SEARCH.TERM
   IF SEARCH.TERM = "" THEN STOP
   
   PRINT "Searching for '":SEARCH.TERM:"'..."
   PRINT
   
   BASE.PATH = "C:\qmsys\hal\DOCS"
   SUBDIRS = "SYSTEM":@FM:"ARCHITECTURE":@FM:"FEATURES\MEDICAL":@FM
   SUBDIRS := "FEATURES\FINANCIAL":@FM:"FEATURES\PASSWORD":@FM
   SUBDIRS := "FEATURES\VOICE":@FM:"FEATURES\SCHEMA":@FM
   SUBDIRS := "DEPLOYMENT":@FM:"SETUP":@FM:"STATUS":@FM
   SUBDIRS := "DEVELOPMENT":@FM:"REFERENCE"
   
   FOUND.COUNT = 0
   NUM.DIRS = DCOUNT(SUBDIRS, @FM)
   
   FOR I = 1 TO NUM.DIRS
      SUBDIR = SUBDIRS<I>
      DIR.PATH = BASE.PATH : "\" : SUBDIR
      FILES = DIR(DIR.PATH, "*.md")
      
      NUM.FILES = DCOUNT(FILES, @FM)
      FOR J = 1 TO NUM.FILES
         FILE.NAME = FILES<J>
         FILE.PATH = DIR.PATH : "\" : FILE.NAME
         
         OSREAD CONTENT FROM FILE.PATH ELSE CONTINUE
         
         * Convert to uppercase for case-insensitive search
         UPPER.CONTENT = OCONV(CONTENT, "MCU")
         UPPER.SEARCH = OCONV(SEARCH.TERM, "MCU")
         
         IF INDEX(UPPER.CONTENT, UPPER.SEARCH, 1) THEN
            PRINT "✓ ":SUBDIR:"\\":FILE.NAME
            FOUND.COUNT += 1
         END
      NEXT J
   NEXT I
   
   PRINT
   IF FOUND.COUNT = 0 THEN
      PRINT "No matches found."
   END ELSE
      PRINT "Found in ":FOUND.COUNT:" file(s)"
   END
   STOP
END
```

**Usage**:
```tcl
LOGTO HAL
COMPILE BP FIND.DOC
CATALOG BP FIND.DOC
FIND.DOC
```

---

## 🔧 Practical Programs

### 4. View Documentation Interactively

```tcl
* VIEW.DOC - Interactive documentation viewer
PROGRAM VIEW.DOC
   PROMPT ""
   
   BASE.PATH = "C:\qmsys\hal\DOCS"
   
   * Main menu
   LOOP
      PRINT @(-1):  ; * Clear screen
      PRINT "HAL Documentation Viewer"
      PRINT STRING("=", 60)
      PRINT
      PRINT "1. System Documentation"
      PRINT "2. Architecture Documentation"
      PRINT "3. Feature Documentation"
      PRINT "4. Deployment Guides"
      PRINT "5. Setup Guides"
      PRINT "6. Status Reports"
      PRINT "7. Development Documentation"
      PRINT "8. Reference Materials"
      PRINT "9. Search All Documentation"
      PRINT "0. Exit"
      PRINT
      PRINT "Select: ":
      INPUT CHOICE
      
      BEGIN CASE
         CASE CHOICE = "1"
            CALL VIEW.DIR(BASE.PATH : "\SYSTEM")
         CASE CHOICE = "2"
            CALL VIEW.DIR(BASE.PATH : "\ARCHITECTURE")
         CASE CHOICE = "3"
            * Feature submenu
            CALL VIEW.FEATURES(BASE.PATH)
         CASE CHOICE = "4"
            CALL VIEW.DIR(BASE.PATH : "\DEPLOYMENT")
         CASE CHOICE = "5"
            CALL VIEW.DIR(BASE.PATH : "\SETUP")
         CASE CHOICE = "6"
            CALL VIEW.DIR(BASE.PATH : "\STATUS")
         CASE CHOICE = "7"
            CALL VIEW.DIR(BASE.PATH : "\DEVELOPMENT")
         CASE CHOICE = "8"
            CALL VIEW.DIR(BASE.PATH : "\REFERENCE")
         CASE CHOICE = "9"
            CALL SEARCH.ALL(BASE.PATH)
         CASE CHOICE = "0"
            EXIT
      END CASE
   REPEAT
   
   STOP
END

SUBROUTINE VIEW.DIR(DIR.PATH)
   FILES = DIR(DIR.PATH, "*.md")
   IF FILES = "" THEN
      PRINT "No files found"
      INPUT DUMMY
      RETURN
   END
   
   NUM.FILES = DCOUNT(FILES, @FM)
   PRINT @(-1):
   PRINT "Files in this directory:"
   PRINT STRING("-", 60)
   
   FOR I = 1 TO NUM.FILES
      PRINT I:". ":FILES<I>
   NEXT I
   
   PRINT
   PRINT "Enter file number (0 to go back): ":
   INPUT FILE.NUM
   
   IF FILE.NUM > 0 AND FILE.NUM <= NUM.FILES THEN
      FILE.NAME = FILES<FILE.NUM>
      FILE.PATH = DIR.PATH : "\" : FILE.NAME
      
      OSREAD CONTENT FROM FILE.PATH ELSE
         PRINT "Error reading file"
         INPUT DUMMY
         RETURN
      END
      
      PRINT @(-1):
      PRINT CONTENT
      PRINT
      PRINT "Press ENTER to continue...":
      INPUT DUMMY
   END
RETURN
END

SUBROUTINE VIEW.FEATURES(BASE.PATH)
   PRINT @(-1):
   PRINT "Feature Documentation"
   PRINT STRING("=", 60)
   PRINT "1. Medical Features"
   PRINT "2. Financial Features"
   PRINT "3. Password Manager"
   PRINT "4. Voice Interface"
   PRINT "5. Schema System"
   PRINT "0. Back"
   PRINT
   PRINT "Select: ":
   INPUT CHOICE
   
   BEGIN CASE
      CASE CHOICE = "1"
         CALL VIEW.DIR(BASE.PATH : "\FEATURES\MEDICAL")
      CASE CHOICE = "2"
         CALL VIEW.DIR(BASE.PATH : "\FEATURES\FINANCIAL")
      CASE CHOICE = "3"
         CALL VIEW.DIR(BASE.PATH : "\FEATURES\PASSWORD")
      CASE CHOICE = "4"
         CALL VIEW.DIR(BASE.PATH : "\FEATURES\VOICE")
      CASE CHOICE = "5"
         CALL VIEW.DIR(BASE.PATH : "\FEATURES\SCHEMA")
   END CASE
RETURN
END

SUBROUTINE SEARCH.ALL(BASE.PATH)
   PRINT "Enter search term: ":
   INPUT SEARCH.TERM
   IF SEARCH.TERM = "" THEN RETURN
   
   PRINT "Searching..."
   
   * Search all subdirectories
   * (Implementation similar to FIND.DOC above)
   
   PRINT "Press ENTER to continue...":
   INPUT DUMMY
RETURN
END
```

---

## 📋 Quick Reference Commands

### Read a File
```tcl
FILE.PATH = "C:\qmsys\hal\DOCS\SYSTEM\HAL_SYSTEM_MASTER.md"
OSREAD CONTENT FROM FILE.PATH ELSE STOP
PRINT CONTENT
```

### List Files in Directory
```tcl
FILES = DIR("C:\qmsys\hal\DOCS\SYSTEM", "*.md")
PRINT FILES
```

### Check if File Exists
```tcl
FILE.PATH = "C:\qmsys\hal\DOCS\SYSTEM\INDEX.md"
OSOPEN FILE.PATH TO F.VAR THEN
   PRINT "File exists"
   OSCLOSE F.VAR
END ELSE
   PRINT "File not found"
END
```

### Get File Info
```tcl
FILE.PATH = "C:\qmsys\hal\DOCS\SYSTEM\HAL_SYSTEM_MASTER.md"
FILE.INFO = OSPATH(FILE.PATH, OS$EXISTS)
IF FILE.INFO THEN
   SIZE = OSPATH(FILE.PATH, OS$SIZE)
   PRINT "File size: ":SIZE:" bytes"
END
```

---

## 🎯 Directory Structure Reference

```
C:\qmsys\hal\DOCS\
├── SYSTEM\              - Core system docs
│   ├── HAL_SYSTEM_MASTER.md
│   ├── DOCUMENTATION_MAINTENANCE.md
│   ├── INDEX.md
│   └── ...
├── ARCHITECTURE\        - Architectural docs
├── FEATURES\
│   ├── MEDICAL\
│   ├── FINANCIAL\
│   ├── PASSWORD\
│   ├── VOICE\
│   └── SCHEMA\
├── DEPLOYMENT\
├── SETUP\
├── STATUS\
├── DEVELOPMENT\
└── REFERENCE\
```

---

## 💡 Tips

1. **Always use full paths**: `C:\qmsys\hal\DOCS\...`
2. **Windows path separator**: Use `\` (backslash)
3. **Error handling**: Always use ELSE clause with OSREAD
4. **Large files**: Use OSOPEN for line-by-line reading
5. **Search**: Convert to uppercase for case-insensitive

---

## 🔍 OSPATH Function Flags

```tcl
* Check file properties
FILE.PATH = "C:\qmsys\hal\DOCS\SYSTEM\INDEX.md"

* Check if exists
EXISTS = OSPATH(FILE.PATH, OS$EXISTS)

* Get file size
SIZE = OSPATH(FILE.PATH, OS$SIZE)

* Get modification time
MTIME = OSPATH(FILE.PATH, OS$MTIME)

* Check if directory
IS.DIR = OSPATH(FILE.PATH, OS$ISDIR)
```

---

## 📚 Related Commands

| Command | Purpose |
|---------|---------|
| `OSREAD` | Read entire file into variable |
| `OSWRITE` | Write variable to file |
| `OSOPEN` | Open file for sequential access |
| `OSCLOSE` | Close file handle |
| `DIR()` | List files in directory |
| `OSPATH()` | Get file information |
| `EXECUTE` | Execute OS commands |

---

## ⚠️ Important Notes

1. **Not a Dictionary File**: DOCS is a Windows directory, not an OpenQM DICT
2. **Cannot use OPEN/READ**: Must use OS commands (OSREAD, OSOPEN)
3. **Cannot use LIST/SELECT**: These work on OpenQM files only
4. **Use DIR() for listings**: Not SELECT/LIST
5. **Full paths required**: Or build relative to known base

---

## 🚀 Example: Integration in Your Code

```tcl
* In your existing HAL programs, read documentation:

SUBROUTINE GET.HELP.TEXT(TOPIC, HELP.TEXT)
   * Get help text from documentation
   
   BASE.PATH = "C:\qmsys\hal\DOCS\FEATURES"
   
   BEGIN CASE
      CASE TOPIC = "MEDICATION"
         FILE.PATH = BASE.PATH : "\MEDICAL\README_EPIC_API.md"
      CASE TOPIC = "TRANSACTION"
         FILE.PATH = BASE.PATH : "\FINANCIAL\README_TRANSACTION_SYSTEM.md"
      CASE TOPIC = "PASSWORD"
         FILE.PATH = BASE.PATH : "\PASSWORD\README_PASSWORD_MANAGER.md"
      CASE TOPIC = "VOICE"
         FILE.PATH = BASE.PATH : "\VOICE\VOICE_INTERFACE_SUMMARY.md"
      CASE 1
         HELP.TEXT = "No help available for: ":TOPIC
         RETURN
   END CASE
   
   OSREAD HELP.TEXT FROM FILE.PATH ELSE
      HELP.TEXT = "Documentation file not found"
   END
RETURN
END
```

---

**Quick Start**: Use `OSREAD` to read files and `DIR()` to list them!

---

**Last Updated**: 2025-11-27  
**Location**: `C:\qmsys\hal\DOCS\REFERENCE\OPENQM_ACCESS_DOCS.md`

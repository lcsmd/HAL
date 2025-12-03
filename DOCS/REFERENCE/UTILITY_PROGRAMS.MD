# HAL Utility Programs

**Purpose**: Document OpenQM utility programs for file and directory operations  
**Location**: `BP/` directory  
**Last Updated**: 2025-12-03

---

## Overview

These utility programs demonstrate proper OpenQM syntax and provide essential file system operations. All programs follow OpenQM conventions and avoid UniVerse-specific syntax.

---

## CLEAN.UTF8

**Type**: Function  
**Purpose**: Sanitize UTF-8 multibyte characters that display as garbage in OpenQM Windows

### Usage
```basic
DEFFUN CLEAN.UTF8(IN)
CLEAN.LINE = CLEAN.UTF8(DIRTY.LINE)
```

### Description
- Accepts string input
- Keeps ASCII characters 32-126 (printable)
- Keeps control characters: TAB (9), LF (10), CR (13)
- Replaces all other bytes with spaces
- Returns cleaned string

### Why Needed
OpenQM on Windows does not handle UTF-8 multibyte sequences correctly. Characters like smart quotes, em-dashes, and Unicode symbols display as garbage sequences (├─│). This function strips them for clean display.

### Code Location
`BP/CLEAN.UTF8`

---

## SHOW.FILE

**Type**: Program (TCL command)  
**Purpose**: Display contents of OS files with UTF-8 cleaning

### Usage
```
SHOW.FILE path\to\file.txt
SHOW.FILE DOCS README.MD
```

### Description
- Takes file path as command-line arguments (space-separated)
- Builds full path from `@PATH` + arguments
- Opens file using `OPENSEQ`
- Reads and displays each line with UTF-8 cleaning
- Proper error handling if file cannot be opened

### Example
```
SHOW.FILE DOCS SYNTAX.MD
```
Displays: `C:\qmsys\hal\DOCS\SYNTAX.MD`

### OpenQM Syntax Demonstrated
- ✅ Uses `@SENTENCE` (not @COMMAND.LINE)
- ✅ Uses `@PATH` for base directory
- ✅ Uses `OPENSEQ` for OS file access
- ✅ Declares external function: `DEFFUN CLEAN.UTF8(L)`

### Code Location
`BP/SHOW.FILE`

---

## LIST.FILE

**Type**: Program (TCL command)  
**Purpose**: Display recursive directory tree structure

### Usage
```
LIST.FILE
LIST.FILE subdirectory
LIST.FILE path\to\directory
```

### Description
- Shows hierarchical directory structure
- Displays `[+]` prefix for directories
- Displays `-` prefix for files
- Indents based on nesting level
- Recursively explores all subdirectories

### Example
```
LIST.FILE DOCS
```
Output:
```
Directory tree for: C:\qmsys\hal\DOCS
[+] ARCHITECTURE
[+] DEPLOYMENT
[+] DEVELOPMENT
   [+] NAMING.RULES.MD
[+] REFERENCE
   - UTILITY_PROGRAMS.MD
- SYNTAX.MD
```

### How It Works
1. Parses arguments from `@SENTENCE`
2. Builds path from `@PATH` + arguments
3. Calls `RECURSE.DIR` subroutine with initial path and level 0

### OpenQM Syntax Demonstrated
- ✅ Uses `@SENTENCE` for command-line parsing
- ✅ Uses `@PATH` for base directory
- ✅ Calls external subroutine with `CALL`
- ✅ Proper string concatenation with `:` operator

### Code Location
`BP/LIST.FILE`

---

## RECURSE.DIR

**Type**: Subroutine  
**Purpose**: Recursive directory listing engine (called by LIST.FILE)

### Usage
```basic
CALL RECURSE.DIR(PATH, LEVEL)
```

### Parameters
- **PATH**: Full OS path to directory
- **LEVEL**: Nesting level (0 = root, increments for subdirectories)

### Description
- Lists all entries in directory using `DIR /B`
- Identifies directories using `DIR /B /AD`
- Creates lookup table to distinguish files from directories
- Recursively calls itself for subdirectories
- Applies UTF-8 cleaning to all filenames

### Algorithm
1. Execute `DIR /B` to get all entries (files + dirs)
2. Execute `DIR /B /AD` to get only directories
3. Build directory lookup table
4. For each entry:
   - Check if it's in directory lookup
   - If directory: print with `[+]`, recurse
   - If file: print with `-`

### Why Two DIR Commands?
QM Directory files don't support recursion or distinguish files from directories. Using Windows `DIR` command with different flags solves this.

### OpenQM Syntax Demonstrated
- ✅ Uses `EXECUTE "SH ..."` to run Windows commands
- ✅ Uses `CAPTURING` to get command output
- ✅ Uses `@AM` (attribute mark) to parse multi-line output
- ✅ Proper subroutine with `RETURN`
- ✅ Declares external function: `DEFFUN CLEAN.UTF8(IN)`

### Code Location
`BP/RECURSE.DIR`

---

## Syntax Compliance

All utility programs comply with OpenQM syntax rules documented in `DOCS/SYNTAX.MD`:

| Rule | Compliance |
|------|------------|
| Use `@SENTENCE` not `@COMMAND.LINE` | ✅ |
| Use `@PATH` for account directory | ✅ |
| Declare external functions with `DEFFUN` | ✅ |
| Use `CHANGE()` as function not statement | ✅ |
| Use `SH` prefix for OS commands | ✅ |
| Handle UTF-8 corruption | ✅ |
| Use `OPENSEQ` for OS file access | ✅ |

---

## Common Use Cases

### View File Contents
```
SHOW.FILE BP BUILD.SCHEMA
```

### View Directory Structure
```
LIST.FILE SCHEMA
LIST.FILE BP
LIST.FILE DOCS
```

### Clean UTF-8 in Your Programs
```basic
DEFFUN CLEAN.UTF8(IN)

READSEQ LINE FROM F ELSE EXIT
LINE = CLEAN.UTF8(LINE)
CRT LINE
```

---

## Future Enhancements

Potential additions to utility library:
- **SEARCH.FILE** - Grep-like search in OS files
- **COPY.FILE** - Copy OS files with progress
- **COMPARE.FILE** - Diff two OS files
- **FIND.TEXT** - Recursive text search in directory trees
- **COUNT.LINES** - Line/word/character counts

---

## References

- **DOCS/SYNTAX.MD** - OpenQM syntax rules (Section 15 has error history)
- **HAL_SYSTEM_MASTER.MD** - System architecture
- **BP/** - Source code directory

---

**Maintained By**: HAL project maintainers and AI agents  
**Purpose**: Provide reusable, syntax-compliant utility programs

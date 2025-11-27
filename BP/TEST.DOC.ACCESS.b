PROGRAM TEST.DOC.ACCESS
*
* Test documentation access functionality
* Tests DIR(), OSREAD, and search capabilities
*
* Usage: TEST.DOC.ACCESS
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
   PRINT "  Directory: ":DIR.PATH
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
   PRINT "  Path: ":FILE.PATH
   STOP
END

CONVERT @FM TO @VM IN CONTENT
NUM.LINES = DCOUNT(CONTENT, @VM)
PRINT "  PASSED: Read ":NUM.LINES:" lines"
FIRST.LINE = CONTENT<1,1>
IF LEN(FIRST.LINE) > 50 THEN
   FIRST.LINE = FIRST.LINE[1,50] : "..."
END
PRINT "    First line: ":FIRST.LINE
PRINT

* Test 3: Search
PRINT "Test 3: Search for text"
UPPER.CONTENT = OCONV(CONTENT, "MCU")
SEARCH.TERM = "HAL"
POS = INDEX(UPPER.CONTENT, SEARCH.TERM, 1)
IF POS > 0 THEN
   PRINT "  PASSED: Search function works"
   PRINT "    Found '":SEARCH.TERM:"' at position ":POS
END ELSE
   PRINT "  WARNING: Search term '":SEARCH.TERM:"' not found"
END
PRINT

* Test 4: Check subdirectories
PRINT "Test 4: Check FEATURES subdirectories"
SUBDIRS = "MEDICAL":@FM:"FINANCIAL":@FM:"PASSWORD":@FM:"VOICE":@FM:"SCHEMA"
BASE.PATH = "C:\qmsys\hal\DOCS\FEATURES"
FOUND.DIRS = 0

FOR I = 1 TO DCOUNT(SUBDIRS, @FM)
   SUBDIR = SUBDIRS<I>
   SUBDIR.PATH = BASE.PATH : "\" : SUBDIR
   TEST.FILES = DIR(SUBDIR.PATH, "*.md")
   IF TEST.FILES # "" THEN
      FOUND.DIRS += 1
      NUM.TEST.FILES = DCOUNT(TEST.FILES, @FM)
      PRINT "    ":SUBDIR:" - ":NUM.TEST.FILES:" files"
   END
NEXT I

IF FOUND.DIRS > 0 THEN
   PRINT "  PASSED: Found ":FOUND.DIRS:" feature directories"
END ELSE
   PRINT "  FAILED: No feature directories found"
END
PRINT

PRINT "All tests completed!"
PRINT

STOP
END

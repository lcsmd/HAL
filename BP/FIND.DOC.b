PROGRAM FIND.DOC
*
* Quick Search for Documentation
* Simple command-line search through all HAL documentation
*
* Usage: FIND.DOC searchterm
*   or: FIND.DOC (will prompt for search term)
*
* Example: FIND.DOC medication
*          FIND.DOC "voice interface"
*

PROMPT ""

* Get search term from command line or prompt
SENTENCE = TRIM(SENTENCE())
IF SENTENCE # "" THEN
   * Remove program name
   SEARCH.TERM = TRIM(FIELD(SENTENCE, " ", 2, 999))
END ELSE
   PRINT "Enter search term: ":
   INPUT SEARCH.TERM
END

IF SEARCH.TERM = "" THEN
   PRINT "Usage: FIND.DOC searchterm"
   STOP
END

PRINT
PRINT "Searching HAL documentation for '":SEARCH.TERM:"'..."
PRINT

BASE.PATH = "C:\qmsys\hal\DOCS"

* Define all subdirectories
SUBDIRS = "SYSTEM":@FM:"ARCHITECTURE":@FM
SUBDIRS := "FEATURES\MEDICAL":@FM:"FEATURES\FINANCIAL":@FM
SUBDIRS := "FEATURES\PASSWORD":@FM:"FEATURES\VOICE":@FM
SUBDIRS := "FEATURES\SCHEMA":@FM:"DEPLOYMENT":@FM
SUBDIRS := "SETUP":@FM:"STATUS":@FM:"DEVELOPMENT":@FM
SUBDIRS := "REFERENCE"

FOUND.COUNT = 0
NUM.DIRS = DCOUNT(SUBDIRS, @FM)

* Search each directory
FOR I = 1 TO NUM.DIRS
   SUBDIR = SUBDIRS<I>
   DIR.PATH = BASE.PATH : "\" : SUBDIR
   FILES = DIR(DIR.PATH, "*.md")
   
   IF FILES # "" THEN
      NUM.FILES = DCOUNT(FILES, @FM)
      FOR J = 1 TO NUM.FILES
         FILE.NAME = FILES<J>
         FILE.PATH = DIR.PATH : "\" : FILE.NAME
         
         OSREAD CONTENT FROM FILE.PATH ELSE CONTINUE
         
         * Case-insensitive search
         UPPER.CONTENT = OCONV(CONTENT, "MCU")
         UPPER.SEARCH = OCONV(SEARCH.TERM, "MCU")
         
         IF INDEX(UPPER.CONTENT, UPPER.SEARCH, 1) THEN
            PRINT "  ":SUBDIR:"\\":FILE.NAME
            FOUND.COUNT += 1
         END
      NEXT J
   END
NEXT I

PRINT
IF FOUND.COUNT = 0 THEN
   PRINT "No matches found."
END ELSE
   PRINT "Found in ":FOUND.COUNT:" file(s)"
END

STOP
END

PROGRAM VIEW.DOC
*
* Interactive Documentation Viewer for HAL
* Allows browsing and viewing all documentation in DOCS directory
*
* Location: C:\qmsys\hal\BP\VIEW.DOC.b
* Compile: COMPILE BP VIEW.DOC
* Catalog: CATALOG BP VIEW.DOC
* Run: VIEW.DOC
*

PROMPT ""
BASE.PATH = "C:\qmsys\hal\DOCS"

* Main menu loop
LOOP
   PRINT @(-1):  ; * Clear screen
   PRINT "HAL Documentation Viewer"
   PRINT STRING("=", 70)
   PRINT
   PRINT "1. System Documentation (Core system docs)"
   PRINT "2. Architecture Documentation (Architectural decisions)"
   PRINT "3. Feature Documentation (Medical, Financial, Password, Voice, Schema)"
   PRINT "4. Deployment Guides (Client deployment, setup)"
   PRINT "5. Setup Guides (Quick starts, installation)"
   PRINT "6. Status Reports (Project status, milestones)"
   PRINT "7. Development Documentation (Naming, organization)"
   PRINT "8. Reference Materials (OpenQM reference, etc.)"
   PRINT "9. Search All Documentation"
   PRINT "0. Exit"
   PRINT
   PRINT "Select: ":
   INPUT CHOICE
   
   BEGIN CASE
      CASE CHOICE = "1"
         CALL VIEW.DIR(BASE.PATH : "\SYSTEM", "System Documentation")
      CASE CHOICE = "2"
         CALL VIEW.DIR(BASE.PATH : "\ARCHITECTURE", "Architecture")
      CASE CHOICE = "3"
         CALL VIEW.FEATURES.MENU(BASE.PATH)
      CASE CHOICE = "4"
         CALL VIEW.DIR(BASE.PATH : "\DEPLOYMENT", "Deployment Guides")
      CASE CHOICE = "5"
         CALL VIEW.DIR(BASE.PATH : "\SETUP", "Setup Guides")
      CASE CHOICE = "6"
         CALL VIEW.DIR(BASE.PATH : "\STATUS", "Status Reports")
      CASE CHOICE = "7"
         CALL VIEW.DIR(BASE.PATH : "\DEVELOPMENT", "Development Docs")
      CASE CHOICE = "8"
         CALL VIEW.DIR(BASE.PATH : "\REFERENCE", "Reference Materials")
      CASE CHOICE = "9"
         CALL SEARCH.ALL.DOCS(BASE.PATH)
      CASE CHOICE = "0"
         EXIT
      CASE 1
         PRINT "Invalid choice"
         SLEEP 1
   END CASE
REPEAT

STOP
END

*
* View files in a directory
*
SUBROUTINE VIEW.DIR(DIR.PATH, TITLE)
   FILES = DIR(DIR.PATH, "*.md")
   
   IF FILES = "" THEN
      PRINT @(-1):
      PRINT "No files found in ":TITLE
      PRINT
      PRINT "Press ENTER to continue...":
      INPUT DUMMY
      RETURN
   END
   
   NUM.FILES = DCOUNT(FILES, @FM)
   
   LOOP
      PRINT @(-1):
      PRINT TITLE
      PRINT STRING("=", 70)
      PRINT
      
      FOR I = 1 TO NUM.FILES
         FILE.NAME = FILES<I>
         * Truncate long filenames for display
         IF LEN(FILE.NAME) > 60 THEN
            DISPLAY.NAME = FILE.NAME[1,57] : "..."
         END ELSE
            DISPLAY.NAME = FILE.NAME
         END
         PRINT FMT(I, "2R"):". ":DISPLAY.NAME
      NEXT I
      
      PRINT
      PRINT "Enter file number to view (0 to go back): ":
      INPUT FILE.NUM
      
      IF FILE.NUM = "0" OR FILE.NUM = "" THEN RETURN
      
      IF FILE.NUM > 0 AND FILE.NUM <= NUM.FILES THEN
         FILE.NAME = FILES<FILE.NUM>
         FILE.PATH = DIR.PATH : "\" : FILE.NAME
         CALL VIEW.FILE.CONTENT(FILE.PATH, FILE.NAME)
      END ELSE
         PRINT "Invalid selection"
         SLEEP 1
      END
   REPEAT
RETURN
END

*
* View file content with paging
*
SUBROUTINE VIEW.FILE.CONTENT(FILE.PATH, FILE.NAME)
   OSREAD CONTENT FROM FILE.PATH ELSE
      PRINT @(-1):
      PRINT "Error reading file: ":FILE.NAME
      PRINT
      PRINT "Press ENTER to continue...":
      INPUT DUMMY
      RETURN
   END
   
   * Display file
   PRINT @(-1):
   PRINT "File: ":FILE.NAME
   PRINT STRING("=", 70)
   PRINT
   
   * Split into lines for paging
   CONVERT @FM TO @VM IN CONTENT
   NUM.LINES = DCOUNT(CONTENT, @VM)
   
   * Display 20 lines at a time
   PAGE.SIZE = 20
   START.LINE = 1
   
   LOOP
      END.LINE = START.LINE + PAGE.SIZE - 1
      IF END.LINE > NUM.LINES THEN END.LINE = NUM.LINES
      
      FOR I = START.LINE TO END.LINE
         LINE = CONTENT<1,I>
         PRINT LINE
      NEXT I
      
      IF END.LINE >= NUM.LINES THEN
         PRINT
         PRINT "[End of file]"
         PRINT
         PRINT "Press ENTER to return...":
         INPUT DUMMY
         EXIT
      END ELSE
         PRINT
         PRINT "[Showing lines ":START.LINE:"-":END.LINE:" of ":NUM.LINES:"]"
         PRINT "Press ENTER for more, Q to quit...":
         INPUT MORE
         IF OCONV(MORE, "MCU") = "Q" THEN EXIT
         START.LINE = END.LINE + 1
         PRINT @(-1):
      END
   REPEAT
RETURN
END

*
* Features submenu
*
SUBROUTINE VIEW.FEATURES.MENU(BASE.PATH)
   LOOP
      PRINT @(-1):
      PRINT "Feature Documentation"
      PRINT STRING("=", 70)
      PRINT
      PRINT "1. Medical Features (Epic API, medical records)"
      PRINT "2. Financial Features (Transactions, AI classification)"
      PRINT "3. Password Manager"
      PRINT "4. Voice Interface (Voice commands, wake word)"
      PRINT "5. Schema System (Database schema)"
      PRINT "0. Back to Main Menu"
      PRINT
      PRINT "Select: ":
      INPUT CHOICE
      
      BEGIN CASE
         CASE CHOICE = "1"
            CALL VIEW.DIR(BASE.PATH : "\FEATURES\MEDICAL", "Medical Features")
         CASE CHOICE = "2"
            CALL VIEW.DIR(BASE.PATH : "\FEATURES\FINANCIAL", "Financial Features")
         CASE CHOICE = "3"
            CALL VIEW.DIR(BASE.PATH : "\FEATURES\PASSWORD", "Password Manager")
         CASE CHOICE = "4"
            CALL VIEW.DIR(BASE.PATH : "\FEATURES\VOICE", "Voice Interface")
         CASE CHOICE = "5"
            CALL VIEW.DIR(BASE.PATH : "\FEATURES\SCHEMA", "Schema System")
         CASE CHOICE = "0"
            EXIT
         CASE 1
            PRINT "Invalid choice"
            SLEEP 1
      END CASE
   REPEAT
RETURN
END

*
* Search all documentation
*
SUBROUTINE SEARCH.ALL.DOCS(BASE.PATH)
   PRINT @(-1):
   PRINT "Search Documentation"
   PRINT STRING("=", 70)
   PRINT
   PRINT "Enter search term (or ENTER to cancel): ":
   INPUT SEARCH.TERM
   
   IF SEARCH.TERM = "" THEN RETURN
   
   PRINT
   PRINT "Searching for '":SEARCH.TERM:"'..."
   PRINT
   
   * Define all subdirectories to search
   SUBDIRS = "SYSTEM":@FM:"ARCHITECTURE":@FM
   SUBDIRS := "FEATURES\MEDICAL":@FM:"FEATURES\FINANCIAL":@FM
   SUBDIRS := "FEATURES\PASSWORD":@FM:"FEATURES\VOICE":@FM
   SUBDIRS := "FEATURES\SCHEMA":@FM:"DEPLOYMENT":@FM
   SUBDIRS := "SETUP":@FM:"STATUS":@FM:"DEVELOPMENT":@FM
   SUBDIRS := "REFERENCE"
   
   RESULTS = ""
   FOUND.COUNT = 0
   NUM.DIRS = DCOUNT(SUBDIRS, @FM)
   
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
            
            * Convert to uppercase for case-insensitive search
            UPPER.CONTENT = OCONV(CONTENT, "MCU")
            UPPER.SEARCH = OCONV(SEARCH.TERM, "MCU")
            
            IF INDEX(UPPER.CONTENT, UPPER.SEARCH, 1) THEN
               FOUND.COUNT += 1
               RESULT.LINE = SUBDIR : "\" : FILE.NAME
               RESULTS<FOUND.COUNT> = RESULT.LINE
               PRINT FMT(FOUND.COUNT, "3R"):". ":RESULT.LINE
            END
         NEXT J
      END
   NEXT I
   
   PRINT
   IF FOUND.COUNT = 0 THEN
      PRINT "No matches found for '":SEARCH.TERM:"'"
   END ELSE
      PRINT "Found ":FOUND.COUNT:" file(s) containing '":SEARCH.TERM:"'"
      PRINT
      PRINT "Enter file number to view (0 to cancel): ":
      INPUT FILE.NUM
      
      IF FILE.NUM > 0 AND FILE.NUM <= FOUND.COUNT THEN
         RESULT.PATH = RESULTS<FILE.NUM>
         FILE.PATH = BASE.PATH : "\" : RESULT.PATH
         * Extract just the filename for display
         FILE.NAME = FIELD(RESULT.PATH, "\", DCOUNT(RESULT.PATH, "\"))
         CALL VIEW.FILE.CONTENT(FILE.PATH, FILE.NAME)
      END
   END
   
   IF FOUND.COUNT > 0 THEN
      PRINT
      PRINT "Press ENTER to continue...":
      INPUT DUMMY
   END
RETURN
END

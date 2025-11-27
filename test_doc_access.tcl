* Test documentation access
* Quick test to verify DIR() and OSREAD work

PRINT "Testing documentation access..."
PRINT

* Test 1: DIR() function
PRINT "Test 1: Listing SYSTEM directory..."
FILES = DIR("C:\qmsys\hal\DOCS\SYSTEM", "*.md")
IF FILES = "" THEN
   PRINT "ERROR: No files found"
END ELSE
   NUM.FILES = DCOUNT(FILES, @FM)
   PRINT "SUCCESS: Found ":NUM.FILES:" files"
   FOR I = 1 TO MINIMUM(5, NUM.FILES)
      PRINT "  - ":FILES<I>
   NEXT I
END
PRINT

* Test 2: OSREAD function
PRINT "Test 2: Reading INDEX.md..."
FILE.PATH = "C:\qmsys\hal\DOCS\SYSTEM\INDEX.md"
OSREAD CONTENT FROM FILE.PATH ELSE
   PRINT "ERROR: Could not read file"
   STOP
END

* Get first few lines
CONVERT @FM TO @VM IN CONTENT
NUM.LINES = DCOUNT(CONTENT, @VM)
PRINT "SUCCESS: Read ":NUM.LINES:" lines"
PRINT "First line: ":CONTENT<1,1>
PRINT

* Test 3: Search functionality
PRINT "Test 3: Searching for 'documentation'..."
UPPER.CONTENT = OCONV(CONTENT, "MCU")
IF INDEX(UPPER.CONTENT, "DOCUMENTATION", 1) THEN
   PRINT "SUCCESS: Search term found"
END ELSE
   PRINT "WARNING: Search term not found"
END
PRINT

PRINT "All basic tests completed!"

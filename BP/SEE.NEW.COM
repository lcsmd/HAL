* SEE.NEW.COM - Review new commands in COM file
* Reads from last viewed ID in CONTROL file
* Shows command/output pairs
* SPACE=next, UP ARROW=previous, Q=quit
* Updates CONTROL with last viewed ID when you quit
* Usage: RUN BP SEE.NEW.COM

PROGRAM SEE.NEW.COM

* Special keys
ESC = CHAR(27)
UP.ARROW = CHAR(27):CHAR(91):CHAR(65)

* Open files
OPEN "COM" TO COM.FH ELSE
   CRT "Cannot open COM file"
   STOP
END

OPEN "CONTROL" TO CTRL.FH ELSE
   CRT "Cannot open CONTROL file"
   STOP
END

* Get last viewed ID
READ LAST.ID FROM CTRL.FH, "LAST.COM.ID" ELSE
   LAST.ID = ""
END

IF LAST.ID = "" THEN
   CRT "No last ID found. Starting from beginning."
   LAST.ID = "0"
END

CRT "Last viewed: ":LAST.ID
CRT "Searching for new commands..."
CRT ""

* Select all COM records greater than last ID
IF LAST.ID = "0" THEN
   EXECUTE "SSELECT COM" CAPTURING OUTPUT
END ELSE
   EXECUTE "SSELECT COM WITH @ID > '":LAST.ID:"'" CAPTURING OUTPUT
END

SELECT.COUNT = OCONV(OUTPUT, "MC/N")
IF SELECT.COUNT = 0 THEN
   CRT "No new commands to review"
   STOP
END

CRT SELECT.COUNT:" new record(s) selected"
CRT ""

* Build array of all IDs to allow navigation
DIM ID.LIST(1000)
ID.COUNT = 0

LOOP
   READNEXT INPUT.ID ELSE EXIT
   IF INPUT.ID[-1,1] = "O" THEN CONTINUE
   ID.COUNT += 1
   ID.LIST(ID.COUNT) = INPUT.ID
REPEAT

IF ID.COUNT = 0 THEN
   CRT "No command pairs found"
   STOP
END

* Navigate through pairs
CURRENT.POS = 1
QUIT.FLAG = 0

LOOP
   IF CURRENT.POS < 1 THEN CURRENT.POS = 1
   IF CURRENT.POS > ID.COUNT THEN CURRENT.POS = ID.COUNT
   
   INPUT.ID = ID.LIST(CURRENT.POS)
   
   * Get the input command
   READ CMD FROM COM.FH, INPUT.ID ELSE
      CMD = "(Command not found)"
   END
   
   * Get corresponding output ID
   BASE.ID = INPUT.ID[1,LEN(INPUT.ID)-1]
   OUTPUT.ID = BASE.ID:"O"
   
   * Get the output
   READ OUTPUT.TEXT FROM COM.FH, OUTPUT.ID ELSE
      OUTPUT.TEXT = "(No output found)"
   END
   
   * Clean control characters from output for display
   DISPLAY.TEXT = OUTPUT.TEXT
   DISPLAY.TEXT = CONVERT(CHAR(1):CHAR(2):CHAR(3):CHAR(4):CHAR(5):CHAR(6):CHAR(7):CHAR(8):CHAR(11):CHAR(12):CHAR(13):CHAR(14):CHAR(15), "", DISPLAY.TEXT)
   DISPLAY.TEXT = CONVERT(CHAR(16):CHAR(17):CHAR(18):CHAR(19):CHAR(20):CHAR(21):CHAR(22):CHAR(23):CHAR(24):CHAR(25):CHAR(26):CHAR(27):CHAR(28):CHAR(29):CHAR(30):CHAR(31), "", DISPLAY.TEXT)
   
   * Clear screen and display
   CRT ESC:"[2J":ESC:"[H"
   CRT STR("=", 70)
   CRT "Command ":CURRENT.POS:" of ":ID.COUNT
   CRT "ID: ":INPUT.ID
   CRT STR("=", 70)
   CRT ""
   CRT "COMMAND:"
   CRT CMD
   CRT ""
   CRT "OUTPUT:"
   CRT DISPLAY.TEXT
   CRT ""
   CRT STR("=", 70)
   CRT "SPACE=Next  UP ARROW=Previous  Q=Quit"
   CRT ""
   
   * Wait for key
   INPUT KEY.IN, 1
   
   * Check for escape sequences (arrow keys)
   IF KEY.IN = CHAR(27) THEN
      * Might be arrow key, read next chars
      INPUT ARROW.SEQ, 2
      FULL.KEY = KEY.IN:ARROW.SEQ
      
      IF FULL.KEY = UP.ARROW THEN
         * Go to previous
         CURRENT.POS -= 1
      END ELSE
         * Just escape, ignore
      END
   END ELSE
      * Regular key
      KEY.IN = OCONV(KEY.IN, "MCU")
      
      IF KEY.IN = "Q" THEN
         QUIT.FLAG = 1
         EXIT
      END ELSE
         * Space or any other key = next
         CURRENT.POS += 1
         IF CURRENT.POS > ID.COUNT THEN
            * At end
            EXIT
         END
      END
   END
REPEAT

* Save the last viewed ID
VIEWED.ID = ID.LIST(CURRENT.POS)

* Update last viewed ID in CONTROL
IF VIEWED.ID # LAST.ID THEN
   WRITE VIEWED.ID TO CTRL.FH, "LAST.COM.ID"
   CRT ""
   CRT "Last viewed ID updated to: ":VIEWED.ID
END

CRT ""
CRT "Reviewed commands"

STOP
END

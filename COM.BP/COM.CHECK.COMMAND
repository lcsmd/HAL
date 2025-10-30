PROGRAM COM.CHECK.COMMAND
*
* Check status and results of a submitted command
* Usage: COM.CHECK.COMMAND <command-id>
*

PROMPT ""

* Get command ID
CMD = TRIM(SENTENCE())
SPACE.POS = INDEX(CMD, " ", 1)
IF SPACE.POS > 0 THEN
   cmd_id = TRIM(CMD[SPACE.POS+1, 999])
END ELSE
   cmd_id = ""
END

IF cmd_id = "" THEN
   CRT "Usage: COM.CHECK.COMMAND <command-id>"
   CRT "Example: COM.CHECK.COMMAND 21118-5588"
   STOP
END

* Open command queue
OPEN "COMMAND.QUEUE" TO F.QUEUE ELSE
   CRT "ERROR: Cannot open COMMAND.QUEUE"
   STOP
END

* Read command record
READ cmd_rec FROM F.QUEUE, cmd_id ELSE
   CRT "ERROR: Command not found: ": cmd_id
   STOP
END

* Display command details
CRT
CRT "Command ID: ": cmd_id
CRT STR("=",70)
CRT "Command: ": cmd_rec<1>
CRT "Status: ": cmd_rec<2>
CRT "Submitted: ": OCONV(cmd_rec<3>, "D4-") : " " : OCONV(cmd_rec<4>, "MTS")

IF cmd_rec<2> = "COMPLETE" OR cmd_rec<2> = "ERROR" THEN
   CRT "Completed: ": OCONV(cmd_rec<7>, "D4-") : " " : OCONV(cmd_rec<8>, "MTS")
END

CRT STR("-",70)

* Display output or error
IF cmd_rec<2> = "ERROR" THEN
   CRT "ERROR: ": cmd_rec<6>
END ELSE IF cmd_rec<2> = "COMPLETE" THEN
   CRT "Output:"
   CRT cmd_rec<5>
END ELSE
   CRT "Status: ": cmd_rec<2>
END

CRT STR("=",70)

STOP
END

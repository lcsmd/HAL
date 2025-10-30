PROGRAM COM.SUBMIT.COMMAND
*
* Submit a command to the command service
* Usage: COM.SUBMIT.COMMAND <command>
*

PROMPT ""

* Get command from command line
CMD = TRIM(SENTENCE())
SPACE.POS = INDEX(CMD, " ", 1)
IF SPACE.POS > 0 THEN
   command = TRIM(CMD[SPACE.POS+1, 999])
END ELSE
   command = ""
END

IF command = "" THEN
   CRT "Usage: COM.SUBMIT.COMMAND <command>"
   CRT "Example: COM.SUBMIT.COMMAND LIST TRANSACTION SAMPLE 5"
   STOP
END

* Open command queue
OPEN "COMMAND.QUEUE" TO F.QUEUE ELSE
   CRT "ERROR: Cannot open COMMAND.QUEUE"
   CRT "Run COM.COMMAND.SERVICE first"
   STOP
END

* Generate command ID
cmd_id = DATE() : "-" : TIME()

* Create command record
cmd_rec = ""
cmd_rec<1> = command
cmd_rec<2> = "PENDING"
cmd_rec<3> = DATE()
cmd_rec<4> = TIME()

WRITE cmd_rec TO F.QUEUE, cmd_id

CRT "Command submitted: ": cmd_id
CRT "Command: ": command
CRT
CRT "Check status with: COM.CHECK.COMMAND ": cmd_id

STOP
END

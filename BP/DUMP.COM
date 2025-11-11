PROGRAM DUMP.COM
* Dump all COM records to screen
OPEN "COM" TO F ELSE STOP
EXECUTE "SSELECT COM" CAPTURING IDS
NUM.IDS = DCOUNT(IDS, @AM)
CRT "Total records: ":NUM.IDS
FOR I = 1 TO NUM.IDS
   ID = IDS<I>
   READ REC FROM F, ID THEN
      CRT "================================"
      CRT "ID: ":ID
      CRT "Length: ":LEN(REC)
      CRT "Content:"
      CRT REC[1,500]
      CRT ""
   END
NEXT I
STOP
END

     PROMPT ""
     LM = 1
     FILE.NAME = ""
     TYPE = TRIM(FIELD(@SENTENCE," ",2))
     IVAL = INDEX('PCVQ',TYPE,1)
     FILE.NAME = ""
     LOOP
          IF TYPE = "P" THEN FILE.NAME = "PRODUCT"
          IF TYPE = "C" THEN FILE.NAME = "CUSTOMER"
          IF TYPE = "V" THEN FILE.NAME = "VM"
          IF TYPE = 'Q' THEN STOP
     WHILE FILE.NAME = "" DO
          PRINT @(-1):"ENTER FILE TO RESTORE ITEM TO (P)roduct, (C)ustomer, OR (V)endor:":;INPUT TYPE,1
     REPEAT

     OPEN FILE.NAME TO F.FILE.NAME ELSE PRINT FILE.NAME ; STOP
     OPEN FILE.NAME:'.ARC' TO F.FILE.NAME.ARC ELSE PRINT FILE.NAME:'.ARC' ; STOP

     PNO = TRIM(FIELD(@SENTENCE," ",3))
     IF PNO ="" THEN
          PRINT "Enter numeric ":FILE.NAME:" numbers to restore OR search term"
          PRINT "Enter each number followed by return.   Q to exit"
          LOOP
               INPUT PNO
          WHILE PNO <> "Q" DO
               IF NOT(NUM(PNO)) THEN GOSUB DISPLAY.FILE:
               GOSUB RESTORE:
          REPEAT
     END ELSE

          GOSUB RESTORE:
     END
     STOP
RESTORE:
     IF TYPE = 'P' THEN
          KEY = "!":PNO
     END ELSE KEY = PNO
     READ PROD.B FROM F.FILE.NAME.ARC,KEY THEN
          WRITE PROD.B ON F.FILE.NAME,KEY
          PRINT FILE.NAME:" ":PNO:" RESTORED FROM ARCHIVE"
     END ELSE
          PRINT PNO:" NOT FOUND IN ARCHIVE"
     END
     RETURN

DISPLAY.FILE:
     BUFF=0
     EXECUTE "TERM 90"
     SELECT.STR = 'SORT ':FILE.NAME:'.ARC WITH ':FILE.NAME:'.INDEX = [':PNO:'] @SHOW HDR.SUP'
     IF LM THEN PRINT "SEARCHING ":FILE.NAME:".ARC"
     EXECUTE SELECT.STR CAPTURING CAP
     GOSUB DISPLAY20:
     LOOP
          PRINT "HIT SPACE FOR MORE OR Q TO QUIT OR TAB TO ENTER A NUMBER:":;INPUT ANS,1
          IF ANS = 'Q' THEN STOP
          IF ANS = ' ' THEN
               BUFF:=20
               GOSUB DISPLAY20:
          END
          IF ANS = CHAR(9) THEN
               INPUT ANS
          END
     UNTIL NUM(ANS) REPEAT
     PNO = ANS
     EXECUTE "TERM 79"
     RETURN

DISPLAY20:
     COUNT = DCOUNT(CAP,@FM)
     PRINT @(-1):
     RESULTS = CAP<COUNT-1>
     CAP<2>:=RESULTS
     FOR LX = 1 TO 21
          PRINT CAP<BUFF+LX>
     NEXT LX
     RETURN

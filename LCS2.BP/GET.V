     OPEN 'INVENT' TO F.INV ELSE STOP
     OPEN 'VEND.ABB' TO F.VA ELSE STOP
     **** INVENT - START OF EQU section
     INCLUDE FILE.EQU INVENT.EQ

     PROMPT ''
     P = 0
     MODE = TRIM(FIELD(@SENTENCE," ",2))
     IF  MODE # "RESET" AND MODE # "CONNECT" AND MODE # "VEND" THEN
          PRINT "DEFAULTING TO CONNECT MODE"
          MODE = "CONNECT"
     END
     IF MODE='RESET' THEN
          PRINT "CLEARING VEND.ABB"
          EXECUTE "CLEAR-FILE DATA VEND.ABB"
          SELECT.STR = "SSELECT INVENT BY DESC1"
     END
     IF MODE='CONNECT' THEN
          PRINT "FINDING UNMATCHED INVENTORY"
          SELECT.STR = "SSELECT INVENT BY DESC1 WITHOUT PS_NUM"
     END
     IF MODE = 'VEND' THEN
          PRINT "FINDING UNPARSED INVENTORY"
          SELECT.STR = "SSELECT INVENT BY DESC1 WITHOUT VEND_ABB"
     END
     PRINT SELECT.STR
     EXECUTE SELECT.STR CAPTURING CAP
     PRINT CAP
     INV.CT = FIELD(CAP<2>," ",1)
     DONE=0
     IF INV.CT > 0 THEN
          READLIST INV.KEYS THEN
               PRINT "LOADING ":INV.CT:" ITERMS FROM INVENTORY...":
               FOR X = 1 TO INV.CT
                    INV.K = INV.KEYS<X>
                    READ INV.B FROM F.INV,INV.K THEN
                         PRINT INV.K
                         INV.B.O = INV.B
                         IF MODE='RESET' THEN
                              INV.VEND_ABB = ""
                              WRITE INV.B ON F.INV,INV.K
                         END ELSE
                              IF MODE='CONNECT' THEN
                                   GOSUB FIND.PSNUM:
                              END ELSE
                                   GOSUB MATCH.VEND:
                              END
                         END
                    END
                    IF NOT(MOD(X,100)) THEN PRINT "*":
               UNTIL DONE
               NEXT X
          END
     END
     PRINT
     STOP


MATCH.VEND:
     PRINT @(-1):
     FOR L = 1 TO 19
          M = L + P
          PRINT INV.KEYS<M> "L#8 ":inv.desc1<M>
     NEXT L
     C = P + 1
     PRINT @(2,21):
     FOR CHOICE = 1 TO 7
          CHOICE.S = CHOICE
          PRINT CHOICE.S:") ":inv.desc1<P+1>[1,CHOICE+1]:"  ":
     NEXT CHOICE
     PRINT @(2,22):
     FOR CHOICE = 8 TO 11
          CHOICE.S = CHOICE
          IF CHOICE = 10 THEN CHOICE.S = "A"
          IF CHOICE = 11 THEN CHOICE.S = "B"
          PRINT CHOICE.S:") ":inv.desc1<P+1>[1,CHOICE+1]:"  ":
     NEXT CHOICE
     PRINT
     PRINT "CHOICE: (0,1-B,Q,. TO LIMIT, Enter for manual)":
     INPUT CHOICE.ANS,1
     IF CHOICE.ANS = "." THEN
          PRINT @(40):"ENTER <CHOICE> <ROW.COUNT>:":
          INPUT CHOICE.ROWS
          CHOICE.ANS = FIELD(CHOICE.ROWS," ",1)
          LIMIT = FIELD(CHOICE.ROWS," ",2)
     END ELSE
          LIMIT = 9999
     END
     IF CHOICE.ANS = "A" THEN CHOICE.ANS = "10"
     IF CHOICE.ANS = "B" THEN CHOICE.ANS = "11"
     IF CHOICE.ANS = "Q" THEN
          DONE = 2
          IF CHOICE.ANS = "" THEN
               PRINT @(40):"ENTER VENDOR ABB:":
               INPUT VEND.ABB.C
          END ELSE
               IF (NUM(CHOICE.ANS) AND CHOICE.ANS < 12) THEN
                    VEND.ABB.C = inv.desc1<P+1>[1,CHOICE.ANS+1]
               END
          END
          IF VEND.ABB.C THEN
               GOSUB REMOVE.DONE:
               GOSUB ADD.VEND.ABB:
          END
     END
     RETURN


REMOVE.DONE:
     VEND.ABB.CT = 0
     LV = LEN(VEND.ABB.C)
     LOOP WHILE (inv.desc1<P+1>[1,LV] = VEND.ABB.C AND VEND.ABB.CT <= LIMIT) DO
          INV.VEND.ABB<P+1> = VEND.ABB.C
          WRITEV VEND.ABB.C ON F.INV,INV.KEYS<P+1>,28
          P += 1
          VEND.ABB.CT += 1
     REPEAT
     RETURN

ADD.VEND.ABB:
     READV EXISTS FROM F.VA,VEND.ABB.C,0 ELSE
          WRITEV VEND.ABB.CT ON F.VA,VEND.ABB.C,1
     END
     RETURN


FIND.PSNUM:
     IF INV.UCAT THEN
     PRINT "LOOKING FOR:":INV.UCAT:
          SELECT.STR2 = "SELECT I2.KEYS WITH UCAT = ":INV.UCAT
          DONE2=0
          LOOP UNTIL (INV.PS_NUM OR DONE2 > 1)
               EXECUTE SELECT.STR2 CAPTURING CAP
               ITEMS.C = FIELD(CAP<2>," ",1)
               IF ITEMS.C > 0 THEN
                    READLIST ITEMS THEN
                         IF ITEMS.C = 1 THEN
                              INV.PS_NUM = ITEMS
                              PRINT "  FOUND ":INV.PS_NUM
                         END ELSE
                              INV.ITEMLIST = CHANGE(ITEMS,@FM,@VM)
                              INV.ITEM.CT = ITEMS.C
                              DONE2=2
                              PRINT " FOUND ":INV.ITEM.CT:"  ":INV.ITEMLIST
                         END
                    END
               END ELSE
                    DONE2+=1
                    SELECT.STR2 := "]"
                    IF DONE = 2 THEN PRINT " NOT FOUND"
               END
          REPEAT
          IF INV.B <> INV.B.O THEN WRITE INV.B ON F.INV,INV.K
     END
     RETURN

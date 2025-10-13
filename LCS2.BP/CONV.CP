     PROGRAM CONV.CP
     OPEN 'CUSTOM.PRICES' TO CP ELSE PRINT 'CP';STOP
     ATTS="1,3,4,5,6,7,12"
     FMT="D4-,D4-,D4-,MD4,MD4,MD4,D4-"
     ATTS=CHANGE(ATTS,",",@FM)
     FMT=CHANGE(FMT,",",@FM)
     SELECT CP
     CT=0
     LOOP
          CT+=1
     WHILE READNEXT AA DO
          READ CUS.B.O FROM CP,AA THEN
               CUS.B = CUS.B.O
               FOR X = 1 TO 7
                    VAL = CUS.B.O<ATTS<X>
                    CONV = FMT<X>
                    CUS.B<ATTS<X>> = ICONV(CUS.B.O<ATTS<X>>,FMT<X>)
               NEXT X
               IF CUS.B <> CUS.B.O THEN
                    WRITE CUS.B ON CP,AA
                    PRINT CUS.B.O:"  ------->  "
                    PRINT CUS.B
                    PRINT
               END
          END
          PRINT CT
     REPEAT
     PRINT "FINISHED"
     STOP


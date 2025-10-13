     FN = TRIM(FIELD(@SENTENCE," ",2))
     OPEN 'DICT',FN TO D_FILE ELSE PRINT "DICT,":FN;STOP
     SELECT.STR = "SELECT DICT ":FN
     EXECUTE SELECT.STR CAPTURING CAP
     LOOP WHILE READNEXT D DO
          L=LEN(D)
          IF RIGHT(D,2) = ".D" THEN
               D2 = LEFT(D,L-2)
               READ DBUFF FROM D_FILE,D THEN
                    WRITE DBUFF ON D_FILE,D2
                    DELETE D_FILE,D
               END
          END
     REPEAT

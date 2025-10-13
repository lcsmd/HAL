     OPEN 'INVOICE' TO INVOICE ELSE STOP
     OPEN 'INVOICE.B' TO INVOICE.B ELSE STOP

     CT=0
     SELECT INVOICE
     LOOP WHILE READNEXT INV DO
          CT+=1
          PRINT CT
          READV LINES1 FROM INVOICE,INV,1 THEN
               READV LINES2 FROM INVOICE.B,INV,1 THEN
                    PRINT LINES1
                    PRINT LINES2
                    PRINT
                    IF LINES1 <> LINES2 THEN
                         *WRITEV LINES2 ON INVOICE,INV,1
                    END
               END
          END
     REPEAT

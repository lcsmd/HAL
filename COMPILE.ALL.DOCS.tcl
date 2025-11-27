* Compile all documentation programs
* Run with: TCL COMPILE.ALL.DOCS.tcl

LOGTO HAL

PRINT "Compiling Documentation Programs"
PRINT STRING("=", 70)
PRINT

* Program list
PROGRAMS = "VIEW.DOC":@FM:"FIND.DOC":@FM:"TEST.DOC.ACCESS"
NUM.PROGRAMS = DCOUNT(PROGRAMS, @FM)

SUCCESS.COUNT = 0
FAIL.COUNT = 0

FOR I = 1 TO NUM.PROGRAMS
   PROG = PROGRAMS<I>
   
   PRINT "Compiling ":PROG:"...":
   
   * Compile the program
   EXECUTE "BASIC BP ":PROG CAPTURING OUTPUT RETURNING STATUS
   
   IF STATUS = 0 THEN
      PRINT " SUCCESS"
      SUCCESS.COUNT += 1
      
      * Catalog it
      PRINT "  Cataloging ":PROG:"...":
      EXECUTE "CATALOG BP ":PROG CAPTURING CAT.OUTPUT RETURNING CAT.STATUS
      
      IF CAT.STATUS = 0 THEN
         PRINT " SUCCESS"
      END ELSE
         PRINT " FAILED"
         IF CAT.OUTPUT # "" THEN PRINT "  ":CAT.OUTPUT
      END
   END ELSE
      PRINT " FAILED"
      FAIL.COUNT += 1
      IF OUTPUT # "" THEN
         PRINT "Error output:"
         PRINT OUTPUT
      END
   END
   PRINT
NEXT I

PRINT STRING("=", 70)
PRINT "Summary: ":SUCCESS.COUNT:" succeeded, ":FAIL.COUNT:" failed"

      *$INCLUDE UNIVERSE.INC

      * Define common constants
      EOL = CHAR(13) : CHAR(10)  * End of line character

      * Define common variables
      COMMON /FileVars/ FileVar, DictFile
      COMMON /RecordVars/ Record, DictRec
      *COMMON /FieldVars/ FieldValue, Line, EachField, FieldNumber
      COMMON /CommandVars/ Command, CmdOutput
      COMMON /NEXTREC/

      * Include other necessary headers
      *$INCLUDE QMBASIC.INC
      *COMMON /NEXTREC/ NEXT_IDS(10)


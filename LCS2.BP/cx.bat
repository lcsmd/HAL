      program cx.bat
      $DEBUG
      execute 'CLEAR.FILE DATA TRANS'
      execute 'CLEAR.FILE DATA LCS.CSV'
      execute 'CLEAR.FILE DATA LCS.CSV2'
      execute 'CLEAR.FILE DATA CONTROL'
      execute 'CLEAR.FILE DATA ACCOUNT'
      execute 'CLEAR.FILE DATA STATEMENT'

      file.name = field(@sentence, ' ', 2)
      list.name = field(@sentence, ' ', 3)
      if file.name = "" then file.name = "LCS.TXT"
      lm=1
      if list.name then
         select.str  = "GET-LIST ":list.name
      end else
         select.str = "SELECT ":file.name
      end
      if lm then print select.str
      execute select.str
      ct=0
      eof = 0
      loop
      while eof = 0
         ct+=1
         readnext item.name then
            cmd.string = "CX ":file.name:",":item.name
            if lm then print cmd.string
            execute cmd.string
            input ams,1
            if ams = q then stop
         end else
            eof =1
         end
      repeat
      print ct:" items converted"
      end



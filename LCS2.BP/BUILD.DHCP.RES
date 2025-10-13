*---> Recovered document: BUILD.DHCP.RES
     EQU SCOPEID TO VAL<2>, IPADDRESS TO VAL<3>, SERVERNAME TO VAL<1>, MAC TO VAL<4>, NAME TO VAL<5>, DESC TO VAL<6>

     OPEN 'DHCP' TO DHCP ELSE PRINT 'DHCP';STOP
     OPEN 'DHCP.RES' TO DHCP.RES ELSE PRINT 'DHCP.RES';STOP
     OPEN 'LCS.CONTROL' TO LCS.CONTROL ELSE PRINT 'LCS.CONTROL'; STOP
     OPEN 'LCS.SCRIPTS' TO LCS.SCRIPT ELSE PRINT 'LCS.SCRIPT';STOP
     READ DEF.SERVER FROM LCS.CONTROL,"DHCP.DEF.SERVER" ELSE DEF.SERVER = ""
     READ DEF.SCOPE FROM LCS.CONTROL,"DHCP.DEF.SCOPE" ELSE DEF.SCOPE = ""

     *DHCP IN FORMAT RES.ID:SERVER,SCOPEID,IPADD,MAC,NAME,DESC

     VAL=""
     LABELS = ""

     IF NOT(DEF.SERVER) THEN DEF.SERVER = "hg3.ce.local"
     IF NOT(DEF.SCOPE) THEN DEF.SCOPE = "10.0.0.0"
     LABELS = "@ServerName@,@ScopeId@,@IPAddress@,@MacAddress@,@Name@,@Desc@"
     LABELS = CHANGE(LABELS,",",@FM)
     LABEL.CT = DCOUNT(LABELS,@FM)

     CT = 0
     SELECT DHCP
     DHCP.PS1 = ""
     LOOP
          CT+=1
     WHILE READNEXT RES.ID DO
          READ BUFF FROM DHCP,RES.ID THEN
               PS.CMD = 'ADD-DhcpServerV4Reservation -ScopeId @ScopeId@ -IPAdDress @IPAddress@ -computername @ServerName@ -clientid @MacAddress@ -Name @Name@ -Description "@Desc@"'
               OBUFF = BUFF
               IF BUFF<1> THEN SERVERNAME = BUFF<1> ELSE SERVERNAME = DEF.SERVER
               IF BUFF<2> THEN SCOPEID = BUFF<2> ELSE SCOPEID = DEF.SCOPE
               IPADDRESS = BUFF<3>
               MAC = BUFF<4>
               NAME = BUFF<5>
               MAC = TRIM(MAC,":","A")
               IF MAC[1,4] = "0004" THEN
                    NAME = "Polycom_":MAC
                    DESC = NAME
               END ELSE

                    DESC = NAME:"_":MAC
               END
               GOSUB SWAP.VALUES2:
               DHCP.PS1<-1> = PS.CMD
               PS.CMD = CHANGE(PS.CMD,@FM,@VM)
               BUFF<5> = PS.CMD
               IF OBUFF <> BUFF THEN WRITE BUFF ON DHCP.RES,RES.ID
               *EXECUTE "PSHELL PS.CMD"
          END
     REPEAT

     WRITE DHCP.PS1 ON LCS.SCRIPT,"BUILD-DHCP.PS1"
     PRINT "FINISHED"
     STOP
     **EMAIL.CMD = 'Send-MailMessage -From "@FromEmailAddress@" -Subject "@Subject@" -To "@ToEmailAddress@" -Attachments "@Attachment@" -Bcc "@Bcc@" -Body "@Body@" -Cc "@CC@" -DeliveryNotificationOption OnSuccess,OnFailure -Port @SMTP.PORT@ -SmtpServer @SMTPServer@'
     **EMAIL.CMD = CHANGE(EMAIL.CMD,"@Subject@",SUBJECT)
     **EMAIL.CMD = CHANGE(EMAIL.CMD,"@ToEmailAddress@",SEND.TO)
     **EMAIL.CMD = CHANGE(EMAIL.CMD,"@FromEmailAddress@",SEND.FROM)
     **EMAIL.CMD = CHANGE(EMAIL.CMD,"@Attachment@",PDF.NAME)
     **EMAIL.CMD = CHANGE(EMAIL.CMD,"@Bcc@","lsullivanmd@gmail.com")
     **EMAIL.CMD = CHANGE(EMAIL.CMD,"@Body@",MESSAGE.BODY)
     **EMAIL.CMD = CHANGE(EMAIL.CMD,"@CC@",SEND.FROM.EMAIL)
     **EMAIL.CMD = CHANGE(EMAIL.CMD,"@SMTPServer@",SMTP.SERVER)
     **EMAIL.CMD = CHANGE(EMAIL.CMD,"@SMTP.PORT@",SMTP.PORT)
     **PS.SCRIPT.BODY = EMAIL.CMD
     **EXECUTE "PSHELL ":PS.SCRIPT.BODY
     **RETURN


SWAP.VALUES:

     FOR LAB.X = 1 TO LABEL.CT
          PS.CMD = CHANGE(PS.CMD,LABELS<LAB.X>,VAL<LAB.X>)
          PRINT "SWAPPING": LABELS<LAB.X>:"  ":VAL<LAB.X>
     NEXT LAB.X
     RETURN

SWAP.VALUES2:
     PS.CMD = 'ADD-DhcpServerV4Reservation -ScopeId @ScopeId@ -IPAdDress @IPAddress@ -computername @ServerName@ -clientid @MacAddress@ -Name @Name@ -Description "@Desc@"'
     PS.CMD = CHANGE(PS.CMD,"@ScopeId@",SCOPEID)
     PS.CMD = CHANGE(PS.CMD,"@IPAddress@",IPADDRESS)
     PS.CMD = CHANGE(PS.CMD,"@ServerName@",SERVERNAME)
     PS.CMD = CHANGE(PS.CMD,"@MacAddress@",MAC)
     PS.CMD = CHANGE(PS.CMD,"@Name@",NAME)
     PS.CMD = CHANGE(PS.CMD,"@Desc@",DESC)
     RETURN

     STOP




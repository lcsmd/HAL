PROGRAM SET.ACCUTERM.SESSION
     * Set the AT Session object for special screen size
     * Author: B.HUGHES
     * Created: 04-24-2009 @ 10:35:26
     * Changed: 04-24-2009 @ 10:35:26
     * Version: 1.0p0e1
     * Program: 'SET.ACCUTERM.SESSION'
     *
     *
     * ---------- Start_Comments
     **** ! Accuterm Mysteries Explained ! ****
     * Screen mode - 0 = Normal, 1 = Extended
     * Scalefont - 0 = off, -1 or 1 = On
     * Boldfont - 0 = off, -1 or 1 = On

     **** ! About the 2 Prompts ! ****
     * ACTION Prompt = required
     * ------> Options <------
     * S or SET = setup the Accuterm session
     * R or RESET = Reset to User's custom settings
     * RD or DEFAULTS = Reset to system default settings
     * SAVE = only save the User's custom settings

     * FLAGS Prompt = Optional
     * Works similar to the setptr function in UniVerse
     * Enter parameters consecutively, comma separated.
     * Only fill those you want changed, comma placeholder.
     * font,fontsize,scalefont,boldfont,extdcols,extdrows,normcols,normrows,mode
     * params - in order of appearance -
     * FONT = Must be one of the font names that loads with basic Accuterm setup
     * FONTSIZE = a nbr, 1.4 thru 22.5 (if setting Scalefont=1 leave blank)
     * SCALEFONT = 1 is On, 0 is off (set to true if using extended screen)
     * BOLDFONT = 1 is On, 0 is off
     * EXTDCOLS = a nbr, usually 81 to 132 ( up to 199 in rare cases)
     * EXTDROWS = a nbr, usually 25 to 40 ( keep proportional to cols)
     * NORMCOLS = a nbr, usually 79 to 82 (if > 82 you should be using extd)
     * NORMROWS = a nbr, usually 24 or 25 (if > 25 you should be using extd)
     * SCRNMODE = 1 is Extended, 0 is normal (pay attention to this)
     * e.g. ",,1,110,30,,1" = 110 X 30 extended screen, scalefont on

     **** ! How This Works ! ****
     * It is assumed that you will call this for a 'S'et, first.
     * During the 'S'et call, we will save the user's settings to the Common.
     * When you exit the program and call for the 'R'eset, we'll restore them.
     * If you call for a 'R'eset, but the Common has not been initialized yet,
     * we will use system defaults. This can also be invoked by 'RD' to reset
     * defaults, but the preferred method is to honor the user's settings.
     * ---------- End_Comments
     *
     * ---------- Start_Release_Log
     * B.HUGHES 1.0 0.0 04-24-2009 Created
     * ---------- End_Release_Log
      PROMPT ''
      COMMON / ATSESSION / SAVESESSION(10), INITIALIZED
      DIM THISSESSION(10)
      MAT THISSESSION = ''
      EQU STX TO CHAR(2), CR TO CHAR(13), CLR.SCR TO @(IT$CS), EM TO CHAR(25)
      EQU ESC TO CHAR(27), TRUE TO 1, FALSE TO 0
      EQU FONT.NAME TO THISSESSION(1)
      EQU FONT.SIZE TO THISSESSION(2)
      EQU SCAL.FONT TO THISSESSION(3)
      EQU BOLD.FONT TO THISSESSION(4)
      EQU EXTD.COLS TO THISSESSION(5)
      EQU EXTD.ROWS TO THISSESSION(6)
      EQU NORM.COLS TO THISSESSION(7)
      EQU NORM.ROWS TO THISSESSION(8)
      EQU SCRN.MODE TO THISSESSION(9)
      METHODS = 'FontName'
      METHODS<2> = 'FontSize'
      METHODS<3> = 'ScaleFont'
      METHODS<4> = 'BoldFont'
      METHODS<5> = 'ExtCols'
      METHODS<6> = 'ExtRows'
      METHODS<7> = 'NormCols'
      METHODS<8> = 'NormRows'
      METHODS<9> = 'ScrMode'
      METHOD.CNT = DCOUNT(METHODS,@FM)
      VALID.ACTIONS = "S,SET,R,RESET,RD,DEFAULTS,SAVE"
      CONVERT ',' TO @VM IN VALID.ACTIONS
      INPUT ACTION
      ACTION = UPCASE(TRIM(ACTION))
      IF NOT(ACTION MATCHES VALID.ACTIONS) THEN RETURN
      INPUT FLAGS
      CONVERT ',' TO @VM IN FLAGS
      BEGIN CASE
           CASE ACTION MATCHES 'S':@VM:'SET'

                IF NOT(INITIALIZED) THEN GOSUB SAVE.SESSION

               * Now set the session to new settings

                MAT THISSESSION = MAT SAVESESSION
                FOR FDX = 1 TO METHOD.CNT
                IF FLAGS<1,FDX> # '' THEN
                     THISSESSION(FDX) = FLAGS<1,FDX>
                END
           NEXT FDX
          * Now apply the settings
           GOSUB SET.SESSION
      CASE ACTION MATCHES 'R':@VM:'RESET' AND INITIALIZED = TRUE
          * Here, we take care of the <R>eset situation, if you did Initialize 1st
           MAT THISSESSION = MAT SAVESESSION
           GOSUB SET.SESSION
      CASE ACTION MATCHES 'R':@VM:'RESET':@VM:'RD':@VM:'DEFAULTS'
          * If you made it to here, you either asked for reset defaults
          * or you asked for Reset but not(initialized) yet [implied]
          * Please don't change the order of the case statement.
           OPENERR = ''
           CALL OPENF.BSUB('BCTL',F.BCTL,OPENERR)
           IF OPENERR THEN CALL ERROR.BSUB(16,5,OPENERR,'') ; STOP
           ITEM = "ACCUTERM.DEFAULTS"
           MATREAD THISSESSION FROM F.BCTL, ITEM ELSE
                CALL ERROR.BSUB(14,2,'BCTL,':ITEM, "Could not set Accuterm Defaults for ":@LOGNAME)
                STOP
           END
           GOSUB SET.SESSION
      CASE ACTION = 'SAVE'
          * This is fairly unlikely, that someone would call for just a save
          * but it is conceivable, but you must ask for it explicitly 'save'
           GOSUB SAVE.SESSION
      END CASE
      STOP
SET.SESSION:
     * Build the Accuterm Script
      ATSCRIPT = 'P '
      ATSCRIPT := \INITSESSION.FONTNAME="\:FONT.NAME:\"\
      ATSCRIPT := EM
      ATSCRIPT := \INITSESSION.FONTSIZE=\:FONT.SIZE
      ATSCRIPT := EM
      ATSCRIPT := \INITSESSION.SCALEFONT=\:SCAL.FONT
      ATSCRIPT := EM
      ATSCRIPT := \INITSESSION.BOLDFONT=\:BOLD.FONT
      ATSCRIPT := EM
      ATSCRIPT := \INITSESSION.EXTCOLS=\:EXTD.COLS
      ATSCRIPT := EM
      ATSCRIPT := \INITSESSION.EXTROWS=\:EXTD.ROWS
      ATSCRIPT := EM
      ATSCRIPT := \INITSESSION.NORMCOLS=\:NORM.COLS
      ATSCRIPT := EM
      ATSCRIPT := \INITSESSION.NORMROWS=\:NORM.ROWS
      ATSCRIPT := EM
      IF SCRN.MODE THEN ; * 1 = Extended
           ATSCRIPT := \INITSESSION.EXTMODE\
           TERM.CMD = \TERM \:EXTD.COLS:\,\:EXTD.ROWS
      END ELSE
           ATSCRIPT := \INITSESSION.NORMMODE\
           TERM.CMD = \TERM \:NORM.COLS:\,\:NORM.ROWS
      END
      ATSCRIPT := \'END'\
      PRINT ESC:STX:ATSCRIPT:CR:
      IF SCRN.MODE THEN PRINT @(-30) ELSE PRINT @(-29)
      EXECUTE TERM.CMD
      RETURN
     *
SAVE.SESSION:
     *
     * We save the User's current session settings to Common before 1st <S>et.
      MAT SAVESESSION = ''
     *
     * Now, we're going to capture all the settings from Accuterm.
     * We do this through a secret handshake & some vb script on client end.
      ECHO OFF
      FOR FDX = 1 TO METHOD.CNT
      SCRIPT = \InitSession.Output CStr(InitSession.\
      SCRIPT:=METHODS<FDX>
      SCRIPT:= \) & Chr$(13)\
     * for timing purposes, the following 2 lines (on next line) must execute
     * in very close to the same instant, otherwise the input statement may
     * not capture the Accuterm response.
      CRT CHAR(27):CHAR(2):'P':SCRIPT:CHAR(13); INPUT SAVESESSION(FDX)
      IF SAVESESSION(FDX) = '' THEN SAVESESSION(FDX) = 0
      NEXT FDX
     *
      INITIALIZED = TRUE
      ECHO ON
      RETURN
     *
      END
     * end of program
     *it is used (from BP REPORT.SCREEN.MENU):
     *
     *************
     *SET.SESSION:
     *************
     * SET.CMND = "AT.SS":@FM
     * SET.CMND:="DATA SET":@FM
     * SET.CMND:="DATA ,,1,1,"
     * IF SCRN.WIDTH GE 82 THEN
     * SET.CMND:=SCRN.WIDTH:",":SCRN.LNGTH:",,,1"
     * END ELSE
     * SET.CMND:=",,":SCRN.WIDTH:",":SCRN.LNGTH:",0"
     * END
     * EXECUTE SET.CMND
     * RETURN
     ****************
     *RESET.SESSION:
     ***************
     * EXECUTE "AT.SS":@FM:"DATA RESET":@FM:"DATA "
     * RETURN
     **

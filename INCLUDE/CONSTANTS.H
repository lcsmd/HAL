* ============================================================================
* CONSTANTS.H - System-wide constants for HAL Voice Assistant
* ============================================================================
* Purpose: Define commonly used constants across all programs
* Usage: Include via MASTER.H at top of programs
* 
* Author: HAL System
* Created: 2025-12-03
* Last Modified: 2025-12-03
* ============================================================================

* ----------------------------------------------------------------------------
* Field Markers (MultiValue Database)
* ----------------------------------------------------------------------------
EQU FM TO CHAR(254)        ; Field Mark
EQU VM TO CHAR(253)        ; Value Mark
EQU SVM TO CHAR(252)       ; SubValue Mark
EQU TM TO CHAR(251)        ; Text Mark
EQU AM TO CHAR(254)        ; Alternative name for Field Mark
EQU IM TO CHAR(255)        ; Item Mark

* ----------------------------------------------------------------------------
* Boolean Constants
* ----------------------------------------------------------------------------
EQU TRUE TO 1
EQU FALSE TO 0
EQU YES TO 1
EQU NO TO 0
EQU ON TO 1
EQU OFF TO 0

* ----------------------------------------------------------------------------
* System Characters
* ----------------------------------------------------------------------------
EQU LF TO CHAR(10)         ; Line Feed
EQU CR TO CHAR(13)         ; Carriage Return
EQU TAB TO CHAR(9)         ; Tab
EQU ESC TO CHAR(27)        ; Escape
EQU DQUOTE TO CHAR(34)     ; Double Quote
EQU SQUOTE TO CHAR(39)     ; Single Quote

* ----------------------------------------------------------------------------
* Network Configuration
* ----------------------------------------------------------------------------
EQU VOICE.SERVER.IP TO '10.1.10.20'
EQU VOICE.SERVER.PORT TO 8585
EQU AI.SERVER.IP TO '10.1.34.103'
EQU AI.SERVER.PORT TO 8745

* ----------------------------------------------------------------------------
* File Names (System Files)
* ----------------------------------------------------------------------------
EQU VOICE.LOG.FILE TO 'VOICE.ASSISTANT.LOG'
EQU VOICE.SESSIONS.FILE TO 'VOICE.SESSIONS'
EQU VOICE.USERS.FILE TO 'VOICE.USERS'
EQU VOICE.CONFIG.FILE TO 'VOICE.CONFIG'

* ----------------------------------------------------------------------------
* Status Codes
* ----------------------------------------------------------------------------
EQU STATUS.SUCCESS TO 'SUCCESS'
EQU STATUS.ERROR TO 'ERROR'
EQU STATUS.WARNING TO 'WARNING'
EQU STATUS.INFO TO 'INFO'
EQU STATUS.PENDING TO 'PENDING'
EQU STATUS.ACTIVE TO 'ACTIVE'
EQU STATUS.INACTIVE TO 'INACTIVE'
EQU STATUS.COMPLETED TO 'COMPLETED'
EQU STATUS.FAILED TO 'FAILED'
EQU STATUS.TIMEOUT TO 'TIMEOUT'

* ----------------------------------------------------------------------------
* Message Types (WebSocket/JSON)
* ----------------------------------------------------------------------------
EQU MSG.TYPE.SESSION.START TO 'session_start'
EQU MSG.TYPE.SESSION.END TO 'session_end'
EQU MSG.TYPE.TEXT.INPUT TO 'text_input'
EQU MSG.TYPE.TEXT.RESPONSE TO 'text_response'
EQU MSG.TYPE.AUDIO.START TO 'audio_start'
EQU MSG.TYPE.AUDIO.DATA TO 'audio_data'
EQU MSG.TYPE.AUDIO.END TO 'audio_end'
EQU MSG.TYPE.ERROR TO 'error'
EQU MSG.TYPE.PING TO 'ping'
EQU MSG.TYPE.PONG TO 'pong'

* ----------------------------------------------------------------------------
* Log Levels
* ----------------------------------------------------------------------------
EQU LOG.LEVEL.DEBUG TO 'DEBUG'
EQU LOG.LEVEL.INFO TO 'INFO'
EQU LOG.LEVEL.WARNING TO 'WARNING'
EQU LOG.LEVEL.ERROR TO 'ERROR'
EQU LOG.LEVEL.CRITICAL TO 'CRITICAL'

* ----------------------------------------------------------------------------
* Intent Types
* ----------------------------------------------------------------------------
EQU INTENT.TIME TO 'time'
EQU INTENT.DATE TO 'date'
EQU INTENT.WEATHER TO 'weather'
EQU INTENT.CALENDAR TO 'calendar'
EQU INTENT.EMAIL TO 'email'
EQU INTENT.REMINDER TO 'reminder'
EQU INTENT.MEDICATION TO 'medication'
EQU INTENT.APPOINTMENT TO 'appointment'
EQU INTENT.TRANSACTION TO 'transaction'
EQU INTENT.BALANCE TO 'balance'
EQU INTENT.GENERAL TO 'general'
EQU INTENT.UNKNOWN TO 'unknown'

* ----------------------------------------------------------------------------
* Voice Settings
* ----------------------------------------------------------------------------
EQU VOICE.DEFAULT.ID TO 'default'
EQU VOICE.DEFAULT.VOLUME TO 1.0
EQU VOICE.DEFAULT.RATE TO 1.0
EQU VOICE.DEFAULT.PITCH TO 1.0

* ----------------------------------------------------------------------------
* Timeout Values (milliseconds)
* ----------------------------------------------------------------------------
EQU TIMEOUT.SHORT TO 1000           ; 1 second
EQU TIMEOUT.MEDIUM TO 5000          ; 5 seconds
EQU TIMEOUT.LONG TO 30000           ; 30 seconds
EQU TIMEOUT.SOCKET.READ TO 1000     ; Socket read timeout
EQU TIMEOUT.SOCKET.WRITE TO 1000    ; Socket write timeout
EQU TIMEOUT.SOCKET.CONNECT TO 5000  ; Socket connect timeout

* ----------------------------------------------------------------------------
* Buffer Sizes
* ----------------------------------------------------------------------------
EQU BUFFER.SIZE.SMALL TO 1024       ; 1 KB
EQU BUFFER.SIZE.MEDIUM TO 8192      ; 8 KB
EQU BUFFER.SIZE.LARGE TO 65536      ; 64 KB
EQU BUFFER.SIZE.AUDIO TO 16384      ; 16 KB for audio chunks

* ----------------------------------------------------------------------------
* Date/Time Format Strings
* ----------------------------------------------------------------------------
EQU DATE.FORMAT.ISO TO 'D4-YMD'
EQU DATE.FORMAT.US TO 'D4-MDY'
EQU DATE.FORMAT.LONG TO 'D4-MDY[A,3]'
EQU TIME.FORMAT.12HR TO 'MTS'
EQU TIME.FORMAT.24HR TO 'MT'

* ----------------------------------------------------------------------------
* Error Codes
* ----------------------------------------------------------------------------
EQU ERR.FILE.NOT.FOUND TO 1001
EQU ERR.RECORD.NOT.FOUND TO 1002
EQU ERR.INVALID.INPUT TO 1003
EQU ERR.PERMISSION.DENIED TO 1004
EQU ERR.SOCKET.ERROR TO 2001
EQU ERR.SOCKET.TIMEOUT TO 2002
EQU ERR.SOCKET.CLOSED TO 2003
EQU ERR.JSON.PARSE TO 3001
EQU ERR.JSON.INVALID TO 3002
EQU ERR.UNKNOWN TO 9999

* ----------------------------------------------------------------------------
* JSON Keys (for consistent parsing)
* ----------------------------------------------------------------------------
EQU JSON.KEY.TYPE TO 'type'
EQU JSON.KEY.CLIENT.ID TO 'client_id'
EQU JSON.KEY.USER.ID TO 'user_id'
EQU JSON.KEY.SESSION.ID TO 'session_id'
EQU JSON.KEY.TEXT TO 'text'
EQU JSON.KEY.TIMESTAMP TO 'timestamp'
EQU JSON.KEY.WAKE.WORD TO 'wake_word'
EQU JSON.KEY.VOICE.ID TO 'voice_id'
EQU JSON.KEY.VOLUME TO 'volume'
EQU JSON.KEY.STATUS TO 'status'
EQU JSON.KEY.ERROR TO 'error'
EQU JSON.KEY.MESSAGE TO 'message'

* ----------------------------------------------------------------------------
* Numeric Constants
* ----------------------------------------------------------------------------
EQU ZERO TO 0
EQU ONE TO 1
EQU MAX.RETRIES TO 3
EQU MAX.SESSIONS TO 100
EQU MAX.MESSAGE.SIZE TO 1048576     ; 1 MB

* ----------------------------------------------------------------------------
* String Constants
* ----------------------------------------------------------------------------
EQU EMPTY.STRING TO ''
EQU SPACE TO ' '
EQU COMMA TO ','
EQU PERIOD TO '.'
EQU COLON TO ':'
EQU SEMICOLON TO ';'
EQU EQUALS TO '='
EQU NEWLINE TO CHAR(10)

* ============================================================================
* End of CONSTANTS.H
* ============================================================================

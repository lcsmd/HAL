* ============================================================================
* VOICE.UTILS.H - Common utility subroutines for Voice Assistant
* ============================================================================
* Purpose: Declare common utility subroutines used across programs
* Usage: Include via MASTER.H
* 
* Author: HAL System
* Created: 2025-12-03
* Last Modified: 2025-12-03
* ============================================================================

* These are subroutine declarations/forward references
* Actual implementations should be in separate programs and cataloged

* ----------------------------------------------------------------------------
* Logging Utilities
* ----------------------------------------------------------------------------
* LOG.MESSAGE(LEVEL, MESSAGE)
* LOG.INTERACTION(SESSION.ID, USER.ID, INPUT.TEXT, RESPONSE.TEXT)
* LOG.ERROR(ERROR.CODE, ERROR.MESSAGE)

* ----------------------------------------------------------------------------
* WebSocket Utilities
* ----------------------------------------------------------------------------
* CREATE.WEBSOCKET.SERVER(PORT, STATUS)
* ACCEPT.WEBSOCKET.CONNECTION(SOCKET, STATUS)
* READ.WEBSOCKET(SOCKET, MESSAGE, TIMEOUT, STATUS)
* WRITE.WEBSOCKET(SOCKET, MESSAGE, STATUS)
* CLOSE.WEBSOCKET(SOCKET)
* CLOSE.WEBSOCKET.SERVER()
* IS.SOCKET.CONNECTED(SOCKET, IS.CONNECTED)

* ----------------------------------------------------------------------------
* JSON Utilities
* ----------------------------------------------------------------------------
* PARSE.JSON(JSON.TEXT, DATA)
* BUILD.JSON(DATA, JSON.TEXT)
* JSON.GET.VALUE(JSON.TEXT, KEY, VALUE)
* JSON.SET.VALUE(JSON.TEXT, KEY, VALUE, NEW.JSON)

* ----------------------------------------------------------------------------
* String Utilities
* ----------------------------------------------------------------------------
* TRIM(INPUT.STRING, OUTPUT.STRING)
* UPPER(INPUT.STRING, OUTPUT.STRING)
* LOWER(INPUT.STRING, OUTPUT.STRING)
* SPLIT.STRING(INPUT.STRING, DELIMITER, ARRAY)
* JOIN.STRING(ARRAY, DELIMITER, OUTPUT.STRING)

* ----------------------------------------------------------------------------
* Date/Time Utilities
* ----------------------------------------------------------------------------
* GET.TIMESTAMP(TIMESTAMP)
* FORMAT.DATE(INTERNAL.DATE, FORMAT.CODE, FORMATTED.DATE)
* FORMAT.TIME(INTERNAL.TIME, FORMAT.CODE, FORMATTED.TIME)
* PARSE.ISO.TIMESTAMP(ISO.STRING, INTERNAL.DATE, INTERNAL.TIME)

* ----------------------------------------------------------------------------
* Validation Utilities
* ----------------------------------------------------------------------------
* VALIDATE.USER.ID(USER.ID, IS.VALID)
* VALIDATE.CLIENT.ID(CLIENT.ID, IS.VALID)
* VALIDATE.SESSION.ID(SESSION.ID, IS.VALID)
* VALIDATE.INPUT(INPUT.TEXT, IS.VALID)

* ============================================================================
* End of VOICE.UTILS.H
* ============================================================================

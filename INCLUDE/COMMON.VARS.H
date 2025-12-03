* ============================================================================
* COMMON.VARS.H - Common variable declarations
* ============================================================================
* Purpose: Declare common variables used across subroutines
* Usage: Include via MASTER.H when common variables are needed
* 
* Note: Use sparingly - prefer passing variables as parameters
* 
* Author: HAL System
* Created: 2025-12-03
* Last Modified: 2025-12-03
* ============================================================================

* ----------------------------------------------------------------------------
* Common File Variables
* ----------------------------------------------------------------------------
* These are commonly opened files that may be shared
* COMMON /FILES/ LOG.FILE, SESSION.FILE, CONFIG.FILE, USERS.FILE

* ----------------------------------------------------------------------------
* Common System Variables
* ----------------------------------------------------------------------------
* COMMON /SYSTEM/ SYSTEM.DATE, SYSTEM.TIME, RUNNING

* ----------------------------------------------------------------------------
* Common Socket Variables
* ----------------------------------------------------------------------------
* COMMON /SOCKETS/ MAIN.SOCKET, CLIENT.SOCKETS

* Note: Uncomment COMMON blocks as needed in your programs
* Most programs should NOT need common variables

* ============================================================================
* End of COMMON.VARS.H
* ============================================================================

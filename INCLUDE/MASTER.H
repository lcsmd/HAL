* ============================================================================
* MASTER.H - Master include file for all HAL Voice Assistant programs
* ============================================================================
* Purpose: Central include file that includes all necessary system includes
* Usage: Add "$INCLUDE INCLUDE MASTER.H" at top of every program
* 
* This file includes:
*   - System constants (CONSTANTS.H)
*   - Utility declarations (VOICE.UTILS.H)
*   - Common variables (COMMON.VARS.H) - optional
* 
* Author: HAL System
* Created: 2025-12-03
* Last Modified: 2025-12-03
* Version: 1.0
* ============================================================================

* ----------------------------------------------------------------------------
* Include Order:
* 1. Constants first (used by everything)
* 2. Utility declarations (may reference constants)
* 3. Common variables last (optional, use sparingly)
* ----------------------------------------------------------------------------

* System-wide Constants
$INCLUDE INCLUDE CONSTANTS.H

* Utility Subroutine Declarations
$INCLUDE INCLUDE VOICE.UTILS.H

* Common Variables (uncomment if needed)
* $INCLUDE INCLUDE COMMON.VARS.H

* ----------------------------------------------------------------------------
* Version Information
* ----------------------------------------------------------------------------
EQU MASTER.H.VERSION TO '1.0'
EQU MASTER.H.DATE TO '2025-12-03'

* ----------------------------------------------------------------------------
* Compilation Information
* To verify this include file is being used, programs can check:
*   IF NOT(ASSIGNED(MASTER.H.VERSION)) THEN
*      CRT 'ERROR: MASTER.H not included'
*      STOP
*   END
* ----------------------------------------------------------------------------

* ============================================================================
* End of MASTER.H
* ============================================================================

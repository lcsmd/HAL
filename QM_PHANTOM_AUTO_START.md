# QM Phantom Auto-Start Using MASTER.LOGIN

**The proper QM-native way to auto-start phantoms**

## Overview

OpenQM provides a built-in mechanism to automatically start phantoms when the QM system starts: the **MASTER.LOGIN** paragraph in the QMSYS account.

This is superior to Windows Services or other external methods because:
- ✅ Native QM functionality
- ✅ Runs when QMSvc starts
- ✅ Proper QM environment
- ✅ Simple configuration
- ✅ No wrapper scripts needed

## Configuration

### Step 1: Create Q-Pointers

**In QMSYS Account** - Create Q-pointer to HAL BP file:

```qm
LOGTO QMSYS
CREATE.FILE VOC HAL.BP Q
* Record type: Q
* Path: HAL,BP
```

This creates a Q-pointer `HAL.BP` that points to the `BP` file in the `HAL` account.

**In HAL Account** - Create Q-pointer to QMSYS VOC (for convenience):

```qm
LOGTO HAL
CREATE.FILE VOC QMSYS.VOC Q
* Record type: Q
* Path: QMSYS,VOC
```

This creates a Q-pointer `QMSYS.VOC` that allows accessing QMSYS VOC from HAL account.

**Benefits:**
- ✅ Edit MASTER.LOGIN from HAL: `ED QMSYS.VOC MASTER.LOGIN`
- ✅ List QMSYS VOC items: `LIST QMSYS.VOC`
- ✅ No need to switch accounts
- ✅ Convenient cross-account management

### Step 2: Edit MASTER.LOGIN

**Option A - From QMSYS account:**

```qm
LOGTO QMSYS
ED VOC MASTER.LOGIN
```

**Option B - From HAL account (using Q-pointer):**

```qm
LOGTO HAL
ED QMSYS.VOC MASTER.LOGIN
```

Add the phantom start command:

```
MASTER.LOGIN
001 PA
002 PHANTOM HAL.BP AI.SERVER
003 * Add more phantoms here if needed
```

### Step 3: Save and Test

```qm
FI
* File saved

* Test by restarting QMSvc or rebooting
```

**Verify from HAL account:**

```qm
LOGTO HAL
LIST QMSYS.VOC MASTER.LOGIN
* Shows MASTER.LOGIN content without switching accounts
```

## Current Configuration

**File**: `QMSYS/VOC/MASTER.LOGIN`  
**Type**: PA (Paragraph)  
**Command**: `PHANTOM HAL.BP AI.SERVER`

This starts the AI.SERVER phantom from the HAL account's BP file when QMSvc starts.

## Verification

### Check MASTER.LOGIN

```qm
LOGTO QMSYS
LIST VOC MASTER.LOGIN
```

### Verify Phantom Started

After QMSvc restart or system reboot:

```qm
LISTU
* Look for iPhantom entry for AI.SERVER
```

```powershell
# Check port is listening
netstat -ano | findstr :8745
```

### Test Connection

```powershell
cd C:\qmsys\hal
python test_ai_server_direct.py
```

## Multiple Phantoms

To start multiple phantoms, add them to MASTER.LOGIN:

```
MASTER.LOGIN
001 PA
002 PHANTOM HAL.BP AI.SERVER
003 PHANTOM HAL.BP ANOTHER.PROGRAM
004 * More commands as needed
```

## Q-Pointer Details

**Purpose**: Access files in other accounts from QMSYS

**HAL.BP Q-Pointer:**
- Points to: HAL account, BP file
- Allows QMSYS to run: `PHANTOM HAL.BP AI.SERVER`
- Equivalent to: `LOGTO HAL; PHANTOM BP AI.SERVER`

**Advantages:**
- No need to switch accounts
- Can reference any file in any account
- Central management from QMSYS
- Clean separation of concerns

## Alternative Locations

MASTER.LOGIN can contain any valid QM commands that should run at startup:

```
MASTER.LOGIN
001 PA
002 * Auto-start phantoms
003 PHANTOM HAL.BP AI.SERVER
004 
005 * Initialize system
006 CREATE.FILE SOME.FILE IF.REQD
007 
008 * Set environment
009 * Any other startup commands
```

## Troubleshooting

### Phantom Not Starting

**Check MASTER.LOGIN exists:**
```qm
LOGTO QMSYS
LIST VOC MASTER.LOGIN
```

**Check Q-pointer:**
```qm
LIST VOC HAL.BP
* Should show: Q-pointer to HAL,BP
```

**Check program compiled:**
```qm
LOGTO HAL
LIST BP.OUT AI.SERVER
* Should exist
```

**Manually test phantom start:**
```qm
LOGTO QMSYS
PHANTOM HAL.BP AI.SERVER
LISTU
* Should show new phantom
```

### Q-Pointer Not Working

**Verify Q-pointer syntax:**
```qm
LOGTO QMSYS
ED VOC HAL.BP

* Should contain:
* Line 1: Q
* Line 2: HAL,BP
```

**Test Q-pointer:**
```qm
LIST HAL.BP
* Should list programs in HAL BP file
```

### Phantom Crashes

**Check phantom log:**
```qm
LOGTO HAL
ED $COMO <phantom-user-number>
```

**Check for errors:**
- Port already in use (8745)
- Compilation errors
- Missing dependencies

## Comparison: Service vs MASTER.LOGIN

| Method | Pros | Cons |
|--------|------|------|
| **MASTER.LOGIN** | Native QM, simple, proper environment | Tied to QMSvc service |
| **Windows Service** | Independent, OS-level control, restart policies | Complex setup, wrapper scripts needed |

**Recommendation**: Use MASTER.LOGIN for QM phantoms. It's the intended method.

## Voice Gateway Auto-Start

**Note**: Voice Gateway (Python) still needs separate auto-start:
- Windows Service (NSSM)
- Or Task Scheduler
- Or startup script

MASTER.LOGIN only handles QM programs/phantoms.

## Complete Auto-Start Solution

**QM Phantom (AI.SERVER):**
- ✅ MASTER.LOGIN in QMSYS account

**Python Server (Voice Gateway):**
- ✅ Windows Service (NSSM)
- Or manual start script

**Ubuntu Services (Faster-Whisper, Ollama):**
- ✅ systemd services

## Documentation Updates Needed

1. ✅ Document MASTER.LOGIN method
2. ✅ Explain Q-pointers
3. ✅ Update service scripts to remove AI.SERVER (not needed)
4. ✅ Simplify to only Voice Gateway service

---

**Best Practice**: Use MASTER.LOGIN for all QM phantom auto-start needs.

**Created**: 2025-12-03  
**Method**: Native QM functionality  
**Status**: Implemented and tested

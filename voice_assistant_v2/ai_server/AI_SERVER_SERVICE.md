# AI Server Auto-Start Service

## Overview

The AI Server can be installed as a Windows auto-start service using Task Scheduler. This ensures:

✅ **Automatic startup** on system boot  
✅ **Automatic restart** if the phantom crashes  
✅ **Continuous monitoring** of the server health  
✅ **Background execution** (no visible windows)  

---

## Installation

### Step 1: Run Setup

```powershell
cd C:\qmsys\hal\voice_assistant_v2\ai_server
.\setup_windows.ps1
```

At the end, it will ask if you want to install the auto-start service.

### Step 2: Install Service (Manual)

If you skipped it during setup:

```powershell
.\install_service.ps1
```

This creates a Windows Scheduled Task that:
- Starts on system boot
- Runs as SYSTEM account
- Has highest privileges
- Auto-restarts on failure (3 times)
- Monitors the phantom every 30 seconds

---

## Management

### Start the Service

**Option 1: Using batch file**
```batch
start_ai_server.bat
```

**Option 2: Using PowerShell**
```powershell
Start-ScheduledTask -TaskName "HAL Voice Assistant AI Server"
```

---

### Stop the Service

**Option 1: Using batch file**
```batch
stop_ai_server.bat
```

**Option 2: Using PowerShell**
```powershell
Stop-ScheduledTask -TaskName "HAL Voice Assistant AI Server"
```

---

### Check Status

**Option 1: Using batch file**
```batch
status_ai_server.bat
```

**Option 2: Using PowerShell**
```powershell
.\status_phantom.ps1
```

This shows:
- Scheduled task status
- QM process information
- Network port status (8745)
- Recent monitor log entries
- Active connections

---

### View Logs

**Monitor log** (auto-restart, health checks):
```
C:\qmsys\hal\voice_assistant_v2\ai_server\phantom_monitor.log
```

**QM application log**:
```batch
view_logs.bat
```

Or directly:
```powershell
cd C:\qmsys\hal
C:\qmsys\bin\qm.exe -aHAL << EOF
LIST VOICE.ASSISTANT.LOG WITH DATE >= TODAY - 1 BY.DSND DATE BY.DSND TIME
QUIT
EOF
```

---

## Uninstall Service

```powershell
.\install_service.ps1 -Uninstall
```

This removes the scheduled task but leaves the program files intact.

---

## How It Works

### Architecture

```
Windows Boot
    ↓
Task Scheduler
    ↓
start_phantom.ps1 (runs as SYSTEM)
    ↓
OpenQM Phantom: AI.SERVER
    ↓
WebSocket Server (port 8745)
```

### Monitoring Loop

The `start_phantom.ps1` script:

1. Starts the OpenQM phantom process
2. Waits 3 seconds for startup
3. Checks if port 8745 is listening
4. Enters monitor loop:
   - Every 30 seconds: Check if port 8745 is still listening
   - If not responding: Auto-restart the phantom
   - Log all events to `phantom_monitor.log`

### Auto-Restart

If the phantom crashes or stops responding:

1. Monitor detects port 8745 not listening
2. Waits 10 seconds (configurable)
3. Kills any stuck QM processes
4. Starts a new phantom instance
5. Logs the restart event
6. Continues monitoring

---

## Task Scheduler Details

**Task Name:** `HAL Voice Assistant AI Server`

**Triggers:**
- At system startup
- At any user logon (backup trigger)

**Action:**
```
PowerShell.exe -NoProfile -WindowStyle Hidden -ExecutionPolicy Bypass -File "C:\qmsys\hal\voice_assistant_v2\ai_server\start_phantom.ps1" -Monitor
```

**Security:**
- Run as: SYSTEM
- Run level: Highest
- Run whether user is logged on or not

**Settings:**
- Allow start on batteries: Yes
- Don't stop on batteries: Yes
- Start when available: Yes
- Restart on failure: Yes (3 attempts, 1 minute interval)
- Execution time limit: 365 days

---

## Troubleshooting

### Service Won't Start

**Check 1: OpenQM installed?**
```powershell
Test-Path C:\qmsys\bin\qm.exe
```

**Check 2: HAL account exists?**
```powershell
Test-Path C:\qmsys\hal
```

**Check 3: AI.SERVER compiled?**
```powershell
Test-Path C:\qmsys\hal\BP.OUT\AI.SERVER
```

**Check 4: Port 8745 available?**
```powershell
Get-NetTCPConnection -LocalPort 8745
# Should be empty or show your phantom
```

---

### Service Keeps Restarting

Check monitor log for errors:
```powershell
Get-Content C:\qmsys\hal\voice_assistant_v2\ai_server\phantom_monitor.log -Tail 50
```

Common issues:
- Port 8745 already in use by another process
- OpenQM license issues
- File permissions problems
- INCLUDE files missing

---

### Check What's Using Port 8745

```powershell
Get-NetTCPConnection -LocalPort 8745 | ForEach-Object {
    $proc = Get-Process -Id $_.OwningProcess
    [PSCustomObject]@{
        LocalAddress = $_.LocalAddress
        LocalPort = $_.LocalPort
        RemoteAddress = $_.RemoteAddress
        State = $_.State
        ProcessId = $_.OwningProcess
        ProcessName = $proc.Name
    }
}
```

---

### Manual Phantom Start (Testing)

If you want to test the phantom without the service:

```powershell
cd C:\qmsys\bin
.\qm.exe -aHAL
```

Then at the QM prompt:
```
LOGTO HAL
PHANTOM BP AI.SERVER
QUIT
```

Check if running:
```powershell
netstat -an | Select-String "8745"
```

---

## Files Created

| File | Purpose |
|------|---------|
| `install_service.ps1` | Install/uninstall scheduled task |
| `start_phantom.ps1` | Start phantom with monitoring |
| `stop_phantom.ps1` | Stop phantom and scheduled task |
| `status_phantom.ps1` | Comprehensive status check |
| `phantom_monitor.log` | Monitor and restart log |
| `start_ai_server.bat` | Quick start (batch file) |
| `stop_ai_server.bat` | Quick stop (batch file) |
| `status_ai_server.bat` | Quick status (batch file) |

---

## Production Deployment

For production servers:

1. **Install the service during setup:**
   ```powershell
   .\setup_windows.ps1
   # Answer "Y" to install auto-start service
   ```

2. **Verify it's running:**
   ```powershell
   .\status_phantom.ps1
   ```

3. **Test restart behavior:**
   - Stop the phantom: `Stop-Process -Name qm -Force`
   - Wait 40 seconds (30s check + 10s restart delay)
   - Check status: `.\status_phantom.ps1`
   - Should show it restarted automatically

4. **Test boot behavior:**
   - Restart Windows
   - After boot, check: `.\status_phantom.ps1`
   - Should show AI Server running

---

## Summary

✅ **One command install:** `.\install_service.ps1`  
✅ **Auto-start on boot:** Yes  
✅ **Auto-restart on crash:** Yes (within 40 seconds)  
✅ **Easy management:** Batch files or PowerShell  
✅ **Comprehensive logging:** phantom_monitor.log  
✅ **Production ready:** Runs as SYSTEM, highest privileges  

---

**The AI Server is now a reliable Windows service!** 🚀

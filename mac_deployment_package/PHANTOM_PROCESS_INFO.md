# HAL WebSocket Listener - Phantom Process

## What is a Phantom Process?

A **phantom process** in OpenQM is a background process that runs independently of any terminal session. It's similar to a daemon in Unix/Linux.

### Characteristics:
- ✅ Runs in background
- ✅ Survives terminal disconnections
- ✅ Persistent until stopped or server reboot
- ✅ No interactive I/O
- ✅ Logs to files instead of terminal

---

## HAL WebSocket Listener

The HAL WebSocket listener runs as a **phantom process** listening on port **8768**.

### Why Phantom?
- Always available for client connections
- No need to keep QM terminal open
- Automatic restart on server boot (if configured)
- Multiple clients can connect simultaneously
- No manual startup required

---

## Checking Status

### Method 1: Network Port
```cmd
# On Windows (QM Server)
netstat -an | findstr 8768
```

**Expected**:
```
TCP    0.0.0.0:8768           0.0.0.0:0              LISTENING
```

### Method 2: QM Command
```qm
* In QM terminal
LOGTO HAL
LIST.READU
```

**Look for**: `WEBSOCKET.LISTENER` in the process list

### Method 3: PowerShell
```powershell
Get-NetTCPConnection -LocalPort 8768 -State Listen
```

---

## Starting the Phantom

### Normal Start (becomes phantom automatically)
```qm
LOGTO HAL
EXECUTE "WEBSOCKET.LISTENER" CAPTURING OUTPUT
```

### Explicit Phantom
```qm
LOGTO HAL
PHANTOM EXECUTE "WEBSOCKET.LISTENER"
```

### With Parameters (if needed)
```qm
LOGTO HAL
PHANTOM EXECUTE "WEBSOCKET.LISTENER":@FM:"param1":@FM:"param2"
```

---

## Stopping the Phantom

### Find Process ID
```qm
LOGTO HAL
LIST.READU
* Note the User No. (process ID)
```

### Stop Process
```qm
LOGTO HAL
KILL.PHANTOM user_no
```

Or from Windows command line:
```cmd
qm -aHAL "KILL.PHANTOM user_no"
```

---

## Logs

Phantom processes typically log to files:

### Check Logs
```qm
LOGTO HAL
LIST HAL.SPLITTER.LOG
```

Or Windows:
```cmd
type C:\qmsys\hal\HAL.SPLITTER.LOG
type C:\qmsys\hal\gateway.log
```

---

## Auto-Start on Server Boot

### Option 1: Windows Task Scheduler
Create scheduled task:
- **Trigger**: At system startup
- **Action**: Start program
  - Program: `C:\qmsys\bin\qm.exe`
  - Arguments: `-aHAL "PHANTOM EXECUTE 'WEBSOCKET.LISTENER'"`
- **Run as**: System account or service account

### Option 2: Windows Service
Create Windows service wrapper that:
1. Starts QM
2. Logs into HAL account
3. Launches phantom process

### Option 3: Startup Script
Create `start_hal_websocket.bat`:
```batch
@echo off
C:\qmsys\bin\qm.exe -aHAL "PHANTOM EXECUTE 'WEBSOCKET.LISTENER'"
```

Place in: `C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Startup`

---

## Monitoring

### Health Check Script
```qm
* Check if phantom is running
PROGRAM CHECK.WEBSOCKET.LISTENER
   PORT = 8768
   EXECUTE "netstat -an" CAPTURING OUTPUT
   IF INDEX(OUTPUT, ":8768", 1) THEN
      PRINT "WebSocket Listener: RUNNING"
   END ELSE
      PRINT "WebSocket Listener: NOT RUNNING"
      PRINT "Restarting..."
      PHANTOM EXECUTE "WEBSOCKET.LISTENER"
   END
END
```

### Windows Task Scheduler Monitor
Run every 5 minutes:
```cmd
qm -aHAL "CHECK.WEBSOCKET.LISTENER"
```

---

## Troubleshooting

### Phantom Not Starting

**Check QM error logs**:
```qm
LOGTO HAL
LIST $COMO
```

**Check compilation**:
```qm
LOGTO HAL
BASIC BP WEBSOCKET.LISTENER
CATALOG BP WEBSOCKET.LISTENER
```

### Port Already in Use

**Find what's using port 8768**:
```powershell
Get-Process -Id (Get-NetTCPConnection -LocalPort 8768).OwningProcess
```

**Stop conflicting process**:
```powershell
Stop-Process -Id <process_id> -Force
```

### Phantom Crashes

**Check crash dumps**:
```qm
LIST HAL.SPLITTER.LOG WITH *A1 = "ERROR"
```

**Restart with logging**:
```qm
PHANTOM EXECUTE "WEBSOCKET.LISTENER" DEBUG
```

### Multiple Phantoms Running

**List all**:
```qm
LIST.READU
```

**Kill extras**:
```qm
KILL.PHANTOM user_no1
KILL.PHANTOM user_no2
```

---

## Performance

### Max Connections
Default: 50 concurrent connections
Configurable in WEBSOCKET.LISTENER code

### Memory Usage
- Idle: ~5-10 MB
- Per connection: ~1-2 MB
- 50 connections: ~100-150 MB

### CPU Usage
- Idle: <1%
- Active (10 clients): 5-10%
- Peak: <20%

---

## Comparison: Phantom vs Python Gateway

| Feature | QM Phantom | Python Gateway |
|---------|------------|----------------|
| Language | QM Basic | Python |
| Startup | Automatic | Manual |
| Database Access | Native | Via client library |
| Performance | Fast | Slower (network hop) |
| Deployment | Single process | Two processes |
| Complexity | Simple | More complex |
| WebSocket | Native (if supported) | websockets library |

**HAL uses QM Phantom for simplicity and performance!**

---

## Configuration

### Environment Variables
Set in QM or Windows:
- `WEBSOCKET_PORT` - Port number (default 8768)
- `WEBSOCKET_HOST` - Bind address (default 0.0.0.0)
- `MAX_CONNECTIONS` - Max concurrent clients (default 50)

### QM Configuration File
Edit `QMCONFIG` in HAL account:
```
WEBSOCKET.PORT = 8768
WEBSOCKET.TIMEOUT = 30000
WEBSOCKET.BUFFER = 32768
```

---

## Best Practices

1. ✅ **Monitor regularly** - Check phantom status daily
2. ✅ **Log rotation** - Prevent log files from growing too large
3. ✅ **Auto-restart** - Configure automatic restart on failure
4. ✅ **Firewall rules** - Allow port 8768 inbound
5. ✅ **Resource limits** - Monitor CPU/memory usage
6. ✅ **Backup config** - Keep WEBSOCKET.LISTENER code backed up
7. ✅ **Test after reboot** - Verify auto-start works

---

## Summary

The HAL WebSocket listener:
- ✅ Runs as QM phantom process
- ✅ Listens on port 8768
- ✅ Handles Mac client connections
- ✅ Processes queries directly in QM
- ✅ No Python gateway needed
- ✅ Auto-starts (if configured)
- ✅ Persistent background service

**Your Mac client connects directly to the QM phantom process!**

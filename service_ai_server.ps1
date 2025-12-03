# AI.SERVER Windows Service Wrapper
# Monitors and maintains AI.SERVER phantom process on port 8745

$ErrorActionPreference = "Continue"
$LogFile = "C:\qmsys\hal\LOGS\ai_server_service.log"
$CheckInterval = 30  # seconds

# Ensure log directory exists
$logDir = Split-Path $LogFile -Parent
if (!(Test-Path $logDir)) {
    New-Item -ItemType Directory -Path $logDir -Force | Out-Null
}

function Write-Log {
    param($Message)
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    "$timestamp - $Message" | Out-File -FilePath $LogFile -Append -Encoding UTF8
    Write-Host "$timestamp - $Message"
}

function Get-AIServerStatus {
    # Check if port 8745 is listening
    $connection = Get-NetTCPConnection -LocalPort 8745 -State Listen -ErrorAction SilentlyContinue
    return ($null -ne $connection)
}

function Get-AIServerUserNumber {
    # Get QM user number for AI.SERVER phantom
    $tempCmd = "C:\qmsys\hal\COM\temp_listu.txt"
    $tempOut = "C:\qmsys\hal\COM\temp_listu_out.txt"
    
    "LISTU" | Out-File -FilePath $tempCmd -Encoding ASCII -NoNewline
    
    try {
        $process = Start-Process -FilePath "C:\QMSYS\BIN\qm.exe" -ArgumentList "-aHAL", "RUN BP COMMAND.EXECUTOR" -Wait -PassThru -WindowStyle Hidden
        
        if (Test-Path $tempOut) {
            $output = Get-Content $tempOut -Raw
            # Look for iPhantom with AI.SERVER pattern (typically last phantom started)
            if ($output -match "(\d+)\s+\d+\s+\d+.*iPhantom") {
                return $matches[1]
            }
        }
    }
    catch {
        Write-Log "Error checking LISTU: $_"
    }
    finally {
        Remove-Item $tempCmd -ErrorAction SilentlyContinue
    }
    
    return $null
}

function Start-AIServer {
    Write-Log "Starting AI.SERVER phantom..."
    
    # Check if already running
    if (Get-AIServerStatus) {
        Write-Log "AI.SERVER already running on port 8745"
        return $true
    }
    
    # Start the phantom using COMMAND.EXECUTOR
    try {
        $cmdFile = "C:\qmsys\hal\COM.DIR\INPUT.COMMANDS.txt"
        "PHANTOM BP AI.SERVER" | Out-File -FilePath $cmdFile -Encoding ASCII
        
        $process = Start-Process -FilePath "C:\QMSYS\BIN\qm.exe" -ArgumentList "-aHAL", "RUN BP COMMAND.EXECUTOR" -WindowStyle Hidden -PassThru -Wait
        
        Write-Log "Executed PHANTOM command via COMMAND.EXECUTOR"
        
        # Wait for service to start (up to 15 seconds)
        for ($i = 0; $i -lt 15; $i++) {
            Start-Sleep -Seconds 1
            if (Get-AIServerStatus) {
                Write-Log "AI.SERVER successfully started on port 8745"
                Remove-Item $cmdFile -ErrorAction SilentlyContinue
                return $true
            }
        }
        
        Write-Log "WARNING: AI.SERVER did not start within 15 seconds"
        Remove-Item $cmdFile -ErrorAction SilentlyContinue
        return $false
    }
    catch {
        Write-Log "ERROR starting AI.SERVER: $_"
        return $false
    }
}

function Stop-AIServer {
    Write-Log "Stopping AI.SERVER phantom..."
    
    $userNum = Get-AIServerUserNumber
    if ($userNum) {
        $killCmd = "C:\qmsys\hal\COM\temp_kill.txt"
        "KILL.PHANTOM $userNum" | Out-File -FilePath $killCmd -Encoding ASCII -NoNewline
        
        try {
            Start-Process -FilePath "C:\QMSYS\BIN\qm.exe" -ArgumentList "-aHAL", "RUN BP COMMAND.EXECUTOR" -Wait -WindowStyle Hidden
            Write-Log "Killed phantom user $userNum"
        }
        catch {
            Write-Log "Error killing phantom: $_"
        }
        finally {
            Remove-Item $killCmd -ErrorAction SilentlyContinue
        }
    }
    
    # Force stop any process on port 8745
    $connection = Get-NetTCPConnection -LocalPort 8745 -ErrorAction SilentlyContinue
    if ($connection) {
        $pid = $connection.OwningProcess
        Write-Log "Force stopping process $pid on port 8745"
        Stop-Process -Id $pid -Force -ErrorAction SilentlyContinue
    }
}

# Service main loop
Write-Log "=== AI.SERVER Service Starting ==="

# Start the server
if (!(Start-AIServer)) {
    Write-Log "CRITICAL: Failed to start AI.SERVER"
    exit 1
}

# Monitor loop
Write-Log "Entering monitor loop (checking every $CheckInterval seconds)"

while ($true) {
    Start-Sleep -Seconds $CheckInterval
    
    if (!(Get-AIServerStatus)) {
        Write-Log "WARNING: AI.SERVER not responding on port 8745. Restarting..."
        Start-AIServer
    }
}

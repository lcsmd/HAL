#
# Start AI Server Phantom Process
# This script is called by Windows Task Scheduler on boot
#
# It starts the OpenQM phantom and monitors it, restarting if it crashes
#

param(
    [switch]$Monitor = $true,
    [int]$RestartDelay = 10  # seconds to wait before restart
)

# Configuration
$QM_HOME = "C:\qmsys"
$QM_BIN = "$QM_HOME\bin"
$HAL_ACCOUNT = "hal"
$LOG_FILE = "$PSScriptRoot\phantom_monitor.log"

# Logging function
function Write-Log {
    param([string]$Message)
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $logEntry = "$timestamp - $Message"
    Write-Host $logEntry
    Add-Content -Path $LOG_FILE -Value $logEntry
}

# Function to check if phantom is running
function Test-PhantomRunning {
    # Check if port 8745 is listening
    $listening = Get-NetTCPConnection -LocalPort 8745 -ErrorAction SilentlyContinue
    return ($null -ne $listening)
}

# Function to start the phantom
function Start-Phantom {
    Write-Log "Starting AI Server phantom process..."
    
    try {
        # Create a background job to start the phantom
        $job = Start-Job -ScriptBlock {
            param($qmBin, $halAccount)
            
            $startScript = @"
LOGTO $halAccount
PHANTOM BP AI.SERVER
QUIT
"@
            $startScript | & "$qmBin\qm.exe" -a$halAccount
            
        } -ArgumentList $QM_BIN, $HAL_ACCOUNT
        
        # Wait a moment for startup
        Start-Sleep -Seconds 3
        
        # Check if it started successfully
        if (Test-PhantomRunning) {
            Write-Log "AI Server started successfully on port 8745"
            return $true
        } else {
            Write-Log "WARNING: AI Server may not have started correctly"
            return $false
        }
        
    } catch {
        Write-Log "ERROR: Failed to start phantom: $($_.Exception.Message)"
        return $false
    }
}

# Function to stop the phantom
function Stop-Phantom {
    Write-Log "Stopping AI Server phantom..."
    
    # Find QM processes
    $qmProcesses = Get-Process -Name "qm" -ErrorAction SilentlyContinue
    
    foreach ($proc in $qmProcesses) {
        try {
            Write-Log "Stopping process: $($proc.Id)"
            Stop-Process -Id $proc.Id -Force
        } catch {
            Write-Log "WARNING: Failed to stop process $($proc.Id)"
        }
    }
    
    Write-Log "Phantom stopped"
}

# Main execution
Write-Log "=========================================="
Write-Log "AI Server Phantom Manager Starting"
Write-Log "=========================================="

# Check if OpenQM is installed
if (-not (Test-Path "$QM_BIN\qm.exe")) {
    Write-Log "ERROR: OpenQM not found at $QM_BIN"
    exit 1
}

# Start the phantom
$started = Start-Phantom

if (-not $started) {
    Write-Log "ERROR: Failed to start phantom"
    exit 1
}

# If not monitoring, exit now
if (-not $Monitor) {
    Write-Log "Phantom started (no monitoring)"
    exit 0
}

# Monitor loop - keep checking if phantom is running
Write-Log "Entering monitor loop (check every 30 seconds)"
Write-Log "Press Ctrl+C to stop monitoring"

$checkCount = 0
while ($true) {
    Start-Sleep -Seconds 30
    $checkCount++
    
    if (Test-PhantomRunning) {
        # Still running - log every 10 checks (5 minutes)
        if ($checkCount % 10 -eq 0) {
            Write-Log "AI Server running (check #$checkCount)"
        }
    } else {
        # Not running - restart it
        Write-Log "WARNING: AI Server not responding on port 8745"
        Write-Log "Attempting restart in $RestartDelay seconds..."
        
        Start-Sleep -Seconds $RestartDelay
        
        # Try to clean up any stuck processes
        Stop-Phantom
        Start-Sleep -Seconds 2
        
        # Restart
        $restarted = Start-Phantom
        
        if ($restarted) {
            Write-Log "AI Server restarted successfully"
        } else {
            Write-Log "ERROR: Failed to restart AI Server"
            Write-Log "Will try again in 30 seconds"
        }
        
        $checkCount = 0  # Reset counter after restart
    }
}

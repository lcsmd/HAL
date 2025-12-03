# Voice Gateway Windows Service Wrapper
# Monitors and maintains Voice Gateway on port 8768

$ErrorActionPreference = "Continue"
$LogFile = "C:\qmsys\hal\LOGS\voice_gateway_service.log"
$CheckInterval = 30  # seconds
$PythonExe = "C:\Python313\python.exe"
$GatewayScript = "C:\qmsys\hal\PY\voice_gateway.py"

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

function Get-VoiceGatewayStatus {
    # Check if port 8768 is listening
    $connection = Get-NetTCPConnection -LocalPort 8768 -State Listen -ErrorAction SilentlyContinue
    return ($null -ne $connection)
}

function Get-VoiceGatewayPID {
    $connection = Get-NetTCPConnection -LocalPort 8768 -State Listen -ErrorAction SilentlyContinue
    if ($connection) {
        return $connection.OwningProcess
    }
    return $null
}

function Start-VoiceGateway {
    Write-Log "Starting Voice Gateway..."
    
    # Check if already running
    if (Get-VoiceGatewayStatus) {
        $pid = Get-VoiceGatewayPID
        Write-Log "Voice Gateway already running on port 8768 (PID: $pid)"
        return $true
    }
    
    # Start the gateway
    try {
        $process = Start-Process -FilePath $PythonExe -ArgumentList $GatewayScript -WorkingDirectory "C:\qmsys\hal" -WindowStyle Hidden -PassThru
        
        Write-Log "Launched Voice Gateway process (PID: $($process.Id))"
        
        # Wait for service to start (up to 10 seconds)
        for ($i = 0; $i -lt 10; $i++) {
            Start-Sleep -Seconds 1
            if (Get-VoiceGatewayStatus) {
                Write-Log "Voice Gateway successfully started on port 8768"
                return $true
            }
        }
        
        Write-Log "WARNING: Voice Gateway did not start within 10 seconds"
        return $false
    }
    catch {
        Write-Log "ERROR starting Voice Gateway: $_"
        return $false
    }
}

function Stop-VoiceGateway {
    Write-Log "Stopping Voice Gateway..."
    
    $pid = Get-VoiceGatewayPID
    if ($pid) {
        Write-Log "Stopping process $pid"
        Stop-Process -Id $pid -Force -ErrorAction SilentlyContinue
        Start-Sleep -Seconds 2
    }
}

# Service main loop
Write-Log "=== Voice Gateway Service Starting ==="

# Verify Python exists
if (!(Test-Path $PythonExe)) {
    Write-Log "CRITICAL: Python not found at $PythonExe"
    exit 1
}

# Verify script exists
if (!(Test-Path $GatewayScript)) {
    Write-Log "CRITICAL: Voice Gateway script not found at $GatewayScript"
    exit 1
}

# Start the gateway
if (!(Start-VoiceGateway)) {
    Write-Log "CRITICAL: Failed to start Voice Gateway"
    exit 1
}

# Monitor loop
Write-Log "Entering monitor loop (checking every $CheckInterval seconds)"

while ($true) {
    Start-Sleep -Seconds $CheckInterval
    
    if (!(Get-VoiceGatewayStatus)) {
        Write-Log "WARNING: Voice Gateway not responding on port 8768. Restarting..."
        Stop-VoiceGateway
        Start-Sleep -Seconds 2
        Start-VoiceGateway
    }
}

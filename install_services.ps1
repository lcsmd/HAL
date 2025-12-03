# Install HAL Services as Windows Services
# Run this script as Administrator

#Requires -RunAsAdministrator

$ErrorActionPreference = "Stop"

Write-Host "=" * 60 -ForegroundColor Cyan
Write-Host "Installing HAL Windows Services" -ForegroundColor Cyan
Write-Host "=" * 60 -ForegroundColor Cyan
Write-Host ""

# Service definitions
$services = @(
    @{
        Name = "HAL-AIServer"
        DisplayName = "HAL AI.SERVER"
        Description = "HAL AI.SERVER phantom process on port 8745 - Core AI logic processor"
        Script = "C:\qmsys\hal\service_ai_server.ps1"
        DependsOn = "QMSvc"
    },
    @{
        Name = "HAL-VoiceGateway"
        DisplayName = "HAL Voice Gateway"
        Description = "HAL Voice Gateway WebSocket server on port 8768 - Client connection handler"
        Script = "C:\qmsys\hal\service_voice_gateway.ps1"
        DependsOn = "HAL-AIServer"  # Voice Gateway depends on AI.SERVER
    }
)

foreach ($svc in $services) {
    Write-Host "Installing $($svc.DisplayName)..." -ForegroundColor Yellow
    
    # Check if service exists
    $existing = Get-Service -Name $svc.Name -ErrorAction SilentlyContinue
    if ($existing) {
        Write-Host "  Service already exists. Stopping and removing..." -ForegroundColor Yellow
        
        if ($existing.Status -eq "Running") {
            Stop-Service -Name $svc.Name -Force
            Start-Sleep -Seconds 2
        }
        
        # Use sc.exe to delete
        & sc.exe delete $svc.Name
        Start-Sleep -Seconds 2
    }
    
    # Verify script exists
    if (!(Test-Path $svc.Script)) {
        Write-Host "  ERROR: Script not found: $($svc.Script)" -ForegroundColor Red
        continue
    }
    
    # Create service using New-Service
    try {
        $params = @{
            Name = $svc.Name
            DisplayName = $svc.DisplayName
            Description = $svc.Description
            BinaryPathName = "powershell.exe -NoProfile -ExecutionPolicy Bypass -File `"$($svc.Script)`""
            StartupType = "Automatic"
        }
        
        if ($svc.DependsOn) {
            $params.DependsOn = $svc.DependsOn
        }
        
        New-Service @params | Out-Null
        
        Write-Host "  Service created successfully" -ForegroundColor Green
        
        # Configure service recovery options (restart on failure)
        & sc.exe failure $svc.Name reset= 86400 actions= restart/5000/restart/10000/restart/30000
        
        # Set service to run as LocalSystem
        & sc.exe config $svc.Name obj= LocalSystem
        
        Write-Host "  Configured auto-restart on failure" -ForegroundColor Green
    }
    catch {
        Write-Host "  ERROR: Failed to create service: $_" -ForegroundColor Red
        continue
    }
}

Write-Host ""
Write-Host "=" * 60 -ForegroundColor Cyan
Write-Host "Service Installation Summary" -ForegroundColor Cyan
Write-Host "=" * 60 -ForegroundColor Cyan
Write-Host ""

# Show service status
Get-Service -Name "HAL-*" | Format-Table Name, DisplayName, Status, StartType -AutoSize

Write-Host ""
Write-Host "Next Steps:" -ForegroundColor Yellow
Write-Host "1. Start services: .\start_services.ps1" -ForegroundColor White
Write-Host "2. Check status: Get-Service HAL-*" -ForegroundColor White
Write-Host "3. View logs: Get-Content C:\qmsys\hal\LOGS\*_service.log -Tail 50" -ForegroundColor White
Write-Host ""
Write-Host "To start services now, run:" -ForegroundColor Yellow
Write-Host "  Start-Service HAL-AIServer" -ForegroundColor White
Write-Host "  Start-Service HAL-VoiceGateway" -ForegroundColor White
Write-Host ""

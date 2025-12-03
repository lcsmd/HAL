# Uninstall HAL Services
# Run this script as Administrator

#Requires -RunAsAdministrator

Write-Host "=" * 60 -ForegroundColor Cyan
Write-Host "Uninstalling HAL Windows Services" -ForegroundColor Cyan
Write-Host "=" * 60 -ForegroundColor Cyan
Write-Host ""

$services = @("HAL-VoiceGateway", "HAL-AIServer")

foreach ($svcName in $services) {
    Write-Host "Removing $svcName..." -ForegroundColor Yellow
    
    $svc = Get-Service -Name $svcName -ErrorAction SilentlyContinue
    if (!$svc) {
        Write-Host "  Service not found" -ForegroundColor Yellow
        continue
    }
    
    # Stop if running
    if ($svc.Status -eq "Running") {
        Write-Host "  Stopping service..." -ForegroundColor Yellow
        Stop-Service -Name $svcName -Force
        Start-Sleep -Seconds 2
    }
    
    # Delete service
    & sc.exe delete $svcName
    Write-Host "  Removed" -ForegroundColor Green
}

Write-Host ""
Write-Host "Services uninstalled successfully" -ForegroundColor Green
Write-Host ""

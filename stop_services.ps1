# Stop HAL Services

Write-Host "=" * 60 -ForegroundColor Cyan
Write-Host "Stopping HAL Services" -ForegroundColor Cyan
Write-Host "=" * 60 -ForegroundColor Cyan
Write-Host ""

$services = @("HAL-VoiceGateway", "HAL-AIServer")  # Reverse order for dependencies

foreach ($svcName in $services) {
    Write-Host "Stopping $svcName..." -ForegroundColor Yellow
    
    $svc = Get-Service -Name $svcName -ErrorAction SilentlyContinue
    if (!$svc) {
        Write-Host "  Service not found" -ForegroundColor Yellow
        continue
    }
    
    if ($svc.Status -ne "Running") {
        Write-Host "  Already stopped" -ForegroundColor Green
        continue
    }
    
    try {
        Stop-Service -Name $svcName -Force
        Start-Sleep -Seconds 2
        
        $svc = Get-Service -Name $svcName
        if ($svc.Status -eq "Stopped") {
            Write-Host "  Stopped successfully" -ForegroundColor Green
        }
        else {
            Write-Host "  WARNING: Service state is $($svc.Status)" -ForegroundColor Yellow
        }
    }
    catch {
        Write-Host "  ERROR: $_" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "Service Status:" -ForegroundColor Cyan
Get-Service -Name "HAL-*" | Format-Table Name, Status, StartType -AutoSize
Write-Host ""

# Start HAL Services
# Can be run as regular user

Write-Host "=" * 60 -ForegroundColor Cyan
Write-Host "Starting HAL Services" -ForegroundColor Cyan
Write-Host "=" * 60 -ForegroundColor Cyan
Write-Host ""

$services = @("HAL-AIServer", "HAL-VoiceGateway")

foreach ($svcName in $services) {
    Write-Host "Starting $svcName..." -ForegroundColor Yellow
    
    $svc = Get-Service -Name $svcName -ErrorAction SilentlyContinue
    if (!$svc) {
        Write-Host "  ERROR: Service not found. Run install_services.ps1 first." -ForegroundColor Red
        continue
    }
    
    if ($svc.Status -eq "Running") {
        Write-Host "  Already running" -ForegroundColor Green
        continue
    }
    
    try {
        Start-Service -Name $svcName
        Start-Sleep -Seconds 3
        
        $svc = Get-Service -Name $svcName
        if ($svc.Status -eq "Running") {
            Write-Host "  Started successfully" -ForegroundColor Green
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
Write-Host "Port Status:" -ForegroundColor Cyan
$ports = @(8745, 8768)
foreach ($port in $ports) {
    $conn = Get-NetTCPConnection -LocalPort $port -State Listen -ErrorAction SilentlyContinue
    if ($conn) {
        Write-Host "  Port $port : LISTENING (PID: $($conn.OwningProcess))" -ForegroundColor Green
    }
    else {
        Write-Host "  Port $port : NOT LISTENING" -ForegroundColor Red
    }
}

Write-Host ""

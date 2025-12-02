# Start Backend Microservices for Agent Testing
# This script starts the key services needed for multi-agent system integration

Write-Host "==================================================================" -ForegroundColor Cyan
Write-Host "  Starting Backend Microservices for Agent Testing" -ForegroundColor Cyan
Write-Host "==================================================================" -ForegroundColor Cyan
Write-Host ""

# Service configuration
$services = @(
    @{Name="Gateway Service"; Path="backend/services/gateway_service"; Port=8000}
    @{Name="Order Service"; Path="backend/services/order_service"; Port=8001}
    @{Name="Returns Service"; Path="backend/services/returns_service"; Port=8002}
    @{Name="Inventory Service"; Path="backend/services/inventory_service"; Port=8003}
    @{Name="Customer Service"; Path="backend/services/customer_service"; Port=8004}
)

Write-Host "Starting essential services..." -ForegroundColor Yellow
Write-Host ""

$jobs = @()

foreach ($service in $services) {
    $serviceName = $service.Name
    $servicePath = $service.Path
    $port = $service.Port
    
    Write-Host "Starting $serviceName on port $port..." -ForegroundColor Green
    
    # Start service in background job
    $job = Start-Job -Name $serviceName -ScriptBlock {
        param($path, $port)
        Set-Location $using:PWD
        cd $path
        $env:PYTHONIOENCODING = "utf-8"
        py -3.10 -m uvicorn main:app --host 0.0.0.0 --port $port
    } -ArgumentList $servicePath, $port
    
    $jobs += $job
    
    # Give each service time to start
    Start-Sleep -Milliseconds 500
}

Write-Host ""
Write-Host "==================================================================" -ForegroundColor Cyan
Write-Host "  Services Started!" -ForegroundColor Green
Write-Host "==================================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Running services:" -ForegroundColor Yellow

foreach ($service in $services) {
    Write-Host "  $($service.Name) on port $($service.Port)" -ForegroundColor White
}

Write-Host ""
Write-Host "Waiting for services to initialize (10 seconds)..." -ForegroundColor Yellow
Start-Sleep -Seconds 10

Write-Host ""
Write-Host "==================================================================" -ForegroundColor Cyan
Write-Host "  Health Check" -ForegroundColor Cyan
Write-Host "==================================================================" -ForegroundColor Cyan
Write-Host ""

foreach ($service in $services) {
    try {
        $response = Invoke-WebRequest -Uri "http://localhost:$($service.Port)/health" -Method Get -TimeoutSec 2 -ErrorAction Stop
        if ($response.StatusCode -eq 200) {
            Write-Host "  OK: $($service.Name)" -ForegroundColor Green
        }
    } catch {
        Write-Host "  ERROR: $($service.Name) not responding" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "==================================================================" -ForegroundColor Cyan
Write-Host "Services are ready for agent testing!" -ForegroundColor Green
Write-Host ""
Write-Host "To view service logs: Get-Job | Receive-Job" -ForegroundColor Yellow
Write-Host "To stop all services: Get-Job | Stop-Job; Get-Job | Remove-Job" -ForegroundColor Yellow
Write-Host "==================================================================" -ForegroundColor Cyan
Write-Host ""

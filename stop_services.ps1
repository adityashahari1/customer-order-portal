# Stop all backend microservices
# Use this to cleanly shut down services started with start_services.ps1

Write-Host "==================================================================" -ForegroundColor Cyan
Write-Host "  Stopping Backend Microservices" -ForegroundColor Cyan
Write-Host "==================================================================" -ForegroundColor Cyan
Write-Host ""

# Get all running service jobs
$jobs = Get-Job | Where-Object { $_.State -eq "Running" }

if ($jobs.Count -eq 0) {
    Write-Host "No running services found." -ForegroundColor Yellow
} else {
    Write-Host "Stopping $($jobs.Count) service(s)..." -ForegroundColor Yellow
    
    foreach ($job in $jobs) {
        Write-Host "  • Stopping $($job.Name)..." -ForegroundColor White
        Stop-Job -Job $job
        Remove-Job -Job $job
    }
    
    Write-Host ""
    Write-Host "✓ All services stopped successfully!" -ForegroundColor Green
}

Write-Host ""
Write-Host "==================================================================" -ForegroundColor Cyan

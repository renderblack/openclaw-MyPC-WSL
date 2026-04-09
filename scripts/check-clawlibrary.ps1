try {
    $response = Invoke-WebRequest -Uri 'http://localhost:5173/' -Method HEAD -TimeoutSec 3 -ErrorAction Stop
    Write-Host "Status: $($response.StatusCode)"
} catch {
    Write-Host "Error: $($_.Exception.Message)"
}

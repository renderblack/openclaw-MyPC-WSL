# Test Quark local API
try {
    $r = Invoke-WebRequest -Uri 'http://127.0.0.1:9128/' -TimeoutSec 5 -ErrorAction Stop
    Write-Host "Status: $($r.StatusCode)"
    Write-Host "Content: $($r.Content)"
} catch {
    Write-Host "Error: $($_.Exception.Message)"
}

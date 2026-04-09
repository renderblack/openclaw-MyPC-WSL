try {
    $response = Invoke-WebRequest -Uri 'http://localhost:5173/' -TimeoutSec 5 -ErrorAction Stop
    Write-Host "Status: $($response.StatusCode)"
    Write-Host "Content length: $($response.Content.Length) bytes"
    Write-Host "First 200 chars: $($response.Content.Substring(0, [Math]::Min(200, $response.Content.Length)))"
} catch {
    Write-Host "Error: $($_.Exception.Message)"
}

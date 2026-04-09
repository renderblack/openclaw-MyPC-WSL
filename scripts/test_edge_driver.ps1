# Test download Edge Driver
$version = "146.0.3856.97"
$url = "https://msedgedriver.azureedge.net/$version/edgedriver_win64.zip"
Write-Host "Testing: $url"

try {
    $response = Invoke-WebRequest -Uri $url -Proxy 'http://127.0.0.1:7890' -TimeoutSec 30 -UseBasicParsing -Method Head
    Write-Host "Status: $($response.StatusCode)"
    Write-Host "Headers: $($response.Headers | Format-Table | Out-String)"
} catch {
    Write-Host "Error: $_"
}

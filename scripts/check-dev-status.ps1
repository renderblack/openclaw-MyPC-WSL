# Check node/npm processes
Write-Host "=== Node/npm Processes ==="
Get-Process | Where-Object { $_.ProcessName -like '*node*' -or $_.ProcessName -like '*npm*' } | Format-Table Id, ProcessName, Path -AutoSize

Write-Host "`n=== Port 5173 ==="
$portCheck = netstat -ano | Where-Object { $_ -match ':5173' }
if ($portCheck) {
    $portCheck | ForEach-Object { Write-Host $_ }
} else {
    Write-Host "Port 5173 NOT in use"
}

Write-Host "`n=== Running ClawLibrary test ==="
try {
    $response = Invoke-WebRequest -Uri 'http://localhost:5173/' -TimeoutSec 3 -ErrorAction Stop
    Write-Host "Success! Status: $($response.StatusCode)"
} catch {
    Write-Host "Failed: $($_.Exception.Message)"
}

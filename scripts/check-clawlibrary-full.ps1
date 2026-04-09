# Check ClawLibrary status
Write-Host "=== Checking ClawLibrary ==="

# Check if port 5173 is in use
$conn = netstat -ano | Select-String "5173"
if ($conn) {
    Write-Host "Port 5173 is in use:"
    $conn | ForEach-Object { Write-Host $_ }
} else {
    Write-Host "Port 5173 is NOT in use"
}

# Check if any node process is running
$nodeProcs = Get-Process -Name node -ErrorAction SilentlyContinue
if ($nodeProcs) {
    Write-Host "Node processes found: $($nodeProcs.Count)"
    $nodeProcs | ForEach-Object { Write-Host "  PID: $($_.Id) - $($_.Path)" }
} else {
    Write-Host "No node processes found"
}

# Try to connect to ClawLibrary
try {
    $response = Invoke-WebRequest -Uri 'http://localhost:5173/' -Method HEAD -TimeoutSec 3 -ErrorAction Stop
    Write-Host "ClawLibrary response: $($response.StatusCode)"
} catch {
    Write-Host "ClawLibrary error: $($_.Exception.Message)"
}

# List D: drive directories
Write-Host "`n=== D: Drive Directories ==="
try {
    Get-ChildItem -Path 'D:\' -Directory -ErrorAction Stop | ForEach-Object { Write-Host $_.Name }
} catch {
    Write-Host "Error listing D:\ : $($_.Exception.Message)"
}

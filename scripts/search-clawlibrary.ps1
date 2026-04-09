# Search for ClawLibrary
Write-Host "=== Searching for ClawLibrary ==="

$searchLocations = @('C:\', 'D:\')
$results = @()

foreach ($location in $searchLocations) {
    Write-Host "Searching in $location..."
    
    # Search for directories with "claw" or "library" in name
    Get-ChildItem -Path $location -Directory -ErrorAction SilentlyContinue |
        Where-Object { $_.Name -match 'claw|library|龙虾' } |
        ForEach-Object {
            Write-Host "Found: $($_.FullName)"
            $results += $_
        }
}

# Also check common locations
$commonPaths = @(
    'C:\Users\Administrator\clawlibrary',
    'C:\Users\Administrator\.clawlibrary',
    'C:\clawlibrary',
    'D:\clawlibrary',
    'D:\ClawLibrary',
    'D:\claw-library',
    'C:\Users\Administrator\Documents\clawlibrary',
    "$env:APPDATA\clawlibrary",
    "$env:LOCALAPPDATA\clawlibrary"
)

Write-Host "`n=== Checking common paths ==="
foreach ($path in $commonPaths) {
    if (Test-Path $path) {
        Write-Host "EXISTS: $path"
        $results += Get-Item $path
    }
}

# Check if there's a node process running on a different port
Write-Host "`n=== Node processes and ports ==="
Get-Process -Name node -ErrorAction SilentlyContinue | ForEach-Object {
    Write-Host "Node PID: $($_.Id)"
    Write-Host "  Path: $($_.Path)"
}

# Check for vite or npm processes
Write-Host "`n=== Looking for vite/npm processes ==="
Get-Process | Where-Object { $_.Name -match 'vite|npm' } | ForEach-Object {
    Write-Host "$($_.Name) PID: $($_.Id)"
}

Write-Host "`n=== Summary ==="
Write-Host "Found $($results.Count) items"

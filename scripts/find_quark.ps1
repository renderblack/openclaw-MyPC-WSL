# Find Quark executable
$searchLocations = @(
    "${env:ProgramFiles}\quark",
    "${env:ProgramFiles(x86)}\quark",
    "$env:LOCALAPPDATA\Programs\quark",
    "$env:APPDATA\quark"
)

$found = $false
foreach ($loc in $searchLocations) {
    if (Test-Path $loc) {
        Write-Host "Found: $loc"
        Get-ChildItem $loc -Recurse -Filter "*.exe" | Select-Object FullName
        $found = $true
    }
}

if (-not $found) {
    Write-Host "Quark not found in standard locations"
}

# Also check for Quark in registry
$regPaths = @(
    "HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\*",
    "HKCU:\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\*"
)

foreach ($regPath in $regPaths) {
    $apps = Get-ItemProperty $regPath -ErrorAction SilentlyContinue | Where-Object { $_.DisplayName -like "*quark*" }
    if ($apps) {
        Write-Host "`nFound in registry:"
        $apps | Select-Object DisplayName, InstallLocation | Format-Table
    }
}

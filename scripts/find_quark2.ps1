# Search for Quark executable broadly
$searchRoots = @("C:\", "D:\", "$env:ProgramFiles", "${env:ProgramFiles(x86)}", "$env:LOCALAPPDATA")

$exeFiles = @()

foreach ($root in $searchRoots) {
    if (Test-Path $root) {
        Write-Host "Searching in: $root"
        Get-ChildItem $root -Recurse -ErrorAction SilentlyContinue -Filter "quark*.exe" | ForEach-Object {
            $exeFiles += $_.FullName
            Write-Host "  Found: $($_.FullName)"
        }
    }
}

if ($exeFiles.Count -eq 0) {
    Write-Host "`nNo quark*.exe found"
    
    # Try looking in registry for installation path
    $regPaths = @(
        "HKLM:\SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall\*",
        "HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\*",
        "HKCU:\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\*"
    )
    
    foreach ($path in $regPaths) {
        Get-ItemProperty $path -ErrorAction SilentlyContinue | ForEach-Object {
            if ($_.DisplayName -like "*quark*" -and $_.InstallLocation) {
                Write-Host "`nRegistry info:"
                Write-Host "  Name: $($_.DisplayName)"
                Write-Host "  Path: $($_.InstallLocation)"
            }
        }
    }
}

# Also check running processes
Write-Host "`nRunning processes with 'quark' in name:"
Get-Process | Where-Object { $_.ProcessName -like "*quark*" } | ForEach-Object {
    Write-Host "  $($_.ProcessName) (PID: $($_.Id))"
    Write-Host "    Path: $($_.Path)"
}

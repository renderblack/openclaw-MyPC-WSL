# List quark directory contents
$quarkPath = "$env:USERPROFILE\AppData\Roaming\quark"
Write-Host "Quark path: $quarkPath"

if (Test-Path $quarkPath) {
    Write-Host "`nContents:"
    Get-ChildItem $quarkPath -ErrorAction SilentlyContinue | ForEach-Object {
        Write-Host $_.FullName
    }
    
    # Search recursively for exe
    Write-Host "`nSearching for .exe files..."
    Get-ChildItem $quarkPath -Recurse -ErrorAction SilentlyContinue | ForEach-Object {
        if ($_.Extension -eq ".exe") {
            Write-Host "EXE: $($_.FullName)"
        }
    }
} else {
    Write-Host "Path does not exist"
}

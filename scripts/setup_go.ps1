$oldPath = [Environment]::GetEnvironmentVariable('Path', 'User')
$newPath = 'D:\go\bin;' + $oldPath
[Environment]::SetEnvironmentVariable('Path', $newPath, 'User')
$env:Path = 'D:\go\bin;' + $env:Path
Write-Host "Added D:\go\bin to PATH"

# Verify
& D:\go\bin\go.exe version

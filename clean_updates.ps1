# Windows Update Cleanup Script
Write-Host "Cleaning Windows Update cache..."

# Stop services
Stop-Service -Name wuauserv -Force -ErrorAction SilentlyContinue
Stop-Service -Name bits -Force -ErrorAction SilentlyContinue

# Clean SoftwareDistribution
$distDir = "C:\Windows\SoftwareDistribution\Download"
if (Test-Path $distDir) {
    Remove-Item -Path "$distDir\*" -Recurse -Force -ErrorAction SilentlyContinue
    Write-Host "Cleaned SoftwareDistribution"
}

# Clean temp files
$tempDir = "C:\Windows\Temp"
if (Test-Path $tempDir) {
    Remove-Item -Path "$tempDir\*.tmp" -Force -ErrorAction SilentlyContinue
    Write-Host "Cleaned temp files"
}

# Restart services
Start-Service -Name bits -ErrorAction SilentlyContinue
Start-Service -Name wuauserv -ErrorAction SilentlyContinue

# Show result
$disk = Get-PSDrive -PSProvider FileSystem | Where-Object {$_.Root -eq "C:\"}
$freeGB = [math]::Round($disk.Free / 1GB, 2)
Write-Host "Done! C drive free: $freeGB GB"
Write-Host "Recommend: Restart PC to finish cleanup"

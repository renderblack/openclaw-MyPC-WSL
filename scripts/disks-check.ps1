$colDisks = Get-CimInstance -ClassName Win32_LogicalDisk -Filter "DriveType=3"
foreach ($disk in $colDisks) {
    $freeGB = [math]::Round($disk.FreeSpace/1GB,1)
    $totalGB = [math]::Round($disk.Size/1GB,1)
    $usedGB = [math]::Round(($disk.Size - $disk.FreeSpace)/1GB,1)
    Write-Host "$($disk.DeviceID) - Free: $freeGB GB / Total: $totalGB GB (Used: $usedGB GB)"
}

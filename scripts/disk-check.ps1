$disk = Get-PSDrive -PSProvider FileSystem | Where-Object { $_.Root -eq 'C:' }
$free = $disk.Free
$total = $disk.Free + $disk.Used
$freeGB = [math]::Round($free / 1GB, 2)
$totalGB = [math]::Round($total / 1GB, 2)
Write-Host "C: $freeGB GB free / $totalGB GB total"

$disk = Get-PSDrive C
$total = [math]::Round(($disk.Free + $disk.Used) / 1GB, 2)
$free = [math]::Round($disk.Free / 1GB, 2)
$used = [math]::Round($disk.Used / 1GB, 2)
$pct = [math]::Round($disk.Used / ($disk.Free + $disk.Used) * 100, 1)
Write-Host "C: $free GB Free / $total GB Total ($pct% used)"

$mem = Get-CimInstance Win32_OperatingSystem
$freemem = [math]::Round($mem.FreePhysicalMemory / 1MB, 1)
Write-Host "RAM: $freemem GB Available"

$openclawProcs = Get-Process | Where-Object {$_.Name -like "*openclaw*"} | Measure-Object
Write-Host "OpenClaw processes: $($openclawProcs.Count)"

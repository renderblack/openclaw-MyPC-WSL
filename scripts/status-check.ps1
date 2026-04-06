$diskC = Get-PSDrive -PSProvider FileSystem | Where-Object {$_.Root -eq "C:"}
$diskD = Get-PSDrive -PSProvider FileSystem | Where-Object {$_.Root -eq "D:"}
$mem = Get-CimInstance Win32_OperatingSystem
$freeMem = [math]::Round($mem.FreePhysicalMemory/1MB,1)
Write-Host "C: $([math]::Round($diskC.Free/1GB,1)) GB free / $([math]::Round($diskC.Used/1GB,1)) GB used"
Write-Host "D: $([math]::Round($diskD.Free/1GB,1)) GB free"
Write-Host "RAM: $freeMem GB available"

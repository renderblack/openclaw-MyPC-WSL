$disk = Get-PSDrive -PSProvider FileSystem | Where-Object {$_.Root -eq "C:"}
$free = [math]::Round($disk.Free/1GB,1)
Write-Host "C: $free GB free"

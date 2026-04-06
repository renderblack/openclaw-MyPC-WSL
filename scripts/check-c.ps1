$d = Get-PSDrive C
$total = [math]::Round(($d.Used+$d.Free)/1GB,2)
$used = [math]::Round($d.Used/1GB,2)
$free = [math]::Round($d.Free/1GB,2)
$pct = [math]::Round($d.Used/($d.Used+$d.Free)*100,1)
Write-Host "C盘状态:"
Write-Host "总容量: $total GB"
Write-Host "已用:   $used GB"
Write-Host "可用:   $free GB"
Write-Host "使用率: $pct%"

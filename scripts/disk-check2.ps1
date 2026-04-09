$d = Get-PSDrive C
$free = [math]::Round($d.Free / 1GB, 2)
$used = [math]::Round($d.Used / 1GB, 2)
$total = [math]::Round(($d.Free + $d.Used) / 1GB, 2)
$pct = [math]::Round($d.Used / ($d.Free + $d.Used) * 100, 1)
Write-Host "C: $free GB free / $total GB total ($pct% used)"

# Check for listening ports
$listening = Get-NetTCPConnection -State Listen
$localPorts = $listening | Where-Object { $_.LocalAddress -eq '127.0.0.1' -or $_.LocalAddress -eq '::1' } | Select-Object LocalAddress, LocalPort, OwningProcess

Write-Host "Local listening ports:"
$localPorts | Format-Table

# Also try to find quark-related ports
$quarkPorts = $listening | Where-Object { $_.OwningProcess -in (Get-Process -Name quark -ErrorAction SilentlyContinue).Id }
Write-Host "`nQuark-related listening ports:"
$quarkPorts | Format-Table

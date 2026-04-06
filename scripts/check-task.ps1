$t = Get-ScheduledTask -TaskName 'OpenClaw Gateway'
Write-Host "=== Actions ==="
$t.Actions | Format-List *
Write-Host "=== Settings ==="
$t.Settings | Format-List *
Write-Host "=== Principal ==="
$t.Principal | Format-List *

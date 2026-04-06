# Extract gateway restart events around 23:21 on April 5
$content = Get-Content 'C:\Users\ADMINI~1\AppData\Local\Temp\openclaw\openclaw-2026-04-06.log' -Raw

# Find entries around 23:21 (UTC+8 = 15:21 UTC)
$pattern = '2026-04-05T15:2[01]:'

$lines = $content -split "`n" | Where-Object { $_ -match $pattern }

Write-Host "=== Entries around 23:21 Beijing time ==="
Write-Host "Found $($lines.Count) lines matching pattern"
Write-Host ""

foreach ($line in $lines) {
    if ($line -match '"time":"([^"]+)"') {
        $time = $matches[1]
    }
    if ($line -match '"name":"([^"]+)"') {
        $name = $matches[1]
    }
    if ($line -match '"logLevelName":"([^"]+)"') {
        $level = $matches[1]
    }
    if ($line -match '"1":"([^"]+)"') {
        $msg = $matches[1]
    }
    
    Write-Host "Time: $time | Level: $level | Name: $name"
    Write-Host "  Msg: $msg"
    Write-Host ""
}

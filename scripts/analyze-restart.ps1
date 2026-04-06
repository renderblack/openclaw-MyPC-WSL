# Extract gateway restart events around 23:21 on April 5
$content = Get-Content 'C:\Users\ADMINI~1\AppData\Local\Temp\openclaw\openclaw-2026-04-06.log' -Raw

# Find entries around 23:21 (UTC+8 = 15:21 UTC)
$lines = $content -split "`n" | Where-Object { $_ -match '"time":"2026-04-05T15:2[01]:' }

Write-Host "=== Entries around 23:21 Beijing time ==="
foreach ($line in $lines) {
    try {
        $json = $line | ConvertFrom-Json
        $name = if ($json._meta) { $json._meta.name } else { "unknown" }
        $level = if ($json._meta) { $json._meta.logLevelName } else { "unknown" }
        Write-Host "Time: $($json.time) | Level: $level | Name: $name"
        Write-Host "  Message: $($json.Message)"
        Write-Host ""
    } catch {
        Write-Host "Parse error: $_"
    }
}

$path = 'C:\Users\Administrator\.openclaw\workspace\MEMORY.md'
$bytes = [System.IO.File]::ReadAllBytes($path)
$content = [System.Text.Encoding]::UTF8.GetString($bytes)

$lines = $content -split "`n"
foreach ($i in 0..($lines.Length-1)) {
    if ($lines[$i] -match 'C .+: .+ GB .+ / 222\.9 GB') {
        Write-Host "Found at line $($i+1): $($lines[$i])"
        # Replace with current value
        $lines[$i] = "- **C 盘**: 77.41 GB 可用 / 222.9 GB 总容量 (65.3% 已用)"
        Write-Host "New: $($lines[$i])"
    }
}

$newContent = $lines -join "`n"
$newBytes = [System.Text.Encoding]::UTF8.GetBytes($newContent)
[System.IO.File]::WriteAllBytes($path, $newBytes)
Write-Host 'Done'

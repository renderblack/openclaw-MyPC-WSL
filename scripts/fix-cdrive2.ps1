$path = 'C:\Users\Administrator\.openclaw\workspace\MEMORY.md'
$bytes = [System.IO.File]::ReadAllBytes($path)
$content = [System.Text.Encoding]::UTF8.GetString($bytes)

# Find the line with C drive info
$lines = $content -split "`n"
foreach ($i in 0..($lines.Length-1)) {
    if ($lines[$i] -match '84\.54') {
        Write-Host "Found at line $($i+1): $($lines[$i])"
        $lines[$i] = $lines[$i] -replace '84\.54 GB.*?/ 222\.9 GB.*?62\.1%.*?已用.*?\)', '77.84 GB 可用 / 222.9 GB 总容量 (65.1% 已用)'
        Write-Host "Replaced with: $($lines[$i])"
    }
}

$newContent = $lines -join "`n"
$newBytes = [System.Text.Encoding]::UTF8.GetBytes($newContent)
[System.IO.File]::WriteAllBytes($path, $newBytes)
Write-Host 'Done'

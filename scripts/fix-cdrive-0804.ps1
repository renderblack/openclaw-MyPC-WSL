$path = 'C:\Users\Administrator\.openclaw\workspace\MEMORY.md'
$bytes = [System.IO.File]::ReadAllBytes($path)
$content = [System.Text.Encoding]::UTF8.GetString($bytes)

$lines = $content -split "`n"
foreach ($i in 0..($lines.Length-1)) {
    if ($lines[$i] -match 'C .+: .+ GB .+ / 222\.9 GB') {
        $lines[$i] = "- **C 盘**: 75.76 GB 可用 / 222.9 GB 总容量 (66% 已用)"
    }
}

$newContent = $lines -join "`n"
$newBytes = [System.Text.Encoding]::UTF8.GetBytes($newContent)
[System.IO.File]::WriteAllBytes($path, $newBytes)
Write-Host 'Done'

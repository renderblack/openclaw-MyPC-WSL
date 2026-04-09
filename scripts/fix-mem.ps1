$content = [System.IO.File]::ReadAllText('C:\Users\Administrator\.openclaw\workspace\MEMORY.md', [System.Text.Encoding]::UTF8)
$content = $content -replace '84\.54 GB 可用 / 222\.9 GB 总容量 \(62\.1% 已用\)', '77.84 GB 可用 / 222.9 GB 总容量 (65.1% 已用)'
[System.IO.File]::WriteAllText('C:\Users\Administrator\.openclaw\workspace\MEMORY.md', $content, [System.Text.Encoding]::UTF8)
Write-Host 'Done'

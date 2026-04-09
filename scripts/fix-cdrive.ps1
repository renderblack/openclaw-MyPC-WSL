# Read with default encoding
$content = Get-Content 'C:\Users\Administrator\.openclaw\workspace\MEMORY.md' -Raw
# Replace old C drive line with new one
$content = $content -replace '84\.54 GB.*?/ 222\.9 GB.*?62\.1% 已用\)', '77.84 GB 可用 / 222.9 GB 总容量 (65.1% 已用)'
# Write back with UTF-8 BOM
$utf8Bom = New-Object System.Text.UTF8Encoding $true
[System.IO.File]::WriteAllText('C:\Users\Administrator\.openclaw\workspace\MEMORY.md', $content, $utf8Bom)
Write-Host 'Updated'

$path = 'C:\Users\Administrator\.openclaw\workspace\MEMORY.md'
$bytes = [System.IO.File]::ReadAllBytes($path)
$content = [System.Text.Encoding]::UTF8.GetString($bytes)
$lines = $content -split "`n"
foreach ($i in 0..($lines.Length-1)) {
    if ($lines[$i] -match '77\.41') {
        $lines[$i] = $lines[$i] -replace '77\.41', '76.37'
        $lines[$i] = $lines[$i] -replace '65\.3%', '65.7%'
    }
}
$newContent = $lines -join "`n"
[System.IO.File]::WriteAllText($path, $newContent, [System.Text.UTF8Encoding]::new($true))

$path = 'C:\Users\Administrator\.openclaw\workspace\MEMORY.md'
$bytes = [System.IO.File]::ReadAllBytes($path)
$content = [System.Text.Encoding]::UTF8.GetString($bytes)

# Find the line with C drive info - look for pattern "84.54" followed by "GB"
$lines = $content -split "`n"
foreach ($i in 0..($lines.Length-1)) {
    if ($lines[$i] -match '84\.54') {
        Write-Host "Found at line $($i+1)"
        # Replace just the 84.54 with 77.84 and 62.1 with 65.1
        $lines[$i] = $lines[$i] -replace '84\.54', '77.84'
        $lines[$i] = $lines[$i] -replace '62\.1%', '65.1%'
        Write-Host "New: $($lines[$i])"
    }
}

$newContent = $lines -join "`n"
$newBytes = [System.Text.Encoding]::UTF8.GetBytes($newContent)
[System.IO.File]::WriteAllBytes($path, $newBytes)
Write-Host 'Done'

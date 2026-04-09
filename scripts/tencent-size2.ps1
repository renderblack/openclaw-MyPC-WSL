$targets = @(
    "C:\Users\Administrator\AppData\Roaming\Tencent",
    "C:\Users\Administrator\AppData\Local\Tencent",
    "C:\ProgramData\Tencent"
)

foreach ($base in $targets) {
    if (!(Test-Path $base)) { continue }
    Write-Host "`n=== $base ===" -ForegroundColor Cyan
    
    $subs = Get-ChildItem $base -Force -ErrorAction SilentlyContinue | Where-Object { $_.PSIsContainer }
    $results = @()
    
    foreach ($sub in $subs) {
        $sizeBytes = 0
        try {
            $files = Get-ChildItem $sub.FullName -Recurse -Force -ErrorAction SilentlyContinue | Where-Object { !$_.PSIsContainer }
            if ($files) {
                $sizeBytes = ($files | Measure-Object -Property Length -Sum).Sum
            }
        } catch {}
        $sizeGB = [math]::Round($sizeBytes / 1GB, 2)
        $results += [PSCustomObject]@{
            Folder = $sub.Name
            SizeGB = $sizeGB
        }
    }
    
    $results | Sort-Object SizeGB -Descending | Where-Object { $_.SizeGB -gt 0 } | Format-Table -AutoSize
}

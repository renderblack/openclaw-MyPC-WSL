param(
    [string]$Keyword = "中铁二十四局沪昆铁路合同",
    [string]$SearchPath = "G:\",
    [int]$MaxResults = 30
)

Write-Host "Searching for: $Keyword" -ForegroundColor Cyan
Write-Host "Search path: $SearchPath" -ForegroundColor Cyan
Write-Host ""

$results = @()

try {
    $files = Get-ChildItem -Path $SearchPath -Recurse -File -ErrorAction SilentlyContinue | Where-Object { $_.Extension -in @('.pdf', '.docx', '.doc', '.txt', '.md', '.xlsx', '.xls', '.pptx', '.ppt') }
    
    $keywords = @($Keyword)
    
    foreach ($file in $files) {
        $score = 0
        $fileName = $file.Name
        $filePath = $file.FullName
        
        if ($fileName -like "*$Keyword*") {
            $score += 100
        }
        
        if ($fileName -like "*中铁*") { $score += 30 }
        if ($fileName -like "*二十四局*") { $score += 30 }
        if ($fileName -like "*沪昆*") { $score += 30 }
        if ($fileName -like "*铁路*") { $score += 20 }
        if ($fileName -like "*合同*") { $score += 20 }
        if ($fileName -like "*动画*") { $score += 10 }
        if ($fileName -like "*演示*") { $score += 10 }
        if ($fileName -like "*施工*") { $score += 10 }
        
        if ($score -gt 0) {
            $results += [PSCustomObject]@{
                Score = $score
                Name = $fileName
                Path = $filePath
                Size = "{0:N2} MB" -f ($file.Length / 1MB)
            }
        }
    }
    
    $results = $results | Sort-Object -Property Score -Descending | Select-Object -First $MaxResults
    
    if ($results.Count -gt 0) {
        Write-Host "Found $($results.Count) results:" -ForegroundColor Green
        foreach ($r in $results) {
            Write-Host "[Score: $($r.Score)] $($r.Name)" -ForegroundColor White
            Write-Host "   Path: $($r.Path)" -ForegroundColor Gray
            Write-Host "   Size: $($r.Size)" -ForegroundColor Gray
            Write-Host ""
        }
    } else {
        Write-Host "No matching files found" -ForegroundColor Red
    }
} catch {
    Write-Host "Error: $_" -ForegroundColor Red
}
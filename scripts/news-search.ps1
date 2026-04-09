# news-search.ps1
# Engineering safety news search using Baidu

param(
    [int]$Count = 5
)

$ErrorActionPreference = "SilentlyContinue"

# Search keywords
$keywords = @(
    "桥梁事故",
    "施工坍塌",
    "工程事故"
)

$headers = @{
    "User-Agent" = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

$allResults = @()

foreach ($keyword in $keywords) {
    $encodedKeyword = [System.Web.HttpUtility]::UrlEncode($keyword)
    $url = "https://www.baidu.com/s?wd=$encodedKeyword&rn=10&ie=utf-8"
    
    try {
        $response = Invoke-WebRequest -Uri $url -Headers $headers -Proxy "http://127.0.0.1:7890" -TimeoutSec 15 -UseBasicParsing
        $html = $response.Content
        
        # Pattern: <h3 class="c-title t"><a ... aria-label="Title">...</a></h3>
        # Extract aria-label from <a> tags inside <h3 class="c-title t">
        $pattern = '<h3 class="c-title t"><a[^>]*href="([^"]*)"[^>]*aria-label="([^"]*)"[^>]*>'
        $matches = [regex]::Matches($html, $pattern)
        
        foreach ($match in $matches | Select-Object -First $Count) {
            $link = $match.Groups[1].Value
            $title = $match.Groups[2].Value
            
            if ($title -and $link -and $title.Length -gt 3) {
                $allResults += [PSCustomObject]@{
                    Title = $title.Trim()
                    Link = $link
                    Keyword = $keyword
                }
            }
        }
    }
    catch {
        Write-Host "[WARN] Search failed for: $keyword - $($_.Exception.Message)"
    }
    
    Start-Sleep -Milliseconds 1000
}

# Deduplicate by title
$uniqueResults = $allResults | Sort-Object { $_.Title } -Unique | Select-Object -First $Count

# Output (use UTF-8 for console)
$OutputEncoding = [System.Text.Encoding]::UTF8
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

Write-Host "=== Engineering Safety News ===" -ForegroundColor Cyan
Write-Host "Time: $(Get-Date -Format 'yyyy-MM-dd HH:mm')"
Write-Host ""

if ($uniqueResults.Count -eq 0) {
    Write-Host "No news found"
    exit 0
}

$index = 1
foreach ($result in $uniqueResults) {
    $shortTitle = if ($result.Title.Length -gt 60) { $result.Title.Substring(0, 57) + "..." } else { $result.Title }
    Write-Host "$index. $shortTitle" -ForegroundColor Green
    Write-Host "   $($result.Link)" -ForegroundColor Gray
    $index++
}

Write-Host ""
Write-Host "Found $($uniqueResults.Count) news items" -ForegroundColor Cyan

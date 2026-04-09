# debug-baidu2.ps1
$url = 'https://www.baidu.com/s?wd=%E5%89%91%E6%A1%A5%E4%BA%8B%E6%95%85&rn=10&ie=utf-8'
$headers = @{
    "User-Agent" = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

$response = Invoke-WebRequest -Uri $url -Headers $headers -Proxy 'http://127.0.0.1:7890' -TimeoutSec 15 -UseBasicParsing
$html = $response.Content

# Try different patterns
$patterns = @(
    '<h3[^>]*class="c-title"[^>]*>.*?<a[^>]*href="([^"]*)"[^>]*>([^<]*)</a>',
    '<h3[^>]*class="[^"]*c-title[^"]*"[^>]*>.*?<a[^>]*href="([^"]*)"[^>]*>([^<]*)</a>',
    '<a[^>]*class="[^"]*c-title[^"]*"[^>]*href="([^"]*)"[^>]*>([^<]*)</a>'
)

foreach ($pattern in $patterns) {
    Write-Host "Testing pattern: $($pattern.Substring(0, 50))..."
    $matches = [regex]::Matches($html, $pattern)
    Write-Host "Matches found: $($matches.Count)"
    if ($matches.Count -gt 0) {
        Write-Host "First match: $($matches[0].Value.Substring(0, [Math]::Min(200, $matches[0].Value.Length)))"
        break
    }
}

# Find a portion with "href" near "c-title"
$idx = $html.IndexOf('c-title')
if ($idx -gt 0) {
    Write-Host ""
    Write-Host "Found c-title at position $idx"
    Write-Host "Context: $($html.Substring($idx, [Math]::Min(500, $html.Length - $idx)))"
}

# debug-rss.ps1
$url = 'https://www.bing.com/search?format=rss&q=%E5%89%91%E6%A1%A5%E4%BA%8B%E6%95%85'
$headers = @{ 'User-Agent' = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36' }

Write-Host "Fetching RSS from: $url"
$response = Invoke-WebRequest -Uri $url -Headers $headers -Proxy 'http://127.0.0.1:7890' -TimeoutSec 15 -UseBasicParsing
Write-Host "Status: $($response.StatusCode)"
Write-Host "Content-Type: $($response.Headers['Content-Type'])"
Write-Host "Length: $($response.Content.Length)"
Write-Host "---First 2000 chars---"
Write-Host $response.Content.Substring(0, [Math]::Min(2000, $response.Content.Length))

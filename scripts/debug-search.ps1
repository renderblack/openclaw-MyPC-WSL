# debug-search.ps1
$url = 'https://www.bing.com/search?q=%E5%89%91%E6%A1%A5%E4%BA%8B%E6%95%85+2026'
$headers = @{ 'User-Agent' = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36' }
$response = Invoke-WebRequest -Uri $url -Headers $headers -Proxy 'http://127.0.0.1:7890' -TimeoutSec 15 -UseBasicParsing
$html = $response.Content
Write-Host "Status: $($response.StatusCode)"
Write-Host "Length: $($html.Length)"
Write-Host "---First 2000 chars---"
Write-Host $html.Substring(0, [Math]::Min(2000, $html.Length))

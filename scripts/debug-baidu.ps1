# debug-baidu.ps1
$url = 'https://www.baidu.com/s?wd=%E5%89%91%E6%A1%A5%E4%BA%8B%E6%95%85&rn=10&ie=utf-8'
$headers = @{
    "User-Agent" = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

Write-Host "Fetching: $url"
$response = Invoke-WebRequest -Uri $url -Headers $headers -Proxy 'http://127.0.0.1:7890' -TimeoutSec 15 -UseBasicParsing
$html = $response.Content

Write-Host "Status: $($response.StatusCode)"
Write-Host "Length: $($html.Length)"

# Check if we got actual search results
if ($html -match "没有找到") {
    Write-Host "No results found message in page"
}

if ($html -match "c-title") {
    Write-Host "Found c-title class in page"
} else {
    Write-Host "No c-title class found"
}

# Show first 3000 chars
Write-Host "---First 3000 chars---"
Write-Host $html.Substring(0, [Math]::Min(3000, $html.Length))

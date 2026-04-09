# debug-baidu3.ps1
$url = 'https://www.baidu.com/s?wd=%E5%89%91%E6%A1%A5%E4%BA%8B%E6%95%85&rn=10&ie=utf-8'
$headers = @{
    "User-Agent" = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

$response = Invoke-WebRequest -Uri $url -Headers $headers -Proxy 'http://127.0.0.1:7890' -TimeoutSec 15 -UseBasicParsing
$html = $response.Content

# Find the position of c-title
$idx = $html.IndexOf('c-title t')
if ($idx -gt 0) {
    Write-Host "Found 'c-title t' at position $idx"
    # Show 1000 chars around it
    $start = [Math]::Max(0, $idx - 100)
    $len = 1500
    $context = $html.Substring($start, [Math]::Min($len, $html.Length - $start))
    Write-Host "Context:"
    Write-Host $context
}

# debug-rss3.ps1
$keywords = @(
    "bridge accident",
    "construction collapse",
    "engineering safety"
)

foreach ($kw in $keywords) {
    $url = "https://www.bing.com/search?format=rss&q=$kw"
    $headers = @{ 'User-Agent' = 'Mozilla/5.0' }
    
    Write-Host "=== Searching: $kw ==="
    $response = Invoke-WebRequest -Uri $url -Headers $headers -Proxy 'http://127.0.0.1:7890' -TimeoutSec 15 -UseBasicParsing
    [xml]$xml = $response.Content
    
    if ($xml.rss.channel.item) {
        foreach ($item in $xml.rss.channel.item | Select-Object -First 2) {
            Write-Host "Title: $($item.title)"
            Write-Host "Link: $($item.link)"
            Write-Host ""
        }
    }
    Write-Host ""
}

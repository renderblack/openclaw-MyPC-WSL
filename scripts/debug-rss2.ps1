# debug-rss2.ps1
Add-Type -AssemblyName System.Xml

$url = 'https://www.bing.com/search?format=rss&q=%E5%89%91%E6%A1%A5%E4%BA%8B%E6%95%85'
$headers = @{ 'User-Agent' = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36' }

Write-Host "Fetching RSS..."
$response = Invoke-WebRequest -Uri $url -Headers $headers -Proxy 'http://127.0.0.1:7890' -TimeoutSec 15 -UseBasicParsing
$content = $response.Content

Write-Host "Content Length: $($content.Length)"

# Try to parse as XML
try {
    [xml]$xml = $content
    Write-Host "XML parsed successfully"
    
    if ($xml.rss.channel.item) {
        Write-Host "Items found: $($xml.rss.channel.item.Count)"
        foreach ($item in $xml.rss.channel.item | Select-Object -First 3) {
            Write-Host "Title: $($item.title)"
            Write-Host "Link: $($item.link)"
            Write-Host "PubDate: $($item.pubDate)"
            Write-Host "---"
        }
    }
}
catch {
    Write-Host "XML Parse Error: $($_.Exception.Message)"
    Write-Host "First 500 chars: $($content.Substring(0, [Math]::Min(500, $content.Length)))"
}

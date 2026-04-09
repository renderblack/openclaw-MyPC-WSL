$r = Invoke-WebRequest -Uri 'https://www.thepaper.cn/rss' -Proxy 'http://127.0.0.1:7890' -TimeoutSec 10 -UseBasicParsing
$html = $r.Content
Write-Host "Length: $($html.Length)"
Write-Host $html.Substring(0, [Math]::Min(2000, $html.Length))

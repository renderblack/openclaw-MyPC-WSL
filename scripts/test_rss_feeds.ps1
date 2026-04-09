$feeds = @(
    'https://www.chinasafety.gov.cn/rss.xml',
    'https://www.mem.gov.cn/rss/index.xml',
    'https://www.thepaper.cn/rss',
    'https://news.163.com/rss',
    'https://www.sina.com.cn/rss.xml'
)

foreach ($feed in $feeds) {
    try {
        $r = Invoke-WebRequest -Uri $feed -Proxy 'http://127.0.0.1:7890' -TimeoutSec 5 -UseBasicParsing
        if ($r.StatusCode -eq 200) {
            Write-Host "OK: $feed"
        } else {
            Write-Host "FAIL ($($r.StatusCode)): $feed"
        }
    } catch {
        Write-Host "ERROR: $feed - $_"
    }
}

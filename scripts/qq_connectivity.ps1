# qq_connectivity.ps1
Write-Host "=== Testing QQ API Connectivity ==="

$urls = @(
    "https://api.q.qq.com/",
    "https://bot.q.qq.com/",
    "https://graph.qq.com/"
)

foreach ($url in $urls) {
    Write-Host "`nTesting: $url"
    try {
        $resp = Invoke-WebRequest -Uri $url -Method GET -TimeoutSec 10 -UseBasicParsing
        Write-Host "  Status: $($resp.StatusCode)"
        Write-Host "  Content length: $($resp.Content.Length)"
    } catch {
        $msg = $_.Exception.Message
        if ($msg.Length -gt 100) {
            $msg = $msg.Substring(0, 100)
        }
        Write-Host "  Error: $msg"
    }
}

Write-Host "`n=== Done ==="

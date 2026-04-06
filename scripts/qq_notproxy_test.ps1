# qq_notproxy_test.ps1
$appId = "1903763830"
$secret = "siPzOhrpcEi2INLJ"

Write-Host "Testing QQ API WITHOUT proxy..."

$urls = @(
    "https://api.q.qq.com/api/oauth2/access_token",
    "https://api.q.qq.com/api/token",
    "https://api.q.qq.com/"
)

foreach ($url in $urls) {
    Write-Host "Trying: $url"
    try {
        $resp = Invoke-WebRequest -Uri $url -Method GET -TimeoutSec 8
        Write-Host "  OK: $($resp.StatusCode)"
    } catch {
        Write-Host "  Error: $($_.Exception.Message.Substring(0, 80))"
    }
}

Write-Host "Done."

# qq_api_test2.ps1
$appId = "1903763830"
$secret = "siPzOhrpcEi2INLJ"
$proxy = "http://127.0.0.1:7890"

Write-Host "=== QQ Bot API Test v2 ==="

# QQ Bot API uses access_token from a different endpoint
# Let's try the QQ Open Platform API

# Test: Try to get access token with different params
$urls = @(
    @{url="https://api.q.qq.com/api/oauth2/access_token"; params=@{grant_type="client_credential";appid=$appId;secret=$secret}},
    @{url="https://api.q.qq.com/api/token"; params=@{grant_type="client_credential";appid=$appId;secret=$secret}},
    @{url="https://api.q.qq.com/api/getAccessToken"; params=@{appid=$appId;secret=$secret}},
    @{url="https://api.q.qq.com/openapi/token"; params=@{grant_type="client_credential";appid=$appId;secret=$secret}}
)

foreach ($test in $urls) {
    Write-Host "`nTrying: $($test.url)"
    try {
        $resp = Invoke-WebRequest -Uri $test.url -Method POST -Body $test.params -ContentType "application/x-www-form-urlencoded" -Proxy $proxy -TimeoutSec 8
        Write-Host "  OK: $($resp.StatusCode) - $($resp.Content.Substring(0, [Math]::Min(100, $resp.Content.Length)))"
    } catch {
        Write-Host "  Error: $($_.Exception.Message.Substring(0, [Math]::Min(80, $_.Exception.Message.Length)))"
    }
}

Write-Host "`n=== Done ==="

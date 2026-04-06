# qq_token_test.ps1
$body = @{
    grant_type = "client_credential"
    appid = "1903763830"
    secret = "siPzOhrpcEi2INLJ"
}

Write-Host "Testing QQ API endpoints..."

# Try different endpoints
$endpoints = @(
    "https://api.q.qq.com/oauth2/access_token",
    "https://api.q.qq.com/api/oauth2/access_token",
    "https://graph.qq.com/oauth2/access_token"
)

foreach ($url in $endpoints) {
    Write-Host "Trying: $url"
    try {
        $resp = Invoke-WebRequest -Uri $url -Method Post -Body $body -ContentType "application/x-www-form-urlencoded" -Proxy "http://127.0.0.1:7890" -TimeoutSec 10
        Write-Host "  Success: $($resp.StatusCode)"
        Write-Host "  Content: $($resp.Content)"
    } catch {
        $status = $_.Exception.Response.StatusCode
        Write-Host "  Error: $status"
    }
}

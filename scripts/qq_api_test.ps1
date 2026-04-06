# qq_api_test.ps1
# Test QQ Bot API authentication and message sending

$appId = "1903763830"
$secret = "siPzOhrpcEi2INLJ"
$proxy = "http://127.0.0.1:7890"

Write-Host "=== QQ Bot API Test ==="

# Test 1: Get Access Token
Write-Host "`n[Test 1] Getting access token..."
$tokenUrl = "https://api.q.qq.com/api/oauth2/access_token"

try {
    $resp = Invoke-WebRequest -Uri $tokenUrl -Method POST -Body @{
        grant_type = "client_credential"
        appid = $appId
        secret = $secret
    } -ContentType "application/x-www-form-urlencoded" -Proxy $proxy -TimeoutSec 10

    Write-Host "Status: $($resp.StatusCode)"
    Write-Host "Response: $($resp.Content)"
} catch {
    Write-Host "Error: $($_.Exception.Message)"
}

# Test 2: Try with JSON content type
Write-Host "`n[Test 2] Try with JSON..."
try {
    $resp = Invoke-WebRequest -Uri $tokenUrl -Method POST -Body (@{
        grant_type = "client_credential"
        appid = $appId
        secret = $secret
    } | ConvertTo-Json) -ContentType "application/json" -Proxy $proxy -TimeoutSec 10

    Write-Host "Status: $($resp.StatusCode)"
    Write-Host "Response: $($resp.Content)"
} catch {
    Write-Host "Error: $($_.Exception.Message)"
}

# Test 3: Try graph.qq.com
Write-Host "`n[Test 3] Try graph.qq.com..."
$graphUrl = "https://graph.qq.com/oauth2.0/token"
try {
    $resp = Invoke-WebRequest -Uri $graphUrl -Method POST -Body @{
        grant_type = "client_credential"
        client_id = $appId
        client_secret = $secret
    } -ContentType "application/x-www-form-urlencoded" -Proxy $proxy -TimeoutSec 10

    Write-Host "Status: $($resp.StatusCode)"
    Write-Host "Response: $($resp.Content)"
} catch {
    Write-Host "Error: $($_.Exception.Message)"
}

Write-Host "`n=== Test Complete ==="

# qq_push.ps1 - QQ Push Test
param(
    [string]$AppId = "1903763830",
    [string]$ClientSecret = "siPzOhrpcEi2INLJ",
    [string]$Proxy = "http://127.0.0.1:7890"
)

$ErrorActionPreference = "SilentlyContinue"

# === 1. Get Access Token ===
$tokenUrl = "https://api.q.qq.com/api/oauth2/access_token"
$tokenBody = @{
    grant_type = "client_credential"
    appid = $AppId
    secret = $ClientSecret
} | ConvertTo-Json

Write-Host "Getting access token..."
try {
    $tokenResponse = Invoke-RestMethod -Uri $tokenUrl -Method Post -Body $tokenBody -ContentType "application/json" -Proxy $Proxy -TimeoutSec 10
    $accessToken = $tokenResponse.access_token
    Write-Host "Access token: $accessToken"
} catch {
    Write-Host "Failed to get access token: $_"
    exit 1
}

# === 2. Build Message ===
$timestamp = Get-Date -Format "HH:mm"

# Gateway status
$gatewayStatus = "OFF"
try {
    $probe = Invoke-WebRequest -Uri "http://127.0.0.1:18789" -TimeoutSec 3 -UseBasicParsing
    if ($probe.StatusCode -eq 200) { $gatewayStatus = "ON" }
} catch { $gatewayStatus = "OFF" }

# Disk usage
$diskUsage = "N/A"
try {
    $disk = Get-PSDrive -Name C
    $diskUsage = "{0}%" -f [math]::Round($disk.Used / ($disk.Used + $disk.Free) * 100, 1)
} catch { }

# Memory
$memAvailable = "N/A"
try {
    $os = Get-CimInstance Win32_OperatingSystem
    $memAvailableGB = [math]::Round($os.FreePhysicalMemory / 1MB, 1)
    $memAvailable = "${memAvailableGB} GB"
} catch { }

$msg = "Proactive check $timestamp - Gateway $gatewayStatus | Disk $diskUsage | Mem $memAvailable"

# === 3. Send to QQ ===
# Note: Need to specify recipient (group ID or user ID)
$sendUrl = "https://api.q.qq.com/api/message/send"
$sendBody = @{
    access_token = $accessToken
    msg = $msg
    toUser = "BED5E915B0092D47986A2CA16BAE2119"
} | ConvertTo-Json

Write-Host "Sending message..."
try {
    $response = Invoke-RestMethod -Uri $sendUrl -Method Post -Body $sendBody -ContentType "application/json" -Proxy $Proxy -TimeoutSec 10
    Write-Host "Response: $($response | ConvertTo-Json)"
} catch {
    Write-Host "Failed to send: $_"
}

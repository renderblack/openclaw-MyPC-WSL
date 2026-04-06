# proactive_check.ps1 - 皮皮虾主动检查 (Windows Native)
param(
    [string]$TelegramToken = "8717931087:AAERcQmiIpkMB0VcpHVMfjKEyhPa7fYq0_M",
    [string]$ChatId = "1022202630",
    [string]$Proxy = "http://127.0.0.1:7890"
)

$ErrorActionPreference = "SilentlyContinue"

# === 1. Gateway Status ===
$gatewayStatus = "[OFF]"
try {
    $probe = Invoke-WebRequest -Uri "http://127.0.0.1:18789" -TimeoutSec 3 -UseBasicParsing
    if ($probe.StatusCode -eq 200) { $gatewayStatus = "[ON]" }
} catch { $gatewayStatus = "[ERR]" }

# === 2. Disk Usage ===
$diskUsage = "N/A"
try {
    $disk = Get-PSDrive -Name C
    $diskUsage = "{0}%" -f [math]::Round($disk.Used / ($disk.Used + $disk.Free) * 100, 1)
} catch { }

# === 3. Memory ===
$memAvailable = "N/A"
try {
    $os = Get-CimInstance Win32_OperatingSystem
    $memAvailableGB = [math]::Round($os.FreePhysicalMemory / 1MB, 1)
    $memAvailable = "${memAvailableGB} GB"
} catch { }

# === 4. Skills Status ===
$morningSkill = "N/A"
$redditSkill = "N/A"
$proactiveSkill = "N/A"

try {
    $skillsOutput = & openclaw skills list 2>$null | Out-String
    if ($skillsOutput -match "morning-email-rollup" -and $skillsOutput -match "ready") { $morningSkill = "OK" } else { $morningSkill = "N/A" }
    if ($skillsOutput -match "reddit" -and $skillsOutput -match "ready") { $redditSkill = "OK" } else { $redditSkill = "N/A" }
    if ($skillsOutput -match "proactive-agent" -and $skillsOutput -match "ready") { $proactiveSkill = "OK" } else { $proactiveSkill = "N/A" }
} catch { }

# === 5. Build Message ===
$timestamp = Get-Date -Format "HH:mm"

$msg = "Proactive check $timestamp`n" +
       "System: Gateway $gatewayStatus | Disk $diskUsage | Mem $memAvailable`n" +
       "Skills: morning=$morningSkill reddit=$redditSkill proactive=$proactiveSkill"

# === 6. Send to Telegram ===
$url = "https://api.telegram.org/bot${TelegramToken}/sendMessage"

$jsonBody = @{
    chat_id = $ChatId
    text = $msg
} | ConvertTo-Json

try {
    $response = Invoke-RestMethod -Uri $url -Method Post -Body $jsonBody -ContentType "application/json" -Proxy $Proxy -TimeoutSec 10
    if ($response.ok) {
        Write-Host "[$timestamp] Sent OK - Gateway $gatewayStatus Disk $diskUsage Mem $memAvailable"
    } else {
        Write-Host "[$timestamp] Failed: $($response.description)"
    }
} catch {
    Write-Host "[$timestamp] Error: $_"
}

# proactive_check.ps1 - Combined Status Check for Telegram
param(
    [string]$TelegramToken = "8717931087:AAERcQmiIpkMB0VcpHVMfjKEyhPa7fYq0_M",
    [string]$ChatId = "1022202630",
    [string]$Proxy = "http://127.0.0.1:7890"
)

$ErrorActionPreference = "SilentlyContinue"
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

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
    $pct = [math]::Round($disk.Used / ($disk.Used + $disk.Free) * 100, 1)
    $freeGB = [math]::Round($disk.Free / 1GB, 1)
    $diskUsage = "${pct}% (${freeGB}GB free)"
} catch { }

# === 3. Memory ===
$memAvailable = "N/A"
try {
    $os = Get-CimInstance Win32_OperatingSystem
    $totalGB = [math]::Round($os.TotalVisibleMemorySize / 1MB, 1)
    $freeGB = [math]::Round($os.FreePhysicalMemory / 1MB, 1)
    $memAvailable = "${freeGB}GB free / ${totalGB}GB"
} catch { }

# === 4. Weather ===
$weather = "N/A"
try {
    $weatherReq = Invoke-WebRequest -Uri "https://wttr.in/Shanghai?format=3" -Headers @{"User-Agent"="Mozilla/5.0"} -Proxy $Proxy -TimeoutSec 10 -UseBasicParsing
    $weatherBytes = $weatherReq.Content
    $weather = [System.Text.Encoding]::UTF8.GetString($weatherBytes).Trim()
} catch { }

# === 5. News - Use Python script ===
$newsOutput = "N/A"
try {
    $pyScript = "C:\Users\Administrator\.openclaw\workspace\scripts\news_search.py"
    if (Test-Path $pyScript) {
        $newsResult = python $pyScript 2>$null
        # Extract just the titles from Python output
        $lines = $newsResult -split "`n" | Where-Object { $_ -match "^\d+\." }
        if ($lines.Count -gt 0) {
            $newsOutput = ($lines | Select-Object -First 3) -join "`n"
        } else {
            $newsOutput = "No news found"
        }
    }
} catch {
    $newsOutput = "News script error"
}

# === 6. Running Processes ===
$processCount = (Get-Process).Count

# === Build Message ===
$timestamp = Get-Date -Format "yyyy-MM-dd HH:mm"

$msg = "Pipixia Status`n"
$msg += "================`n`n"
$msg += "[1/4] System`n"
$msg += "  Gateway: $gatewayStatus`n"
$msg += "  Disk: $diskUsage`n"
$msg += "  Memory: $memAvailable`n"
$msg += "  Processes: $processCount`n`n"
$msg += "[2/4] Weather (Shanghai)`n"
$msg += "  $weather`n`n"
$msg += "[3/4] Industry News`n"
$msg += "$newsOutput`n`n"
$msg += "================`n"
$msg += "Time: $timestamp"

# === Send to Telegram ===
$url = "https://api.telegram.org/bot${TelegramToken}/sendMessage"

$body = @{
    chat_id = $ChatId
    text = $msg
} | ConvertTo-Json -Compress

try {
    $response = Invoke-RestMethod -Uri $url -Method Post -Body ([System.Text.Encoding]::UTF8.GetBytes($body)) -ContentType "application/json; charset=utf-8" -Proxy $Proxy -TimeoutSec 15
    if ($response.ok) {
        Write-Host "[$timestamp] Sent OK"
    } else {
        Write-Host "[$timestamp] Failed: $($response.description)"
    }
} catch {
    Write-Host "[$timestamp] Error: $_"
}

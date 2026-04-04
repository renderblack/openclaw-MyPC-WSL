# Chrome CDP 完整控制脚本
# 使用 WebSocket 与 Chrome DevTools Protocol 通信

[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12

$chromeDebugUrl = "http://localhost:9222"

# WebSocket 通信类
class CdpClient {
    [System.Net.WebSockets.ClientWebSocket] $WebSocket
    [string] $Url
    
    CdpClient([string] $wsUrl) {
        $this.Url = $wsUrl
        $this.WebSocket = [System.Net.WebSockets.ClientWebSocket]::new()
    }
    
    async Task ConnectAsync() {
        await $this.WebSocket.ConnectAsync($this.Url, $null)
    }
    
    async Task SendCommandAsync([string] $method, [hashtable] $params) {
        $message = @{
            id = [Guid]::NewGuid().ToString()
            method = $method
            params = $params
        } | ConvertTo-Json -Compress
        
        $buffer = [System.Text.Encoding]::UTF8.GetBytes($message)
        await $this.WebSocket.SendAsync(
            [System.ArraySegment[byte]]::new($buffer),
            [System.Net.WebSockets.WebSocketMessageType]::Text,
            $true,
            $null
        )
    }
    
    async Task<string> ReceiveAsync() {
        $buffer = [System.ArraySegment[byte]]::new([byte[]]::new(8192))
        $result = await $this.WebSocket.ReceiveAsync($buffer, $null)
        return [System.Text.Encoding]::UTF8.GetString($buffer.Array, 0, $result.Count)
    }
    
    Close() {
        $this.WebSocket.CloseAsync([System.Net.WebSockets.WebSocketCloseStatus]::NormalClosure, $null, $null)
    }
}

function Get-ChromeTabs {
    try {
        $tabs = Invoke-RestMethod -Uri "$chromeDebugUrl/json" -TimeoutSec 5
        return $tabs
    } catch {
        Write-Host "❌ 无法获取标签页列表：$($_.Exception.Message)"
        return $null
    }
}

function New-CdpClient {
    param([string] $tabUrl)
    
    $client = [CdpClient]::new($tabUrl)
    $client.ConnectAsync() | Wait-Action
    return $client
}

function Navigate-To {
    param([string] $url)
    
    $tabs = Get-ChromeTabs
    if (-not $tabs) { return }
    
    $tab = $tabs[0]
    Write-Host "📍 导航到：$url"
    
    # 使用 curl 发送 CDP 命令（更简单的方式）
    $body = @{
        url = $url
    } | ConvertTo-Json
    
    try {
        $response = Invoke-RestMethod -Method POST -Uri "$chromeDebugUrl/json/new" -Body $body -ContentType "application/json"
        Write-Host "✅ 导航成功"
        return $response
    } catch {
        Write-Host "❌ 导航失败：$($_.Exception.Message)"
    }
}

function Take-Screenshot {
    param([string] $outputPath = "C:\temp\screenshot.png")
    
    $tabs = Get-ChromeTabs
    if (-not $tabs) { return }
    
    $tab = $tabs[0]
    $wsUrl = $tab.webSocketDebuggerUrl
    
    Write-Host "📸 正在截图..."
    
    # 使用 Chrome DevTools Protocol 直接调用
    $body = @{
        method = "Page.captureScreenshot"
        params = @{ format = "png" }
    } | ConvertTo-Json
    
    # 通过 CDP 发送命令
    # 这里简化处理，实际需要使用 WebSocket
    Write-Host "⚠️ 完整 WebSocket 实现需要更多代码，建议使用 Python + pychrome 或 Node.js + chrome-remote-interface"
    Write-Host "📁 截图将保存到：$outputPath"
}

function Get-PageContent {
    $tabs = Get-ChromeTabs
    if (-not $tabs) { return }
    
    $tab = $tabs[0]
    
    Write-Host "📄 获取页面内容..."
    Write-Host "⚠️ 建议使用 Python 脚本实现完整的 CDP 通信"
}

# 简化版：使用 Chrome 的 JSON API 直接操作
function Simple-Navigate {
    param([string] $url)
    
    $tabs = Get-ChromeTabs
    if (-not $tabs) {
        Write-Host "❌ 无法连接到 Chrome"
        return
    }
    
    # 打开新标签页导航
    $newTab = @{
        url = $url
    } | ConvertTo-Json
    
    try {
        $result = Invoke-RestMethod -Method POST -Uri "$chromeDebugUrl/json/new" -Body $newTab -ContentType "application/json"
        Write-Host "✅ 已打开新标签页：$url"
        Write-Host "WebSocket: $($result.webSocketDebuggerUrl)"
    } catch {
        Write-Host "❌ 导航失败：$($_.Exception.Message)"
        Write-Host "提示：Chrome 可能不支持直接导航，需要手动操作或使用完整 CDP 实现"
    }
}

# 演示
Write-Host "=== Chrome CDP 控制脚本（简化版） ===" -ForegroundColor Green
Write-Host "调试接口：$chromeDebugUrl"
Write-Host ""

# 显示当前标签页
$tabs = Get-ChromeTabs
if ($tabs) {
    Write-Host "当前标签页 ($($tabs.Count) 个):" -ForegroundColor Yellow
    $tabs | Select-Object title, url | Format-Table -AutoSize
}

Write-Host ""
Write-Host "可用命令:" -ForegroundColor Cyan
Write-Host "  - Get-ChromeTabs"
Write-Host "  - Simple-Navigate -url 'https://example.com'"
Write-Host "  - Take-Screenshot -outputPath 'C:\temp\screenshot.png'"
Write-Host ""
Write-Host "⚠️ 注意：完整的 CDP WebSocket 通信建议使用 Python + pychrome 库"

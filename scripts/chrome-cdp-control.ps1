# Chrome CDP 控制脚本
# 使用 Chrome DevTools Protocol 直接控制浏览器

$chromeDebugUrl = "http://localhost:9222"

function Get-ChromeTabs {
    try {
        $tabs = Invoke-RestMethod -Uri "$chromeDebugUrl/json" -TimeoutSec 5
        return $tabs
    } catch {
        Write-Host "❌ 无法获取标签页列表"
        return $null
    }
}

function Navigate-To {
    param(
        [string]$url
    )
    
    $tabs = Get-ChromeTabs
    if (-not $tabs) { return }
    
    # 使用第一个标签页
    $tab = $tabs[0]
    $wsUrl = $tab.webSocketDebuggerUrl
    
    # 构建 CDP 命令
    $command = @{
        id = 1
        method = "Page.navigate"
        params = @{ url = $url }
    } | ConvertTo-Json -Compress
    
    # 注意：实际 WebSocket 通信需要使用 WebSocket 库
    # 这里演示 CDP 命令结构
    Write-Host "📍 导航到：$url"
    Write-Host "WebSocket: $wsUrl"
    Write-Host "CDP 命令: $($command)"
}

function Take-Screenshot {
    param(
        [string]$outputPath = "C:\temp\screenshot.png"
    )
    
    $tabs = Get-ChromeTabs
    if (-not $tabs) { return }
    
    $tab = $tabs[0]
    $wsUrl = $tab.webSocketDebuggerUrl
    
    $command = @{
        id = 2
        method = "Page.captureScreenshot"
        params = @{ format = "png" }
    } | ConvertTo-Json -Compress
    
    Write-Host "📸 截图保存到：$outputPath"
    Write-Host "CDP 命令: $($command)"
}

function Get-PageContent {
    $tabs = Get-ChromeTabs
    if (-not $tabs) { return }
    
    $tab = $tabs[0]
    $wsUrl = $tab.webSocketDebuggerUrl
    
    $command = @{
        id = 3
        method = "Runtime.evaluate"
        params = @{
            expression = "document.documentElement.outerHTML"
        }
    } | ConvertTo-Json -Compress
    
    Write-Host "📄 获取页面内容"
    Write-Host "CDP 命令: $($command)"
}

# 演示
Write-Host "=== Chrome CDP 控制脚本 ===" -ForegroundColor Green
Write-Host "调试接口：$chromeDebugUrl"
Write-Host ""
Write-Host "可用命令:"
Write-Host "  - Get-ChromeTabs"
Write-Host "  - Navigate-To -url 'https://example.com'"
Write-Host "  - Take-Screenshot -outputPath 'C:\temp\screenshot.png'"
Write-Host "  - Get-PageContent"
Write-Host ""

# 测试：获取标签页
Write-Host "当前标签页:" -ForegroundColor Yellow
Get-ChromeTabs | Select-Object title, url | Format-Table -AutoSize

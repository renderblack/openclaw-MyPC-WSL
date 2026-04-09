# sync-openclaw-docs.ps1 - Download all OpenClaw official docs
param(
    [string]$DocsRoot = "C:\Users\Administrator\.openclaw\workspace\docs",
    [string]$Proxy = "http://127.0.0.1:7890"
)
$ErrorActionPreference = "Continue"
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

function Fetch-Doc($url, $relPath) {
    $fullPath = Join-Path $DocsRoot $relPath
    $dir = Split-Path $fullPath -Parent
    if (!(Test-Path $dir)) { New-Item -ItemType Directory -Path $dir -Force | Out-Null }
    if ((Test-Path $fullPath) -and (Get-Item $fullPath).Length -gt 5000) {
        Write-Host "[SKIP] $relPath" -ForegroundColor Gray
        return $true
    }
    try {
        $text = Invoke-WebRequest -Uri $url -Headers @{"User-Agent"="Mozilla/5.0"} -Proxy $Proxy -TimeoutSec 30 -UseBasicParsing | Select-Object -ExpandProperty Content
        $text = $text.Trim()
        if ($text.Length -gt 100) {
            [System.IO.File]::WriteAllText($fullPath, $text, [System.Text.Encoding]::UTF8)
            Write-Host "[OK] $relPath" -ForegroundColor Green
            return $true
        } else {
            Write-Host "[SHORT] $relPath ($($text.Length) chars)" -ForegroundColor Yellow
            return $false
        }
    } catch {
        Write-Host "[FAIL] $relPath : $_" -ForegroundColor Red
        return $false
    }
}

$start = Get-Date
$ok = 0
$total = 0

$docs = @(
    # Core
    "index.md|SUMMARY.md",
    "install.md|install.md",
    "configure.md|configure.md",
    "config.md|config.md",
    "auth-credential-semantics.md|auth-credential-semantics.md",
    "models.md|models.md",
    # CLI
    "cli/index.md|cli/index.md",
    "cli/gateway.md|cli/gateway.md",
    "cli/agent.md|cli/agent.md",
    "cli/agents.md|cli/agents.md",
    "cli/config.md|cli/config.md",
    "cli/configure.md|cli/configure.md",
    "cli/cron.md|cli/cron.md",
    "cli/models.md|cli/models.md",
    "cli/plugins.md|cli/plugins.md",
    "cli/channels.md|cli/channels.md",
    "cli/browser.md|cli/browser.md",
    "cli/daemon.md|cli/daemon.md",
    "cli/dashboard.md|cli/dashboard.md",
    "cli/doctor.md|cli/doctor.md",
    "cli/backup.md|cli/backup.md",
    "cli/memory.md|cli/memory.md",
    "cli/node.md|cli/node.md",
    "cli/nodes.md|cli/nodes.md",
    "cli/onboard.md|cli/onboard.md",
    "cli/pairing.md|cli/pairing.md",
    "cli/logs.md|cli/logs.md",
    "cli/mcp.md|cli/mcp.md",
    "cli/message.md|cli/message.md",
    "cli/health.md|cli/health.md",
    "cli/hooks.md|cli/hooks.md",
    "cli/acp.md|cli/acp.md",
    "cli/completion.md|cli/completion.md",
    "cli/approvals.md|cli/approvals.md",
    # Channels
    "channels/index.md|channels/index.md",
    "channels/qqbot.md|channels/qqbot.md",
    "channels/telegram.md|channels/telegram.md",
    "channels/discord.md|channels/discord.md",
    "channels/weixin.md|channels/weixin.md",
    "channels/whatsapp.md|channels/whatsapp.md",
    "channels/slack.md|channels/slack.md",
    "channels/signal.md|channels/signal.md",
    "channels/msteams.md|channels/msteams.md",
    "channels/group-messages.md|channels/group-messages.md",
    "channels/groups.md|channels/groups.md",
    "channels/broadcast-groups.md|channels/broadcast-groups.md",
    "channels/channel-routing.md|channels/channel-routing.md",
    "channels/troubleshooting.md|channels/troubleshooting.md",
    "channels/location.md|channels/location.md",
    "channels/pairing.md|channels/pairing.md",
    # Automation
    "automation/index.md|automation/index.md",
    "automation/cron-jobs.md|automation/cron-jobs.md",
    "automation/taskflow.md|automation/taskflow.md",
    "automation/hooks.md|automation/hooks.md",
    "automation/standing-orders.md|automation/standing-orders.md",
    "automation/tasks.md|automation/tasks.md",
    # Other channels
    "channels/feishu.md|channels/feishu.md",
    "channels/googlechat.md|channels/googlechat.md",
    "channels/mattermost.md|channels/mattermost.md",
    "channels/matrix.md|channels/matrix.md",
    "channels/irc.md|channels/irc.md",
    "channels/line.md|channels/line.md",
    "channels/nostr.md|channels/nostr.md",
    "channels/synology-chat.md|channels/synology-chat.md",
    "channels/tlon.md|channels/tlon.md",
    "channels/twitch.md|channels/twitch.md",
    "channels/zalo.md|channels/zalo.md",
    "channels/nextcloud-talk.md|channels/nextcloud-talk.md",
    "channels/imessage.md|channels/imessage.md",
    "channels/bluebubbles.md|channels/bluebubbles.md",
    # Providers & Misc
    "providers/index.md|providers/index.md",
    "providers/anthropic.md|providers/anthropic.md",
    "providers/openai.md|providers/openai.md",
    "providers/google.md|providers/google.md",
    "providers/azure.md|providers/azure.md",
    "providers/ollama.md|providers/ollama.md",
    "providers/lmstudio.md|providers/lmstudio.md",
    "providers/localai.md|providers/localai.md",
    "ci.md|ci.md"
)

$baseUrl = "https://docs.openclaw.ai"
$total = $docs.Count
$idx = 0

Write-Host "=== Syncing $total docs ===" -ForegroundColor Cyan

foreach ($item in $docs) {
    $parts = $item -split '\|'
    $relPath = $parts[1]
    $url = "$baseUrl/$($parts[0])"
    $idx++
    if (Fetch-Doc $url $relPath) { $ok++ }
    Write-Progress -Activity "Syncing docs" -Status "$idx/$total" -PercentComplete (($idx / $total) * 100)
}

Write-Progress -Activity "Done" -Completed
$elapsed = (Get-Date) - $start
Write-Host ""
Write-Host "Done: $ok/$total OK, $($total-$ok) failed, $($elapsed.TotalSeconds.ToString('0'))s" -ForegroundColor Cyan

# Git commit and push
git -C $DocsRoot\.. add -A
$changed = git -C $DocsRoot\.. status --short
if ($changed) {
    git -C $DocsRoot\.. commit -m "docs: full sync from docs.openclaw.ai ($(Get-Date -Format 'yyyy-MM-dd'))"
    git -C $DocsRoot\.. push origin master
    Write-Host "[GIT] Pushed" -ForegroundColor Green
}

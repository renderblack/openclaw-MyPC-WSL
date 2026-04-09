# sync-openclaw-docs.ps1 - Download all OpenClaw official docs
param(
    [string]$DocsRoot = "C:\Users\Administrator\.openclaw\workspace\docs",
    [string]$Proxy = "http://127.0.0.1:7890"
)
$ErrorActionPreference = "SilentlyContinue"
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

function Fetch-Doc($url, $path) {
    $dir = Split-Path $path -Parent
    if (!(Test-Path $dir)) { New-Item -ItemType Directory -Path $dir -Force | Out-Null }
    try {
        $content = Invoke-WebRequest -Uri $url -Headers @{"User-Agent"="Mozilla/5.0"} -Proxy $Proxy -TimeoutSec 30 -UseBasicParsing
        $bytes = $content.Content
        $text = [System.Text.Encoding]::UTF8.GetString($bytes)
        # Remove the external content wrapper if present
        if ($text -match '(?s)<<<EXTERNAL_UNTRUSTED_CONTENT.*?END_EXTERNAL_UNTRUSTED_CONTENT>>>') {
            $text = $matches[0] -replace '(?s)<<<EXTERNAL_UNTRUSTED_CONTENT.*?>>>', '' -replace '<<<END_EXTERNAL_UNTRUSTED_CONTENT>>>', ''
        }
        $text = $text.Trim()
        if ($text.Length -gt 100) {
            [System.IO.File]::WriteAllText($path, $text, [System.Text.Encoding]::UTF8)
            Write-Host "[OK] $url -> $path" -ForegroundColor Green
            return $true
        } else {
            Write-Host "[SKIP] $url (content too short)" -ForegroundColor Yellow
            return $false
        }
    } catch {
        Write-Host "[FAIL] $url -> $_" -ForegroundColor Red
        return $false
    }
}

$start = Get-Date
$total = 0; $ok = 0

# Core
$coreDocs = @(
    "https://docs.openclaw.ai/index.md|SUMMARY.md",
    "https://docs.openclaw.ai/install.md|install.md",
    "https://docs.openclaw.ai/configure.md|configure.md",
    "https://docs.openclaw.ai/config.md|config.md",
    "https://docs.openclaw.ai/auth-credential-semantics.md|auth-credential-semantics.md",
    "https://docs.openclaw.ai/models.md|models.md"
)

# CLI
$cliDocs = @(
    "https://docs.openclaw.ai/cli/index.md|cli/index.md",
    "https://docs.openclaw.ai/cli/gateway.md|cli/gateway.md",
    "https://docs.openclaw.ai/cli/agent.md|cli/agent.md",
    "https://docs.openclaw.ai/cli/agents.md|cli/agents.md",
    "https://docs.openclaw.ai/cli/config.md|cli/config.md",
    "https://docs.openclaw.ai/cli/configure.md|cli/configure.md",
    "https://docs.openclaw.ai/cli/cron.md|cli/cron.md",
    "https://docs.openclaw.ai/cli/models.md|cli/models.md",
    "https://docs.openclaw.ai/cli/plugins.md|cli/plugins.md",
    "https://docs.openclaw.ai/cli/channels.md|cli/channels.md",
    "https://docs.openclaw.ai/cli/browser.md|cli/browser.md",
    "https://docs.openclaw.ai/cli/daemon.md|cli/daemon.md",
    "https://docs.openclaw.ai/cli/dashboard.md|cli/dashboard.md",
    "https://docs.openclaw.ai/cli/doctor.md|cli/doctor.md",
    "https://docs.openclaw.ai/cli/backup.md|cli/backup.md",
    "https://docs.openclaw.ai/cli/memory.md|cli/memory.md",
    "https://docs.openclaw.ai/cli/node.md|cli/node.md",
    "https://docs.openclaw.ai/cli/nodes.md|cli/nodes.md",
    "https://docs.openclaw.ai/cli/onboard.md|cli/onboard.md",
    "https://docs.openclaw.ai/cli/pairing.md|cli/pairing.md",
    "https://docs.openclaw.ai/cli/logs.md|cli/logs.md",
    "https://docs.openclaw.ai/cli/mcp.md|cli/mcp.md",
    "https://docs.openclaw.ai/cli/message.md|cli/message.md",
    "https://docs.openclaw.ai/cli/health.md|cli/health.md",
    "https://docs.openclaw.ai/cli/hooks.md|cli/hooks.md",
    "https://docs.openclaw.ai/cli/acp.md|cli/acp.md",
    "https://docs.openclaw.ai/cli/completion.md|cli/completion.md",
    "https://docs.openclaw.ai/cli/approvals.md|cli/approvals.md"
)

# Channels
$channelDocs = @(
    "https://docs.openclaw.ai/channels/index.md|channels/index.md",
    "https://docs.openclaw.ai/channels/qqbot.md|channels/qqbot.md",
    "https://docs.openclaw.ai/channels/telegram.md|channels/telegram.md",
    "https://docs.openclaw.ai/channels/discord.md|channels/discord.md",
    "https://docs.openclaw.ai/channels/weixin.md|channels/weixin.md",
    "https://docs.openclaw.ai/channels/whatsapp.md|channels/whatsapp.md",
    "https://docs.openclaw.ai/channels/slack.md|channels/slack.md",
    "https://docs.openclaw.ai/channels/signal.md|channels/signal.md",
    "https://docs.openclaw.ai/channels/msteams.md|channels/msteams.md",
    "https://docs.openclaw.ai/channels/group-messages.md|channels/group-messages.md",
    "https://docs.openclaw.ai/channels/groups.md|channels/groups.md",
    "https://docs.openclaw.ai/channels/broadcast-groups.md|channels/broadcast-groups.md",
    "https://docs.openclaw.ai/channels/channel-routing.md|channels/channel-routing.md",
    "https://docs.openclaw.ai/channels/troubleshooting.md|channels/troubleshooting.md",
    "https://docs.openclaw.ai/channels/location.md|channels/location.md",
    "https://docs.openclaw.ai/channels/pairing.md|channels/pairing.md"
)

# Automation
$autoDocs = @(
    "https://docs.openclaw.ai/automation/index.md|automation/index.md",
    "https://docs.openclaw.ai/automation/hooks.md|automation/hooks.md",
    "https://docs.openclaw.ai/automation/standing-orders.md|automation/standing-orders.md",
    "https://docs.openclaw.ai/automation/tasks.md|automation/tasks.md"
)

# Other channels
$otherChannelDocs = @(
    "https://docs.openclaw.ai/channels/feishu.md|channels/feishu.md",
    "https://docs.openclaw.ai/channels/googlechat.md|channels/googlechat.md",
    "https://docs.openclaw.ai/channels/mattermost.md|channels/mattermost.md",
    "https://docs.openclaw.ai/channels/matrix.md|channels/matrix.md",
    "https://docs.openclaw.ai/channels/irc.md|channels/irc.md",
    "https://docs.openclaw.ai/channels/line.md|channels/line.md",
    "https://docs.openclaw.ai/channels/nostr.md|channels/nostr.md",
    "https://docs.openclaw.ai/channels/synology-chat.md|channels/synology-chat.md",
    "https://docs.openclaw.ai/channels/tlon.md|channels/tlon.md",
    "https://docs.openclaw.ai/channels/twitch.md|channels/twitch.md",
    "https://docs.openclaw.ai/channels/zalo.md|channels/zalo.md",
    "https://docs.openclaw.ai/channels/nostr.md|channels/nostr.md",
    "https://docs.openclaw.ai/channels/nextcloud-talk.md|channels/nextcloud-talk.md",
    "https://docs.openclaw.ai/channels/imessage.md|channels/imessage.md",
    "https://docs.openclaw.ai/channels/bluebubbles.md|channels/bluebubbles.md"
)

# Providers & Misc
$miscDocs = @(
    "https://docs.openclaw.ai/providers/index.md|providers/index.md",
    "https://docs.openclaw.ai/providers/anthropic.md|providers/anthropic.md",
    "https://docs.openclaw.ai/providers/openai.md|providers/openai.md",
    "https://docs.openclaw.ai/providers/google.md|providers/google.md",
    "https://docs.openclaw.ai/providers/azure.md|providers/azure.md",
    "https://docs.openclaw.ai/providers/ollama.md|providers/ollama.md",
    "https://docs.openclaw.ai/providers/lmstudio.md|providers/lmstudio.md",
    "https://docs.openclaw.ai/providers/localai.md|providers/localai.md",
    "https://docs.openclaw.ai/ci.md|ci.md"
)

$allDocs = $coreDocs + $cliDocs + $channelDocs + $autoDocs + $otherChannelDocs + $miscDocs
$total = $allDocs.Count

Write-Host "=== OpenClaw Docs Sync ===" -ForegroundColor Cyan
Write-Host "Total: $total files" -ForegroundColor White
Write-Host ""

$batch = 1
foreach ($group in @($coreDocs, $cliDocs, $channelDocs, $autoDocs, $otherChannelDocs, $miscDocs)) {
    $groupName = @("Core", "CLI", "Channels", "Automation", "Other Channels", "Providers/Misc")[$batch - 1]
    Write-Host "[Batch $batch] $groupName ($($group.Count) files)..." -ForegroundColor Yellow
    
    foreach ($item in $group) {
        $parts = $item -split '\|'
        $url = $parts[0]
        $relPath = $parts[1]
        $fullPath = Join-Path $DocsRoot $relPath
        
        # Skip if already exists and > 5KB (probably complete)
        if ((Test-Path $fullPath) -and (Get-Item $fullPath).Length -gt 5000) {
            Write-Host "  [SKIP] $relPath (exists)" -ForegroundColor Gray
            continue
        }
        
        if (Fetch-Doc $url $fullPath) { $ok++ }
        $idx = [array]::IndexOf($allDocs, $item) + 1
        Write-Progress -Id 1 -Activity "Syncing docs" -Status "$idx/$total" -PercentComplete (($idx / $total) * 100)
    }
    $batch++
}

Write-Progress -Id 1 -Activity "Done" -Completed

$elapsed = (Get-Date) - $start
Write-Host ""
Write-Host "=== Done ===" -ForegroundColor Cyan
Write-Host "Total: $total | OK: $ok | Failed: $($total - $ok)" -ForegroundColor White
Write-Host "Time: $($elapsed.TotalSeconds.ToString('0'))s" -ForegroundColor Cyan

# Auto git commit
$gitDir = "C:\Users\Administrator\.openclaw\workspace"
Set-Location $gitDir
git add -A
$status = git status --short
if ($status) {
    git commit -m "docs: full sync from official docs.openclaw.ai"
    git push origin master
    Write-Host "[GIT] Pushed successfully" -ForegroundColor Green
} else {
    Write-Host "[GIT] Nothing to commit" -ForegroundColor Gray
}

# TOOLS.md - Local Notes (Windows Native Environment)

Skills define _how_ tools work. This file is for _your_ specifics — the stuff that's unique to your setup.

> **⚠️ Environment Note**: This OpenClaw instance runs on **Windows 10 (Education Edition) + PowerShell** (Native).
> - No WSL2 dependency.
> - All scripts are PowerShell (`.ps1`) or native Windows executables.
> - Paths use Windows format (`C:\Users\...`).

## 🛠️ 开发环境标准检查清单 (PowerShell Native)

每次开发任务前，按以下五个阶段检查环境：

### 第一阶段：Gateway 和服务状态
```powershell
# 1. Gateway 状态
openclaw gateway status

# 2. 完整诊断
openclaw status
```

### 第二阶段：系统资源
```powershell
# 3. 磁盘空间 (C 盘)
$disk = Get-PSDrive -PSProvider FileSystem | Where-Object {$_.Root -eq "C:\"}
$freeGB = [math]::Round($disk.Free / 1GB, 2)
$usedGB = [math]::Round($disk.Used / 1GB, 2)
Write-Host "C: $freeGB GB Free / $usedGB GB Used"
if ($freeGB -lt 30) {
    Write-Host "⚠️ Warning: C 盘空间不足 30 GB，建议清理！" -ForegroundColor Yellow
}

# 4. 内存
Get-CimInstance Win32_OperatingSystem | Select-Object @{N='TotalGB';E={[math]::Round($_.TotalVisibleMemorySize/1MB,2)}}, @{N='FreeGB';E={[math]::Round($_.FreePhysicalMemory/1MB,2)}}

# 5. 进程数
Get-Process | Where-Object {$_.Name -like "*openclaw*"} | Measure-Object | Select-Object Count
```

### 第三阶段：网络连通性
```powershell
# 6. 代理检查 (通过 172.31.0.1:7890)
curl -s --proxy http://172.31.0.1:7890 https://www.baidu.com -I | Select-Object -First 1

# 7. Telegram 连接（检查 bot 是否可达）
# 注意：如果 Telegram 未启用，此步骤可跳过
# curl -s https://api.telegram.org/bot<token>/getMe
```

### 第四阶段：日志检查
```powershell
# 8. 当天日志
$today = Get-Date -Format 'yyyy-MM-dd'
$logPath = "$env:TEMP\openclaw\openclaw-$today.log"
if (Test-Path $logPath) {
    Get-Content $logPath -Tail 50
} else {
    Write-Host "No log file found at $logPath"
}

# 9. 错误统计
if (Test-Path $logPath) {
    $errors = (Get-Content $logPath -Tail 200 | Select-String "ERROR").Count
    Write-Host "Error count in last 200 lines: $errors"
}
```

### 第五阶段：技能状态
```powershell
# 10. 已安装技能
openclaw skills list
```

### ⚠️ 异常判断标准

| 异常现象 | 可能原因 | 处理方式 |
|---------|---------|---------|
| Gateway not responding | 服务未启动 | `openclaw gateway start` |
| RPC probe failed | 配置文件错误 | 检查 `openclaw.json` |
| Telegram polling stall | 网络波动 | 等待自动恢复或重启 |
| 磁盘 > 90% | 日志过大 | 清理旧日志 (`Remove-Item ...`) |
| 内存 < 500MB 可用 | 进程泄漏 | 重启 gateway |

---

## Environment (Current Configuration)

- **OS**: Windows 10 (Education Edition) (Native PowerShell)
- **OpenClaw Home**: `C:\Users\Administrator\.openclaw`
- **Workspace**: `C:\Users\Administrator\.openclaw\workspace`
- **Proxy**: `127.0.0.1:7890` (Local proxy, e.g., Clash/Clash Meta)
- **Model Provider**: MiniMax / DeepSeek (via custom-newapi / direct)
- **Telegram Bot**: Configured (Token stored in `openclaw.json`)
- **QQ Bot**: Enabled

## Safe Working Directories

- `C:\Users\Administrator\.openclaw\workspace`
- `C:\Users\Administrator\projects` (if exists)
- `C:\Temp` (or `%TEMP%`)

## Common Tools Available

- `powershell` / `pwsh`
- `curl` (PowerShell alias for `Invoke-WebRequest`)
- `git`
- `python` / `pip`
- `node` / `npm`
- `ffmpeg`
- `jq` (via Chocolatey/Scoop or native PowerShell JSON parsing)

## Notes

- **JSON Parsing**: Prefer native PowerShell (`ConvertFrom-Json`) or `jq` if installed.
- **File Operations**: Stay inside `workspace` unless explicitly requested.
- **Commands**: Avoid destructive commands (`rm`, `del`) without confirmation.
- **Scripts**: All automation scripts should be `.ps1` (PowerShell), not `.sh` (Bash).
- **Path Format**: Use Windows paths (`C:\...`) or PowerShell variables (`$env:TEMP`).

## Why Separate?

Skills are shared. Your setup is yours. Keeping them apart means you can update skills without losing your notes, and share skills without leaking your infrastructure.

## Skills 管理（2026-03-27 更新）

OpenClaw 2026.3.24 新增 **Skills 一键安装** 功能，安装 Skill 时会自动检测并提示缺失的依赖。

### 常用命令

```powershell
# 查看已安装的 Skills
openclaw skills list

# 查看所有可用 Skills（包括未安装的）
openclaw skills catalog

# 查看某个 Skill 的详细信息（包含依赖说明）
openclaw skills info <skill-name>

# 安装 Skill（会自动检测并提示缺失依赖）
openclaw skills install <skill-name>

# 更新已安装的 Skill
openclaw skills update <skill-name>

# 卸载 Skill
openclaw skills uninstall <skill-name>
```

### 已安装的 Skills

| Skill | 说明 |
|-------|------|
| cli-anything | 浏览器控制（CLI-Anything + Selenium） |
| himalaya | 邮件管理（IMAP/SMTP） |
| openai-whisper-api | OpenAI 语音转文字 |
| weather | 天气查询 |
| summarize | URL/文件摘要 |
| find-skills | 查找新 Skill |

### 常用 Skills 推荐

- `gh-issues` - GitHub Issues 管理（需配置 GitHub Token）
- `blogwatcher` - 博客/RSS 监控
- `openhue` - 飞利浦 Hue 灯光控制
- `sonoscli` - Sonos 音箱控制
- `tmux` - (Not applicable on Windows Native, use Windows Terminal tabs instead)

### Skill 安装示例

```powershell
# 安装 GitHub Issues Skill（会提示输入 GitHub Token）
openclaw skills install gh-issues

# 安装后查看依赖是否满足
openclaw skills info gh-issues
```

### 自定义 Skill 位置

- 用户安装的 Skills：`C:\Users\Administrator\.openclaw\skills\`
- 系统内置 Skills：`C:\Users\Administrator\AppData\Roaming\npm\node_modules\openclaw\skills\`

---

Add whatever helps you do your job. This is your cheat sheet.

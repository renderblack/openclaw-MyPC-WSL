# TOOLS.md - Local Notes

Skills define _how_ tools work. This file is for _your_ specifics — the stuff that's unique to your setup.

## 🛠️ 开发环境标准检查清单

每次开发任务前，按以下五个阶段检查环境：

### 第一阶段：Gateway 和服务状态
```bash
# 1. Gateway 状态
openclaw gateway status

# 2. 完整诊断
openclaw status
```

### 第二阶段：系统资源
```bash
# 3. 磁盘空间
df -h /

# 4. 内存
free -h

# 5. 进程数
ps aux | grep -c openclaw
```

### 第三阶段：网络连通性
```bash
# 6. 代理检查
curl -s --proxy http://172.31.0.1:7890 https://www.baidu.com -I

# 7. Telegram 连接（检查 bot 是否可达）
curl -s https://api.telegram.org/bot<token>/getMe
```

### 第四阶段：日志检查
```bash
# 8. 当天日志（Windows PowerShell）
Get-Content "$env:TEMP\openclaw\openclaw-$(Get-Date -Format 'yyyy-MM-dd').log" -Tail 50

# 9. 错误统计
(Get-Content "$env:TEMP\openclaw\openclaw-$(Get-Date -Format 'yyyy-MM-dd').log" -Tail 200 | Select-String "ERROR").Count
```

### 第五阶段：技能状态
```bash
# 10. 已安装技能
openclaw skills list
```

### ⚠️ 异常判断标准
| 异常现象 | 可能原因 | 处理方式 |
|---------|---------|---------|
| Gateway not responding | 服务未启动 | `openclaw gateway start` |
| RPC probe failed | 配置文件错误 | 检查 openclaw.json |
| Telegram polling stall | 网络波动 | 等待自动恢复或重启 |
| 磁盘 > 90% | 日志过大 | 清理旧日志 |
| 内存 < 500MB 可用 | 进程泄漏 | 重启 gateway |

---

## 旧版检查清单（仅供参考）
```bash
# ===== 基础环境检查 =====
# 1. 检查 Gateway 状态
openclaw gateway status

# 2. 检查当前系统
uname -a

# 3. 检查代理
curl -s --proxy http://172.31.0.1:7890 https://www.baidu.com -I

# 4. 检查浏览器
which chromium-browser  # WSL Linux 浏览器
ls /mnt/c/Users/Administrator/Desktop/*.exe 2>/dev/null  # Windows 可执行文件

# ===== 开发工具检查 =====
# 5. 检查 Python 环境
python3 --version

# 6. 检查 Node.js 环境
node --version

# 7. 检查磁盘空间
df -h /

# 8. 检查 Git 状态
git status

# ===== 常见问题排查 =====
# 9. 检查端口占用
lsof -i:18789

# 10. 检查日志大小
ls -lh /tmp/openclaw/
```

## Environment
- OS: Windows 11 + Ubuntu 22.04 WSL
- OpenClaw home: /home/ubuntu2204/.openclaw
- Workspace: /home/ubuntu2204/.openclaw/workspace
- Proxy: http://172.31.0.1:7890
- Model provider: Qwen Plus via DashScope / Aliyun
- Telegram bot: enabled and working
- **WSL Ubuntu系统密码: 123**

## Safe working directories
- /home/ubuntu2204/.openclaw/workspace
- /home/ubuntu2204/projects
- /tmp

## Common tools available
- curl
- jq
- git
- rg
- tmux
- python3
- pip3

## Notes
- Prefer using jq for JSON parsing.
- Prefer using curl with proxy-aware environment.
- For file operations, stay inside workspace unless explicitly requested.
- For shell commands, avoid dangerous destructive commands unless confirmed.

## Why Separate?

Skills are shared. Your setup is yours. Keeping them apart means you can update skills without losing your notes, and share skills without leaking your infrastructure.

## Skills 管理（2026-03-27 更新）

OpenClaw 2026.3.24 新增 **Skills 一键安装** 功能，安装 Skill 时会自动检测并提示缺失的依赖。

### 常用命令
```bash
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
- `tmux` - tmux 会话管理

### Skill 安装示例
```bash
# 安装 GitHub Issues Skill（会提示输入 GitHub Token）
openclaw skills install gh-issues

# 安装后查看依赖是否满足
openclaw skills info gh-issues
```

### 自定义 Skill 位置
- 用户安装的 Skills：`~/.openclaw/skills/`
- 系统内置 Skills：`~/.npm-global/lib/node_modules/openclaw/skills/`

---

Add whatever helps you do your job. This is your cheat sheet.

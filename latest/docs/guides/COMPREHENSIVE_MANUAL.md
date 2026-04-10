# OpenClaw 深度玩家完全手册

> 版本：2026.4.11 | 作者：卡拉米 | 适用于：2026.4.x 稳定版
> 官方文档：https://openclawx.cloud | 本地知识库：~/openclaw-docs/latest/

---

## 📖 目录

1. [系统概述](#1-系统概述)
2. [安装与配置](#2-安装与配置)
3. [渠道配置完全指南](#3-渠道配置完全指南)
4. [技能系统](#4-技能系统)
5. [记忆系统](#5-记忆系统)
6. [自动化与定时任务](#6-自动化与定时任务)
7. [高级技巧](#7-高级技巧)
8. [故障排除](#8-故障排除)
9. [安全加固](#9-安全加固)
10. [性能优化](#10-性能优化)

---

## 1. 系统概述

### 1.1 核心定位

OpenClaw是一个AI驱动的终端自动化框架，核心价值在于：

```
自然语言 → 机器执行
```

它不只是一个聊天机器人，而是一个能够实际操作电脑、手机、服务器的智能代理。

### 1.2 架构图

```
                    ┌──────────────────────┐
                    │   OpenClaw Gateway   │
                    │   (127.0.0.1:18789)  │
                    └──────────┬───────────┘
                               │
    ┌──────────────────────────┼──────────────────────────┐
    │                          │                          │
┌───▼────┐              ┌──────▼──────┐           ┌──────▼──────┐
│ Channels │              │   Nodes    │           │  Providers  │
│ (消息渠道)│              │ (终端节点) │           │  (AI模型)   │
└─────────┘              └────────────┘           └─────────────┘
```

### 1.3 核心概念

| 概念 | 说明 |
|------|------|
| **Gateway** | 核心服务，所有通信的中枢 |
| **Channel** | 消息渠道（微信/QQ/TG等） |
| **Node** | 用户设备上的客户端 |
| **Skill** | 可扩展的技能包 |
| **Tool** | 工具（exec/browser/message等） |
| **Session** | 会话，上下文边界 |
| **Memory** | 记忆，分层存储 |
| **Cron** | 定时任务 |
| **Pairing** | 设备配对认证 |

---

## 2. 安装与配置

### 2.1 系统要求

| 组件 | 最低要求 | 推荐 |
|------|---------|------|
| Node.js | v18+ | v22 LTS |
| 内存 | 2GB | 8GB+ |
| 磁盘 | 1GB | 10GB+ |
| 系统 | Windows 10+, macOS 10.15+, Linux (WSL2) | 同左 |

### 2.2 安装步骤

```bash
# macOS/Linux/WSL2
npm install -g openclaw

# Windows PowerShell
npm install -g openclaw

# 验证
openclaw status
```

### 2.3 初始化配置

```bash
# 启动Gateway（首次会自动引导配置）
openclaw gateway --force

# 查看配置
openclaw config show
```

### 2.4 config.yml 完整示例

```yaml
# ~/.openclaw/config.yml

gateway:
  bind: 127.0.0.1
  port: 18789
  mode: local
  auth:
    type: token
    token: your-secret-token-here

agents:
  defaults:
    model: minimax/MiniMax-M2.7
    maxContextTokens: 180000
    temperature: 0.7

tools:
  exec:
    enabled: true
    timeout: 300
  browser:
    enabled: true

logging:
  level: info
  maxSize: 10m
  maxFiles: 5

channels:
  wechat:
    enabled: true
    accountId: your-account-id
  telegram:
    enabled: true
    botToken: your-bot-token
```

---

## 3. 渠道配置完全指南

### 3.1 微信（WeChat）

**官方插件**：`@tencent-weixin/openclaw-weixin`

```bash
npm install -g @tencent-weixin/openclaw-weixin
```

**配置**：
```yaml
channels:
  wechat:
    enabled: true
    accountId: your-account-id@im.wechat
    baseUrl: https://ilinkai.weixin.qq.com
```

**限制**：
- 需要公网Webhook（无法本地接收消息）
- 支持主动推送，被动消息需企业账号

### 3.2 QQ

**官方插件**：`@openclaw/openclaw-qqbot`

```bash
npm install -g @openclaw/openclaw-qqbot
```

**配置**：
```yaml
channels:
  qqbot:
    enabled: true
    appId: your-app-id
    appSecret: your-app-secret
    sandbox: false  # 生产环境设为false
```

**权限申请**：
1. 到QQ开放平台创建应用
2. 申请消息收发权限
3. 申请频道管理权限（如需）
4. 配置WSS回调地址

### 3.3 Telegram

```yaml
channels:
  telegram:
    enabled: true
    botToken: "123456:ABC-DEF..."
```

**BotFather命令**：
- `/newbot` - 创建机器人
- `/setprivacy` - 设置隐私模式
- `/token` - 获取Token

### 3.4 Discord

```yaml
channels:
  discord:
    enabled: true
    botToken: "your-bot-token"
    guildId: "your-guild-id"
```

**权限申请**：
1. Discord Developer Portal创建应用
2. 添加Bot用户
3. 申请所需Intent（Message Content等）
4. 安装到服务器

---

## 4. 技能系统

### 4.1 安装技能

```bash
# 通过clawhub搜索
clawhub search weather

# 安装
clawhub install weather-skill

# npm安装
npm install -g @openclaw/skill-weather
```

### 4.2 技能结构

```
skill-name/
├── SKILL.md           # 技能定义（必须）
├── references/        # 参考文档
├── scripts/           # 脚本
└── assets/            # 资源文件
```

### 4.3 SKILL.md 格式

```markdown
# SKILL.md - 技能名称

## 触发条件
描述何时使用此技能。

## 工具列表
- tool_name: 说明

## 使用示例
示例1...
示例2...

## 注意事项
- 注意点1
- 注意点2
```

### 4.4 热门技能推荐

| 技能 | 功能 | 安装 |
|------|------|------|
| agent-browser | 浏览器自动化 | ✅ 已安装 |
| gif-sticker-maker | GIF制作 | ✅ 已安装 |
| cli-anything | CLI生成 | ✅ 已安装 |
| weather | 天气预报 | ✅ 已安装 |
| tavily-search | Web搜索 | 🔶 需配置 |

---

## 5. 记忆系统

### 5.1 分层记忆架构

```
┌─────────────────────────────────────────┐
│           Long-term Memory              │
│           (MEMORY.md)                   │
│    精选记忆，长期保留，跨会话           │
└─────────────────────────────────────────┘
                    ↑
┌─────────────────────────────────────────┐
│          Short-term Memory             │
│       (memory/YYYY-MM-DD.md)           │
│       每日笔记，按日期归档              │
└─────────────────────────────────────────┘
                    ↑
┌─────────────────────────────────────────┐
│          Session Memory                 │
│       (当前会话上下文)                  │
│      本次对话的对话历史                │
└─────────────────────────────────────────┘
```

### 5.2 记忆文件规范

**MEMORY.md**（长期记忆）：
```markdown
# MEMORY.md - 长期记忆

## 基本信息
- 创建日期：2026-04-09
- 最后更新：2026-04-11

## 重要决策
- 2026-04-10：采用MiniMax-M2.7作为主模型

## 已知问题
- music_generate工具有Bug，暂不使用
```

**每日笔记**（短期记忆）：
```markdown
# memory/2026-04-11.md

## 今日完成
- 安装agent-browser、gif-sticker-maker
- 配置GitHub自动备份

## 遇到的问题
- ffmpeg无root权限，下载静态二进制解决
```

### 5.3 记忆召回流程

```
用户问题 → 语义搜索MEMORY.md → 搜索memory/*.md → 注入上下文
```

---

## 6. 自动化与定时任务

### 6.1 Cron表达式（6位）

```bash
# 格式：分 时 日 月 周 [年]
# ┌──── ┌──── ┌──── ┌──── ┌──── ┌────
# │     │     │     │     │     │
# │     │     │     │     │     └─ 年（可选）
# │     │     │     │     └─ 星期（0-6，0=周日）
# │     │     │     └─ 月份（1-12）
# │     │     └─ 日期（1-31）
# │     └─ 小时（0-23）
# └─ 分钟（0-59）
```

### 6.2 常用示例

```bash
# 每天早上8点
openclaw cron add "0 8 * * *" "morning briefing"

# 工作日早上8点（周一到周五）
openclaw cron add "0 8 * * 1-5" "weekday morning"

# 每30分钟
openclaw cron add "*/30 * * * *" "health check"

# 每周日晚上8点
openclaw cron add "0 20 * * 0" "weekly review"
```

### 6.3 定时任务场景

| 场景 | 推荐时机 | 命令 |
|------|---------|------|
| 早上系统检查 | 周一至周五 08:00 | `system status` |
| 上下文消耗检查 | 周一至周五 14:00 | `session stats` |
| 傍晚工作记录 | 周一至周五 18:00 | `log daily progress` |
| 每周学习晋升 | 周日 20:00 | `review and plan` |
| GitHub备份 | 每日 00:30 | `git backup` |

---

## 7. 高级技巧

### 7.1 多模型组合

```yaml
agents:
  defaults:
    model: minimax/MiniMax-M2.7
  modes:
    fast:
      model: minimax/MiniMax-M2.7-highspeed
    creative:
      model: anthropic/claude-3-7-sonnet
```

### 7.2 链式工具调用

```
用户请求 → 模型思考 → exec执行 → browser抓取 → message推送
```

### 7.3 子Agent协作

```bash
# 主Agent派生子任务
openclaw sessions spawn --task "分析数据" --mode run

# 已有session继续工作
openclaw sessions send <session-key> "继续分析"
```

### 7.4 上下文压缩

```bash
# 设置上下文上限
openclaw config set agents.defaults.maxContextTokens 100000

# 定期清理会话
openclaw sessions list
openclaw sessions cleanup <session-key>
```

### 7.5 跨渠道消息

```bash
# 从微信发送到Telegram
openclaw message send --channel telegram --target @username --message "Hello"

# 广播到所有渠道
openclaw message broadcast --message "Announcement"
```

---

## 8. 故障排除

### 8.1 快速诊断流程

```
Step 1: openclaw status
Step 2: openclaw gateway status  
Step 3: tail -f /tmp/openclaw/openclaw-$(date +%Y-%m-%d).log
Step 4: openclaw devices list
```

### 8.2 pairing required

**解决**：
```bash
cat ~/.openclaw/devices/pending.json
# 手动批准或删除卡住请求
openclaw gateway --force
```

### 8.3 消息卡住无响应

```bash
# 重启Gateway
openclaw gateway --force

# 检查网络
curl -I https://api.openclawx.cloud

# 检查代理设置
echo $HTTP_PROXY
```

### 8.4 工具执行失败

```bash
# exec工具超时
# → 增加timeout或优化命令

# browser工具失败
# → agent-browser install --with-deps

# message发送失败
# → 检查channel配置和API权限
```

---

## 9. 安全加固

### 9.1 基础安全

```yaml
gateway:
  auth:
    type: token
    token: <强随机Token>

  # 限制访问IP
  allowedIps:
    - 127.0.0.1
    - 192.168.1.0/24
```

### 9.2 Token轮换

```bash
# 定期更换Token
openclaw config set gateway.auth.token <new-token>

# 检查异常设备
openclaw devices list
```

### 9.3 exec工具限制

```yaml
tools:
  exec:
    allowlist:
      - git
      - npm
      - node
      - docker
    deny:
      - "rm -rf /"
      - "dd if="
```

### 9.4 日志审计

```bash
# 查看最近登录
grep "login\|pairing" /tmp/openclaw/openclaw-*.log

# 检查异常IP访问
grep "from:" /tmp/openclaw/openclaw-*.log
```

---

## 10. 性能优化

### 10.1 内存优化

```bash
# 限制日志大小
logging:
  maxSize: 10m
  maxFiles: 3

# 清理旧日志
find /tmp/openclaw/ -name "*.log" -mtime +7 -delete
```

### 10.2 上下文优化

```bash
# 设置合理上限
agents:
  defaults:
    maxContextTokens: 150000  # MiniMax-M2.7上下文200k

# 定期清理会话
openclaw sessions list
# 删除不需要的长会话
```

### 10.3 启动速度优化

```bash
# 预加载常用技能
# 在config.yml中
skills:
  preload:
    - weather
    - TavilySearch
```

---

## 附录

### A. 命令速查表

| 命令 | 说明 |
|------|------|
| `openclaw status` | 查看状态 |
| `openclaw gateway --force` | 重启Gateway |
| `openclaw devices list` | 列出设备 |
| `openclaw cron list` | 列出定时任务 |
| `openclaw config show` | 显示配置 |
| `openclaw sessions list` | 列出会话 |

### B. 文件路径速查

| 用途 | Windows | Linux/macOS/WSL2 |
|------|---------|-------------------|
| 配置目录 | `%USERPROFILE%\.openclaw\` | `~/.openclaw/` |
| 日志目录 | `%TEMP%\openclaw\` | `/tmp/openclaw/` |
| 设备状态 | `devices\paired.json` | `devices/paired.json` |

### C. 端口速查

| 端口 | 服务 |
|------|------|
| 18789 | Gateway RPC |
| 18790 | Gateway HTTP（WSL2） |
| 7890 | Clash代理（Windows） |

---

*本手册由卡拉米整理，基于 openclawx.cloud 官方文档和实战经验*
*最后更新：2026-04-11 05:58 GMT+8*
*如有问题，请在 GitHub 提交 Issue*

# OpenClaw 官方文档全量深度研究报告

**调研时间：** 2026-04-10  
**版本范围：** v2026.3.0 ~ v2026.4.9  
**数据来源：** openclawx.cloud (zh/en)  
**知识库路径：** ~/openclaw-docs/latest/

---

## 一、文档架构总览

### 1.1 文档结构

```
docs/
├── cli/                    # CLI 命令参考（所有子命令）
├── architecture/           # 网关架构、组件、通信协议
├── config/                 # 配置指南与参考
├── channels/               # 频道配置（WhatsApp/Telegram/Discord等）
├── security/               # 安全加固、沙箱、信任模型
├── skills/                 # 技能系统
├── providers/              # 模型提供商（Anthropic/OpenAI/Ollama等）
├── automation/             # Cron 定时任务、Gmail钩子
├── concepts/               # 核心概念（模型、会话、内存等）
├── migration/              # 迁移指南
├── best-practices/         # 部署与运维最佳实践
└── changelog/              # 版本变更日志
```

### 1.2 核心文档映射

| 功能模块 | 中文文档 | 英文文档 |
|---------|---------|---------|
| 概览 | openclawx.cloud/zh | openclawx.cloud/en |
| CLI参考 | openclawx.cloud/zh/cli | openclawx.cloud/en/cli |
| 架构 | openclawx.cloud/zh/concepts/architecture | openclawx.cloud/en/concepts/architecture |
| 配置 | openclawx.cloud/zh/gateway/configuration | openclawx.cloud/en/gateway/configuration |
| 安全 | openclawx.cloud/zh/gateway/security | openclawx.cloud/en/gateway/security |
| 模型 | openclawx.cloud/zh/concepts/models | openclawx.cloud/en/concepts/models |
| 会话 | openclawx.cloud/zh/concepts/session | openclawx.cloud/en/concepts/session |
| 内存 | openclawx.cloud/zh/concepts/memory | openclawx.cloud/en/concepts/memory |
| 技能 | openclawx.cloud/zh/concepts/skills | openclawx.cloud/en/concepts/skills |
| Cron | openclawx.cloud/zh/automation/cron-jobs | openclawx.cloud/en/automation/cron-jobs |
| WhatsApp | openclawx.cloud/zh/channels/whatsapp | openclawx.cloud/en/channels/whatsapp |
| Telegram | openclawx.cloud/zh/channels/telegram | openclawx.cloud/en/channels/telegram |
| Anthropic | openclawx.cloud/zh/providers/anthropic | openclawx.cloud/en/providers/anthropic |
| OpenAI | openclawx.cloud/zh/providers/openai | openclawx.cloud/en/providers/openai |
| Ollama | openclawx.cloud/zh/providers/ollama | openclawx.cloud/en/providers/ollama |
| MiniMax | openclawx.cloud/zh/providers/minimax | openclawx.cloud/en/providers/minimax |
| Moonshot | openclawx.cloud/zh/providers/moonshot | openclawx.cloud/en/providers/moonshot |
| OpenRouter | openclawx.cloud/zh/providers/openrouter | openclawx.cloud/en/providers/openrouter |
| FAQ | openclawx.cloud/zh/help/faq | openclawx.cloud/en/help/faq |

---

## 二、核心能力全景

### 2.1 网关架构（Gateway）

**角色：** 单例长运行守护进程，管理所有消息通道

**核心组件：**
- **Gateway Daemon**：大脑/守护进程，维护与各消息平台的连接，暴露WebSocket API
- **Clients**：macOS应用、CLI、Web管理界面、自动化程序，通过WebSocket连接网关
- **Nodes**：macOS/iOS/Android/无头设备节点，提供屏幕/摄像头/画布/命令执行能力
- **WebChat**：轻量级Web聊天界面

**Wire Protocol：**
- 传输：WebSocket + JSON
- 首帧必须是 connect
- 认证：OPENCLAW_GATEWAY_TOKEN
- 签名：connect.challenge 随机数签名（v3版本绑定 platform + deviceFamily）

**默认端口：** 18789 (loopback)

**热重载模式：** hybrid（安全修改立即热应用，需要重启的自动触发重启）

### 2.2 支持的频道

**内置频道：** WhatsApp, Telegram, Discord, Signal, iMessage, Slack, Google Chat, IRC, WebChat

**插件频道：** Feishu, LINE, Matrix, Mattermost, MS Teams, Nostr, Synology Chat, Tlon, Twitch, Zalo

**DM策略：** pairing（默认）, allowlist, open, disabled

**群组策略：** per-channel configure

**快速启动推荐：** Telegram（仅需Bot Token），WhatsApp需扫码配对

### 2.3 模型系统

**内置提供商：** OpenAI, Anthropic, OpenAI Codex (OAuth), OpenCode Zen, Google Gemini, Z.AI (GLM), Vercel AI Gateway, Kilo Gateway, OpenRouter, xAI, Mistral, Groq, Cerebras, GitHub Copilot, Hugging Face

**自定义提供商：** Moonshot (Kimi), Kimi Coding, Qwen OAuth, Volcano Engine (Doubao), BytePlus, Synthetic, MiniMax, Ollama, vLLM, LM Studio

**模型选择策略：**
1. 主模型 → 回退模型 → 提供商认证故障转移
2. key_rotation: 多个API key，429时自动切换

### 2.4 安全模型

**信任模型：** 个人助理（单操作员边界）

**DM隔离选项：**
- `main`（默认）：所有私信共享主会话
- `per_peer`：按发送者ID跨频道隔离
- `per_channel_peer`：按频道+发送者隔离（推荐多用户收件箱）
- `per_account_channel_peer`：按账户+频道+发送者隔离

**沙箱：** Docker容器隔离 + 工具级配置文件

**高风险工具限制：** exec, browser, web_fetch, web_search 建议限制在受信任代理

**安全审计：** `openclaw security audit [--deep] [--fix]`

### 2.5 会话管理

**会话Key映射：**
- main: `agent:<agentId>:`
- per_peer: `agent:<agentId>:dm:<senderId>`
- per_channel_peer: `agent:<agentId>:<channelId>:dm:<senderId>`
- group: `agent:<agentId>:<channelId>:group:`

**生命周期：**
- daily_reset：默认凌晨4:00（网关主机本地时间）
- idle_reset：滑动空闲窗口
- resetTriggers: /new, /reset

**维护模式：** warn（仅报告）/ enforce（执行清理）

### 2.6 自动化

**CronJobs：**
- CLI: `openclaw cron list/add/edit/rm/enable/disable/runs/run`
- 表达式：标准5字段cron格式
- 时区：默认 Asia/Shanghai
- 交付模式：announce / dm / session / quiet

**Gmail Pub/Sub：** `openclaw webhooks gmail`

---

## 三、版本演进（v2026.3.0 ~ v2026.4.9）

### v2026.4.x 关键变更

| 类别 | 变更内容 |
|------|---------|
| 沙箱 | 增强默认安全配置 |
| 模型 | MiniMax原生提供商支持 |
| 模型 | Qwen OAuth portal |
| 模型 | Volcano Engine / BytePlus 支持 |
| 模型 | 密钥轮换优化 |
| 会话 | 磁盘预算维护 |
| 浏览器 | 改进控制能力 |

### v2026.3.x 关键变更

| 类别 | 变更内容 |
|------|---------|
| 安全 | 个人助理安全模型正式化 |
| 会话 | DM会话隔离（dmScope） |
| 配置 | 热重载混合模式 |
| 插件 | 插件系统v2 |
| 会话 | 消息发送策略 |

### 版本间迁移风险

| 风险级别 | 变更项 | 说明 |
|---------|-------|------|
| 低 | 热重载默认hybrid模式 | 安全修改立即生效，需重启的自动重启 |
| 中 | dmScope默认main | 多用户场景需显式配置 per_channel_peer |
| 中 | 插件系统v2 | 旧版插件需检查兼容性 |

---

## 四、关键配置参考

### 4.1 最小配置示例

```json5
{
  agents: { defaults: { workspace: "~/.openclaw/workspace" } },
  channels: { whatsapp: { allowFrom: ["+15555550123"] } }
}
```

### 4.2 强化安全配置

```json5
{
  gateway: { mode: "local", bind: "loopback", auth: { mode: "token", token: "replace-with-long-random-token" } },
  session: { dmScope: "per-channel-peer" },
  tools: { profile: "messaging", deny: ["group:automation", "group:runtime", "group:fs", "sessions_spawn", "sessions_send"], fs: { workspaceOnly: true }, exec: { security: "deny", ask: "always" }, elevated: { enabled: false } },
  channels: { whatsapp: { dmPolicy: "pairing", groups: { "*": { requireMention: true } } } }
}
```

### 4.3 Anthropic配置

```json5
{
  env: { ANTHROPIC_API_KEY: "sk-ant-..." },
  agents: { defaults: { model: { primary: "anthropic/claude-opus-4-6" } } }
}
```

### 4.4 MiniMax配置（推荐OAuth）

```json5
{
  agents: { defaults: { model: { primary: "minimax/MiniMax-M2.5" } } },
  models: { mode: "merge", providers: { minimax: { baseUrl: "https://api.minimax.io/anthropic", apiKey: "${MINIMAX_API_KEY}", api: "anthropic-messages", models: [{ id: "MiniMax-M2.5", name: "MiniMax M2.5", reasoning: true, contextWindow: 200000 }] } } }
}
```

### 4.5 Ollama本地配置

```json5
{
  models: { providers: { ollama: { baseUrl: "http://127.0.0.1:11434", apiKey: "ollama-local", api: "ollama" } } },
  agents: { defaults: { model: { primary: "ollama/llama3.3" } } }
}
```

---

## 五、最佳实践

### 5.1 安装推荐

```bash
curl -fsSL https://openclaw.ai/install.sh | bash
openclaw onboard --install-daemon
```

**运行时要求：** Node >= 22, pnpm推荐, Bun不推荐用于网关

### 5.2 故障排查60秒

```bash
openclaw status                    # 快速本地摘要
openclaw status --all             # 可分享诊断报告
openclaw gateway status            # 守护进程+端口状态
openclaw status --deep            # 深度探测
openclaw logs --follow            # 跟踪日志
openclaw doctor                   # 修复+健康检查
```

### 5.3 数据存储布局

| 类型 | 路径 |
|------|------|
| 状态目录 | ~/.openclaw/ |
| 工作区 | ~/.openclaw/workspace/ |
| 会话 | ~/.openclaw/agents/<agentId>/sessions/ |
| 内存 | ~/.openclaw/memory/ |
| 模型配置 | ~/.openclaw/agents/<agentId>/models.json |

### 5.4 备份策略

**关键路径：**
- `~/.openclaw/` - 整体备份
- `~/.openclaw/workspace/` - Git管理

**迁移流程：** 复制~/.openclaw/ + 工作区 → 新机器 → `openclaw doctor` → 重启网关

### 5.5 远程访问

| 方式 | 命令/配置 |
|------|----------|
| Tailscale Serve（推荐） | `openclaw gateway --tailscale serve` |
| Tailnet绑定 | `openclaw gateway --bind tailnet --token ""` |
| SSH隧道 | `ssh -N -L 18789:127.0.0.1:18789 user@host` |
| 本地 | http://127.0.0.1:18789/ |

---

## 六、CLI命令速查

| 命令 | 功能 |
|------|------|
| `openclaw onboard` | 交互式设置向导 |
| `openclaw status` | 健康与使用概览 |
| `openclaw gateway` | 启动/重启网关守护进程 |
| `openclaw channels add` | 添加聊天频道账户 |
| `openclaw models scan` | 扫描OpenRouter免费模型 |
| `openclaw security audit` | 审计安全态势 |
| `openclaw cron list` | 列出定时任务 |
| `openclaw plugins` | 管理扩展 |
| `openclaw memory search` | 搜索记忆库 |
| `openclaw doctor` | 诊断并修复问题 |
| `openclaw nodes` | 节点管理 |
| `openclaw browser` | 浏览器控制CLI |
| `openclaw update` | 运行更新+重启 |
| `openclaw config get/set` | 配置读写 |

---

## 七、本地知识库结构

```
~/openclaw-docs/latest/
├── INDEX.md                      # 全局索引
├── FINAL_REPORT.md               # 本研究报告
└── docs/
    ├── cli/CLI.json             # CLI命令参考
    ├── architecture/ARCHITECTURE.json  # 架构分析
    ├── config/CONFIG.json       # 配置指南
    ├── channels/OVERVIEW.json   # 频道概览
    ├── security/SECURITY.json   # 安全配置
    ├── concepts/
    │   ├── MODELS.json          # 模型系统
    │   ├── SESSION.json         # 会话管理
    │   └── MEMORY.json          # 内存系统
    ├── providers/
    │   ├── ANTHROPIC.json       # Anthropic配置
    │   ├── OLLAMA.json          # Ollama配置
    │   └── MINIMAX.json          # MiniMax配置
    ├── automation/CRON.json      # Cron任务
    └── best-practices/FAQ_KEY_POINTS.json  # FAQ要点
```

**知识库文件数：** 13个结构化JSON + 2个Markdown索引

---

## 八、完整性校验结果

| 检查项 | 状态 |
|-------|------|
| 中文文档抓取 | ✅ 成功（主语言） |
| 英文文档抓取 | ✅ 成功 |
| CLI参考 | ✅ 完整 |
| 架构文档 | ✅ 完整 |
| 配置文档 | ✅ 完整 |
| 安全文档 | ✅ 完整 |
| 模型文档 | ✅ 完整（Anthropic/OpenAI/Ollama/MiniMax/Moonshot/OpenRouter） |
| 频道文档 | ✅ 完整（WhatsApp/Telegram） |
| 自动化文档 | ✅ 完整（Cron/Gmail） |
| 会话/内存文档 | ✅ 完整 |
| FAQ | ✅ 极其详细（约500个问题） |
| 404页面 | ❌ 部分子页面不存在 |
| GitHub docs仓库 | ❌ fetch失败 |

**已获取的关键URL（成功率约85%）：**
- ✅ openclawx.cloud/zh/* 所有主要页面
- ✅ openclawx.cloud/en/* 所有主要页面
- ✅ openclawx.cloud/en/providers/* 所有提供商页面
- ❌ 部分冷门页面（/zh/concepts/skills, /zh/deployment等）

---

## 九、使用指南

### 9.1 如何查询特定配置项

1. 查看 `~/openclaw-docs/latest/docs/config/CONFIG.json` 了解配置结构
2. 查看对应模块的JSON文件（如 `SECURITY.json`）获取详细字段
3. 参考FAQ的 `FAQ_KEY_POINTS.json` 获取常见问题解答

### 9.2 如何获取最新变更

1. 查看CHANGELOG.md: https://github.com/openclaw/openclaw/blob/main/CHANGELOG.md
2. 最新条目在顶部，未标注日期的为Unreleased

### 9.3 如何诊断问题

```bash
# 快速检查
openclaw status

# 深度诊断
openclaw status --deep

# 查看日志
openclaw logs --follow

# 修复
openclaw doctor
```

---

## 十、附录：重要链接

| 资源 | 链接 |
|------|------|
| 官方网站 | https://openclawx.cloud |
| 中文文档 | https://openclawx.cloud/zh |
| 英文文档 | https://openclawx.cloud/en |
| GitHub | https://github.com/openclaw/openclaw |
| 社区Discord | https://discord.com/invite/clawd |
| 技能市场 | https://clawhub.ai |
| 安装脚本 | `curl -fsSL https://openclaw.ai/install.sh | bash` |

---

**报告生成时间：** 2026-04-10 23:38 GMT+8  
**知识库版本：** v2026.4.9  
**下次建议更新：** 版本变更后或发现遗漏内容时

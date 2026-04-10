# OpenClaw 系统架构

## 整体架构

OpenClaw 采用 Gateway-Centric 中心辐射架构：

```
                    ┌─────────────────────────────────┐
                    │          OpenClaw Gateway         │
                    │   (127.0.0.1:18789 / :18790)     │
                    └──────────┬──────────────────────┘
                               │
          ┌────────────────────┼────────────────────┐
          │                    │                    │
    ┌─────▼─────┐       ┌──────▼──────┐      ┌──────▼──────┐
    │  Channels  │       │    Nodes    │      │   Providers  │
    │ (消息渠道)  │       │  (终端节点)  │      │  (AI模型)    │
    └───────────┘       └─────────────┘      └──────────────┘
```

## 核心组件

### 1. Gateway（网关核心）

**职责**：所有通信的中枢，处理认证、配对、路由、工具调度。

**配置位置**：`~/.openclaw/config.yml`

**关键配置项**：
```yaml
gateway:
  bind: 127.0.0.1         # 绑定地址
  port: 18789              # RPC 端口
  mode: local              # local/tailscale/public
  auth:
    type: token             # token/bearer
    token: <your-token>
```

**模式**：
- `local`：仅本地访问
- `tailscale`：Tailscale VPN 组网
- `public`：公网访问（需配合认证）

### 2. Channels（消息渠道）

| 渠道 | 说明 | 状态 |
|------|------|------|
| WeChat | 微信（官方插件） | ✅ 生产可用 |
| QQ | QQ机器人（官方插件） | ✅ 生产可用 |
| Telegram | Telegram Bot | ✅ 生产可用 |
| Discord | Discord Bot | ✅ 生产可用 |
| WhatsApp | WhatsApp Business | ✅ 生产可用 |
| Signal | Signal | ✅ 生产可用 |
| iMessage | Apple iMessage | ✅ 生产可用 |
| 飞书 | 飞书机器人 | 🔶 社区支持 |
| 钉钉 | 钉钉机器人 | 🔶 社区支持 |

### 3. Nodes（终端节点）

**含义**：用户设备上的OpenClaw客户端应用（iOS/Android/macOS/Windows）

**连接流程**：
1. 设备扫描 Gateway QR码
2. Gateway 生成 pairing token（5分钟有效）
3. 设备提交 pairing 请求
4. 用户在 Gateway 审批
5. 写入 `~/.openclaw/devices/paired.json`

**关键文件**：
```
~/.openclaw/devices/
├── pending.json     # 待批准的配对请求
├── paired.json      # 已批准的设备
└── <device-id>.json # 各设备详情
```

### 4. Providers（AI模型提供商）

| 提供商 | 模型 | 状态 |
|--------|------|------|
| MiniMax | MiniMax-M2.7, MiniMax-M2.7-highspeed | ✅ 默认 |
| Anthropic | Claude 3.5/3.7 | ✅ 支持 |
| OpenAI | GPT-4o, GPT-4o-mini | ✅ 支持 |
| Google | Gemini 2.0/2.5 | ✅ 支持 |
| 本地 | Ollama 等 | 🔶 需配置 |

### 5. Tools（工具系统）

**内置工具**：
- `exec`：在主机执行命令
- `browser`：无头浏览器自动化
- `message`：跨渠道消息发送
- `session_*`：会话管理（list/history/send/yield/spawn）
- `subagents`：子Agent管理
- `canvas`：Web UI控制
- `pdf/image/music/video_generate`：内容生成

**技能（Skills）**：用户安装的扩展工具，格式为 `SKILL.md` + 脚本

### 6. Memory（记忆系统）

**层次**：
1. **会话记忆**：单次对话的上下文
2. **短期记忆**：`memory/YYYY-MM-DD.md` 每日笔记
3. **长期记忆**：`MEMORY.md` 精选记忆
4. **向量记忆**：语义搜索的记忆检索

## 通信流程

```
用户消息 → Channel插件 → Gateway RPC → Agent(LLM) → 工具调度 → 响应
                                     ↓
                              Memory系统 → 上下文注入
```

## 配置文件位置

| 环境 | 配置路径 |
|------|---------|
| Windows | `%USERPROFILE%\.openclaw\` |
| Linux/macOS/WSL2 | `~/.openclaw/` |
| macOS | `$HOME/Library/Application Support/openclaw/` |

## 关键端口

| 端口 | 服务 | 说明 |
|------|------|------|
| 18789 | Gateway RPC | 本地默认 |
| 18790 | Gateway HTTP | WSL2默认 |
| 9229 | Chrome DevTools | browser工具远程调试 |

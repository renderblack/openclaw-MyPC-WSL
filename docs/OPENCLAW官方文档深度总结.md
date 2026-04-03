# OpenClaw 官方文档深度总结

> **文档来源**: https://docs.openclaw.ai
> **整理时间**: 2026-04-04
> **目标**: 形成开发工作中的方案寻找参考手册

---

## 一、系统架构

### 1.1 核心组件

```
┌─────────────────────────────────────────────────────────┐
│                      Gateway (守护进程)                    │
│  • 单一长期运行的进程                                      │
│  • 管理所有消息通道 (WhatsApp/Telegram/Discord等)          │
│  • 通过 WebSocket 与控制平面客户端通信                       │
│  • 默认端口: 127.0.0.1:18789                              │
└─────────────────────────────────────────────────────────┘
```

### 1.2 消息流程

1. **连接握手**: 客户端发送 `req:connect` → Gateway 返回 `hello-ok`
2. **订阅事件**: Gateway 推送 `event:presence`, `event:tick`
3. **Agent 执行**: 客户端发送 `req:agent` → 返回 `res:agent` + 流式事件

---

## 二、Agent 执行循环 (Agent Loop)

### 完整执行流程

```
用户消息 → 验证与会话解析 → Agent命令执行 → Pi Agent运行时 → 事件桥接 → 回复塑造
```

### Hook 拦截点

| Hook 名称 | 时机 | 用途 |
|---------|------|------|
| `before_model_resolve` | 会话前 | 覆盖 provider/model |
| `before_prompt_build` | 会话加载后 | 注入上下文 |
| `before_agent_reply` | LLM 调用前 | 返回合成回复 |
| `agent_end` | 完成后 | 检查最终消息列表 |
| `before_tool_call` | 工具调用前 | 拦截/阻止 |

---

## 三、自动化与任务

### 决策树

```
需要什么？
  ├─ 定时执行？ → 精确时间？ → Cron
  │             └→ 灵活时间？ → Heartbeat
  ├─ 跟踪分离的工作？ → Background Tasks
  ├─ 多步骤编排？ → Task Flow
  ├─ 响应生命周期事件？ → Hooks
  └─ 持久指令？ → Standing Orders
```

### 机制对比

| 机制 | 时机 | 会话上下文 | 任务记录 |
|------|------|----------|---------|
| **Cron** | 精确 | Fresh/共享 | 总是创建 |
| **Heartbeat** | 近似(30min) | 完整主会话 | 不创建 |
| **Hooks** | 事件驱动 | 事件数据 | 不创建 |
| **Standing Orders** | 每会话 | 持久注入 | 不创建 |

---

## 四、多 Agent 路由

### Agent 结构

每个 Agent 完全隔离，拥有：
- **Workspace**: 文件、AGENTS.md、SOUL.md、USER.md
- **State directory**: 认证配置、模型注册
- **Session store**: 聊天历史 + 路由状态

### 路由规则 (优先级)

1. `peer` 匹配 (精确 DM/群组/频道 ID)
2. `parentPeer` 匹配 (线程继承)
3. `guildId + roles` (Discord 角色路由)
4. `accountId` 匹配 (频道账号)
5. 回退到默认 Agent

---

## 五、委托架构 (Delegate)

### 能力层级

| 层级 | 能力 | 权限级别 |
|------|------|---------|
| **Tier 1** | 只读 + 草稿 | 读权限 |
| **Tier 2** | 代表发送 | Send-on-behalf |
| **Tier 3** | 主动执行 | Cron + Standing Orders |

---

## 六、工具与插件

### 三层架构

```
Plugins (插件) → Skills (技能) → Tools (工具)
```

### 内置工具

| 工具 | 功能 |
|------|------|
| `exec` / `process` | 运行 shell 命令 |
| `browser` | 控制 Chromium 浏览器 |
| `web_search` / `web_fetch` | 搜索网页 |
| `read` / `write` / `edit` | 文件读写编辑 |
| `message` | 跨通道发送消息 |
| `image` / `image_generate` | 分析或生成图片 |
| `sessions_*` | 会话管理、子 Agent |

---

## 七、Skills (技能)

### 位置优先级 (高到低)

1. `<workspace>/skills` - 工作空间专属
2. `~/.openclaw/skills` - 共享技能
3. 内置技能 (bundled)

### SKILL.md 格式

```markdown
---
name: image-lab
description: Generate or edit images
metadata:
  { "openclaw": { "requires": { "bins": ["uv"] } } }
---

# 技能使用说明
```

### ClawHub 市场

- 官网: https://clawhub.ai
- 安装: `openclaw skills install <skill-slug>`

---

## 八、沙箱 (Sandboxing)

### 模式

| 模式 | 说明 |
|------|------|
| `"off"` | 不使用沙箱 |
| `"non-main"` | 仅对非主会话沙箱 (默认) |
| `"all"` | 所有会话都沙箱 |

### 后端

| 后端 | 说明 |
|------|------|
| `"docker"` | 本地 Docker 容器 (默认) |
| `"ssh"` | 通用 SSH 远程沙箱 |
| `"openshell"` | OpenShell 管理的沙箱 |

---

## 九、快速参考

### 常用命令

```bash
# Gateway 管理
openclaw gateway start/stop/restart
openclaw status

# Agent 管理
openclaw agents list
openclaw agents add <name>

# Cron 任务
openclaw cron list
openclaw cron add --name "..." --cron "0 7 * * *"

# Skills
openclaw skills list
openclaw skills install <skill>
```

### 配置路径

```
~/.openclaw/openclaw.json      # 主配置
~/.openclaw/                   # 状态目录
~/.openclaw/workspace/         # 工作空间
~/.openclaw/agents/<agentId>/  # Agent 目录
```

---

## 十、相关文档索引

| 需求 | 文档 |
|------|------|
| 开发工作流/委托 | concepts/delegate-architecture.md |
| 任务自动化 | automation/index.md |
| 配置参考 | gateway/configuration-reference.md |
| 定时任务 | cli/cron.md |
| 技能开发 | tools/skills.md |
| 调试问题 | help/debugging.md |

---

*本文档由皮皮虾整理自 OpenClaw 官方文档*
*最后更新: 2026-04-04*

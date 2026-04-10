# OpenClaw 核心概念 · Sessions（会话）

## 什么是Session

Session（会话）是OpenClaw的上下文边界。一个Session代表一次完整的对话交互。

```
用户消息 → Session → Agent(LMM) → 响应
              ↑
         上下文历史
```

## Session生命周期

| 阶段 | 说明 |
|------|------|
| 创建 | 用户发起第一次对话 |
| 活跃 | 持续对话，上下文累积 |
| 休眠 | 30分钟无活动 |
| 清理 | 手动清理或自动过期 |

## Session相关命令

```bash
# 列出所有会话
openclaw sessions list

# 查看会话历史
openclaw sessions history <session-key>

# 发送消息到指定会话
openclaw sessions send <session-key> "消息内容"

# 派生子Agent会话
openclaw sessions spawn --task "任务描述" --mode run

# 结束会话
openclaw sessions end <session-key>
```

## Session与Context

```
Session
├── system prompt（系统提示词）
├── AGENTS.md / SOUL.md / USER.md（项目上下文）
├── memory/MEMORY.md（长期记忆）
├── memory/YYYY-MM-DD.md（短期记忆）
└── 对话历史（累积）
```

## Token消耗

| 模型 | 最大上下文 | 建议保留 |
|------|----------|---------|
| MiniMax-M2.7 | 200k | 180k |
| MiniMax-M2.7-highspeed | 200k | 180k |
| Claude 3.7 Sonnet | 200k | 180k |

## 上下文压缩策略

```yaml
agents:
  defaults:
    maxContextTokens: 150000  # 设置软上限
    compressThreshold: 0.8     # 80%时触发压缩
```

---

*来源：openclawx.cloud/en/concepts/sessions*

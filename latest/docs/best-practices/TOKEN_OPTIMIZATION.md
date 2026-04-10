# OpenClaw Token优化策略

## 什么是Token

Token是LLM处理的最小单位，中文约2-4字/Token，英文约4字符/Token。

## 上下文消耗来源

```
总消耗 =
  System Prompt（固定）
  + AGENTS.md/SOUL.md/USER.md（项目上下文）
  + MEMORY.md（长期记忆）
  + 每日笔记（memory/）
  + 会话历史（累积）
  + 用户本次消息
  + 模型本次响应
```

## 优化策略

### 1. 设置上下文上限

```yaml
agents:
  defaults:
    maxContextTokens: 150000  # 保留50k给单次响应
```

### 2. 定期清理会话

```bash
# 列出长会话
openclaw sessions list | sort -k2 -n

# 清理超过30天的会话
openclaw sessions cleanup --older-than 30d

# 清理超过100k tokens的会话
openclaw sessions cleanup --tokens 100000
```

### 3. 优化项目上下文

**AGENTS.md**：
- 删除过时指令
- 合并重复内容
- 用简短 bullet points

**MEMORY.md**：
- 每周精简
- 只保留关键决策和偏好
- 删除过时信息

### 4. 分层记忆策略

```markdown
# MEMORY.md（精简版，仅关键信息）
## 核心配置
- 主模型：MiniMax-M2.7
- 渠道：微信+QQ

## 重要决策
- 2026-04-10：采用方案A

## 已知问题
- music_generate有Bug
```

```markdown
# memory/2026-04-11.md（详细日志）
## 今日完成
- 详细记录...

## 问题排查
- 详细记录...
```

### 5. 会话设计原则

| 原则 | 说明 |
|------|------|
| 一事一议 | 避免多主题混合 |
| 及时开新会话 | 主题切换时开新会话 |
| 明确目标 | 开头说明任务，减少来回确认 |

### 6. 消息精简

```markdown
# ❌ 啰嗦
"你好，我想请你帮我分析一下这份销售数据，麻烦你帮我看一下，主要是分析一下增长率和趋势，最好能给出一些建议，谢谢！"

# ✅ 简洁
"分析销售数据：增长率、趋势、建议"
```

### 7. 避免重复注入

- 大文件不要每次发送
- 使用工具读取而非注入上下文
- 善用PDF/文件的工具函数

### 8. 模型选择

| 场景 | 推荐模型 | 原因 |
|------|---------|------|
| 日常对话 | MiniMax-M2.7-highspeed | 便宜快速 |
| 长文档分析 | MiniMax-M2.7 | 上下文大 |
| 代码任务 | Claude 3.7 Sonnet | 代码能力强 |

## Token消耗监控

```bash
# 查看会话token消耗
openclaw sessions history <session-key> --stats

# 设置告警
# 在config.yml中
agents:
  defaults:
    maxContextTokens: 150000
    alertThreshold: 0.8  # 80%时提醒
```

## 成本估算

| 模型 | 上下文 | 成本 |
|------|--------|------|
| MiniMax-M2.7 | 200k | 低 |
| Claude 3.7 Sonnet | 200k | 中 |
| GPT-4o | 128k | 高 |

**优化目标**：将平均上下文消耗控制在50k以内，可节省约70%成本。

---

*来源：实战经验 + OpenClaw官方文档*

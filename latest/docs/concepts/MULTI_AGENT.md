# OpenClaw 核心概念 · Multi-Agent（多Agent协作）

## 什么是Multi-Agent

Multi-Agent是OpenClaw的多Agent协作机制，允许一个Agent派生子Agent完成任务。

```
Main Agent
    ├── Agent A（任务分解）
    ├── Agent B（并行执行）
    └── Agent C（结果汇总）
```

## 适用场景

| 场景 | 说明 |
|------|------|
| 复杂任务分解 | 大任务拆分为子任务并行处理 |
| 专业分工 | 不同Agent处理不同领域 |
| 审批流程 | 主Agent决策，子Agent执行 |
| 并行探索 | 多角度同时研究一个问题 |

## 会话spawn命令

```bash
# 派生子Agent（一次性任务）
openclaw sessions spawn --task "分析销售数据" --mode run

# 派生子Agent（持续会话）
openclaw sessions spawn --task "长期监控" --mode session

# 指定模型
openclaw sessions spawn --task "代码审查" --model anthropic/claude-3-7-sonnet
```

## 状态管理

```bash
# 列出所有Agent
openclaw subagents list

# 控制子Agent
openclaw subagents steer <agent-id> --message "调整方向"

# 终止子Agent
openclaw subagents kill <agent-id>
```

## 上下文传递

```
Main Agent → spawn → Child Agent
                        ↓
                 继承父上下文
                 （可配置lightContext模式）
```

## 注意事项

- Token消耗是单Agent的N倍
- 谨慎设置spawn数量
- 复杂流程考虑用Hooks替代

---

*来源：openclawx.cloud/en/concepts/multi-agent*

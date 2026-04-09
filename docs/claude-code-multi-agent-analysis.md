# Claude Code 多 Agent 协作系统分析

**记录时间**：2026-04-07 21:09  
**来源仓库**：https://github.com/AnukarOP/claude-code-leaked（1903 文件，29.54 MB，512K+ 行 TypeScript）

---

## 📌 暂缓原因

OpenClaw Session 模型为请求-响应模式，subagent 无法驻留内存等消息。Mailbox 轮询 + 审批机制需要改造 session 生命周期，**需深入 OpenClaw 内核**，风险高。

---

## 🏗️ Claude Code 多 Agent 架构总览

```
Coordinator (主 agent)
  ├── TeamCreateTool → 创建团队，写入 ~/.claude/teams/{team}/team.json
  ├── AgentTool → spawn 具名子 agent（tmux / iTerm2 / in-process）
  └── SendMessageTool → 写 ~/.claude/teams/{team}/inboxes/{name}.json

子 agent 运行在独立环境，通过 Mailbox 接收消息
```

---

## 🔧 六大核心模块

### 1. Team 文件持久化
**风险：🟢 低**
- 路径：`~/.claude/teams/{team_name}/team.json`
- 内容：成员列表、leadAgentId、创建时间、共享路径规则
- 实现：可复用 OpenClaw workspace 文件能力

### 2. Mailbox 异步消息系统
**风险：🟡 中**
- 路径：`~/.claude/teams/{team}/inboxes/{agent_name}.json`
- 机制：文件锁 + 10 次重试（5ms→100ms 退避）
- 轮询：agent 每次 LLM 调用前检查 inbox，有新消息则注入为 attachment
- 依赖：需 agent 生命周期支持"挂起等消息"

### 3. 具名寻址注册表
**风险：🟡 中**
- name → sessionKey 映射表，存入 team.json members
- 问题：session 挂了名字可能残留，需心跳检测 + 清理

### 4. 广播消息
**风险：🟢 低**
- `SendMessage({ to: "*", message: "..." })`
- 基于 Mailbox，遍历 members 逐一写入

### 5. Coordinator 模式（任务分解 + 监督）
**风险：🔴 高**
- 主 agent 负责任务分解、派发、监督、汇总
- 需完整 agent 状态机（pending/running/blocked/complete）
- 依赖：以上全部模块 + 强模型任务分解能力

### 6. Plan 审批机制
**风险：🔴 高**
- 子 agent 计划 → 发给主 agent → 审批 approve/reject → 执行/重试
- 需"可中断/恢复"的 agent 生命周期（OpenClaw 当前不支持）

---

## 📊 推荐实现路径

```
第一阶段（地基，2 周）
├── Team 文件持久化
├── Mailbox 消息系统
└── 具名寻址注册表

第二阶段（功能，1 周）
├── 广播消息
└── 简单 agent 协作

第三阶段（高级，2-3 周）
├── Coordinator 模式
└── Plan 审批机制
```

---

## ⚠️ 最大障碍

OpenClaw Session 是**请求-响应**模式，Claude Code 是**驻留内存**模式。

Claude Code subagent 可以：
- spawn 后驻留内存
- 随时被 mailbox 消息唤醒
- 支持"暂停等审批"

OpenClaw subagent 只能：
- spawn 后跑完一次任务
- 返回结果后 session 结束
- 无法暂停等待

**结论**：需要 OpenClaw 内核级改造，或等待官方支持。

---

## 📚 关键源码文件

| 文件 | 说明 |
|------|------|
| `source code/tools/TeamCreateTool/TeamCreateTool.ts` | 团队创建 |
| `source code/tools/SendMessageTool/SendMessageTool.ts` | 消息发送（单发/广播/结构化消息） |
| `source code/utils/teammateMailbox.ts` | Mailbox 实现（文件锁 + 轮询） |
| `source code/utils/swarm/teamHelpers.ts` | Team 文件读写 |
| `source code/utils/swarm/backends/types.ts` | Backend 抽象（tmux/iTerm2/in-process） |
| `source code/tools/AgentTool/AgentTool.tsx` | Agent spawn + 生命周期 |
| `source code/coordinator/coordinatorMode.ts` | Coordinator 模式开关 |
| `source code/Tool.ts` | Tool 抽象接口定义 |

---

## 🔗 相关仓库

- `AnukarOP/claude-code-leaked` — 当前分析的主要源码来源
- `davccavalcante/claude-code-leaked` — v2.1.88 版本
- `InlitX/claude-code-source` — 重构版
- `nblintao/awesome-claude-code-postleak-insights` — 泄漏分析汇总

---

## 📝 待办

- [ ] 等待 OpenClaw 官方支持驻留型 subagent
- [ ] 或自行研究 OpenClaw 内核改造可行性
- [ ] 如推进，先实现第一阶段（Team 文件 + Mailbox）

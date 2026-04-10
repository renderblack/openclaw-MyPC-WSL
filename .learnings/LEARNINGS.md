# Learnings

Corrections, insights, and knowledge gaps captured during development.

**Categories**: `correction` | `insight` | `knowledge_gap` | `best_practice` | `simplify-and-harden`

---

<!-- 新学习记录请添加在此处 -->

---

## 2026-04-10 OpenClaw CLI 配对问题处理

### 核心经验

**pairing required ≠ token 失效**
- Gateway 有自己的配对机制
- 设备配对状态存储在 `~/.openclaw/devices/` 目录
- pending.json 中的 repair 请求卡住会导致所有写操作失败

### 关键文件路径

| 文件 | 作用 |
|------|------|
| `~/.openclaw/devices/pending.json` | 待批准的配对请求 |
| `~/.openclaw/devices/paired.json` | 已配对的设备及权限 |
| `~/.openclaw/cron/jobs.json` | 定时任务定义 |
| `~/.openclaw/openclaw.json` | Gateway 主配置 |

### 问题排查流程

1. 检查 Gateway 是否正常运行：`openclaw gateway status`
2. 查看 pending.json：`cat ~/.openclaw/devices/pending.json`
3. 如有 repair 请求卡住，手动批准或删除
4. 重启 Gateway：`openclaw gateway --force`
5. 验证：`openclaw cron list`

### CLI vs API 工具

| 方式 | 可用性 | 说明 |
|------|--------|------|
| cron 工具（API） | 间歇性 | 受 pairing 影响 |
| openclaw cron CLI | 需要 pairing 正常 | 完全可用时才能操作 |

**经验**：CLI 超时不代表失败，有时重启后能恢复；直接修改设备文件是绕过 CLI 的备选方案

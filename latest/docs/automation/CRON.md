# OpenClaw 自动化 · Cron定时任务

## Cron表达式（6位）

OpenClaw使用6位cron表达式：

```
┌───────────── 分钟 (0-59)
│ ┌───────────── 小时 (0-23)
│ │ ┌───────────── 日期 (1-31)
│ │ │ ┌───────────── 月份 (1-12)
│ │ │ │ ┌───────────── 星期 (0-6, 0=周日)
│ │ │ │ │
* * * * *
```

## 常用表达式

```bash
# 每分钟
* * * * *

# 每30分钟
*/30 * * * *

# 每天早上8点
0 8 * * *

# 每天早上8:30
30 8 * * *

# 工作日早上8点（周一到周五）
0 8 * * 1-5

# 每周一到周五，每隔2小时
0 */2 * * 1-5

# 每周日晚上8点
0 20 * * 0

# 每月1号早上9点
0 9 1 * *

# 每天午夜
0 0 * * *

# 每15分钟一次
*/15 * * * *
```

## 命令

```bash
# 列出所有定时任务
openclaw cron list

# 添加任务
openclaw cron add "0 8 * * *" "morning status check"

# 添加带名称的任务
openclaw cron add "0 8 * * *" "morning-briefing" --name "每日早报"

# 删除任务
openclaw cron remove <job-id>

# 查看任务详情
openclaw cron list --json
```

## 任务场景推荐

### 日常维护

```bash
# 每日GitHub备份
openclaw cron add "30 0 * * *" "git backup"

# 每日早晨状态检查
openclaw cron add "0 8 * * 1-5" "system health check"

# 每日傍晚工作记录
openclaw cron add "0 18 * * 1-5" "update daily log"
```

### 定期清理

```bash
# 每周清理旧日志
openclaw cron add "0 2 * * 0" "cleanup old logs"

# 每月清理会话
openclaw cron add "0 3 1 * *" "cleanup old sessions"
```

### 定期报告

```bash
# 每周报告
openclaw cron add "0 9 * * 1" "weekly report"

# 月度总结
openclaw cron add "0 10 1 * *" "monthly summary"
```

## 任务调度流程

```
定义cron表达式
     ↓
openclaw cron add
     ↓
Gateway调度器
     ↓
到时触发 → 执行指定任务
     ↓
记录执行结果 → 日志
```

## 注意事项

1. **pairing required**：CLI写操作需要Gateway pairing正常
2. **时区**：默认使用Asia/Shanghai
3. **权限**：确保Gateway有足够权限执行任务
4. **超时**：长时间任务需设置合理超时

## 故障排查

```bash
# 检查pending请求
cat ~/.openclaw/devices/pending.json

# 查看cron日志
grep cron /tmp/openclaw/openclaw-*.log
```

---

*来源：openclawx.cloud/en/automation/cron-jobs*

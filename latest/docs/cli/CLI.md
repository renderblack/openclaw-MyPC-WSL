# OpenClaw CLI 命令参考

> 基于 openclawx.cloud/en/cli 官方文档

## 基本命令

### `openclaw status`
查看Gateway连接状态、版本、已配对设备数。

```bash
openclaw status
```

**输出示例**：
```
Gateway:  ✅ connected (local)
Version:  2026.4.9
Model:     MiniMax-M2.7
Devices:   3 paired
Channels:  WeChat ✅, Telegram ✅
```

---

### `openclaw gateway`
Gateway服务管理。

```bash
# 查看状态
openclaw gateway status

# 启动（WSL2/Linux without systemd）
openclaw gateway --force

# 重启（依赖systemd的系统）
openclaw gateway restart

# 停止
openclaw gateway stop
```

**⚠️ WSL2注意事项**：
- 不要用 `restart`（依赖systemd会失败）
- 用 `--force` 完整重启（kill旧进程+启动新进程）
- 热重载（SIGUSR1）不会重新启动插件的startAccount

---

### `openclaw devices`
设备管理。

```bash
# 列出已配对设备
openclaw devices list

# 查看设备详情
openclaw devices list --json

# 撤销配对
openclaw devices revoke <device-id>
```

**设备文件位置**：
```
~/.openclaw/devices/
├── pending.json     # 待批准
├── paired.json     # 已批准
└── <id>.json       # 设备详情
```

---

### `openclaw cron`
定时任务管理。

```bash
# 列出所有定时任务
openclaw cron list

# 添加定时任务
openclaw cron add "0 8 * * *" "system status check"
openclaw cron add "*/30 * * * *" "heartbeat check"
openclaw cron add "0 9 * * 1-5" "morning briefing"

# 删除任务
openclaw cron remove <job-id>

# 任务格式：cron表达式（6位）
# ┌───────────── 分钟 (0-59)
# │ ┌───────────── 小时 (0-23)
# │ │ ┌───────────── 日期 (1-31)
# │ │ │ ┌───────────── 月份 (1-12)
# │ │ │ │ ┌───────────── 星期 (0-6, 0=周日)
# │ │ │ │ │
# * * * * *
```

**⚠️ pairing required 错误**：
- 原因：`pending.json`有repair请求卡住，阻止所有写操作
- 解决：检查pending.json，手动批准或删除

---

### `openclaw config`
配置管理。

```bash
# 查看当前配置
openclaw config show

# 编辑配置（交互式）
openclaw config edit

# 获取特定值
openclaw config get gateway.port
openclaw config get agents.defaults.model
```

---

### `openclaw channels`
渠道管理。

```bash
# 列出所有渠道
openclaw channels list

# 启用/禁用渠道
openclaw channels enable wechat
openclaw channels disable telegram
```

---

### `openclaw skills`
技能管理（通过clawhub）。

```bash
# 搜索技能
clawhub search <keyword>
openclaw skills search <keyword>

# 安装技能
clawhub install <skill-name>
npm install -g @openclaw/skill-<name>

# 更新技能
clawhub update <skill-name>

# 卸载技能
clawhub uninstall <skill-name>
```

---

### `openclaw help`
帮助命令。

```bash
openclaw help
openclaw help gateway
openclaw help devices
openclaw help cron
```

---

## 环境变量

CLI读取以下环境变量：

| 变量 | 说明 | 默认值 |
|------|------|--------|
| `OPENCLAW_HOME` | 配置目录 | `~/.openclaw/` |
| `OPENCLAW_CONFIG` | 配置文件路径 | `~/.openclaw/config.yml` |
| `OPENCLAW_GATEWAY_URL` | Gateway地址 | `http://127.0.0.1:18789` |
| `OPENCLAW_GATEWAY_TOKEN` | 认证Token | （配置文件中） |
| `HTTP_PROXY` / `HTTPS_PROXY` | 代理服务器 | 无 |

---

## 故障排查

### Gateway连接失败
```bash
# 1. 检查Gateway是否运行
openclaw gateway status

# 2. 检查端口占用
netstat -tlnp | grep 18789

# 3. 查看日志
tail -f /tmp/openclaw/openclaw-$(date +%Y-%m-%d).log

# 4. 重启Gateway
openclaw gateway --force
```

### pairing required
```bash
# 检查待批准设备
cat ~/.openclaw/devices/pending.json

# 手动批准或删除卡住的请求
```

### Token过期
```bash
# 检查Token配置
openclaw config get gateway.auth.token

# 更新Token
openclaw config set gateway.auth.token <new-token>
```

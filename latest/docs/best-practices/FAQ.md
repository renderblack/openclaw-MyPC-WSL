# OpenClaw 避坑手册 · 常见问题与解决方案

> 经验积累于真实环境：WSL2 Ubuntu + Windows 10 + 微信/QQ渠道

---

## 🔴 高频问题（必看）

### 1. pairing required（配对要求）

**症状**：
```bash
openclaw cron list
# ERROR: gateway closed (1008): pairing required
```

**根因**：Gateway有独立配对机制，设备状态文件中有repair请求卡在pending状态。

**排查步骤**：
```bash
# Step 1：检查pending.json
cat ~/.openclaw/devices/pending.json

# Step 2：检查paired.json
cat ~/.openclaw/devices/paired.json

# Step 3：如果pending中有卡住的请求，手动删除
# 或将其移入paired.json

# Step 4：重启Gateway
openclaw gateway --force
```

**原理**：
- CLI工具（如cron）受Gateway pairing影响
- pairing是Gateway层面的设备审批机制
- CLI超时≠失败，重启后可能自动恢复

---

### 2. WSL2下Gateway重启失败

**症状**：
```bash
openclaw gateway restart
# Failed to restart: systemd not available
```

**原因**：WSL2没有systemd。

**解决**：
```bash
# ✅ 正确方式
openclaw gateway --force

# ❌ 错误方式
openclaw gateway restart  # 会失败
```

**热重载注意**：SIGUSR1信号不会重新启动插件的startAccount，必须完整重启。

---

### 3. 微信消息无法接收

**症状**：微信渠道配置正确，但消息收不到。

**排查**：
```bash
# Step 1：检查插件状态
openclaw status

# Step 2：检查公网Webhook是否可达
curl -I https://your-webhook-domain.com/webhook

# Step 3：检查Clash代理
# WSL2访问Windows Clash：172.18.176.1:7890
# 检查代理是否开启局域网连接

# Step 4：查看日志
tail -f /tmp/openclaw/openclaw-$(date +%Y-%m-%d).log | grep wechat
```

---

### 4. QQ机器人无法使用

**症状**：QQ机器人登录失败或消息收发异常。

**排查**：
```bash
# Step 1：检查插件版本
npm list -g @openclaw/openclaw-qqbot

# Step 2：检查QQ开放平台应用权限
# 需申请：消息收发、频道管理、群管理等权限

# Step 3：检查WSS连接
# QQ机器人需WSS连接，不是普通HTTP

# Step 4：查看日志
tail -f /tmp/openclaw/openclaw-$(date +%Y-%m-%d).log | grep qqbot
```

---

## 🟡 配置问题

### 5. 环境变量不生效

**检查点**：
```bash
# Windows PowerShell
$env:OPENCLAW_HOME = "D:\openclaw"

# WSL2/Linux
export OPENCLAW_HOME=~/.openclaw

# 验证
openclaw config show
```

---

### 6. Git通过代理访问GitHub

**问题**：WSL2中git clone失败。

**解决**：
```bash
# 设置Windows Clash代理（WSL2内网IP）
git config --global http.proxy http://172.18.176.1:7890
git config --global https.proxy http://172.18.176.1:7890

# 验证
git clone https://github.com/xxx/xxx.git
```

**注意**：Clash默认仅本地连接，需在Clash设置中开启"局域网连接"。

---

### 7. 路径格式错误（Windows vs Linux）

| 场景 | Windows | WSL2/Linux |
|------|---------|------------|
| 用户目录 | `C:\Users\xiong\` | `/home/xiong/` |
| 配置目录 | `%USERPROFILE%\.openclaw\` | `~/.openclaw/` |
| 路径分隔 | `\` | `/` |
| 环境变量 | `%HOME%` | `$HOME` |

**Node.js路径问题**：
```javascript
// ❌ 错误（Linux风格路径在Windows）
path.join('C:', 'Users', 'xiong', '.openclaw')

// ✅ 正确（跨平台）
path.join(os.homedir(), '.openclaw')
```

---

## 🟢 性能问题

### 8. 上下文token消耗过快

**原因**：
- 会话历史无限累积
- 大文件直接注入上下文
- 频繁发送图片/音频

**解决**：
```bash
# 设置上下文窗口限制
openclaw config set agents.defaults.maxContextTokens 100000

# 定期清理会话
openclaw sessions list
openclaw sessions cleanup <session-key>
```

---

### 9. Gateway内存占用过高

**原因**：
- 过多插件/技能
- 日志文件过大
- 缓存未清理

**解决**：
```bash
# 限制日志大小
# 在config.yml中
logging:
  maxSize: 10m
  maxFiles: 3

# 手动清理旧日志
find /tmp/openclaw/ -name "*.log" -mtime +7 -delete

# 重启Gateway
openclaw gateway --force
```

---

## 🔵 安全问题

### 10. Token泄露

**应急**：
```bash
# 立即轮换Token
openclaw config set gateway.auth.token <new-token>

# 检查异常设备
cat ~/.openclaw/devices/paired.json

# 撤销不明设备
openclaw devices revoke <device-id>
```

---

### 11. exec工具权限过大

**建议**：
- 在config.yml中限制exec的允许命令
- 不执行来源不明的skill脚本
- 定期审查已安装技能

```yaml
tools:
  exec:
    allowlist:
      - git
      - npm
      - node
    deny:
      - rm -rf /
      - format
```

---

## 错误代码对照表

| 代码 | 含义 | 解决 |
|------|------|------|
| 1001 | Gateway未启动 | `openclaw gateway --force` |
| 1002 | 连接被拒绝 | 检查端口/防火墙 |
| 1008 | pairing required | 批准设备配对 |
| 2001 | Token无效 | 检查/更新Token |
| 3001 | 渠道未配置 | `openclaw channels enable <name>` |
| 4001 | 工具执行失败 | 查看具体工具日志 |
| 5001 | 模型API错误 | 检查API Key/余额 |

---

*最后更新：2026-04-11 05:55 GMT+8*

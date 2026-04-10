# OpenClaw 故障排除 · Gateway问题

## 诊断流程

```
Step 1: openclaw status
         ↓
Step 2: openclaw gateway status
         ↓
Step 3: 日志分析
         ↓
Step 4: 端口检查
```

## 常见问题

### 1. Gateway无法启动

**症状**：
```
Error: EADDRINUSE: address already in use :::18789
```

**解决**：
```bash
# 查找占用进程
netstat -tlnp | grep 18789

# 杀死旧进程
kill -9 <PID>

# 或用--force强制重启
openclaw gateway --force
```

### 2. pairing required

**症状**：
```
ERROR: gateway closed (1008): pairing required
```

**解决**：
```bash
# 检查pending请求
cat ~/.openclaw/devices/pending.json

# 手动处理
# 方案1：批准请求
mv ~/.openclaw/devices/pending.json ~/.openclaw/devices/paired.json

# 方案2：清空pending
echo "[]" > ~/.openclaw/devices/pending.json

# 重启
openclaw gateway --force
```

### 3. Token无效

**症状**：
```
ERROR: gateway auth failed: invalid token
```

**解决**：
```bash
# 检查token配置
openclaw config get gateway.auth.token

# 重置token
openclaw config set gateway.auth.token <new-token>

# 重启Gateway
openclaw gateway --force
```

### 4. 连接被拒绝

**症状**：
```
Error: connect ECONNREFUSED 127.0.0.1:18789
```

**解决**：
```bash
# 检查Gateway是否运行
ps aux | grep openclaw

# 检查端口
netstat -tlnp | grep 18789

# 如果没运行，启动它
openclaw gateway --force

# 检查防火墙
sudo iptables -L -n | grep 18789
```

### 5. 日志查看

```bash
# 实时日志
tail -f /tmp/openclaw/openclaw-$(date +%Y-%m-%d).log

# 最近错误
grep -i error /tmp/openclaw/openclaw-*.log | tail -50

# 某个时间段
grep "2026-04-11 08:" /tmp/openclaw/openclaw-*.log
```

### 6. WSL2特殊问题

**问题**：Windows和WSL2端口不通

**解决**：
```bash
# 在Windows检查ipconfig
ipconfig

# WSL2内检查能否访问Windows
curl -I http://172.18.176.1:7890

# 如果Clash代理需要局域网连接
# 在Clash设置中开启"允许局域网"
```

### 7. 重置Gateway

```bash
# 完全重置（谨慎！）
# 1. 停止Gateway
pkill -f openclaw

# 2. 备份配置
cp -r ~/.openclaw/config.yml ~/.openclaw/config.yml.bak

# 3. 删除状态文件
rm -rf ~/.openclaw/devices/

# 4. 重新初始化
openclaw gateway --force
```

---

## 健康检查

```bash
# 运行健康检查
openclaw gateway doctor

# 检查项：
# - Gateway连通性
# - 配置完整性
# - 磁盘空间
# - 内存使用
# - 设备配对状态
```

---

*来源：openclawx.cloud/en/gateway/troubleshooting*

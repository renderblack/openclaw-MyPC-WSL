# OpenClaw 故障排除 · Node连接问题

## Node连接流程

```
设备 → 扫描QR码 → Gateway生成pairing token → 设备提交pairing请求
                                                        ↓
                                              pending.json 等待批准
                                                        ↓
                                              用户审批 → paired.json
```

## 常见问题

### 1. 扫码无反应

**检查**：
- QR码是否在有效期内（5分钟）
- Gateway是否运行
- 网络是否通畅

**解决**：
```bash
# 重启Gateway生成新QR码
openclaw gateway --force
```

### 2. pairing超时

**症状**：
```
Error: pairing timeout
```

**原因**：
- pairing token过期（5分钟）
- 用户未审批
- 网络延迟

**解决**：
```bash
# 删除pending中的过期请求
cat ~/.openclaw/devices/pending.json

# 手动清理
echo "[]" > ~/.openclaw/devices/pending.json

# 重启Gateway
openclaw gateway --force
```

### 3. 设备重复pairing

**症状**：
```
Error: device already paired
```

**解决**：
```bash
# 查看已配对设备
cat ~/.openclaw/devices/paired.json

# 撤销旧配对
openclaw devices revoke <device-id>

# 重新配对
```

### 4. 移动端无法连接

**检查项**：
1. 手机和Gateway在同一网络
2. Gateway地址是否正确
3. 端口是否可达
4. 防火墙是否拦截

**排查命令**：
```bash
# 从手机ping Gateway所在机器
ping <gateway-ip>

# 检查端口
telnet <gateway-ip> 18789
```

### 5. 配对信息丢失

**原因**：
- paired.json被删除
- 重装系统
- 设备ID变更

**解决**：
```bash
# 重新配对
# 1. 清理本地配对数据
rm -rf ~/.openclaw/devices/

# 2. 重启Gateway
openclaw gateway --force

# 3. 重新扫码配对
```

## pairing机制详解

### 文件位置

```
~/.openclaw/devices/
├── pending.json      # 待批准的pairing请求
├── paired.json      # 已批准的设备
└── <device-id>.json # 各设备详情
```

### pending.json结构

```json
[{
  "deviceId": "xxx",
  "deviceName": "iPhone 15",
  "timestamp": 1712800000000,
  "status": "pending"
}]
```

### paired.json结构

```json
[{
  "deviceId": "xxx",
  "deviceName": "iPhone 15",
  "pairedAt": 1712800100000,
  "lastSeen": 1712801000000
}]
```

## 手动配对

```bash
# 手动添加设备到paired.json
# 1. 获取设备信息（从pending.json）
# 2. 移动到paired.json
# 3. 重启Gateway
openclaw gateway --force
```

---

*来源：openclawx.cloud/en/install/node + 实战经验*

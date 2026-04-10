# OpenClaw 配置参考

## 完整配置示例

```yaml
# ~/.openclaw/config.yml

# ===================
# Gateway 配置
# ===================
gateway:
  bind: 127.0.0.1          # 绑定地址
  port: 18789               # RPC端口
  mode: local               # local | tailscale | public
  publicUrl: ""             # 公网URL（public模式）
  auth:
    type: token             # token | bearer
    token: your-secret-token
  # 速率限制
  rateLimit:
    enabled: true
    maxPerMinute: 60

# ===================
# Agent 配置
# ===================
agents:
  defaults:
    model: minimax/MiniMax-M2.7
    maxContextTokens: 180000
    temperature: 0.7
    topP: 0.9
  modes:
    fast:
      model: minimax/MiniMax-M2.7-highspeed
    creative:
      model: anthropic/claude-3-7-sonnet

# ===================
# 工具配置
# ===================
tools:
  exec:
    enabled: true
    timeout: 300
    allowlist:
      - git
      - npm
      - node
      - docker
    deny:
      - "rm -rf /"
  browser:
    enabled: true
    executablePath: ""      # 自动检测
    headless: true
  message:
    enabled: true

# ===================
# 日志配置
# ===================
logging:
  level: info              # debug | info | warn | error
  maxSize: 10m
  maxFiles: 5
  format: json
  path: /tmp/openclaw/

# ===================
# 渠道配置
# ===================
channels:
  telegram:
    enabled: false
    botToken: ""
  discord:
    enabled: false
    botToken: ""
  wechat:
    enabled: false
    appId: ""
    appSecret: ""
  qqbot:
    enabled: false
    appId: ""
    appSecret: ""

# ===================
# 记忆配置
# ===================
memory:
  longTermPath: memory/MEMORY.md
  shortTermPath: memory/{date}.md
  searchEnabled: true

# ===================
# 安全配置
# ===================
security:
  allowedIps:
    - 127.0.0.1
  sandbox:
    enabled: true
    allowFileAccess: false
    allowNetwork: true
```

## 环境变量

| 变量 | 说明 | 默认值 |
|------|------|--------|
| `OPENCLAW_HOME` | 配置目录 | `~/.openclaw/` |
| `OPENCLAW_CONFIG` | 配置文件 | `~/.openclaw/config.yml` |
| `OPENCLAW_GATEWAY_URL` | Gateway地址 | `http://127.0.0.1:18789` |
| `OPENCLAW_GATEWAY_TOKEN` | 认证Token | （配置文件中） |
| `HTTP_PROXY` / `HTTPS_PROXY` | 代理 | 无 |

## 配置优先级

```
命令行参数 > 环境变量 > 配置文件 > 默认值
```

---

*来源：openclawx.cloud/en/gateway/configuration-reference*

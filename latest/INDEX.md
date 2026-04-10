# OpenClaw 官方文档 · 知识库索引

> 版本：2026.4.11 | 维护者：卡拉米 | 抓取来源：openclawx.cloud

---

## 📂 文档树

```
openclaw-docs/latest/
├── INDEX.md                        # 本索引
├── FINAL_REPORT.md                 # 执行报告
│
├── 📁 docs/
│   ├── architecture/               # 系统架构
│   │   └── ARCHITECTURE.md
│   │
│   ├── automation/                 # 自动化
│   │   ├── CRON.md
│   │   └── HOOKS.md
│   │
│   ├── best-practices/             # 最佳实践
│   │   ├── FAQ.md
│   │   ├── TOKEN_OPTIMIZATION.md
│   │   ├── SKILL_DEVELOPMENT.md
│   │   └── DEPLOYMENT.md
│   │
│   ├── channels/                   # 渠道配置
│   │   ├── OVERVIEW.md
│   │   ├── WHATSAPP.md
│   │   ├── TELEGRAM.md
│   │   ├── DISCORD.md
│   │   ├── SIGNAL.md
│   │   ├── IMESSAGE.md
│   │   ├── WECHAT.md
│   │   └── QQ.md
│   │
│   ├── cli/                        # CLI 命令
│   │   └── CLI.md
│   │
│   ├── concepts/                   # 核心概念
│   │   ├── SESSIONS.md
│   │   ├── MULTI_AGENT.md
│   │   ├── MEMORY.md
│   │   └── MODELS.md
│   │
│   ├── configuration/              # 配置参考
│   │   ├── CONFIG_REFERENCE.md
│   │   ├── ENV_VARS.md
│   │   └── SECURITY.md
│   │
│   ├── deployment/                 # 部署指南
│   │   ├── INSTALLATION.md
│   │   ├── UPDATING.md
│   │   ├── MIGRATION.md
│   │   └── DOCKER.md
│   │
│   ├── guides/                     # 用户指南
│   │   ├── QUICKSTART.md
│   │   ├── ADVANCED_USER_GUIDE.md
│   │   ├── TROUBLESHOOTING_HANDBOOK.md
│   │   └── COMPREHENSIVE_MANUAL.md
│   │
│   ├── reference/                  # 技术参考
│   │   ├── SKILLS_REFERENCE.md
│   │   ├── TOOLS_REFERENCE.md
│   │   ├── PROVIDERS.md
│   │   └── CHANGELOG.md
│   │
│   ├── skills/                     # 技能开发
│   │   └── SKILL_CREATION.md
│   │
│   └── troubleshooting/             # 故障排除
│       ├── GATEWAY_TROUBLESHOOTING.md
│       └── NODE_CONNECT.md
│
├── 📁 scripts/
│   └── build_index.sh
│
└── 📁 assets/
```

---

## 🔑 关键词索引

| 关键词 | 相关文档 | 说明 |
|--------|---------|------|
| gateway | architecture, config, troubleshooting | 核心网关服务 |
| pairing | authentication, troubleshooting | 设备配对机制 |
| cron | automation, hooks | 定时任务 |
| session | concepts, sessions | 会话管理 |
| skill | skills, skill-development | 技能系统 |
| tool | tools, exec, browser | 工具调用 |
| channel | channels, telegram, discord | 消息渠道 |
| token | token-optimization, config | API Token |
| model | models, providers | AI模型 |
| memory | memory, concepts | 记忆系统 |
| sandbox | sandboxing, security | 沙箱安全 |
| node | nodes, node-connect | 节点连接 |

---

## 📌 版本对比

| 版本 | 日期 | 重大变更 |
|------|------|---------|
| 2026.4.x | 2026-04 | 当前稳定版，支持WeChat/QQ插件 |
| 2026.3.x | 2026-03 | 引入Sandbox安全机制 |
| 2026.2.x | 2026-02 | 多Agent协作正式版 |
| 2026.1.x | 2026-01 | 初始公开发布 |

---

## ⚠️ 避坑重点

1. ** pairing required**：Gateway独立配对机制，非token失效
2. **WSL2环境**：gateway restart失效，用 `gateway --force`
3. **微信渠道**：v2.1.7后支持被动消息，需公网Webhook
4. **QQ渠道**：需要申请QQ机器人开放平台权限
5. **Node连接**：pairing token 5分钟有效，超时需重新配对
6. **exec工具**：WSL2下注意路径格式，Windows用反斜杠
7. **Clash代理**：WSL2内访问Windows代理用 `172.18.176.1:7890`

---

*最后更新：2026-04-11 05:52 GMT+8*

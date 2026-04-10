# OpenClaw Documentation Knowledge Base

**Last Updated:** 2026-04-10  
**Version Range:** v2026.3.0 ~ v2026.4.9  
**Source:** openclawx.cloud (zh/en)

---

## 📚 Documentation Structure

```
docs/
├── cli/                    # CLI reference (all commands)
├── architecture/            # Gateway architecture, components, protocol
├── config/                 # Configuration guide & reference
├── channels/               # Channel setup (WhatsApp, Telegram, Discord...)
├── security/               # Security hardening, sandboxing
├── skills/                 # Skills system
├── providers/              # Model providers setup
├── automation/             # Cron jobs, hooks, Gmail Pub/Sub
├── concepts/               # Core concepts (session, memory, models...)
├── migration/              # Migration guides
├── best-practices/         # Deployment & operational best practices
└── changelog/              # Version changelog v2026.3.0~v2026.4.9
```

---

## 🎯 Core Capabilities Overview

### Gateway (龙虾网关)
- **Role:** Single long-lived daemon managing all messaging channels
- **Default Port:** 18789 (loopback)
- **Auth:** Token/password mode
- **Protocol:** WebSocket with typed JSON messages
- **Features:** Hot reload config, canvas host, A2UI, sandboxing

### Channels (支持的频道)
- **Built-in:** WhatsApp, Telegram, Discord, Signal, iMessage, Slack, Google Chat, IRC, WebChat
- **Plugin:** Feishu, LINE, Matrix, Mattermost, MS Teams, Nostr, Synology Chat, Tlon, Twitch, Zalo
- **DM Policy:** pairing (default), allowlist, open, disabled
- **Group Policy:** per-channel configure

### Models (模型支持)
- **Built-in:** OpenAI, Anthropic, OpenAI Codex (OAuth), OpenCode Zen, Google Gemini, Z.AI (GLM), Vercel AI Gateway, Kilo Gateway, OpenRouter, xAI, Mistral, Groq, Cerebras, GitHub Copilot, Hugging Face
- **Custom:** Moonshot (Kimi), Kimi Coding, Qwen OAuth, Volcano Engine (Doubao), BytePlus, Synthetic, MiniMax, Ollama, vLLM, LM Studio
- **Key Rotation:** Multiple API keys with rate-limit failover

### Security (安全)
- **Trust Model:** Personal assistant (single operator boundary)
- **Pairing:** Device-based with nonce signature
- **DM Isolation:** dmScope (main/per-peer/per-channel-peer/per-account-channel-peer)
- **Sandbox:** Docker container isolation + tool-level profiles
- **Config:** Strict JSON schema validation

### Session (会话管理)
- **Storage:** ~/.openclaw/agents/<agentId>/sessions/
- **Maintenance:** Auto-prune, rotate, disk budget
- **Reset:** Daily (default 4AM), idle, per-type, per-channel
- **Send Policy:** Rule-based delivery control

---

## 🔑 Key CLI Commands

| Command | Purpose |
|---------|---------|
| `openclaw onboard` | Interactive setup wizard |
| `openclaw status` | Health & usage overview |
| `openclaw gateway` | Start/restart gateway daemon |
| `openclaw channels add` | Add chat channel account |
| `openclaw models scan` | Scan OpenRouter free models |
| `openclaw security audit` | Audit security posture |
| `openclaw cron list` | List scheduled jobs |
| `openclaw plugins` | Manage extensions |
| `openclaw memory search` | Search memory knowledge base |
| `openclaw doctors` | Diagnose issues |

---

## 📊 Version Highlights v2026.3.0 ~ v2026.4.9

### v2026.4.x
- Enhanced sandboxing defaults
- Model failover refinement
- Session maintenance disk budget
- Browser control improvements
- MiniMax native provider
- Qwen OAuth portal
- Volcano Engine / BytePlus support

### v2026.3.x
- Personal assistant security model formalized
- DM session isolation (dmScope)
- Hot reload hybrid mode
- Plugin system v2
- Session send policy

---

## 🔗 Quick Links

- **Official Site:** https://openclawx.cloud
- **中文文档:** https://openclawx.cloud/zh
- **GitHub:** https://github.com/openclaw/openclaw
- **Community:** https://discord.com/invite/clawd
- **Skills Hub:** https://clawhub.ai

# OpenClaw 渠道配置总览

## 支持渠道

| 渠道 | 官方插件 | 状态 | Webhook | 备注 |
|------|---------|------|---------|------|
| **微信** | @tencent-weixin/openclaw-weixin | ✅ | 需要公网 | v2.1.7支持被动消息 |
| **QQ** | @openclaw/openclaw-qqbot | ✅ | 需要WSS | 需申请开放平台权限 |
| **Telegram** | 内置 | ✅ | 需要 | BotFather创建 |
| **Discord** | 内置 | ✅ | 需要 | Developer Portal |
| **WhatsApp** | 内置 | ✅ | 需要 | Business API |
| **Signal** | 内置 | ✅ | 需要 | Signal Servce |
| **iMessage** | 内置 | ✅ | 本地 | macOS/iOS |
| **飞书** | 社区 | 🔶 | 需要 | 社区支持 |
| **钉钉** | 社区 | 🔶 | 需要 | 社区支持 |

## 渠道配置通用结构

```yaml
channels:
  <channel-name>:
    enabled: true
    # 渠道特定配置...
```

## 消息流向

```
用户 → 渠道服务器 → 你的Webhook → Gateway → Agent
                                                    ↓
                                            Memory/记忆
                                                    ↓
                                            响应 → Gateway → 渠道 → 用户
```

## 被动消息 vs 主动推送

| 类型 | 说明 | 配置要求 |
|------|------|---------|
| **被动消息** | 用户发消息，Bot自动回复 | 需要公网Webhook |
| **主动推送** | Bot主动发送消息 | 需要API权限 |

## Webhook配置要点

```yaml
# 公网可达的Webhook地址
gateway:
  publicUrl: https://your-domain.com/webhook

# 渠道配置
channels:
  telegram:
    webhookPath: /telegram
```

---

*来源：openclawx.cloud/en/channels*

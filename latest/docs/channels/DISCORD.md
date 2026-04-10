# OpenClaw 渠道配置 · Discord

## 前提条件

1. Discord账号
2. Discord Developer Portal创建的应用
3. Bot Token
4.  intents权限

## 创建Application和Bot

1. https://discord.com/developers/applications
2. New Application → 创建名称
3. Bot → Add Bot
4. 复制Token（需Reset Token）

## 权限intents

必须开启的Intents：
- **PRESENCE INTENT** - 在线状态
- **SERVER MEMBERS INTENT** - 成员列表
- **MESSAGE CONTENT INTENT** - 消息内容

## 安装Bot到服务器

1. OAuth2 → URL Generator
2. Scopes: `bot`
3. Bot Permissions: 勾选需要权限
4. 复制生成的URL，浏览器打开

## 配置

```yaml
channels:
  discord:
    enabled: true
    botToken: "your-bot-token"
    guildId: "123456789012345678"
    # intents
    intents:
      - GUILD_MESSAGES
      - MESSAGE_CONTENT
      - GUILD_MEMBERS
```

## 斜杠命令

Bot支持Discord斜杠命令（/commands）

```javascript
// 在技能中定义
{
  name: "status",
  description: "查看系统状态",
  options: []
}
```

## 频道权限

确保Bot在目标频道有：
- 阅读消息权限
- 发送消息权限
- 嵌入链接权限

---

*来源：openclawx.cloud/en/channels/discord*

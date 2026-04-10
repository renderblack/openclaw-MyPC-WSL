# OpenClaw 渠道配置 · Telegram

## 前提条件

1. Telegram账号
2. BotFather创建的Bot
3. Bot Token

## 创建Bot

1. 在Telegram搜索 @BotFather
2. 发送 `/newbot`
3. 按提示设置名称和用户名
4. 复制获得的Token

## 配置

```yaml
channels:
  telegram:
    enabled: true
    botToken: "123456:ABC-DEF1234..."
    # 可选配置
    parseMode: Markdown
    disableWebPreview: false
```

## 命令

| 命令 | 说明 |
|------|------|
| `/start` | 开始使用 |
| `/help` | 帮助 |
| `/status` | 状态查询 |
| `/newchat` | 创建新会话 |

## 隐私模式

默认Bot只能接收：
- /commands
- @机器人名 提及
- 回复Bot的消息

如需接收所有消息：
1. @BotFather → `/setprivacy` → 选「Disable」

## 群组配置

```yaml
channels:
  telegram:
    groups:
      allowedIds:
        - -1001234567890  # 群组ID
```

## 常见问题

**Q: 消息收不到？**
- 检查botToken是否正确
- 确认已设置Webhook
- 检查privacy模式

**Q: 如何获取Chat ID？**
- 将Bot拉入群组
- 发送消息
- 访问：`https://api.telegram.org/bot<TOKEN>/getUpdates`

---

*来源：openclawx.cloud/en/channels/telegram*

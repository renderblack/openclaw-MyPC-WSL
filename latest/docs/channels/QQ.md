# OpenClaw 渠道配置 · QQ

## 官方插件

```bash
npm install -g @openclaw/openclaw-qqbot
```

## 版本

当前稳定版：v2.x

## 前提条件

1. QQ开放平台账号
2. 创建的应用AppID和AppSecret
3. 频道机器人权限

## QQ开放平台申请

1. 登录 https://q.qq.com
2. 创建应用 → 选择「机器人」
3. 填写应用信息
4. 申请权限：
   - 消息收发
   - 频道管理
   - 群管理
   - 成员管理

## 配置

```yaml
channels:
  qqbot:
    enabled: true
    appId: "1234567890"
    appSecret: "your-app-secret"
    # 生产环境
    sandbox: false
    # WSS连接地址
    gateway: "wss://api.sgroup.qq.com"
```

## 机器人权限一览

| 权限 | 说明 |
|------|------|
| READ_MESSAGE | 读取消息 |
| SEND_MESSAGE | 发送消息 |
| MANAGE_MESSAGES | 管理消息 |
| SPEAK | 在语音频道发言 |
| MOVE_USER | 移动用户 |

## 频道相关配置

```yaml
channels:
  qqbot:
    intents:
      - GUILDS
      - GUILD_MESSAGES
      - DIRECT_MESSAGE
      - MESSAGE_AUDIT
```

## 消息格式

QQ机器人支持的消息类型：
- 文本消息
- 图片消息（URL或Base64）
- @提及
- 引用回复
- 卡片消息（Ark/Embed）

## 频道操作

```javascript
// 使用skill中的工具
// 创建频道
POST /guilds/{guild_id}/channels

// 创建子频道
PUT /channels/{channel_id}/threads

// 发送消息
POST /channels/{channel_id}/messages
```

## 常见问题

**Q: WSS连接失败？**
- 检查appId和appSecret
- 确认已申请正确权限
- 检查服务器防火墙

**Q: 消息收不到？**
- 确认机器人已加入频道
- 检查 intents 配置
- 查看日志确认连接状态

**Q: 如何获取guild_id？**
- 开发者模式开启后，右键频道名称可见ID

---

*来源：QQ开放平台官方文档 + 插件内置文档*

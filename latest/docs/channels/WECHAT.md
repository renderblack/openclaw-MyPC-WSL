# OpenClaw 渠道配置 · 微信（WeChat）

## 官方插件

```bash
npm install -g @tencent-weixin/openclaw-weixin
```

## 版本说明

| 版本 | 说明 |
|------|------|
| v2.1.7 | 当前稳定版，支持被动消息 |
| v2.0.x | 仅支持主动推送 |

## 前提条件

1. 微信公众号/企业微信
2. 公网可达的Webhook服务器
3. 开发者ID（AppID和AppSecret）

## 微信公众平台配置

1. 登录微信公众平台：https://mp.weixin.qq.com
2. 设置 → 公众密码（获取AppSecret）
3. 基本配置 → 修改EncodingAESKey
4. 开发 → 基本配置
   - URL：设置为你的Webhook地址
   - Token：设置验证Token
   - EncodingAESKey：消息加密密钥

## 企业微信配置

1. 登录企业微信管理后台
2. 应用管理 → 创建应用
3. 获取AgentId和Secret
4. 配置可信IP（你的服务器IP）

## 配置

```yaml
channels:
  wechat:
    enabled: true
    type: public  # public | work
    # 公众号配置
    appId: "wx1234567890abcdef"
    appSecret: "your-appsecret"
    token: "your-token"
    encodingAesKey: "your-aes-key"
    # 或企业微信配置
    # agentId: "1000001"
    # corpId: "ww1234567890abcdef"
    # agentSecret: "your-agent-secret"
```

## Webhook地址格式

```
https://your-domain.com/wechat/webhook
```

## 被动消息接收

微信服务器会在用户发消息时POST到你的Webhook：

```javascript
// Express示例
app.post('/wechat/webhook', (req, res) => {
  const { FromUserName, Content, MsgType } = req.body;
  
  // 处理不同消息类型
  switch(MsgType) {
    case 'text':
      // 文本消息
      break;
    case 'image':
      // 图片消息
      break;
    case 'event':
      // 事件（关注/取消等）
      break;
  }
  
  // 返回空字符串表示成功
  res.send('');
});
```

## 主动消息限制

| 账号类型 | 主动发送限制 |
|---------|-------------|
| 订阅号 | 48小时内只能回复 |
| 服务号 | 48小时内只能回复 |
| 企业微信 | 可主动发送，但需审批 |

## 常见问题

**Q: 消息收不到？**
- 确认公网Webhook可达
- 检查Token和EncodingAESKey配置
- 查看日志确认请求到达

**Q: 如何获取用户OpenID？**
- 通过消息中的FromUserName字段

**Q: 如何发送模板消息？**
```javascript
// 调用发送模板消息API
const templateId = 'template_id';
const data = { ... };
// 使用message工具发送
```

---

*来源：openclawx.cloud/en/channels（微信官方文档页面）*

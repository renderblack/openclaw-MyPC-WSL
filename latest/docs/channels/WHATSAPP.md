# OpenClaw 渠道配置 · WhatsApp

## 前提条件

1. WhatsApp Business API账号
2. Business Phone Number
3. Webhook URL（公网可达）

## WhatsApp Business API

两种方式：

### 方式1：Meta Business API（官方）

1. 创建Meta Business账户
2. 创建WhatsApp Business应用
3. 获取Phone Number ID和Access Token
4. 配置Webhook

### 方式2：第三方服务商

通过Twilio等服务商接入（更简单）

```yaml
channels:
  whatsapp:
    enabled: true
    provider: twilio
    accountSid: "AC..."
    authToken: "xxx"
    fromNumber: "+1234567890"
```

## 配置

```yaml
channels:
  whatsapp:
    enabled: true
    phoneNumber: "+1234567890"
    phoneNumberId: "123456789"
    accessToken: "EAAB..."
    webhookVerifyToken: "your-verify-token"
    # Webhook配置
    webhook:
      path: /whatsapp
      verify: GET      # Webhook验证
      receive: POST    # 消息接收
```

## 消息模板

WhatsApp需要预先审批的消息模板（Template）才能主动发送：

```yaml
templates:
  greeting:
    name: hello_world
    language: zh_CN
    components:
      - type: body
        text: "你好，{{1}}！"
```

## 接收消息

WhatsApp通过Webhook接收消息，需要公网可达地址：

```bash
# 验证脚本示例
const express = require('express');
const app = express();

app.get('/webhook', (req, res) => {
  const mode = req.query['hub.mode'];
  const token = req.query['hub.verify_token'];
  const challenge = req.query['hub.challenge'];
  
  if (mode === 'subscribe' && token === VERIFY_TOKEN) {
    return res.status(200).send(challenge);
  }
  res.sendStatus(403);
});

app.post('/webhook', (req, res) => {
  // 处理消息
});
```

## 限制

| 类型 | 限制 |
|------|------|
| 消息模板 | 需预审批 |
| 主动发送 | 24小时内仅能回复 |
| 速率 | 遵守WhatsApp政策 |

---

*来源：openclawx.cloud/en/channels/whatsapp*

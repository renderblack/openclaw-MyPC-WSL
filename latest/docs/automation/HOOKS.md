# OpenClaw 自动化 · Hooks（钩子）

## 什么是Hooks

Hooks是OpenClaw的事件触发机制，在特定事件发生时自动执行预设任务。

```
事件发生 → 检查Hook规则 → 匹配则触发 → 执行任务
```

## 钩子类型

| 事件 | 说明 | 用途 |
|------|------|------|
| `session.start` | 会话开始时 | 初始化上下文 |
| `session.end` | 会话结束时 | 保存会话摘要 |
| `message.received` | 收到消息时 | 消息预处理 |
| `message.sent` | 发送消息时 | 发送后处理 |
| `tool.before` | 工具执行前 | 参数验证 |
| `tool.after` | 工具执行后 | 结果处理 |
| `cron.before` | Cron任务执行前 | 准备环境 |
| `cron.after` | Cron任务执行后 | 记录结果 |
| `error` | 发生错误时 | 错误通知 |

## 配置

```yaml
hooks:
  - event: session.end
    action: save_summary
  - event: message.received
    action: auto_translate
  - event: error
    action: notify_admin
```

## 内置Actions

```yaml
actions:
  save_summary:
    type: memory
    path: "memory/sessions/{date}/{session_id}.md"
    
  notify_admin:
    type: message
    channel: telegram
    target: "@admin"
    template: "Error: {error_message}"
    
  log_session:
    type: file
    path: "/tmp/openclaw/sessions.log"
    format: json
```

## 自定义Hook脚本

```yaml
hooks:
  - event: message.received
    script: /path/to/hook.js
```

```javascript
// hook.js 示例
module.exports = async (event, context) => {
  const { message, session } = event;
  
  // 消息预处理
  if (message.content.includes('!')) {
    message.content = message.content.replace('!', '');
    return { modified: true, message };
  }
  
  return { modified: false };
};
```

## 使用场景

### 1. 会话摘要自动保存

```yaml
- event: session.end
  action: save_summary
  config:
    path: "memory/sessions/{date}/{session_id}.md"
    includeMessages: true
    maxTokens: 5000
```

### 2. 敏感词过滤

```yaml
- event: message.received
  script: /scripts/filter_sensitive.js
  config:
    blockWords: ['password', 'secret']
    replaceWith: '***'
```

### 3. 错误自动通知

```yaml
- event: error
  action: notify_admin
  config:
    channel: telegram
    level: [error, critical]
```

### 4. Token消耗统计

```yaml
- event: session.end
  action: log_token_usage
  config:
    path: "/tmp/openclaw/token_usage.log"
```

---

*来源：openclawx.cloud/en/automation/hooks*

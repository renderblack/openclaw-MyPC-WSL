# OpenClaw 高级用户指南

## 进阶技巧

### 1. 多模型组合策略

```yaml
agents:
  defaults:
    model: minimax/MiniMax-M2.7
  modes:
    fast:
      model: minimax/MiniMax-M2.7-highspeed
    coding:
      model: anthropic/claude-3-7-sonnet
    long-context:
      model: openai/gpt-4o
```

**使用**：在对话中指定模式
```
@fast 请快速总结这个文档
@coding 帮我审查这段代码
@long-context 分析这份100页的合同
```

### 2. 链式工具调用

```javascript
// 场景：用户说"帮我分析这个网站"
//
// 执行流程：
// 1. browser抓取网页
browser({ action: "navigate", url: "https://example.com" })
// 2. AI分析内容
// 3. exec生成报告
// 4. message推送到微信
```

### 3. 子Agent任务分解

```javascript
// 复杂任务分解
sessions_spawn({
  task: "并行研究三个主题",
  mode: "run"
})
// 主Agent等待结果，统一汇总
```

### 4. 上下文预加载

```yaml
# 在SKILL.md中指定预加载
context:
  preload:
    - memory/long-term/MEMORY.md
    - memory/projects/current.md
```

### 5. 动态系统提示词

```yaml
# 根据渠道切换不同system prompt
agents:
  channelPrompts:
    telegram:
      - "你是一个Telegram助手"
      - "使用简洁的语言"
    wechat:
      - "你是一个微信助手"
      - "使用表情符号"
```

## 高级配置

### 1. 模型温度微调

```yaml
agents:
  defaults:
    temperature: 0.7
  modeConfigs:
    creative:
      temperature: 1.0
    precise:
      temperature: 0.3
```

### 2. 工具并行控制

```yaml
tools:
  exec:
    maxParallel: 3  # 最多3个并行
    queueSize: 10   # 队列大小
```

### 3. 自定义工具

```javascript
// 在skill中定义工具
tools:
  - name: my_tool
    type: exec
    command: "python3 /path/to/script.py"
    timeout: 60
```

### 4. 记忆自动摘要

```yaml
memory:
  autoSummarize:
    enabled: true
    threshold: 50000  # token超过50k时触发
    output: memory/summaries/{date}.md
```

## 工作流自动化

### 1. 事件触发工作流

```yaml
workflows:
  - name: "网站监控"
    trigger:
      type: cron
      schedule: "*/15 * * * *"
    steps:
      - browser:
          action: navigate
          url: "https://example.com"
      - evaluate:
          script: "document.body.innerText.includes('Out of Stock')"
      - message:
          channel: telegram
          if: "result == true"
          message: "库存变化！"
```

### 2. 审批工作流

```yaml
workflows:
  - name: "敏感操作审批"
    trigger:
      type: tool
      tool: "exec"
      pattern: "rm -rf|drop table"
    steps:
      - wait:
          channel: telegram
          timeout: 300
      - if:
          approved: true
          then:
            - continue
          else:
            - block
```

### 3. 数据处理流水线

```
用户上传CSV
    ↓
exec解析CSV
    ↓
AI分析数据
    ↓
生成图表
    ↓
推送到邮箱
```

## 性能调优

### 1. 会话池管理

```yaml
sessions:
  pool:
    maxActive: 50
    idleTimeout: 3600
    maxLifetime: 86400
```

### 2. 缓存策略

```yaml
cache:
  enabled: true
  ttl: 3600
  maxSize: 100
```

### 3. 日志优化

```yaml
logging:
  level: warn  # 生产环境用warn
  maxSize: 5m
  maxFiles: 3
```

## 安全加固

### 1. 工具权限细粒度控制

```yaml
tools:
  exec:
    allowedCommands:
      - git
      - npm
      - docker
    deniedPatterns:
      - "curl.*sh"
      - "wget.*sh"
```

### 2. 敏感操作二次确认

```yaml
security:
  confirmActions:
    - exec
    - file_write
    - message_broadcast
```

### 3. 审计日志

```yaml
logging:
  audit:
    enabled: true
    path: /var/log/openclaw/audit.log
    events:
      - login
      - tool_exec
      - config_change
```

## 集成扩展

### 1. Webhook集成

```yaml
webhooks:
  - name: "GitHub Webhook"
    url: "https://openclaw.example.com/webhook/github"
    events:
      - push
      - pull_request
```

### 2. API集成

```yaml
apis:
  - name: "Slack"
    type: slack
    webhookUrl: "https://hooks.slack.com/..."
```

### 3. 数据库连接

```yaml
databases:
  - name: "main"
    type: postgresql
    connection: "postgresql://user:pass@host/db"
```

---

*来源：openclawx.cloud 高级文档 + 实战经验*

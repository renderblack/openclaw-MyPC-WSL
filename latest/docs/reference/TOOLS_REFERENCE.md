# OpenClaw 工具参考

## 内置工具一览

| 工具 | 功能 | 风险 |
|------|------|------|
| `exec` | 在主机执行命令 | 🔴 高 |
| `browser` | 无头浏览器自动化 | 🟡 中 |
| `message` | 跨渠道消息发送 | 🟢 低 |
| `session_*` | 会话管理 | 🟢 低 |
| `subagents` | 子Agent管理 | 🟡 中 |
| `canvas` | Web UI控制 | 🟡 中 |
| `pdf` | PDF分析 | 🟢 低 |
| `image` | 图片分析 | 🟢 低 |
| `music_generate` | 音乐生成 | 🟢 低 |
| `video_generate` | 视频生成 | 🟢 低 |
| `tts` | 文字转语音 | 🟢 低 |

---

## exec（命令执行）

**功能**：在主机上执行shell命令。

```javascript
// 调用格式
exec({
  command: "ls -la",
  timeout: 30,        // 超时秒数
  workdir: "/home/xiong",
  env: { KEY: "value" }
})
```

### 参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| command | string | ✅ | 要执行的命令 |
| timeout | number | ❌ | 超时秒数，默认30 |
| workdir | string | ❌ | 工作目录 |
| env | object | ❌ | 环境变量 |

### 安全建议

```yaml
tools:
  exec:
    allowlist:
      - git
      - npm
      - node
      - docker
    deny:
      - "rm -rf /"
      - "dd if="
```

### 常见错误

| 错误 | 原因 | 解决 |
|------|------|------|
| Permission denied | 权限不足 | 检查命令权限 |
| Command not found | 命令不存在 | 检查PATH |
| Timeout | 执行超时 | 增加timeout |

---

## browser（浏览器自动化）

**功能**：无头浏览器控制，可抓取网页、操作UI。

```javascript
// 调用格式
browser({
  action: "goto",       // navigate | snapshot | evaluate | submit
  url: "https://example.com",
  screenshot: true
})
```

### 参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| action | string | ✅ | 操作类型 |
| url | string | 条件 | 目标URL（navigate时） |
| script | string | 条件 | JS脚本（evaluate时） |
| selector | string | 条件 | 元素选择器 |

### 操作类型

```javascript
// 导航
browser({ action: "navigate", url: "https://..." })

// 截图
browser({ action: "screenshot", fullPage: true })

// 执行脚本
browser({ action: "evaluate", script: "document.title" })

// 点击元素
browser({ action: "click", selector: "#submit-btn" })

// 填写表单
browser({ action: "fill", selector: "#email", text: "test@example.com" })
```

### 安装

```bash
# Linux/macOS
agent-browser install --with-deps

# WSL2
agent-browser install --with-deps
```

---

## message（消息发送）

**功能**：跨渠道发送消息。

```javascript
// 调用格式
message({
  action: "send",
  channel: "telegram",
  target: "@username",
  message: "Hello!"
})
```

### 参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| action | string | ✅ | send/broadcast |
| channel | string | ✅ | 渠道名称 |
| target | string | 条件 | 目标用户/频道 |
| message | string | ✅ | 消息内容 |

### 示例

```javascript
// 发送文本
message({
  action: "send",
  channel: "telegram",
  target: "@username",
  message: "Hello from OpenClaw!"
})

// 发送图片
message({
  action: "send",
  channel: "telegram",
  target: "@username",
  message: "Check this out!",
  media: "/path/to/image.png"
})

// 广播
message({
  action: "broadcast",
  channel: "telegram",
  message: "Announcement to all!"
})
```

---

## session_*（会话管理）

### sessions_list

```javascript
sessions_list({ limit: 10, activeMinutes: 60 })
```

### sessions_history

```javascript
sessions_history({ sessionKey: "xxx", limit: 50 })
```

### sessions_send

```javascript
sessions_send({ sessionKey: "xxx", message: "Hello!" })
```

### sessions_spawn

```javascript
sessions_spawn({
  task: "分析数据",
  mode: "run",          // run | session
  runtime: "subagent"
})
```

### sessions_yield

```javascript
sessions_yield({ message: "任务完成" })
```

---

## subagents（子Agent）

### subagents list

```javascript
subagents({ action: "list", recentMinutes: 30 })
```

### subagents kill

```javascript
subagents({ action: "kill", target: "agent-id" })
```

### subagents steer

```javascript
subagents({ action: "steer", target: "agent-id", message: "调整方向" })
```

---

## canvas（Web控制）

```javascript
// 截图
canvas({ action: "snapshot", target: "https://example.com" })

// 执行JS
canvas({ action: "eval", target: "https://example.com", javaScript: "alert(1)" })
```

---

## pdf（PDF分析）

```javascript
// 单个PDF
pdf({ pdf: "/path/to/file.pdf", prompt: "提取所有文本" })

// 多个PDF
pdfs({ pdfs: ["/path/a.pdf", "/path/b.pdf"], prompt: "对比分析" })
```

---

## image（图片分析）

```javascript
// 单张图片
image({ image: "/path/to/image.png", prompt: "描述图片内容" })

// 多张图片
images({ images: ["/path/a.png", "/path/b.png"], prompt: "对比两张图" })
```

---

## tts（文字转语音）

```javascript
tts({ text: "你好，这是语音播报", channel: "telegram" })
```

---

*来源：openclawx.cloud/en/tools + 官方文档综合*

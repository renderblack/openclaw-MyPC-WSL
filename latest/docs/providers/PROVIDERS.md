# OpenClaw Provider（AI模型提供商）配置

## 支持的提供商

| 提供商 | 状态 | 模型 | 官网 |
|--------|------|------|------|
| **MiniMax** | ✅ 默认 | MiniMax-M2.7, M2.7-highspeed | minimax.io |
| **Anthropic** | ✅ | Claude 3.5/3.7 Sonnet | anthropic.com |
| **OpenAI** | ✅ | GPT-4o, GPT-4o-mini, o3 | openai.com |
| **Google** | ✅ | Gemini 2.0/2.5 Pro | deepmind.google |
| **Ollama** | 🔶 | 本地模型 | ollama.ai |

---

## MiniMax（默认）

```yaml
providers:
  minimax:
    apiKey: "your-minimax-api-key"
    apiBase: "https://api.minimax.chat/v"  # 默认
    # 模型配置
    models:
      default: MiniMax-M2.7
      highspeed: MiniMax-M2.7-highspeed
```

### 可用模型

| 模型 | 上下文 | 适用场景 |
|------|--------|---------|
| MiniMax-M2.7 | 200k | 通用对话，默认 |
| MiniMax-M2.7-highspeed | 200k | 快速响应场景 |

---

## Anthropic

```yaml
providers:
  anthropic:
    apiKey: "sk-ant-..."
    # 可选
    apiBase: "https://api.anthropic.com/v1"
    # 模型配置
    models:
      default: claude-3-7-sonnet-20250620
      Sonnet: claude-3-5-sonnet-20250620
```

### 可用模型

| 模型 | 上下文 | 特点 |
|------|--------|------|
| Claude 3.7 Sonnet | 200k | 最新强模型，代码能力强 |
| Claude 3.5 Sonnet | 200k | 性价比高 |

---

## OpenAI

```yaml
providers:
  openai:
    apiKey: "sk-..."
    # 可选
    apiBase: "https://api.openai.com/v1"
    organization: "org-xxx"  # 可选
    models:
      default: gpt-4o
      fast: gpt-4o-mini
```

### 可用模型

| 模型 | 上下文 | 特点 |
|------|--------|------|
| GPT-4o | 128k | 强模型，多模态 |
| GPT-4o-mini | 128k | 快速，便宜 |
| o3 | 200k | 最新推理模型 |

---

## Google Gemini

```yaml
providers:
  google:
    apiKey: "your-google-api-key"
    apiBase: "https://generativelanguage.googleapis.com/v1beta"
    models:
      default: gemini-2.0-pro
      flash: gemini-2.0-flash
```

---

## Ollama（本地）

```yaml
providers:
  ollama:
    apiBase: "http://localhost:11434/v1"
    apiKey: "ollama"  # 占位符
    models:
      default: llama3
```

**注意**：Ollama需要本地安装并启动。

```bash
# 安装Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# 拉取模型
ollama pull llama3

# 启动服务
ollama serve
```

---

## 模型选择策略

| 场景 | 推荐模型 | 原因 |
|------|---------|------|
| 日常对话 | MiniMax-M2.7 | 性价比高 |
| 快速问答 | MiniMax-M2.7-highspeed | 延迟低 |
| 代码任务 | Claude 3.7 Sonnet | 代码能力强 |
| 长文档分析 | GPT-4o / Claude 3.7 | 上下文大 |
| 预算敏感 | GPT-4o-mini | 成本低 |

---

## API Key安全

```bash
# 不要明文写在配置里
# 使用环境变量
export MINIMAX_API_KEY="your-key"

# 或使用密钥管理服务
```

---

*来源：openclawx.cloud/en/providers + 官方文档综合*

# OpenClaw养虾经验：10个效率翻倍的技巧

来源：https://mp.weixin.qq.com/s/bO-Tq4w5YG5jrayzzyJTAA
作者：开发者阿橙（OpenClaw创业实战营发起人）
抓取日期：2026-04-09

---

## 10个技巧摘要

### 1. CLI 命令
- `openclaw onboard` — 重新运行入门引导
- `openclaw tui` — 启动终端UI
- `openclaw dashboard` — 启动仪表板
- `openclaw models list/set` — 切换模型
- `openclaw gateway status/stop/start/restart` — 网关管理
- `openclaw security audit --deep` — 安全审计

### 2. Cron 和工作流自动化
- 触发方式：定时任务、Webhook、消息触发、系统事件
- 案例：每日新闻汇总、代码审查自动化、依赖项监控、错误检测

### 3. Perplexity 网页搜索
- 配置 OpenRouter API + Perplexity Sonar
- 比 Brave Search 更强

### 4. Nano Banana 2 图片生成
- `npm i -g clawdhub`
- `clawdhub install nano-banana-pro`
- 使用 gemini-3.1-flash-image-preview 模型

### 5. 语音播放
- Edge TTS 中文语音
- zh-CN-XiaoxiaoNeural / zh-CN-YunxiNeural

### 6. 第二大脑
- 核心理念：记笔记像发短信一样简单，找起来像搜索一样方便
- GitHub: awesome-openclaw-usecases

### 7. MCP 服务器
- Apify MCP 抓取实时数据
- GitHub: Awesome-MCP-Servers

### 8. 仪表板
- 管理 Cron 任务、查看 token 用量

### 9. 子 agent
- 不同角色的 agent（CEO、秘书等）

### 10. 自定义 SKILL.md
- 大模型写 Markdown + Python 脚本

---

## 安全建议
- 默认把 OpenClaw 设为私有
- 从低风险、只读自动化开始
- 别随意装 ClawHub 技能
- 定期跑审计

---

## GitHub 资源
- https://github.com/hesamsheikh/awesome-openclaw-usecases
- https://github.com/awesome-mcp-servers/Awesome-MCP-Servers

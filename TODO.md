# TODO.md - 待办事项列表

---

## 🎯 技能配置板块

### ✅ 已配置技能（直接可用）

| 技能 | 状态 | 说明 |
|------|------|------|
| **天气查询** | ✅ 已配置 | `weather` skill，wttr.in 数据源 |
| **OCR 文字识别** | ✅ 已配置 | Tesseract Windows 版，支持中文 PDF/图片 |
| **文件搜索** | ✅ 已配置 | `hybrid-search.ps1`，Everything + ripgrep |
| **系统诊断** | ✅ 已配置 | `healthcheck` / `node-connect` skill |
| **记忆系统** | ✅ 已配置 | `memory/` 日志 + MEMORY.md 长期记忆 |

### 🔧 媒体生成（内置工具）

| 能力 | 状态 | 说明 |
|------|------|------|
| **图片生成** | ✅ 可用 | `image_generate` 工具 |
| **视频生成** | ✅ 可用 | `video_generate` 工具 |
| **音乐生成** | ✅ 可用 | `music_generate` 工具 |
| **语音合成** | ✅ 可用 | `tts` 工具 |
| **PDF 读取** | ✅ 可用 | `pdf` 工具 |

### 📦 平台集成（可选）

| 技能 | 优先级 | 说明 |
|------|--------|------|
| **GitHub** | 🟡 中 | `github` skill，自动化操作 |
| **Notion** | 🟡 中 | `notion` skill，笔记同步 |
| **Obsidian** | 🟡 中 | `obsidian` skill，笔记同步 |
| **Discord** | 🟢 低 | `discord` skill，消息推送 |
| **Slack** | 🟢 低 | `slack` skill，消息推送 |

### 🔬 高级能力（可选）

| 技能 | 优先级 | 说明 |
|------|--------|------|
| **语音转文字** | 🟢 低 | `openai-whisper`，音频转文本 |
| **视频帧提取** | 🟢 低 | `video-frames`，分析视频内容 |
| **Tailscale 远程访问** | 🟡 中 | 外网安全访问 Gateway |

### 🦐 养虾经验可试试

| 技巧 | 优先级 | 说明 |
|------|--------|------|
| **第二大脑** | 🟡 中 | 笔记像发短信，找资料像搜索，参考 `awesome-openclaw-usecases` |
| **MCP 服务器** | 🟡 中 | Apify MCP 抓取实时数据（新闻/房产等），参考 `Awesome-MCP-Servers` |
| **Perplexity 搜索** | 🟢 低 | 比 web_search 更强，需 API Key |
| **ClawdHub CLI** | 🟢 低 | 一键安装 GitHub 技能：`npm i -g clawdhub` |
| **Dashboard 仪表板** | 🟢 低 | `openclaw dashboard` 可视化管理 |
| **安全审计** | 🟢 低 | `openclaw security audit --deep` 定期检查 |

---

## 系统配置

### 🔴 高优先级（均已解决）

- [x] **plugins.allow 白名单** — ✅ 已配置 `["openclaw-weixin", "minimax"]`
- [x] **systemd 开机服务** — ✅ 已用 Windows 计划任务代替，无需 systemd

### 🟢 已省略（不需要）

- [ ] **安全审计** — 评估后认为当前风险可接受，暂不执行
- [ ] **图片识别能力** — 评估后认为当前纯文本模型足够，暂不配置

### 🟡 中优先级

- [ ] **Tailscale 远程访问** — 让外网设备安全访问 Gateway（可选方案）

### 🟢 低优先级

- [ ] **gateway.trustedProxies** — 如使用反向代理（Nginx/Caddy）才需要
- [ ] **Heartbeat 周期** — 当前默认 30 分钟，可按需调整
- [ ] **Cron 定时任务** — 按需配置定期检查/提醒

---

## ✅ 已完成

- [x] GitHub 仓库新建并同步（openclaw-MyPC-WSL）
- [x] 本地备份配置
- [x] 微信插件连接修复（Gateway 完整重启）
- [x] plugins.allow 白名单配置
- [x] Gateway 开机自启（Windows 计划任务）
- [x] ClawLibrary 部署 + 开机自启
- [x] OCR 能力配置（Tesseract Windows 版）
- [x] 文件搜索能力配置（hybrid-search.ps1）

---

## WSL2 环境说明

- 宿主机：Windows 10 + WSL2 Ubuntu
- OpenClaw：npm 全局安装 v2026.4.9
- Gateway：127.0.0.1:18790（本地回环）
- 微信插件：openclaw-weixin v2.1.7，已连接

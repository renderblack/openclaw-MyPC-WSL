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
| **Summarize** | ✅ 已配置 | 内容总结技能 |
| **Skill-Vetter** | ✅ 已配置 | 安全审计，安装前检查恶意代码 |
| **Agent Browser** | ✅ 已配置 | `agent-browser-clawdbot`，浏览器自动化 |
| **Tavily 搜索** | ✅ 已配置 | `openclaw-tavily-search`，AI专用搜索引擎 |
| **Find-Skills** | ✅ 已配置 | `find-skills-skill`，自动发现相关技能 |
| **Proactive Agent** | ✅ 已配置 | 主动提醒，变被动为主动 |
| **Humanizer** | ✅ 已配置 | 输出更人性化 |

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
| **Self-Improving** | 🟡 中 | 让龙虾记住错误、持续进化（类似 `.learnings/` 系统） |
| **Perplexity 搜索** | 🟢 低 | 比 web_search 更强，需 API Key |
| **Dashboard 仪表板** | 🟢 低 | `openclaw dashboard` 可视化管理 |
| **安全审计** | 🟢 低 | `openclaw security audit --deep` 定期检查 |

---

## 系统配置

### 🔴 高优先级（均已解决）

- [x] **plugins.allow 白名单** — ✅ 已配置 `["openclaw-weixin", "minimax"]`
- [x] **systemd 开机服务** — ✅ 已用 Windows 计划任务代替，无需 systemd

### 🟢 已省略（不需要）

- [ ] **图片识别能力** — 评估后认为当前纯文本模型足够，暂不配置

### 🟡 中优先级

- [ ] **Tailscale 远程访问** — 让外网设备安全访问 Gateway（可选方案）

### 🟢 低优先级

- [ ] **gateway.trustedProxies** — 如使用反向代理（Nginx/Caddy）才需要
- [ ] **Heartbeat 周期** — 当前默认 30 分钟，可按需调整
- [ ] **Cron 定时任务** — 按需配置定期检查/提醒

---

## 🎯 三维重建实战项目

**目标**：获取最新3DGS开源项目，在本地搭建环境并实现三维重建

### 阶段一：市场调研（1-2天）
- [ ] 搜索 GitHub trending，找出近3个月活跃的3DGS项目
- [ ] 对比主流项目特点，选出最适合入门的
- [ ] 整理到 `learn/3d-reconstruction/projects-compare.md`

**候选项目**：
- gaussian-splatting（原版）
- gaustudio（模块化）
- supersplat（浏览器编辑器）

### 阶段二：环境搭建（2-3天）
- [ ] 检查 GPU 型号、显存、CUDA 版本
- [ ] 安装/更新 CUDA + cuDNN
- [ ] 创建 Python 虚拟环境
- [ ] 安装项目依赖
- [ ] 下载测试数据集

### 阶段三：部署测试（3-5天）
- [ ] 运行官方 Demo，确保输出正常
- [ ] 用自己的测试图像进行重建
- [ ] 导出结果（点云/mesh）
- [ ] 记录完整流程到文档

### 关键里程碑
- [ ] Milestone 1：选定项目，整理对比文档
- [ ] Milestone 2：环境搭建完成
- [ ] Milestone 3：Demo 运行成功
- [ ] Milestone 4：自己的图像重建成功

**参考文档**：`learn/3d-reconstruction/README.md`

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
- [x] ClawdHub CLI 安装 + 登录
- [x] 养虾经验九大必备技能安装（Skill-Vetter、Agent Browser、Tavily、Find-Skills、Proactive Agent、Humanizer）

---

## WSL2 环境说明

- 宿主机：Windows 10 + WSL2 Ubuntu
- OpenClaw：npm 全局安装 v2026.4.9
- Gateway：127.0.0.1:18790（本地回环）
- 微信插件：openclaw-weixin v2.1.7，已连接
- 已安装技能：160+

---

## 📚 3D图像重建学习板块

**路径**：`learn/3d-reconstruction/README.md`

**计划周期**：12周系统性学习

### 学习阶段
| 阶段 | 周数 | 内容 | 状态 |
|------|------|------|------|
| 理论基础 | 1-3周 | NeRF → 3DGS 原理 | ⬜ |
| 工具掌握 | 4-6周 | 环境搭建 + gaustudio | ⬜ |
| 进阶应用 | 7-9周 | SuGaR + 编辑器 | ⬜ |
| 前沿探索 | 10-12周 | 最新论文 + 项目实战 | ⬜ |

### Week 1 任务（NeRF入门）
- [ ] 精读 NeRF 论文
- [ ] 理解 MLP 隐式表示
- [ ] 理解体素渲染原理

### 工具链
- gaustudio（训练框架）
- supersplat（编辑器）
- COLMAP（数据预处理）

### GitHub 资源
- awesome-3D-gaussian-splatting ⭐8488
- supersplat ⭐4107
- gaustudio ⭐1735

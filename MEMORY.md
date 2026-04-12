# MEMORY.md - 长期记忆

## 基本信息
- **创建日期**: 2026-04-09
- **创建原因**: WSL2 环境首次配置
- **最后更新**: 2026-04-12

---

## 系统环境

### 硬件配置
- **CPU**: Intel Core i7-9700KF @ 3.60GHz (8 核 8 线程)
- **内存**: 25Gi (约 23Gi 可用)
- **主机名**: xiong
- **磁盘**: 233GB 可用 / 251GB 总计

### 软件环境
- **操作系统**: WSL2 Ubuntu (Linux 5.10.16.3-microsoft-standard-WSL2)
- **Node**: v22.22.2
- **OpenClaw 版本**: 2026.4.11
- **工作空间**: `/home/xiong/.openclaw/workspace`
- **代理配置**: `http://127.0.0.1:7890` (Clash 代理)

### 工具链状态
| 工具 | 版本 | 状态 |
|------|------|------|
| Node.js | v22.22.2 | ✅ |
| npm | 10.9.7 | ✅ |
| Git | 2.37.1 | ✅ |
| curl | 7.81.0 | ✅ |

---

## AI 模型配置

- **主模型**: `minimax/MiniMax-M2.7` (上下文 200k)
- **备用**: `minimax/MiniMax-M2.7-highspeed`

---

## 已安装技能

- weather
- summarize
- find-skills
- (其他技能待补充)

---

## GitHub 仓库

- **仓库**: https://github.com/renderblack/openclaw-MyPC-WSL
- **Token**: 已配置

---

## 已知问题

### OpenClaw CLI pairing required 故障
- **问题**：`openclaw cron list/add` 等 CLI 命令报错 `gateway closed (1008): pairing required`，但 Gateway RPC probe 正常
- **根因**：`~/.openclaw/devices/pending.json` 中有 repair 请求卡在待批准状态，阻止所有写操作
- **排查流程**：
  1. `cat ~/.openclaw/devices/pending.json` 查看待批准请求
  2. 手动批准或从 pending.json 删除该请求
  3. `openclaw gateway --force` 重启
- **关键文件**：pending.json（待批准）/ paired.json（已批准）/ jobs.json（定时任务）
- **经验**：CLI 超时 ≠ 失败，重启后可能恢复；直接修改设备文件是绕过 CLI 的备选方案

### music_generate 工具 Bug
- **问题**: 使用内置 `music_generate` 工具时 Gateway 崩溃
- **建议**: 暂不使用，等官方修复

---

## 完成项目日志

| 日期 | 项目 |
|------|------|
| 2026-04-09 | WSL2 OpenClaw 安装配置完成 |
| 2026-04-09 | GitHub 仓库新建并同步 (openclaw-MyPC-WSL) |
| 2026-04-09 | 微信插件连接修复 |

---

## 经验总结

### OpenClaw 配对机制（2026-04-10）
- **pairing required ≠ token 失效**：Gateway 有独立的配对机制，设备状态存在 `~/.openclaw/devices/`
- **CLI vs API 工具**：cron 工具（API）受 pairing 影响；openclaw cron CLI 需要 pairing 正常才能操作
- **CLI 超时**：不代表失败，有时重启后自动恢复
- **备选方案**：直接修改 `~/.openclaw/devices/paired.json` 可绕过 CLI

### Gateway 重启（2026-04-09）
- WSL2 环境下不要用 `openclaw gateway restart`（依赖 systemd）
- 正确方式：`openclaw gateway --force`
- 热重载（SIGUSR1）不会重新启动插件的 startAccount，必须完整重启

### Git 操作（2026-04-09）
- Token 认证：`https://ghp_xxx@github.com/...`
- 远程有内容时先 pull --rebase 再 push

### ⚠️ Git 仓库环境混淆教训（2026-04-09）

**问题**：WSL2 workspace 绑定了 Windows 的 Git 仓库，导致 Windows 配置文件覆盖了 WSL2 配置。

**原因**：
1. WSL2 workspace 最初绑定了 `openclaw-MyPC`（Windows 仓库）
2. 执行 `git reset --hard origin/master` 把 Windows 文件全部拉下来
3. 后来建了新仓库 `openclaw-MyPC-WSL`，但 Windows 文件已存在于历史

**教训**：
- 不同环境（Windows / WSL2）应该用**不同的仓库**
- 建新仓库前先确认 remote 是否对应正确的环境
- 或者新建仓库时先 `rm -rf .git` 清理干净再 init

---

## OCR 文字识别

**工具**：Tesseract OCR（Windows 版）
- 路径：`C:\Program Files\Tesseract-OCR\tesseract.exe`
- 中文模型：`chi_sim.traineddata`
- 依赖：GhostScript（已安装，用于 PDF 转图片）

**用途**：
- 识别 PDF 扫描件
- 识别图片中的文字
- 合同、文档关键信息提取

**工作流程**：
1. `gs` → PDF 转 JPG 图片
2. `tesseract` → OCR 识别中文
3. 输出纯文本

**验证**：成功识别智慧梁场演示动画制作合同（93240元）

## OpenClaw 文档知识库（2026-04-10）

### 知识库路径
~/openclaw-docs/latest/

### 知识库结构
- INDEX.md — 全局索引
- FINAL_REPORT.md — 完整深度研究报告
- docs/cli/CLI.json — CLI命令参考
- docs/architecture/ARCHITECTURE.json — 网关架构
- docs/config/CONFIG.json — 配置指南
- docs/channels/OVERVIEW.json — 频道概览
- docs/channels/WHATSAPP.json — WhatsApp配置
- docs/channels/TELEGRAM.json — Telegram配置
- docs/security/SECURITY.json — 安全配置
- docs/concepts/MODELS.json — 模型系统
- docs/concepts/SESSION.json — 会话管理
- docs/concepts/MEMORY.json — 内存系统
- docs/providers/ANTHROPIC.json — Anthropic配置
- docs/providers/OLLAMA.json — Ollama配置
- docs/providers/MINIMAX.json — MiniMax配置
- docs/automation/CRON.json — Cron任务
- docs/best-practices/FAQ_KEY_POINTS.json — FAQ要点

### 关键文档URL
- 官网: https://openclawx.cloud
- 中文: https://openclawx.cloud/zh
- 英文: https://openclawx.cloud/en
- GitHub: https://github.com/openclaw/openclaw

### 版本范围
v2026.3.0 ~ v2026.4.9

### 重要配置
- Gateway端口: 18789 (loopback)
- 热重载: hybrid模式
- DM隔离: dmScope选项（main/per_peer/per_channel_peer）
- 安全审计: openclaw security audit [--deep] [--fix]

### 故障排查命令
1. openclaw status
2. openclaw status --all
3. openclaw status --deep
4. openclaw logs --follow
5. openclaw doctor


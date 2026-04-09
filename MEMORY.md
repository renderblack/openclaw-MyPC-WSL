# MEMORY.md - 长期记忆

## 基本信息
- **创建日期**: 2026-04-04
- **创建原因**: 整合 2026-04-03 至 2026-04-04 的每日记录形成长期记忆
- **最后更新**: 2026-04-09 重建（编码损坏，PowerShell Get-Content 显示乱码，read 工具正常）

---

## 系统环境

### 硬件配置
- **CPU**: Intel Core i7-9700KF @ 3.60GHz (8 核 8 线程)
- **内存**: 32GB (31.93 GB 可用)
- **主机名**: XIONG
- **C 盘**: 74.36 GB 可用 / 222.9 GB 总容量 (66.6% 已用)
- **D 盘**: 201.5 GB 可用 / 962.2 GB 总容量

### 软件环境
- **操作系统**: Windows 10 教育版 (Build 19045, 64 位)
- **运行环境**: Windows Native PowerShell (无 WSL2)
- **OpenClaw 版本**: 2026.4.2 (d74a122)
- **工作空间**: `C:\Users\Administrator\.openclaw\workspace`
- **代理配置**: `http://127.0.0.1:7890` (Clash for Windows 本地代理)

### 工具链状态
| 工具 | 版本 | 状态 |
|------|------|------|
| Node.js | v24.14.1 | ✅ 已安装 |
| npm | v11.12.1 | ✅ 已安装 |
| Python | v3.7.4 | ✅ 已安装 |
| Git | v2.37.1 (Windows) | ✅ 已安装 |
| curl | v7.78.0 | ✅ 已安装 |
| ffmpeg | N-123824 | ✅ 已安装 |
| gh (GitHub CLI) | v2.40.1 | ✅ 已安装 |
| jq | v1.7.1 | ✅ 已安装 |

### 镜像配置
- **npm 镜像**: `registry.npmmirror.com`
- **pip 镜像**: `pypi.tuna.tsinghua.edu.cn` + `mirrors.aliyun.com`

---

## AI 模型配置

### 当前模型
- **默认模型**: `minimax/MiniMax-M2.7-highspeed` (通过 minimax-portal)
  - 上下文上限: 200k
  - 特点: 快速响应，适合日常任务

### 备用模型
- `deepseek/deepseek-chat`
- 切换命令: `/model DeepSeek`

---

## 已安装技能 (Skills)

14个 MiniMax-AI/skills 通过目录连接方式接入:
- android-native-dev, flutter-dev, frontend-dev, fullstack-dev
- gif-sticker-maker, ios-application-dev
- minimax-docx, minimax-multimodal-toolkit, minimax-pdf, minimax-xlsx
- pptx-generator, react-native-dev, shader-dev, vision-analysis

---

## 已知问题

### music_generate 工具 Bug (2026-04-08)
- **问题**: 使用内置 `music_generate` 工具时 Gateway 崩溃
- **错误**: `Unhandled promise rejection: Error: Agent listener invoked outside active run`
- **原因**: 异步生成完成后回调 agent 时 session 已结束
- **影响**: Gateway 崩溃重启
- **建议**: 暂不使用，等官方修复；替代方案：手动通过 MiniMax 平台生成

---

## 待办事项

### 高优先级
- [ ] 夸克网盘上传（Selenium 方案待测试）
- [ ] 定时推送功能配置（Cron）
- [ ] 修复网关启动冲突（Scheduled Task LogonTrigger/BootTrigger 冲突）

### 中优先级
- [ ] 关注 music_generate bug 修复
- [ ] TG 群消息获取（需用户确认）
- [ ] 每周学习记录晋升（周末处理）

### 低优先级/维护
- [ ] SpaceSniffer/WizTree CLI 研究
- [ ] gdu 其他功能测试
- [ ] 全盘分析 C:\ + 清理报告
- [ ] 清理孤立 transcript 文件

---

## 完成项目日志

| 日期 | 项目 |
|------|------|
| 2026-04-08 | MiniMax-AI/skills 配置（14个技能） |
| 2026-04-08 | 重新配置模型（M2.7-highspeed） |
| 2026-04-08 | Claude Code 源码分析（4756文件 + 5份文档） |
| 2026-04-06 | FFmpeg CLI 自动化工具 |
| 2026-04-06 | OCR 文字识别服务（PaddleOCR GPU） |
| 2026-04-03 | C盘清理 45GB（89GB→34GB 后回升至 74GB） |

---

## 经验总结

### 编码问题（2026-04-09）
- **现象**: MEMORY.md 在 PowerShell `Get-Content` 中显示乱码（�?），但 OpenClaw `read` 工具正常读取
- **原因**: 文件编码问题，Git 仓库中所有版本均已损坏（所有 commits 都包含乱码）
- **解决**: 用 `read` 工具读取内容，用 `write` 工具重建文件（write 以 UTF-8 保存，正常）
- **教训**: 避免用 PowerShell 直接读写含中文的 UTF-8 文件；优先用 OpenClaw 的 read/write 工具

### 环境兼容性原则
- 推荐/安装任何工具前，先确认环境兼容性（Windows Native vs WSL2）
- 当前 OpenClaw 运行在 Windows Native PowerShell，所有脚本应为 .ps1 格式

---

## GitHub 仓库

| 仓库 | 地址 | 用途 |
|------|------|------|
| openclaw-MyPC | github.com/renderblack/openclaw-MyPC | 皮皮虾的开发空间 |
| openclaw (fork) | github.com/renderblack/openclaw | OpenClaw 官方库 fork |

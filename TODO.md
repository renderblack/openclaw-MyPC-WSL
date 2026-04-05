# TODO.md - 待办事项列表

## 待办任务

### 🔴 高优先级

- [ ] **Claude Code 源码分析** (2026-04-05 新增)
  - 描述：下载并分析 Claude Code 2.1.88 泄露源码
  - 存储位置：D:\ClaudeCode\
  - 分析维度：架构、Agent 实现、工具系统、OpenClaw 对比、技术亮点
  - 计划文档：`docs/Claude-Code源码分析计划.md`
  - 状态：⏳ 待执行（等待下载源确认）

- [ ] **FFmpeg CLI 自动化测试**
  - 描述：测试 ffmpeg-cli.ps1 脚本的 7 种功能
  - 脚本位置：`scripts/ffmpeg-cli.ps1`
  - 功能：convert/trim/merge/extract-audio/add-watermark/batch-convert/info
  - 状态：已创建脚本，待测试

- [ ] **ClawLibrary 修复** (502 Bad Gateway)
  - 描述：Vite 开发服务器异常，本机访问 http://localhost:5173/ 失败
  - 状态：待排查

- [ ] **WizTree 添加到安全软件白名单**
  - 描述：安全软件曾终止 WizTree 进程，导致网关重启
  - 状态：待处理

- [ ] **腾讯系文件迁移到 D: 盘**
  - 描述：企业微信、微信等腾讯系软件迁移，释放 C 盘空间
  - 涉及：Tencent\WXWork\ 等目录
  - 状态：待执行

### 🟡 中优先级

- [ ] **本地文件自然语言模糊搜索** (2026-04-05 新增)
  - 描述：通过自然语言描述快速从本地文件查找内容
  - 建议方案：ripgrep 全文检索 + LLM 语义筛选（方案 A）
  - 待确认：搜索范围（workspace/C盘）、速度要求
  - 状态：⏳ 待用户选择方案

- [ ] **命令执行智能判断准则落地**
  - 描述：执行前判断 Linux vs Windows 命令，Linux 用 bash -c 包装
  - 规则位置：IDENTITY.md → 核心执行准则
  - 状态：已确立，执行时遵守

- [ ] **OCR 能力配置** (2026-04-05 新增)
  - 方案：PaddleOCR + Tesseract 双轨制
  - 硬件：NVIDIA RTX 2070 (8GB GDDR6, CUDA 13.0)
  - 目标：支持截图/文档/扫描件/手写体，离线使用
  - 执行步骤：
    1. 安装 Tesseract (Windows OCR 引擎)
    2. 安装 PaddlePaddle GPU 版 (CUDA 13.0)
    3. 安装 PaddleOCR
    4. 测试验证
  - 状态：⏳ 待执行

### 🟢 低优先级

- [ ] **插件依赖修复**
  - 命令：openclaw doctor --fix
  - 状态：43 个可选插件依赖未安装

- [ ] **proactive_check.sh 验证**
  - 描述：确保主动推送机制正常运行
  - 状态：待验证

---

## ✅ 已完成任务 (2026-04-05)

- [x] C 盘清理（45GB → 89GB）
- [x] WizTree 安装 + CLI-Anything 自动化
- [x] FFmpeg 安装完成
- [x] Claude Code 源码分析计划制定
- [x] 模型切换回 M2.7-highspeed
- [x] Chrome 浏览器自动化（已实现 via cli-anything skill）
- [x] 集成 agency-agents 智能体集合 (162 个)
- [x] NPM 镜像配置（npmmirror.com）
- [x] pip 镜像配置（清华 + 阿里云）
- [x] Git 代理配置修复
- [x] 依赖包完整性检查
- [x] GitHub 仓库同步（openclaw-MyPC）

---

## 📝 更新记录

| 日期 | 内容 | 更新人 |
|------|------|--------|
| 2026-04-05 | 删除 Chrome 自动化（已实现）；新增本地文件模糊搜索（待确认方案）；小米10Pro 标注待确认 | 龙虾壳 🦞 |
| 2026-04-05 | 新增 Claude Code 源码分析、FFmpeg 测试、ClawLibrary 修复等任务 | 龙虾壳 🦞 |
| 2026-04-04 | 新增 claw-code 研究（低优先级） | 龙虾壳 🦞 |
| 2026-04-04 | 整合 agency-agents、镜像配置等已完成任务 | 龙虾壳 🦞 |

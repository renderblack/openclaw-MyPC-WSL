# TODO.md - 待办事项列表

## WSL2 OpenClaw 安装配置

### 🔴 高优先级

- [ ] **安全审计** — 运行 `openclaw security audit`，处理 Critical/WARN 项
- [ ] **plugins.allow 白名单** — 配置可信插件列表，消除 WARN
- [ ] **systemd 开机服务** — WSL2 需先开启 systemd，再配置 Gateway 开机自启

### 🟡 中优先级

- [ ] **Tailscale 远程访问** — 让外网设备安全访问 Gateway（可选方案）
- [ ] **图片识别能力配置** — 当前模型均为纯文本，需要配置多模态模型

### 🟢 低优先级

- [ ] **gateway.trustedProxies** — 如使用反向代理（Nginx/Caddy）才需要
- [ ] **Heartbeat 周期** — 当前默认 30 分钟，可按需调整
- [ ] **Cron 定时任务** — 按需配置定期检查/提醒

---

## ✅ 已完成

- [x] GitHub 仓库新建并同步（openclaw-MyPC-WSL）
- [x] 本地备份配置
- [x] 微信插件连接修复（Gateway 完整重启）

---

## WSL2 环境说明

- 宿主机：Windows 10 + WSL2 Ubuntu
- OpenClaw：npm 全局安装 v2026.4.9
- Gateway：127.0.0.1:18790（本地回环）
- 微信插件：openclaw-weixin v2.1.7，已连接

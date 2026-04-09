# TOOLS.md - Local Notes (WSL2 Ubuntu)

## 系统环境

- **宿主机:** Windows 10 + WSL2 Ubuntu
- **Node:** v22.22.2
- **OpenClaw 版本:** 2026.4.9
- **安装方式:** npm 全局安装

## Gateway 配置

- **地址:** 127.0.0.1:18790 (WSL2 本地回环)
- **模式:** local
- **认证:** Token 模式
- **日志:** /tmp/openclaw/openclaw-YYYY-MM-DD.log

## 微信渠道

- **插件:** @tencent-weixin/openclaw-weixin v2.1.7
- **账号:** o9cq80xO-9exHj-UMC1xQUSNgK5g@im.wechat
- **Base URL:** https://ilinkai.weixin.qq.com

## 重要备注

- WSL2 Ubuntu 环境下，Gateway 默认绑定 127.0.0.1，外部网络无法直接访问
- 如果需要外网访问微信 Webhook，需要配置 WSL2 端口转发或使用 Tailscale 等方案
- Clash 代理端口: 7890（已开启局域网连接）

## Gateway 重启方法

WSL2 环境下，不要用 `openclaw gateway restart`（依赖 systemd，会失败），用：

```bash
openclaw gateway --force
```

这会自动 kill 旧进程并启动新的。

## 模型

- **主模型:** MiniMax-M2.7（上下文 204800 tokens）
- **备用:** MiniMax-M2.7-highspeed

## GitHub 仓库

- **仓库:** https://github.com/renderblack/openclaw-MyPC-WSL
- **Token:** 已配置（ghp_yGC4...）

## 常用命令

```bash
# 查看 Gateway 状态
openclaw status

# 查看日志
tail -f /tmp/openclaw/openclaw-$(date +%Y-%m-%d).log

# 重启 Gateway（WSL2 专用）
openclaw gateway --force
```

## 文件路径

- OpenClaw 配置: ~/.openclaw/
- 工作区: ~/.openclaw/workspace/
- 微信凭证: ~/.openclaw/openclaw-weixin/accounts/

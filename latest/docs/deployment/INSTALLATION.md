# OpenClaw 部署指南

## 安装方式

### 方式1：npm全局安装（推荐）

```bash
# macOS/Linux/WSL2
npm install -g openclaw

# Windows PowerShell
npm install -g openclaw

# 验证
openclaw --version
```

### 方式2：Docker

```bash
# 拉取镜像
docker pull openclaw/openclaw:latest

# 运行
docker run -d \
  --name openclaw \
  -p 18789:18789 \
  -v ~/.openclaw:/root/.openclaw \
  openclaw/openclaw:latest
```

### 方式3：源码安装

```bash
# 克隆仓库
git clone https://github.com/openclaw/openclaw.git
cd openclaw

# 安装依赖
npm install

# 链接
npm link
```

## 环境要求

| 组件 | 最低 | 推荐 |
|------|------|------|
| Node.js | v18 | v22 LTS |
| 内存 | 2GB | 8GB |
| 磁盘 | 1GB | 10GB |
| OS | Win10+/macOS10.15+/Ubuntu18+ | 同 |

## Windows特殊考虑

### PowerShell vs CMD

```powershell
# PowerShell（推荐）
npm install -g openclaw

# CMD也可以
npm install -g openclaw
```

### WSL2注意事项

```bash
# WSL2内安装
npm install -g openclaw

# Gateway命令
openclaw gateway --force  # 不要用restart
```

### 路径差异

```powershell
# Windows
$env:USERPROFILE\.openclaw\
# 或
%USERPROFILE%\.openclaw\

# WSL2/Linux
~/.openclaw/
```

## 首次启动

```bash
# 1. 启动Gateway
openclaw gateway --force

# 2. 查看状态
openclaw status

# 3. 配置第一个渠道
openclaw channels enable telegram
```

## 开机自启

### systemd（Linux/macOS）

```ini
# /etc/systemd/system/openclaw.service
[Unit]
Description=OpenClaw Gateway
After=network.target

[Service]
Type=simple
ExecStart=/usr/bin/openclaw gateway
Restart=always
User=ubuntu

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl enable openclaw
sudo systemctl start openclaw
```

### Windows任务计划

```powershell
# 创建任务
schtasks /create /tn "OpenClaw" /tr "openclaw gateway" /sc onlogon /rl highest
```

## 反向代理配置

### Nginx

```nginx
server {
    listen 443 ssl;
    server_name openclaw.example.com;

    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;

    location / {
        proxy_pass http://127.0.0.1:18789;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }
}
```

## Docker Compose完整示例

```yaml
version: '3.8'
services:
  openclaw:
    image: openclaw/openclaw:latest
    container_name: openclaw
    ports:
      - "18789:18789"
    volumes:
      - ~/.openclaw:/root/.openclaw
    environment:
      - HTTP_PROXY=http://host.docker.internal:7890
      - HTTPS_PROXY=http://host.docker.internal:7890
    restart: unless-stopped
```

---

*来源：openclawx.cloud/en/install + 实战经验*

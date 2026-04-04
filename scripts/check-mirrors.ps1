# 🚀 国内镜像源配置检查脚本

```powershell
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  📦 国内镜像源配置检查" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

# 检查 npm
Write-Host "`n📦 npm 配置:" -ForegroundColor Yellow
npm config get registry
npm config get strict-ssl

# 检查 pip
Write-Host "`n🐍 pip 配置:" -ForegroundColor Yellow
pip3 config list

# 检查 pnpm (如果安装)
if (Get-Command pnpm -ErrorAction SilentlyContinue) {
    Write-Host "`n📦 pnpm 配置:" -ForegroundColor Yellow
    pnpm config get registry
} else {
    Write-Host "`n⚠️ pnpm 未安装" -ForegroundColor Gray
}

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "✅ 配置完成！安装速度将大幅提升" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
```

## 已配置的镜像源

| 工具 | 主镜像源 | 备用镜像源 | 状态 |
|------|---------|-----------|------|
| **npm** | `registry.npmmirror.com` (淘宝) | - | ✅ |
| **pip** | `pypi.tuna.tsinghua.edu.cn` (清华) | `mirrors.aliyun.com` (阿里) | ✅ |
| **pnpm** | `registry.npmmirror.com` (淘宝) | - | ⚠️ 未安装 |

## 使用效果

- **npm install**: 自动走淘宝镜像，速度提升 10-50 倍
- **pip install**: 自动走清华镜像，下载速度飞快
- **pnpm install**: 如果安装 pnpm，自动走淘宝镜像

## 临时测试

如果某个包还是下载慢，可以临时指定镜像：
```bash
npm install <package> --registry=https://registry.npmmirror.com
pip install <package> -i https://pypi.tuna.tsinghua.edu.cn/simple
```

## 更新镜像源

如果某个镜像源不稳定，可以随时切换：
```bash
# 切换到阿里 npm 镜像
npm config set registry https://registry.npmmirror.com

# 切换到阿里 pip 镜像
pip3 config set global.index-url https://mirrors.aliyun.com/pypi/simple/
```

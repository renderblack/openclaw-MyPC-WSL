# CLI-Anything 自动化方法论

> 如何通过命令行接口实现第三方软件的自动化控制

---

## 核心理念

**CLI-Anything** = 通过分析工具的 CLI 接口，实现自动化控制。

不猜测、不试错，而是：
1. 查阅官方文档/源码
2. 分析 CLI 参数
3. 编写自动化脚本

---

## 工作流程 (5 步法)

### Step 1: 识别目标工具
- 明确要自动化的任务
- 列出候选工具
- 检查是否有 CLI 接口

### Step 2: 文档/源码调研
- 官方文档网站
- GitHub README
- `--help` / `/?` 参数
- 源码中的 CLI 处理逻辑

### Step 3: 环境准备
- 下载/安装工具
- 检查依赖（.NET, VC++ Runtime 等）
- **重要：关闭安全软件测试**

### Step 4: CLI 参数测试
```powershell
# 基础测试
tool.exe --help
tool.exe -?

# 导出测试
tool.exe "C:" /export="output.csv" /admin=1

# 验证输出
Test-Path output.csv
```

### Step 5: 脚本封装
- 自动查找工具路径
- 参数化配置
- 输出解析（编码处理）
- 错误处理

---

## 常见问题与解决方案

### 问题 1: 下载链接失效
| 现象 | 解决方案 |
|------|----------|
| 官网 404/403 | 从 GitHub 下载 |
| 没有 portable 版 | 用安装包 + `/VERYSILENT /DIR=` 提取 |

### 问题 2: 安全软件拦截
| 现象 | 解决方案 |
|------|----------|
| 进程被 Kill | 临时关闭安全软件 |
| CSV 未生成 | 添加到白名单 |

### 问题 3: 编码问题
| 现象 | 解决方案 |
|------|----------|
| Import-Csv 失败 | 指定 GBK 编码 |
| 中文乱码 | `[System.Text.Encoding]::GetEncoding(936)` |

### 问题 4: 权限不足
| 现象 | 解决方案 |
|------|----------|
| 拒绝访问 | 添加 `/admin=1` 参数 |
| UAC 弹窗 | 使用 `-Wait` 或提权脚本 |

---

## 已验证的工具清单

| 工具 | 用途 | CLI 支持 | 状态 |
|------|------|----------|------|
| WizTree | 磁盘分析 | ✅ | 已验证 |
| SpaceSniffer | 磁盘分析 | ❌ | GUI 正常 |
| gdu | 磁盘分析 | ✅ | 未测试 |
| du (Windows) | 磁盘分析 | ✅ | 原生支持 |

---

## 脚本模板

### 模板 1: 基础 CLI 调用
```powershell
param(
    [string]$ToolPath,
    [string]$OutputFile
)

# 1. 查找工具
if (-not (Test-Path $ToolPath)) {
    $ToolPath = (Get-Command tool -ErrorAction SilentlyContinue).Source
}

# 2. 执行 CLI
$process = Start-Process -FilePath $ToolPath -ArgumentList "/export=`"$OutputFile`"" -NoNewWindow -Wait -PassThru

# 3. 验证输出
if ((Test-Path $OutputFile) -and (Get-Item $OutputFile).Length -gt 0) {
    Write-Host "SUCCESS"
} else {
    Write-Host "FAILED"
}
```

### 模板 2: CSV 解析（含编码处理）
```powershell
function Parse-CsvWithEncoding {
    param([string]$Path)
    
    $bytes = [System.IO.File]::ReadAllBytes($Path)
    
    # 尝试 GBK (936) 或 UTF8
    $encodings = @(
        [System.Text.Encoding]::GetEncoding(936),  # GBK
        [System.Text.Encoding]::UTF8
    )
    
    foreach ($enc in $encodings) {
        try {
            $content = $enc.GetString($bytes)
            return $content -split "`n"
        } catch { continue }
    }
    
    throw "Failed to parse CSV"
}
```

---

## 经验教训

1. **文档是第一优先级** - 官方文档比猜测更可靠
2. **安全软件是隐藏变量** - 测试时先关闭
3. **编码问题很常见** - Windows 工具默认 GBK
4. **从简单开始** - 先测试基础参数，再测试高级功能
5. **输出验证** - 每次 CLI 调用后检查文件是否生成

---

## 下一步

- [ ] 验证 gdu 工具的 CLI 自动化
- [ ] 测试其他磁盘工具
- [ ] 扩展到其他场景（截图、压缩、解压等）
- [ ] 建立工具 CLI 参数知识库

---

*最后更新：2026-04-05*
*作者：皮皮虾 🦞*
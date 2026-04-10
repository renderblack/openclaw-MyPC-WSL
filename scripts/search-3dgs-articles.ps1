# search-3dgs-articles.ps1
# 每两天运行一次，搜索3DGS最新文章
# 运行方式：Windows计划任务

$Date = Get-Date -Format "yyyy-MM-dd"
$LogFile = "C:\Users\Administrator\.openclaw\workspace\logs\3dgs-search.log"

# 记录日志
$LogDir = Split-Path $LogFile -Parent
if (!(Test-Path $LogDir)) { New-Item -ItemType Directory -Path $LogDir -Force }

"$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') - 开始搜索3DGS文章" | Out-File -FilePath $LogFile -Append

# 搜索会在下次 heartbeat 时告知用户
# 这里只是记录检查时间

"$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') - 检查完成" | Out-File -FilePath $LogFile -Append

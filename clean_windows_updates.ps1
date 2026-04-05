# Windows 更新清理脚本 (自动执行)
# 运行方式：右键 -> 以管理员身份运行

Write-Host "正在清理 Windows 更新缓存..." -ForegroundColor Cyan

# 停止 Windows Update 服务
Stop-Service -Name wuauserv -Force -ErrorAction SilentlyContinue
Stop-Service -Name bits -Force -ErrorAction SilentlyContinue

# 清理 SoftwareDistribution 目录
$distDir = "C:\Windows\SoftwareDistribution\Download"
if (Test-Path $distDir) {
    Remove-Item -Path $distDir\* -Recurse -Force -ErrorAction SilentlyContinue
    Write-Host "已清理 SoftwareDistribution: 约 2-5 GB" -ForegroundColor Green
}

# 清理 Windows 更新日志
$logDir = "C:\Windows\Logs\WindowsUpdate"
if (Test-Path $logDir) {
    Remove-Item -Path $logDir\* -Recurse -Force -ErrorAction SilentlyContinue
    Write-Host "已清理 WindowsUpdate 日志" -ForegroundColor Green
}

# 清理临时更新文件
$tempDir = "C:\Windows\Temp"
if (Test-Path $tempDir) {
    Remove-Item -Path $tempDir\*.tmp -Force -ErrorAction SilentlyContinue
    Write-Host "已清理临时文件" -ForegroundColor Green
}

# 重启服务
Start-Service -Name bits -ErrorAction SilentlyContinue
Start-Service -Name wuauserv -ErrorAction SilentlyContinue

# 显示剩余空间
$disk = Get-PSDrive -PSProvider FileSystem | Where-Object {$_.Root -eq "C:\"}
$freeGB = [math]::Round($disk.Free / 1GB, 2)
Write-Host "`n 清理完成！C 盘剩余空间：$freeGB GB" -ForegroundColor Yellow
Write-Host " 建议：重启电脑以完成清理" -ForegroundColor Cyan

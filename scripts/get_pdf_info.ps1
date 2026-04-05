[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

# 获取PDF文件信息
$files = Get-ChildItem -Path "G:\桥梁项目\2023\202312中铁24局沪昆铁路抬升改建项目演示动画" -Filter "*.pdf" -ErrorAction SilentlyContinue

foreach ($f in $files) {
    Write-Host "文件: $($f.Name)"
    Write-Host "大小: $($f.Length) bytes"
    Write-Host "完整路径: $($f.FullName)"
    Write-Host ""
}
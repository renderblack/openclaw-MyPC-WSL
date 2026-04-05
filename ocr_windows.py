# -*- coding: utf-8 -*-
"""
使用 Windows.Media.Ocr 提取 PDF 文本
Windows 10 内置 OCR，无需额外安装
"""
import subprocess
import os
import sys

pdf_path = r"C:\Users\Administrator\.openclaw\workspace\合同_中铁二十四局沪昆铁路.pdf"
output_file = r"C:\Users\Administrator\.openclaw\workspace\ocr_result_windows.txt"

print("使用 Windows.Media.Ocr 提取 PDF 文本...")
print(f"文件: {pdf_path}")
print()

# 使用 PowerShell 调用 Windows.Media.Ocr
ps_script = f'''
Add-Type -AssemblyName System.Runtime.WindowsRuntime
Add-Type -AssemblyName Windows.Graphics.Imaging
Add-Type -AssemblyName Windows.Storage

$file = [Windows.Storage.StorageFile]::GetFileFromPathAsync("{pdf_path}").GetAwaiter().GetResult()
$streams = $file.OpenReadAsync().GetAwaiter().GetResult()
$stream = $streams.GetInputStreamAt(0)
$reader = [Windows.Storage.Streams.DataReader]::new($stream)
$reader.LoadAsync($streams.Size).GetAwaiter().GetResult()

# 读取 PDF 内容
$bytes = [byte[]]::new($streams.Size)
$reader.ReadBytes($bytes)

# 保存为临时图片文件用于 OCR
$tempPng = "$env:TEMP\\ocr_temp.png"
[System.IO.File]::WriteAllBytes($tempPng, $bytes)

# 使用 Windows.Media.Ocr
$ocrEngine = [Windows.Media.Ocr.OcrEngine]::TryCreateFromUserProfileLanguages()
$imageFile = [Windows.Storage.StorageFile]::GetFileFromPathAsync($tempPng).GetAwaiter().GetResult()
$image = [Windows.Graphics.Imaging.BitmapDecoder]::CreateAsync($imageFile.OpenReadAsync().GetAwaiter().GetResult()).GetAwaiter().GetResult()
$bitmap = $image.GetSoftwareBitmapAsync().GetAwaiter().GetResult()
$result = $ocrEngine.RecognizeAsync($bitmap).GetAwaiter().GetResult()

Write-Host "识别结果:"
Write-Host $result.Text

# 保存结果
$result.Text | Out-File -FilePath "{output_file}" -Encoding UTF8

# 清理
Remove-Item $tempPng -ErrorAction SilentlyContinue
'''

# 写入 PowerShell 脚本
ps_file = r"C:\Users\Administrator\.openclaw\workspace\ocr_ps.ps1"
with open(ps_file, "w", encoding="utf-8") as f:
    f.write(ps_script)

print("执行 OCR...")
print("=" * 50)

# 执行 PowerShell 脚本
result = subprocess.run(
    ["powershell", "-ExecutionPolicy", "Bypass", "-File", ps_file],
    capture_output=True,
    text=True
)

print(result.stdout)
if result.stderr:
    print("错误:", result.stderr)
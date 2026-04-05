# -*- coding: utf-8 -*-
"""
将 PDF 转换为图片，然后使用 Windows.Media.Ocr 识别
"""
import subprocess
import os
import sys
from pdf2image import convert_from_path

pdf_path = r"C:\Users\Administrator\.openclaw\workspace\合同_中铁二十四局沪昆铁路.pdf"
output_dir = r"C:\Users\Administrator\.openclaw\workspace\pdf_images"
output_txt = r"C:\Users\Administrator\.openclaw\workspace\ocr_result_final.txt"

os.makedirs(output_dir, exist_ok=True)

print("使用 pdf2image + Windows.Media.Ocr 进行 OCR...")
print(f"文件: {pdf_path}")
print()

# 1. 将 PDF 转换为图片
print("第1步: 将 PDF 转换为图片...")
images = convert_from_path(pdf_path, dpi=200)
print(f"PDF 共 {len(images)} 页，已转换为图片")
print()

# 保存第一页作为测试
test_image_path = os.path.join(output_dir, "page_1.png")
images[0].save(test_image_path, "PNG")
print(f"第1页已保存到: {test_image_path}")
print()

# 2. 使用 PowerShell 的 Windows.Media.Ocr 识别
print("第2步: 使用 Windows.Media.Ocr 识别...")
ps_script = f'''
Add-Type -AssemblyName Windows.Graphics.Imaging
Add-Type -AssemblyName Windows.Storage
Add-Type -AssemblyName System.Runtime.WindowsRuntime

$imagePath = "{test_image_path}"
$storageFile = [Windows.Storage.StorageFile]::GetFileFromPathAsync($imagePath).GetAwaiter().GetResult()
$stream = $storageFile.OpenReadAsync().GetAwaiter().GetResult()
$bitmapDecoder = [Windows.Graphics.Imaging.BitmapDecoder]::CreateAsync($stream).GetAwaiter().GetResult()
$bitmap = $bitmapDecoder.GetSoftwareBitmapAsync().GetAwaiter().GetResult()

$ocrEngine = [Windows.Media.Ocr.OcrEngine]::TryCreateFromUserProfileLanguages()
$result = $ocrEngine.RecognizeAsync($bitmap).GetAwaiter().GetResult()

Write-Output $result.Text
'''

ps_file = r"C:\Users\Administrator\.openclaw\workspace\ocr_final.ps1"
with open(ps_file, "w", encoding="utf-8") as f:
    f.write(ps_script)

result = subprocess.run(
    ["powershell", "-ExecutionPolicy", "Bypass", "-File", ps_file],
    capture_output=True,
    text=True
)

print("识别结果:")
print("=" * 50)
print(result.stdout)
print("=" * 50)

# 保存结果
with open(output_txt, "w", encoding="utf-8") as f:
    f.write(result.stdout)

print(f"\n结果已保存到: {output_txt}")
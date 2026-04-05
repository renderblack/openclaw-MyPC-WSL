# -*- coding: utf-8 -*-
"""
使用 Windows.Media.Ocr 识别 PDF 图片
Windows 10 内置，无需额外安装
"""
import fitz
import subprocess
import os

pdf_path = r"C:\Users\Administrator\.openclaw\workspace\合同_中铁二十四局沪昆铁路.pdf"
output_dir = r"C:\Users\Administrator\.openclaw\workspace\pdf_images"
os.makedirs(output_dir, exist_ok=True)

print("=" * 60)
print("Windows.Media.Ocr PDF 识别")
print("=" * 60)
print()

# 1. 将 PDF 转换为图片
print("第1步: 将 PDF 转换为图片...")
doc = fitz.open(pdf_path)
print(f"PDF 共 {len(doc)} 页")

image_paths = []
for page_num in range(len(doc)):
    page = doc[page_num]
    mat = fitz.Matrix(2, 2)  # 2x scale
    pix = page.get_pixmap(matrix=mat)
    image_path = os.path.join(output_dir, f"page_{page_num+1}.png")
    pix.save(image_path)
    image_paths.append(image_path)
    print(f"  第 {page_num+1} 页已保存")

doc.close()
print()

# 2. 使用 Windows.Media.Ocr 识别
print("第2步: OCR 识别...")
all_results = []

for i, img_path in enumerate(image_paths):
    print(f"  识别第 {i+1} 页...")
    
    # PowerShell script for Windows.Media.Ocr
    ps_script = f'''
Add-Type -AssemblyName Windows.Graphics.Imaging
Add-Type -AssemblyName Windows.Storage

$imagePath = "{img_path}"
$storageFile = [Windows.Storage.StorageFile]::GetFileFromPathAsync($imagePath).GetAwaiter().GetResult()
$stream = $storageFile.OpenReadAsync().GetAwaiter().GetResult()
$bitmapDecoder = [Windows.Graphics.Imaging.BitmapDecoder]::CreateAsync($stream).GetAwaiter().GetResult()
$bitmap = $bitmapDecoder.GetSoftwareBitmapAsync().GetAwaiter().GetResult()

$ocrEngine = [Windows.Media.Ocr.OcrEngine]::TryCreateFromUserProfileLanguages()
if ($ocrEngine -eq $null) {{
    Write-Output "ERROR: OCR engine not available"
}} else {{
    $result = $ocrEngine.RecognizeAsync($bitmap).GetAwaiter().GetResult()
    Write-Output $result.Text
}}
'''
    
    ps_file = r"C:\Users\Administrator\.openclaw\workspace\ocr_windows.ps1"
    with open(ps_file, "w", encoding="utf-8") as f:
        f.write(ps_script)
    
    result = subprocess.run(
        ["powershell", "-ExecutionPolicy", "Bypass", "-File", ps_file],
        capture_output=True,
        text=True,
        encoding="utf-8"
    )
    
    text = result.stdout.strip()
    if text and text != "ERROR: OCR engine not available":
        all_results.append(f"=== 第 {i+1} 页 ===")
        all_results.append(text)
        print(f"    识别到 {len(text)} 字符")
    else:
        print(f"    未识别到文本或引擎不可用")

# 3. 保存结果
print()
print("=" * 60)
print("OCR 结果:")
print("=" * 60)

full_text = "\n\n".join(all_results)
print(full_text)

output_txt = r"C:\Users\Administrator\.openclaw\workspace\ocr_result_windows.txt"
with open(output_txt, "w", encoding="utf-8") as f:
    f.write(full_text)

print()
print("=" * 60)
print(f"结果已保存到: {output_txt}")
# -*- coding: utf-8 -*-
"""
使用 PyMuPDF 转换 PDF 为图片，然后使用 PaddleOCR 识别
"""
import fitz  # PyMuPDF
import os
import subprocess

pdf_path = r"C:\Users\Administrator\.openclaw\workspace\合同_中铁二十四局沪昆铁路.pdf"
output_dir = r"C:\Users\Administrator\.openclaw\workspace\pdf_images"
os.makedirs(output_dir, exist_ok=True)

print("使用 PyMuPDF + PaddleOCR 进行 OCR...")
print(f"文件: {pdf_path}")
print()

# 1. 使用 PyMuPDF 将 PDF 转换为图片
print("第1步: 将 PDF 转换为图片...")
doc = fitz.open(pdf_path)
print(f"PDF 共 {len(doc)} 页")

image_paths = []
for page_num in range(len(doc)):
    page = doc[page_num]
    # 渲染页面为图片 (dpi=200 适合 OCR)
    mat = fitz.Matrix(200/72, 200/72)
    pix = page.get_pixmap(matrix=mat)
    
    image_path = os.path.join(output_dir, f"page_{page_num+1}.png")
    pix.save(image_path)
    image_paths.append(image_path)
    print(f"  第 {page_num+1} 页已保存: {image_path}")

doc.close()
print()

# 2. 使用 Windows.Media.Ocr 识别
print("第2步: 使用 Windows.Media.Ocr 识别...")
ocr_results = []

for img_path in image_paths:
    print(f"  识别: {os.path.basename(img_path)}")
    
    ps_script = f'''
Add-Type -AssemblyName Windows.Graphics.Imaging
Add-Type -AssemblyName Windows.Storage

$imagePath = "{img_path}"
$storageFile = [Windows.Storage.StorageFile]::GetFileFromPathAsync($imagePath).GetAwaiter().GetResult()
$stream = $storageFile.OpenReadAsync().GetAwaiter().GetResult()
$bitmapDecoder = [Windows.Graphics.Imaging.BitmapDecoder]::CreateAsync($stream).GetAwaiter().GetResult()
$bitmap = $bitmapDecoder.GetSoftwareBitmapAsync().GetAwaiter().GetResult()

$ocrEngine = [Windows.Media.Ocr.OcrEngine]::TryCreateFromUserProfileLanguages()
$result = $ocrEngine.RecognizeAsync($bitmap).GetAwaiter().GetResult()

Write-Output $result.Text
'''
    
    ps_file = r"C:\Users\Administrator\.openclaw\workspace\ocr_page.ps1"
    with open(ps_file, "w", encoding="utf-8") as f:
        f.write(ps_script)
    
    result = subprocess.run(
        ["powershell", "-ExecutionPolicy", "Bypass", "-File", ps_file],
        capture_output=True,
        text=True,
        encoding="utf-8"
    )
    
    text = result.stdout.strip()
    if text:
        ocr_results.append(f"=== 第 {image_paths.index(img_path)+1} 页 ===")
        ocr_results.append(text)
        print(f"    识别到 {len(text)} 字符")
    else:
        print(f"    未识别到文本")

print()
print("=" * 50)
print("OCR 结果:")
print("=" * 50)

full_text = "\n\n".join(ocr_results)
print(full_text)

# 保存结果
output_txt = r"C:\Users\Administrator\.openclaw\workspace\ocr_result_final.txt"
with open(output_txt, "w", encoding="utf-8") as f:
    f.write(full_text)

print()
print("=" * 50)
print(f"结果已保存到: {output_txt}")
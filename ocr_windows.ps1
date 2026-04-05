
Add-Type -AssemblyName Windows.Graphics.Imaging
Add-Type -AssemblyName Windows.Storage

$imagePath = "C:\Users\Administrator\.openclaw\workspace\pdf_images\page_4.png"
$storageFile = [Windows.Storage.StorageFile]::GetFileFromPathAsync($imagePath).GetAwaiter().GetResult()
$stream = $storageFile.OpenReadAsync().GetAwaiter().GetResult()
$bitmapDecoder = [Windows.Graphics.Imaging.BitmapDecoder]::CreateAsync($stream).GetAwaiter().GetResult()
$bitmap = $bitmapDecoder.GetSoftwareBitmapAsync().GetAwaiter().GetResult()

$ocrEngine = [Windows.Media.Ocr.OcrEngine]::TryCreateFromUserProfileLanguages()
if ($ocrEngine -eq $null) {
    Write-Output "ERROR: OCR engine not available"
} else {
    $result = $ocrEngine.RecognizeAsync($bitmap).GetAwaiter().GetResult()
    Write-Output $result.Text
}

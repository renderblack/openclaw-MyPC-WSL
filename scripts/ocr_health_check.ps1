# ocr_health_check.ps1
# PaddleOCR Health Check Script
# Usage: powershell -File ocr_health_check.ps1

$ErrorActionPreference = "Continue"
$script:Failed = $false

function Write-Status($msg, $type = "info") {
    $timestamp = Get-Date -Format "HH:mm:ss"
    switch ($type) {
        "ok"    { Write-Host "$timestamp [OK]    $msg" -ForegroundColor Green }
        "warn"  { Write-Host "$timestamp [WARN]  $msg" -ForegroundColor Yellow }
        "error" { Write-Host "$timestamp [ERROR] $msg" -ForegroundColor Red; $script:Failed = $true }
        default { Write-Host "$timestamp [INFO]  $msg" }
    }
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host " PaddleOCR Health Check" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# 1. Python
Write-Status "Checking Python..."
try {
    $pyVersion = python --version 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Status "Python: $pyVersion" "ok"
    } else {
        Write-Status "Python not found" "error"
    }
} catch {
    Write-Status "Python check failed: $_" "error"
}

# 2. PaddleOCR module
Write-Status "Checking PaddleOCR..."
try {
    $paddleCheck = python -c "import paddleocr; print('OK')" 2>&1
    if ($paddleCheck -match "OK") {
        Write-Status "PaddleOCR: installed" "ok"
    } else {
        Write-Status "PaddleOCR: not installed" "error"
    }
} catch {
    Write-Status "PaddleOCR check failed: $_" "error"
}

# 3. OpenCV
Write-Status "Checking OpenCV..."
try {
    $cvCheck = python -c "import cv2; print(cv2.__version__)" 2>&1
    if ($LASTEXITCODE -eq 0 -and $cvCheck -match "^\d") {
        Write-Status "OpenCV: $cvCheck" "ok"
    } else {
        Write-Status "OpenCV: not installed or broken" "error"
    }
} catch {
    Write-Status "OpenCV check failed: $_" "error"
}

# 4. Tesseract
Write-Status "Checking Tesseract..."
$tesseractPath = "C:\Program Files\Tesseract-OCR\tesseract.exe"
if (Test-Path $tesseractPath) {
    $ver = & $tesseractPath --version 2>&1 | Select-Object -First 1
    Write-Status "Tesseract: $ver" "ok"
} else {
    Write-Status "Tesseract: not found" "warn"
}

# 5. GPU
Write-Status "Checking GPU..."
try {
    $gpuCheck = python -c "
import paddle
try:
    paddle.device.set_device('gpu:0')
    x = paddle.to_tensor([1.0])
    print('GPU_OK')
except Exception as e:
    print('GPU_FAIL:', str(e))
" 2>&1
    if ($gpuCheck -match "GPU_OK") {
        Write-Status "NVIDIA GPU: available (RTX series)" "ok"
    } else {
        Write-Status "GPU: unavailable - $($gpuCheck -replace 'GPU_FAIL:', '')" "warn"
    }
} catch {
    Write-Status "GPU check failed: $_" "warn"
}

# 6. CUDA DLL
Write-Status "Checking CUDA libs..."
$cublas = "C:\Windows\System32\cublas64_112.dll"
if (Test-Path $cublas) {
    $size = (Get-Item $cublas).Length / 1MB
    Write-Status "cublas64_112.dll: OK ($([math]::Round($size, 1)) MB)" "ok"
} else {
    Write-Status "cublas64_112.dll: MISSING (PaddleOCR GPU will fail)" "error"
}

# 7. Model files
Write-Status "Checking PaddleOCR models..."
$modelDirs = @(
    "$env:USERPROFILE\.paddleocr\whl\det",
    "$env:USERPROFILE\.paddleocr\whl\rec",
    "$env:USERPROFILE\.paddleocr\whl\cls"
)
$allModelsExist = $true
foreach ($dir in $modelDirs) {
    if (Test-Path $dir) {
        $subdirs = Get-ChildItem $dir -Directory -ErrorAction SilentlyContinue
        if ($subdirs) {
            Write-Status "  $(Split-Path $dir -Leaf): $($subdirs.Count) models" "ok"
        } else {
            Write-Status "  $(Split-Path $dir -Leaf): empty dir" "warn"
            $allModelsExist = $false
        }
    } else {
        Write-Status "  $(Split-Path $dir -Leaf): not found" "error"
        $allModelsExist = $false
    }
}

# 8. Quick OCR test
Write-Status "Running OCR quick test..."
$testImg = "$env:USERPROFILE\Desktop\ocr_test.png"
if (Test-Path $testImg) {
    $start = Get-Date
    try {
        $testScript = @"
import sys
sys.path.insert(0, r'C:\Users\Administrator\.openclaw\workspace\scripts')
from ocr_stable import init, ocr_image
engine, mode = init()
if engine:
    r = ocr_image(r'$testImg')
    print('OK|{0}|{1} blocks'.format(mode, len(r)))
else:
    print('FAIL|unknown|0')
"@
        $result = python -c $testScript 2>&1 | Select-String "OK|FAIL"
        if ($result -match "OK\|(\w+)\|(\d+)") {
            $ocrMode = $Matches[1]
            $blocks = $Matches[2]
            $elapsed = ((Get-Date) - $start).TotalSeconds
            Write-Status "OCR Test: OK (${ocrMode} mode, ${blocks} text blocks, ${elapsed}s)" "ok"
        } else {
            Write-Status "OCR Test: failed" "error"
        }
    } catch {
        Write-Status "OCR test exception: $_" "error"
    }
} else {
    Write-Status "Test image not found: $testImg" "warn"
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
if ($script:Failed) {
    Write-Host " Result: ISSUES FOUND (see RED items above)" -ForegroundColor Red
} else {
    Write-Host " Result: ALL CHECKS PASSED" -ForegroundColor Green
}
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

exit [int]$script:Failed

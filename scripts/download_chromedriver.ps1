# Download ChromeDriver for manual installation
$chromeVersion = "146.0.7680.178"
$downloadUrl = "https://storage.googleapis.com/chrome-for-testing-public/$chromeVersion/win64/chromedriver-win64.zip"
$outputPath = "$env:TEMP\chromedriver-win64.zip"
$extractPath = "$env:TEMP\chromedriver"

Write-Host "Downloading ChromeDriver $chromeVersion..."
Write-Host "URL: $downloadUrl"

try {
    Invoke-WebRequest -Uri $downloadUrl -Proxy 'http://127.0.0.1:7890' -TimeoutSec 120 -OutFile $outputPath
    Write-Host "[OK] Downloaded to $outputPath"
    
    # Extract
    Write-Host "Extracting..."
    Expand-Archive -Path $outputPath -DestinationPath $extractPath -Force
    
    # List contents
    $driverPath = "$extractPath\chromedriver-win64\chromedriver.exe"
    if (Test-Path $driverPath) {
        Write-Host "[OK] ChromeDriver extracted to: $driverPath"
        Write-Host "Size: $((Get-Item $driverPath).Length / 1MB) MB"
        
        # Copy to a permanent location
        $destPath = "C:\Users\Administrator\.wdm\chromedriver.exe"
        Copy-Item $driverPath $destPath -Force
        Write-Host "[OK] Copied to: $destPath"
    } else {
        Write-Host "[ERROR] chromedriver.exe not found after extraction"
        Get-ChildItem $extractPath -Recurse | Select-Object FullName
    }
} catch {
    Write-Host "[ERROR] Failed: $_"
}

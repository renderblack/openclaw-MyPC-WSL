# Start ClawLibrary dev server
Set-Location 'C:\Users\Administrator\clawlibrary'
Write-Host "Starting ClawLibrary dev server..."
$env:Path = "D:\Program Files\nodejs;$env:Path"
Start-Process -FilePath "npm" -ArgumentList "run","dev" -WorkingDirectory "C:\Users\Administrator\clawlibrary" -WindowStyle Hidden
Write-Host "Started npm run dev"
Start-Sleep -Seconds 5
Write-Host "Checking port 5173..."
netstat -ano | Select-String ":5173"

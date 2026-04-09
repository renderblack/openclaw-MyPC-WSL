$os = Get-CimInstance Win32_OperatingSystem
$freeMemGB = [math]::Round($os.FreePhysicalMemory / 1MB, 2)
$totalMemGB = [math]::Round($os.TotalVisibleMemorySize / 1MB, 2)
Write-Host "Memory: $freeMemGB GB free / $totalMemGB GB total"

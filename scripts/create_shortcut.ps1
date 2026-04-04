$WshShell = New-Object -ComObject WScript.Shell
$Shortcut = $WshShell.CreateShortcut("C:\Users\Administrator\Desktop\SpaceSniffer.lnk")
$Shortcut.TargetPath = "C:\Users\Administrator\Downloads\SpaceSniffer\SpaceSniffer.exe"
$Shortcut.WorkingDirectory = "C:\Users\Administrator\Downloads\SpaceSniffer"
$Shortcut.Description = "Disk Space Analyzer"
$Shortcut.Save()
Write-Host "Done"

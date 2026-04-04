import os
import subprocess

# Create shortcut using VBScript
vbs_code = """
Set WshShell = CreateObject("WScript.Shell")
Set oShellLink = WshShell.CreateShortcut("C:\\Users\\Administrator\\Desktop\\SpaceSniffer.lnk")
oShellLink.TargetPath = "C:\\Users\\Administrator\\Downloads\\SpaceSniffer\\SpaceSniffer.exe"
oShellLink.WorkingDirectory = "C:\\Users\\Administrator\\Downloads\\SpaceSniffer"
oShellLink.Description = "Disk Space Analyzer"
oShellLink.Save
Set oShellLink = Nothing
Set WshShell = Nothing
"""

# Write VBS script
vbs_path = "C:\\temp\\create_shortcut.vbs"
os.makedirs("C:\\temp", exist_ok=True)
with open(vbs_path, "w", encoding="utf-8") as f:
    f.write(vbs_code)

# Run VBS script
subprocess.run(["cscript", "//nologo", vbs_path], check=True)
print("Shortcut created successfully!")

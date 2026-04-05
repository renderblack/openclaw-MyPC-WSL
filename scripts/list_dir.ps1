[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
Get-ChildItem G:\桥梁项目\2023\ -ErrorAction SilentlyContinue | ForEach-Object { $_.Name }
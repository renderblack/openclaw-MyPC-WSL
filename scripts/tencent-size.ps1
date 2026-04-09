$results = @()

$dirs = @(
    @{Path="C:\Users\Administrator\AppData\Roaming\Tencent\WeChat"; Name="WeChat"},
    @{Path="C:\Users\Administrator\AppData\Roaming\Tencent\QQ"; Name="QQ"},
    @{Path="C:\Users\Administrator\AppData\Roaming\Tencent\WXWork"; Name="WXWork"},
    @{Path="C:\Users\Administrator\AppData\Roaming\Tencent\WeMeet"; Name="WeMeet"}
)

foreach ($dir in $dirs) {
    if (Test-Path $dir.Path) {
        $subDirs = Get-ChildItem $dir.Path -Force -ErrorAction SilentlyContinue | Where-Object { $_.PSIsContainer }
        foreach ($sub in $subDirs) {
            $size = (Get-ChildItem $sub.FullName -Recurse -Force -ErrorAction SilentlyContinue | Measure-Object -Property Length -Sum).Sum
            $sizeGB = [math]::Round($size / 1GB, 2)
            $results += [PSCustomObject]@{
                Parent = $dir.Name
                Folder = $sub.Name
                SizeGB = $sizeGB
            }
        }
    }
}

$results | Sort-Object SizeGB -Descending | Select-Object -First 20 | Format-Table -AutoSize

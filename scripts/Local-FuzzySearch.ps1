# Local-FuzzySearch.ps1
# 本地文件自然语言模糊搜索工具
# 使用方法: .\Local-FuzzySearch.ps1 "搜索关键词" [搜索路径]

param(
    [Parameter(Mandatory=$true)]
    [string]$Keyword,
    
    [Parameter(Mandatory=$false)]
    [string]$SearchPath = "C:\Users\Administrator\.openclaw\workspace",
    
    [Parameter(Mandatory=$false)]
    [int]$MaxResults = 20
)

Write-Host "🔍 搜索关键词: $Keyword" -ForegroundColor Cyan
Write-Host "📂 搜索路径: $SearchPath" -ForegroundColor Cyan
Write-Host ""

# 如果是中文关键词，尝试简繁转换
$keywords = @($Keyword)

# 常见简繁对照
$simpleToTraditional = @{
    "项目" = "項目"
    "动画" = "動畫"
    "铁路" = "鐵路"
    "施工" = "施工"
    "演示" = "演示"
    "合同" = "合同"
    "桥梁" = "橋樑"
    "建设" = "建設"
    "工程" = "工程"
}

foreach ($key in $simpleToTraditional.Keys) {
    if ($Keyword -like "*$key*") {
        $trad = $simpleToTraditional[$key]
        $altKeyword = $Keyword -replace $key, $trad
        $keywords += $altKeyword
    }
}

Write-Host "📋 搜索变体: $($keywords -join ', ')" -ForegroundColor Yellow
Write-Host ""

$results = @()
$searchPatterns = @()

# 生成搜索模式
foreach ($kw in $keywords) {
    # 提取关键字符
    $chars = $kw.ToCharArray()
    foreach ($char in $chars) {
        if ($char -notmatch '[a-zA-Z0-9]' -and $char -notin $searchPatterns) {
            $searchPatterns += $char
        }
    }
}

Write-Host "🔤 搜索字符: $($searchPatterns -join ' ')" -ForegroundColor Yellow

# 搜索文件
try {
    $files = Get-ChildItem -Path $SearchPath -Recurse -File -ErrorAction SilentlyContinue | 
             Where-Object { $_.Extension -in @('.pdf', '.docx', '.doc', '.txt', '.md', '.xlsx', '.xls', '.pptx', '.ppt') }
    
    foreach ($file in $files) {
        $score = 0
        $matchedPatterns = @()
        
        $fileName = $file.Name
        $filePath = $file.FullName
        
        # 检查每个关键词变体
        foreach ($kw in $keywords) {
            if ($fileName -like "*$kw*") {
                $score += 50
                $matchedPatterns += $kw
            }
            if ($filePath -like "*$kw*") {
                $score += 30
            }
        }
        
        # 检查关键字符匹配
        foreach ($pattern in $searchPatterns) {
            if ($fileName -like "*$pattern*") {
                $score += 5
            }
        }
        
        # 中铁/24局 特殊匹配
        if ($Keyword -like "*24局*" -or $Keyword -like "*中铁*") {
            if ($fileName -match "24|二十四|中铁") {
                $score += 20
            }
        }
        
        # 合同关键词
        if ($Keyword -like "*合同*") {
            if ($fileName -like "*合同*") {
                $score += 30
            }
        }
        
        if ($score -gt 0) {
            $results += [PSCustomObject]@{
                Score = $score
                Name = $fileName
                Path = $filePath
                Size = "{0:N2} MB" -f ($file.Length / 1MB)
                MatchedPatterns = ($matchedPatterns -join ', ')
            }
        }
    }
    
    # 按分数排序
    $results = $results | Sort-Object -Property Score -Descending | Select-Object -First $MaxResults
    
    if ($results.Count -gt 0) {
        Write-Host "✅ 找到 $($results.Count) 个结果:" -ForegroundColor Green
        Write-Host ""
        foreach ($r in $results) {
            Write-Host "[分数: $($r.Score)] $($r.Name)" -ForegroundColor White
            Write-Host "   路径: $($r.Path)" -ForegroundColor Gray
            Write-Host "   大小: $($r.Size)" -ForegroundColor Gray
            Write-Host ""
        }
    } else {
        Write-Host "❌ 未找到匹配的文件" -ForegroundColor Red
    }
    
} catch {
    Write-Host "❌ 搜索出错: $_" -ForegroundColor Red
}

# 返回结果供后续使用
return $results
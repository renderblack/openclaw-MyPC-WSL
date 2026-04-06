# hybrid-search.ps1 - Local File Hybrid Search Tool
# Uses: ripgrep (content) + Everything/es.exe (filename)
# Usage: .\hybrid-search.ps1 <keyword> [-dir <dir>] [-type content|name|all] [-ext <ext>]

param(
    [Parameter(Mandatory=$true, Position=0)]
    [string]$Keyword,
    
    [Parameter(Mandatory=$false)]
    [string]$Dir = "C:\Users\Administrator\.openclaw\workspace",
    
    [Parameter(Mandatory=$false)]
    [ValidateSet("content", "name", "all")]
    [string]$Type = "all",
    
    [Parameter(Mandatory=$false)]
    [string]$Ext = "",
    
    [Parameter(Mandatory=$false)]
    [int]$MaxResults = 30
)

$ErrorActionPreference = "SilentlyContinue"
$startTime = Get-Date
$esExe = "C:\ProgramData\chocolatey\lib\es\tools\es.exe"

Write-Host "=== Hybrid Search ===" -ForegroundColor Cyan
Write-Host "Keyword: $Keyword" -ForegroundColor White
Write-Host "Directory: $Dir" -ForegroundColor White
Write-Host "Mode: $Type" -ForegroundColor White
if ($Ext) { Write-Host "Extension: $Ext" -ForegroundColor White }
Write-Host ""

$results = @()
$errors = @()

# ========== 1. Filename Search (Everything) ==========
if ($Type -eq "name" -or $Type -eq "all") {
    Write-Host "[1/2] Filename search (Everything)..." -ForegroundColor Yellow
    
    $searchQuery = $Keyword
    if ($Ext) { $searchQuery = "$searchQuery ext:$Ext" }
    
    # Use cmd /c to avoid PowerShell IPC issues with es.exe
    $esCmd = "cmd /c `"$esExe`" $searchQuery -path `"$Dir`" -max-results $MaxResults -sort name"
    
    try {
        $esOutput = Invoke-Expression $esCmd 2>&1
        
        if ($LASTEXITCODE -eq 0 -and $esOutput) {
            $fileResults = $esOutput -split "`n" | Where-Object { $_.Trim() -ne "" }
            foreach ($file in $fileResults) {
                $results += [PSCustomObject]@{
                    Type = "name"
                    File = $file.Trim()
                    Line = ""
                    Content = ""
                }
            }
            Write-Host "  -> Found $($fileResults.Count) files" -ForegroundColor Green
        } else {
            Write-Host "  -> No matching filenames found" -ForegroundColor Gray
        }
    } catch {
        Write-Host "  -> ES CLI Error: $_" -ForegroundColor Red
        $errors += "ES CLI: $_"
    }
}

# ========== 2. Content Search (ripgrep) ==========
if ($Type -eq "content" -or $Type -eq "all") {
    Write-Host "[2/2] Content search (ripgrep)..." -ForegroundColor Yellow
    
    $rgExt = ""
    if ($Ext) { 
        if ($Ext -match "^\*?\.") { $rgExt = $Ext }
        else { $rgExt = "*.$Ext" }
    }
    
    $rgArgs = @(
        "-i",
        "--max-count", $MaxResults,
        "--json"
    )
    if ($rgExt) { $rgArgs += "--glob=$rgExt" }
    $rgArgs += $Keyword
    $rgArgs += $Dir
    
    try {
        $rgOutput = & rg @rgArgs 2>&1
        
        if ($LASTEXITCODE -ge 0) {
            $jsonResults = $rgOutput | Where-Object { $_ -match "^\{" }
            foreach ($line in $jsonResults) {
                try {
                    $obj = $line | ConvertFrom-Json
                    if ($obj.type -eq "match") {
                        $results += [PSCustomObject]@{
                            Type = "content"
                            File = $obj.data.path.text
                            Line = $obj.data.line_number
                            Content = $obj.data.lines.text.Trim()
                        }
                    }
                } catch { }
            }
            $contentCount = ($results | Where-Object { $_.Type -eq "content" }).Count
            Write-Host "  -> Found $contentCount matches" -ForegroundColor Green
        }
        
        if ($LASTEXITCODE -eq 1) {
            Write-Host "  -> No matching content found" -ForegroundColor Gray
        }
    } catch {
        Write-Host "  -> ripgrep Error: $_" -ForegroundColor Red
        $errors += "ripgrep: $_"
    }
}

# ========== Output Results ==========
Write-Host ""
Write-Host "=== Results ($($results.Count) items) ===" -ForegroundColor Cyan

if ($results.Count -eq 0) {
    Write-Host "No results found" -ForegroundColor Gray
    if ($errors) {
        Write-Host ""
        Write-Host "Errors:" -ForegroundColor Red
        foreach ($e in $errors) { Write-Host "  - $e" -ForegroundColor Red }
    }
    exit 1
}

# Group by file
$grouped = $results | Group-Object File | Select-Object -First $MaxResults

foreach ($group in $grouped) {
    Write-Host ""
    Write-Host "File: $($group.Name)" -ForegroundColor White
    
    if ($group.Group[0].Type -eq "name") {
        Write-Host "   (filename match)" -ForegroundColor Gray
    } else {
        foreach ($item in $group.Group | Select-Object -First 3) {
            Write-Host "   $($item.Line): $($item.Content)" -ForegroundColor Gray
        }
        if ($group.Count -gt 3) {
            Write-Host "   ... and $($group.Count - 3) more matches" -ForegroundColor DarkGray
        }
    }
}

$elapsed = (Get-Date) - $startTime
Write-Host ""
Write-Host "Time: $($elapsed.TotalSeconds.ToString('0.00'))s" -ForegroundColor Cyan

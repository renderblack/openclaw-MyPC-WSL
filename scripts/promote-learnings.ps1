# promote-learnings.ps1 - Auto-promote learnings from .learnings/ to MEMORY.md, AGENTS.md, TOOLS.md
# Usage: powershell -ExecutionPolicy Bypass -File scripts\promote-learnings.ps1

$ErrorActionPreference = "Stop"

# Paths
$Workspace = "C:\Users\Administrator\.openclaw\workspace"
$LearningsDir = Join-Path $Workspace ".learnings"
$MemoryFile = Join-Path $Workspace "MEMORY.md"
$AgentsFile = Join-Path $Workspace "AGENTS.md"
$ToolsFile = Join-Path $Workspace "TOOLS.md"

# Color output
function Write-Colored {
    param([string]$Text, [string]$Color)
    $oldColor = $Host.UI.RawUI.ForegroundColor
    $Host.UI.RawUI.ForegroundColor = $Color
    Write-Host $Text
    $Host.UI.RawUI.ForegroundColor = $oldColor
}

Write-Colored "🧠 Starting learning promotion check..." "Green"

# Check directory
if (-not (Test-Path $LearningsDir)) {
    Write-Colored "❌ .learnings/ directory not found" "Red"
    exit 1
}

# Counters
$errorCount = 0
$learningCount = 0
$featureCount = 0

# 1. Check ERRORS.md
$ErrorsFile = Join-Path $LearningsDir "ERRORS.md"
if (Test-Path $ErrorsFile) {
    Write-Colored "📋 Checking ERRORS.md..." "Yellow"
    $content = Get-Content $ErrorsFile -Raw
    $recentErrors = [regex]::Matches($content, '\[\d{4}-\d{2}-\d{2}\].*?Fix:')
    $errorCount = $recentErrors.Count
    if ($errorCount -gt 0) {
        Write-Colored "  Found $errorCount recent error records" "Cyan"
    }
}

# 2. Check LEARNINGS.md
$LearningsFile = Join-Path $LearningsDir "LEARNINGS.md"
if (Test-Path $LearningsFile) {
    Write-Colored "📋 Checking LEARNINGS.md..." "Yellow"
    $content = Get-Content $LearningsFile -Raw
    $bestPractices = ([regex]::Matches($content, 'best_practice')).Count
    $insights = ([regex]::Matches($content, 'insight')).Count
    if ($bestPractices -gt 0) {
        Write-Colored "  Found $bestPractices best_practices" "Cyan"
    }
    if ($insights -gt 0) {
        Write-Colored "  Found $insights insights" "Cyan"
    }
    $learningCount = $bestPractices + $insights
}

# 3. Check FEATURE_REQUESTS.md
$FeaturesFile = Join-Path $LearningsDir "FEATURE_REQUESTS.md"
if (Test-Path $FeaturesFile) {
    Write-Colored "📋 Checking FEATURE_REQUESTS.md..." "Yellow"
    $content = Get-Content $FeaturesFile -Raw
    $pendingFeatures = ([regex]::Matches($content, 'Status: Pending')).Count
    if ($pendingFeatures -gt 0) {
        Write-Colored "  Found $pendingFeatures pending features" "Cyan"
    }
    $featureCount = $pendingFeatures
}

# Summary
Write-Host ""
Write-Colored "📊 Summary:" "Green"
Write-Host "  - Recent errors: $errorCount"
Write-Host "  - Learning records: $learningCount"
Write-Host "  - Pending features: $featureCount"
Write-Host ""

if (($errorCount + $learningCount + $featureCount) -eq 0) {
    Write-Colored "✅ No content to promote" "Green"
    exit 0
}

Write-Colored "⚠️  Found content to promote. Please check manually:" "Yellow"
Write-Host "  - $ErrorsFile"
Write-Host "  - $LearningsFile"
Write-Host "  - $FeaturesFile"
Write-Host ""
Write-Colored "💡 Recommendations:" "Green"
Write-Host "  1. Open the files above and confirm what needs promotion"
Write-Host "  2. Copy general learnings to $MemoryFile"
Write-Host "  3. Copy workflow improvements to $AgentsFile"
Write-Host "  4. Copy tool tips to $ToolsFile"
Write-Host ""
Write-Colored "🎉 Check complete" "Green"

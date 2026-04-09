$url = 'https://www.baidu.com/s?wd=%E5%89%91%E6%A1%A5%E4%BA%8B%E6%95%85&rn=5'
$req = Invoke-WebRequest -Uri $url -Headers @{'User-Agent'='Mozilla/5.0'} -Proxy 'http://127.0.0.1:7890' -TimeoutSec 15 -UseBasicParsing
$html = [System.Text.Encoding]::UTF8.GetString($req.Content)
Write-Host "Length:" $html.Length

if ($html -match 'aria-label') {
    Write-Host "Found aria-label"
} else {
    Write-Host "No aria-label found"
}

# Check for c-title pattern
if ($html -match 'c-title') {
    Write-Host "Found c-title"
} else {
    Write-Host "No c-title found"
}

# Show a sample of the HTML around c-title
$idx = $html.IndexOf('c-title')
if ($idx -gt 0) {
    Write-Host "---c-title context---"
    Write-Host $html.Substring($idx, 500)
}

# Remove deepseek from OpenClaw config
$configPath = "$env:USERPROFILE\.openclaw\openclaw.json"
$json = Get-Content $configPath -Raw | ConvertFrom-Json

# 1. Remove deepseek from providers
$json.models.providers.PSObject.Properties.Remove('deepseek')

# 2. Remove deepseek/deepseek-chat from agents.defaults.models
$json.agents.defaults.models.PSObject.Properties.Remove('deepseek/deepseek-chat')

# 3. Remove deepseek:default from auth.profiles
$json.auth.profiles.PSObject.Properties.Remove('deepseek:default')

# Save
$json | ConvertTo-Json -Depth 20 | Set-Content $configPath -Encoding UTF8

Write-Host "DeepSeek models removed successfully"
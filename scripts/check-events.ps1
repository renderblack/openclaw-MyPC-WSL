# Check Task Scheduler events related to OpenClaw
try {
    $events = Get-WinEvent -FilterHashtable @{
        LogName='System'
        ProviderName='Microsoft-Windows-TaskScheduler'
    } -MaxEvents 50 -ErrorAction SilentlyContinue | Where-Object {
        $_.Message -like '*OpenClaw*' -or $_.Message -like '*gateway*' -or $_.Message -like '*267009*'
    }
    
    if ($events) {
        foreach ($e in $events) {
            Write-Host "Time: $($e.TimeCreated)"
            Write-Host "ID: $($e.Id)"
            Write-Host "Message: $($e.Message)"
            Write-Host "---"
        }
    } else {
        Write-Host "No OpenClaw-related Task Scheduler events found"
    }
} catch {
    Write-Host "Error: $_"
}

# Also check the Operational log
Write-Host "=== TaskScheduler Operational ==="
try {
    $opEvents = Get-WinEvent -FilterHashtable @{
        LogName='Microsoft-Windows-TaskScheduler/Operational'
    } -MaxEvents 30 -ErrorAction SilentlyContinue | Where-Object {
        $_.Message -like '*OpenClaw*' -or $_.Message -like '*gateway*'
    }
    
    if ($opEvents) {
        foreach ($e in $opEvents) {
            Write-Host "Time: $($e.TimeCreated)"
            Write-Host "ID: $($e.Id)"
            Write-Host "Message: $($e.Message.Substring(0, [Math]::Min(300, $_.Message.Length)))"
            Write-Host "---"
        }
    } else {
        Write-Host "No OpenClaw events in Operational log"
    }
} catch {
    Write-Host "Operational Error: $_"
}

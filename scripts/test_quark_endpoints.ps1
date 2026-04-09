# Test various Quark API endpoints
$endpoints = @(
    "http://127.0.0.1:9128/",
    "http://127.0.0.1:9128/api",
    "http://127.0.0.1:9128/api/v1",
    "http://127.0.0.1:9128/file",
    "http://127.0.0.1:9128/upload",
    "http://127.0.0.1:9128/cloud",
    "http://127.0.0.1:9128/user",
    "http://127.0.0.1:9128/quark",
    "http://127.0.0.1:9128/pcs"
)

foreach ($endpoint in $endpoints) {
    try {
        $r = Invoke-WebRequest -Uri $endpoint -TimeoutSec 3 -ErrorAction Stop
        Write-Host "$endpoint -> $($r.StatusCode)"
    } catch {
        Write-Host "$endpoint -> Error: $($_.Exception.Response.StatusCode)"
    }
}

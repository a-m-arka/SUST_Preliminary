$ErrorActionPreference = 'SilentlyContinue'
$conns = Get-NetTCPConnection -LocalPort 8000 -State Listen
foreach ($c in $conns) {
  $p = $c.OwningProcess
  Write-Host "Killing PID $p"
  Stop-Process -Id $p -Force
}
Start-Sleep -Seconds 1
$left = (Get-NetTCPConnection -LocalPort 8000 -State Listen -ErrorAction SilentlyContinue | Measure-Object).Count
Write-Host "Listeners remaining: $left"
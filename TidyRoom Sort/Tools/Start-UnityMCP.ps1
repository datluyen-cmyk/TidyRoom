$ErrorActionPreference='Stop'
$toolUv=Join-Path $env:USERPROFILE '.local\bin\uvx.exe'
if (-not (Test-Path -LiteralPath $toolUv)) { $toolUv=(Get-Command uvx).Source }
if (Get-NetTCPConnection -LocalPort 8080 -State Listen -ErrorAction SilentlyContinue) {
    Write-Host 'Port 8080 is already listening. Unity: Tidy Room > Connect Unity MCP.'
    exit 0
}
$logDir=Join-Path (Split-Path $PSScriptRoot) 'Evidence'
New-Item -ItemType Directory -Force -Path $logDir | Out-Null
Start-Process -FilePath $toolUv -ArgumentList '--from','mcpforunityserver==10.3.0','mcp-for-unity','--transport','http','--http-url','http://127.0.0.1:8080' -WindowStyle Hidden -RedirectStandardOutput (Join-Path $logDir 'mcp-server.log') -RedirectStandardError (Join-Path $logDir 'mcp-server-error.log')
Write-Host 'Started local Unity MCP. Unity: Tidy Room > Connect Unity MCP.'

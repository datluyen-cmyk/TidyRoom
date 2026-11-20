$ErrorActionPreference = 'Stop'
$studioUrl = 'http://127.0.0.1:37846'
function Test-Studio {
    try { return (Invoke-WebRequest -Uri "$studioUrl/" -UseBasicParsing -TimeoutSec 1).Content.Contains('Tidy Room Level Studio') } catch { return $false }
}
try {
    if (-not (Test-Studio)) {
        $studioNode = Join-Path $env:USERPROFILE '.cache\codex-runtimes\codex-primary-runtime\dependencies\node\bin\node.exe'
        if (-not (Test-Path -LiteralPath $studioNode)) {
            $foundNode = Get-Command node.exe -ErrorAction SilentlyContinue
            if (-not $foundNode) { throw 'Cần Node.js 20 trở lên để mở Level Studio.' }
            $studioNode = $foundNode.Source
        }
        $entry = Join-Path $PSScriptRoot 'server.js'
        $studioProcess = Start-Process -FilePath $studioNode -ArgumentList @('"' + $entry + '"') -WorkingDirectory $PSScriptRoot -WindowStyle Hidden -PassThru
        for ($i = 0; $i -lt 35; $i++) {
            if (Test-Studio) { break }
            if ($studioProcess.HasExited) { throw 'Không khởi động được Level Studio. Kiểm tra cổng 37846.' }
            Start-Sleep -Milliseconds 150
        }
        if (-not (Test-Studio)) { throw 'Level Studio chưa phản hồi.' }
    }
    Start-Process -FilePath $studioUrl
} catch {
    Add-Type -AssemblyName System.Windows.Forms
    [System.Windows.Forms.MessageBox]::Show($_.Exception.Message, 'Tidy Room Level Studio') | Out-Null
}

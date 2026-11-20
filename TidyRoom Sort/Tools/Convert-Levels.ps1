param(
    [string]$HappyRoot = (Join-Path $PSScriptRoot '..\..\APK\HappyTidyRoom'),
    [string]$RoomRoot = (Join-Path $PSScriptRoot '..\..\APK\RoomSort'),
    [string]$TidyRoomApks = (Join-Path $PSScriptRoot '..\..\APK\Tidy Room\Tidy-Room_57_apkcube.apks'),
    [string]$PythonPath = 'python',
    [string]$NodePath = 'node'
)
$ErrorActionPreference='Stop'
if (-not (Test-Path -LiteralPath $PythonPath)) { $PythonPath=(Get-Command python).Source }
if (-not (Test-Path -LiteralPath $NodePath)) { $NodePath=(Get-Command node).Source }
$env:PYTHONIOENCODING='utf-8'
& $NodePath (Join-Path $PSScriptRoot 'prepare_sources.mjs') (Join-Path $RoomRoot 'analysis')
if ($LASTEXITCODE -ne 0) { throw 'Preparing RoomSort sources failed' }
& $PythonPath (Join-Path $PSScriptRoot 'convert_levels.py') --happy-root $HappyRoot --room-root $RoomRoot
if ($LASTEXITCODE -ne 0) { throw 'Conversion failed' }
& $NodePath (Join-Path $PSScriptRoot 'bake_reference_rules.mjs') (Join-Path $RoomRoot 'analysis')
if ($LASTEXITCODE -ne 0) { throw 'Baking source collision failed' }
& $PythonPath (Join-Path $PSScriptRoot 'export_happy_ui.py') (Join-Path $HappyRoot 'analysis')
if ($LASTEXITCODE -ne 0) { throw 'Importing Happy backgrounds failed' }
& $PythonPath (Join-Path $PSScriptRoot 'pack_levels.py')
if ($LASTEXITCODE -ne 0) { throw 'Packing runtime levels failed' }
if ($TidyRoomApks) {
    & $PythonPath (Join-Path $PSScriptRoot 'import_tidy_room_art.py') --apks $TidyRoomApks --room-root $RoomRoot --vendor (Join-Path $HappyRoot 'analysis/vendor')
    if ($LASTEXITCODE -ne 0) { throw 'Importing Tidy Room art failed' }
}
Write-Host 'Done. Unity: Tidy Room > Validate Conversion and Gameplay, then Open Level Test.'

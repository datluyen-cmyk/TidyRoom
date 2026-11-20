@echo off
setlocal
pushd "%~dp0"
python "%~dp0open_tool.py"
if errorlevel 1 pause
popd

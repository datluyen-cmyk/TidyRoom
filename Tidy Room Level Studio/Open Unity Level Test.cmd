@echo off
setlocal
set "tidyEditor=%ProgramFiles%\Unity\Hub\Editor\2022.3.62f2\Editor\Unity.exe"
set "tidyProject=%~dp0Unity Level Test"
if not exist "%tidyEditor%" (
  echo Unity 2022.3.62f2 was not found in the default Unity Hub location.
  echo Open the Unity Level Test project through Unity Hub instead.
  pause
  exit /b 1
)
if exist "%tidyProject%\Temp\UnityLockfile" (
  echo If Unity Level Test is already open, go to its Game tab.
  echo If it is not playing, use Tidy Room ^> Play Level Test.
  pause
  exit /b 0
)
start "Unity Level Test" "%tidyEditor%" -projectPath "%tidyProject%" -executeMethod TidyPreviewEditor.OpenForPlay -logFile "%tidyProject%\editor-unity.log"

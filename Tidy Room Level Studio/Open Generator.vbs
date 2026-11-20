Option Explicit
Dim sh, fs, p, q
Set sh = CreateObject("WScript.Shell")
Set fs = CreateObject("Scripting.FileSystemObject")
p = fs.BuildPath(fs.GetParentFolderName(WScript.ScriptFullName), "Open-Generator.ps1")
q = Chr(34)
sh.Run "powershell.exe -NoProfile -ExecutionPolicy Bypass -File " & q & p & q, 0, False

. "$PSScriptRoot\SchmodVars.ps1"

$CodeCMD = "py " + $env:TOOLS_ROOT + "\Python\schmod\schmod_launcher\tray_launcher.py"
Write-Output ($CodeCMD)
Invoke-Expression $CodeCMD
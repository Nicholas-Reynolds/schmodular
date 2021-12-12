param (
    [string][ValidateNotNullOrEmpty()][ValidateNotNull()]$hipFile
)

. "$PSScriptRoot\SchmodVars.ps1"

if (($null -eq $hipFile) -or ($hipFile -eq ''))
{
    Start-Process -FilePath "houdinifx.exe" -WorkingDirectory $env:HOUDINI_BIN
}
else
{
    Write-Host ("Hip File: " + $hipFile)
    Start-Process -FilePath "houdinifx.exe" -WorkingDirectory $env:HOUDINI_BIN -ArgumentList "$hipFile"   
}
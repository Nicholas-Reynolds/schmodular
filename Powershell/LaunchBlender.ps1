param (
    [string][ValidateNotNullOrEmpty()][ValidateNotNull()]$projectPath,
    [string][ValidateNotNullOrEmpty()][ValidateNotNull()]$pythonScript
)

. "$PSScriptRoot\SchmodVars.ps1"

if (($null -eq $projectPath) -or ($projectPath -eq ''))
{
    Start-Process -FilePath 'blender.exe' -WorkingDirectory $env:BLENDER_BIN
}
else
{
    Start-Process -FilePath 'blender.exe' -WorkingDirectory $env:BLENDER_BIN -ArgumentList $projectPath
}


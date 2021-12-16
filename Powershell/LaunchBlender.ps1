param (
    [string]$projectPath,
    [string]$pythonScript
)

. "$PSScriptRoot\SchmodVars.ps1"

if (($null -eq $projectPath) -or ($projectPath -eq ''))
{
    Start-Process -FilePath 'blender.exe' -WorkingDirectory $env:BLENDER_BIN
}
else
{
    $pathQuote = '"' + $projectPath + '"'
    
    Write-Host ("Project Path: " + $pathQuote)
    Start-Process -FilePath 'blender.exe' -WorkingDirectory $env:BLENDER_BIN -ArgumentList $pathQuote
}


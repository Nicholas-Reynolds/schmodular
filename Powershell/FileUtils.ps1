function SearchForParentDirectory([string]$searchParam, [bool]$startsWith=$false)
{
    $currentDir = $PSScriptRoot
    Write-Host ('Searching ' + $currentDir + ' for ' + $searchParam)

    $tempToolsRoot = ''
    while ($tempToolsRoot -eq '')
    {
        $childDirectories = [System.IO.Directory]::GetDirectories($currentDir)

        foreach ($dir in $childDirectories)
        {
            $lowestDir = Split-Path -Path $dir -Leaf

            $foundDir = $false
            if ($startsWith -eq $true)
            {
                $foundDir = $lowestDir.StartsWith($searchParam)
            }
            else
            {
                $foundDir = $lowestDir.EndsWith($searchParam)
            }

            if ($foundDir)
            {
                $tempToolsRoot = $dir
                Write-Host ("Found Directory at: " + $tempToolsRoot)
                return $tempToolsRoot
            }
        }

        $currentDir = [System.IO.Directory]::GetParent($currentDir)
        if ($null -eq $currentDir)
        {
            Write-Host ("No dir found for: " + $searchParam)
            Break
        }
    }

    return $tempToolsRoot
}

function SearchForFirstChildDirectory([string]$startDir, [string]$searchParam, [bool]$checkForNumber=$false)
{
    # C:\Program Files\Side Effects Software
    $outDir = ''
    $directories = Get-ChildItem -Path $startDir -Directory -Name
    foreach ($dir in $directories)
    {
        if ($dir.StartsWith($searchParam))
        {
            if ($checkForNumber)
            {
                if ($dir -match '\d')
                {
                    $outDir = $dir
                }
            }
            else
            {
                $outDir = $dir
            }
        }
    }

    return [string]$outDir
}

function ParseNumberFromString([string]$inStr)
{
    $Out = $inStr -replace("[^\d]")
    try
    {
        return [int]$Out
    }
    catch
    {

    }
    try
    {
        return [uint64]$Out
    }
    catch
    {
        return 0
    }
}
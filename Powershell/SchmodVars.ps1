# Include
. "$PSScriptRoot\FileUtils.ps1"

# Get Dev Root
$env:DEV_ROOT = SearchForParentDirectory 'Dev' $false
if ($env:DEV_ROOT -eq '') { Exit }
# Get Tools Paths
$env:TOOLS_ROOT = Join-Path -Path $env:DEV_ROOT -ChildPath 'Tools'
# Get External Root
$env:EXTERNAL_ROOT = Join-Path -Path $env:DEV_ROOT -ChildPath 'External'

# Setup Python Env Vars
$env:PYTHON_ROOT = Join-Path -Path $env:EXTERNAL_ROOT -ChildPath 'Python310'
$PYTHON_SCRIPTS = Join-Path -Path $env:TOOLS_ROOT -ChildPath 'Python'
$BLENDER_PY_SCRIPTS = Join-Path -Path $env:TOOLS_ROOT -ChildPath 'Blender\Python'
$HOUDINI_PY_SCRIPTS = Join-Path -Path $env:TOOLS_ROOT -ChildPath 'Houdini\Python'
$UNREAL_PY_SCRIPTS = Join-Path -Path $env:TOOLS_ROOT -ChildPath 'Unreal\Python'
$env:PYTHONPATH = "$PYTHON_ROOT;$PYTHON_SCRIPTS;$BLENDER_PY_SCRIPTS;$HOUDINI_PY_SCRIPTS;$UNREAL_PY_SCRIPTS"

# Setup Powershell Env Vars
$env:POWERSHELL_SCRIPTS = Join-Path -Path $env:TOOLS_ROOT -ChildPath 'Powershell'

# Setup Houdini Env Vars
$env:HOUDINI_VERSION = (SearchForFirstChildDirectory 'C:\Program Files\Side Effects Software' 'Houdini' $true).Split(' ')[1]
$env:HOUDINI_BIN = 'C:\Program Files\Side Effects Software' + "\Houdini $env:HOUDINI_VERSION\bin"
$env:HOUDINI_EXE = Join-Path -Path $env:HOUDINI_BIN -ChildPath 'houdinifx.exe'
$env:HOUDINI_OTLSCAN_PATH = 'D:\Dev\Media\_Library\HDA;&'
$env:HOUDINI_PATH = "$HOUDINI_PY_SCRIPTS;&"

# Setup Blender Env Vars
$env:BLENDER_VERSION = (SearchForFirstChildDirectory 'C:\Program Files\Blender Foundation' 'Blender' $true).Split(' ')[1]
$env:BLENDER_BIN = 'C:\Program Files\Blender Foundation' + "\Blender $env:BLENDER_VERSION"
$env:BLENDER_EXE = Join-Path -Path $env:BLENDER_BIN -ChildPath 'blender.exe'
$env:BLENDER_USER_SCRIPTS = Join-Path -Path $BLENDER_PY_SCRIPTS -ChildPath 'blender'

# Setup Pico-8 Env Vars
# TODO: Find this as opposed to abs
$env:PICO8_EXE = 'C:\Program Files (x86)\PICO-8\pico8.exe'

# Set Location
Set-Location -Path $env:DEV_ROOT
import sys
import os
import pathlib
import subprocess

from schmod.schmod_utils import file_utils

def getFileHistory():
    ## Get base unreal directories
    home_path = pathlib.Path.home()

    app_data_path = ''
    if sys.platform == 'win32':
        app_data_path = home_path / 'AppData/'

    # blender_path = app_data_path / 'Roaming\Blender Foundation\Blender\3.0\config'
    blender_path = app_data_path / 'Roaming\Blender Foundation\Blender'
    
    blender_vers = []
    for dir in blender_path.iterdir():
        try:
            blender_vers.append(float(dir.stem))
        except:
            pass
    
    recent_files_path = blender_path / str(max(blender_vers)) / 'config' / 'recent-files.txt'
    if recent_files_path.exists():
        return recent_files_path
    else:
        return ''

def getRecentlyOpenedFiles(skip_valid_dir_check=False):
    split_line_history = str.splitlines(getFileHistory().read_text())
    
    valid_directories = []
    for dir in split_line_history:
        if os.path.exists(dir):
            valid_directories.append(dir)

    return split_line_history if skip_valid_dir_check else valid_directories

def launchWithProject(project_path):
    input_path = '"{0}"'.format(project_path)
    ps_script = os.getenv("POWERSHELL_SCRIPTS") + r'\LaunchBlender.ps1'
    cmd = ["powershell.exe", ps_script, input_path]
    subprocess.Popen(cmd)

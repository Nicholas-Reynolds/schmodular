import os
import re
import sys
import pathlib
import subprocess

from schmod.schmod_utils import file_utils

def getFileHistory():
    home_path = pathlib.Path.home()
    
    document_path = ''
    if sys.platform == "win32":
        document_path = home_path / "Documents/"

    houdini_version = ''
    for path in document_path.iterdir():
        if path.name.startswith("houdini"):
            houdini_version = file_utils.getTrailingInt(path.name)
            
            ## Number is float value, or half version
            if(houdini_version < 10):
                houdini_version = file_utils.getTrailingFloat(path.name)

    
    houdini_doc_path = document_path / ("houdini" + str(houdini_version))
    final_path = houdini_doc_path / "file.history"

    return final_path

def getRecentlyOpenedFiles(skip_valid_dir_check=False):
    ## HIP{
    recent_houdini_projects_buffer = file_utils.getSubstringBetweenStringFromFile(
                                        getFileHistory(),
                                        'HIP\n{',
                                        '}\n')
    
    split_houdini_projects = str.splitlines(recent_houdini_projects_buffer)
    split_houdini_projects.reverse()

    valid_directories = []
    for dir in split_houdini_projects:
        if os.path.exists(dir):
            valid_directories.append(dir)

    return split_houdini_projects if skip_valid_dir_check else valid_directories

def launchWithProject(project_path):
    ps_script = os.getenv("POWERSHELL_SCRIPTS") + r'\LaunchHoudini.ps1'
    cmd = ["powershell.exe", ps_script, project_path]
    subprocess.Popen(cmd)

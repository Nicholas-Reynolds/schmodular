import os
import sys
import pathlib
import subprocess

from schmod.schmod_utils import file_utils

def getFileHistory():
    ## Get base unreal directories
    home_path = pathlib.Path.home()

    app_data_path = ''
    if sys.platform == "win32":
        app_data_path = home_path / "AppData/"
    elif sys.platform == "linux":
        app_data_path = home_path / ".local/share"
    elif sys.platform == "darwin":
        app_data_path = home_path / "Library/Application Support"

    unreal_path = app_data_path / 'Local/UnrealEngine/'

    ## Get highest engine version
    engine_versions = []
    for path in unreal_path.iterdir():
        try:
            engine_num = float(path.parts[-1])
            engine_versions.append(path.parts[-1])
        except:
            print ('')

    highest_engine_version_path = unreal_path / (str(max(engine_versions)) + '/')
    final_path = highest_engine_version_path / 'Saved/Config/Windows/EditorSettings.ini'

    return final_path

def getRecentlyOpenedFiles(skip_valid_dir_check=False):
    recent_unreal_projects_buffer = file_utils.getSubstringBetweenStringFromFile(
                                    getFileHistory(),
                                    '[/Script/UnrealEd.EditorSettings]',
                                    '[/Script/IntroTutorials.TutorialStateSettings]')

    split_unreal_projects = str.splitlines(recent_unreal_projects_buffer)

    project_begin = 'RecentlyOpenedProjectFiles='
    projects_only = []
    for line in split_unreal_projects:
        if(line.startswith(project_begin)):
            projects_only.append(line.split(project_begin)[-1])

    valid_directories = []
    for dir in projects_only:
        if os.path.exists(dir):
            valid_directories.append(dir)
    
    return projects_only if skip_valid_dir_check else valid_directories

def launchWithProject(project_path):
    engine_path = r'C:\Program Files\Epic Games\UE_4.27\Engine\Binaries\Win64\UE4Editor.exe'
    fixed_project_path = '"' + project_path + '"'
    subprocess.Popen([engine_path, fixed_project_path])
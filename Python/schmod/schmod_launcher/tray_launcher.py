import sys
import os
import subprocess

import unreal.application
import houdini.application
import blender.application

from schmod.schmod_command_server import command_server_ui

from PyQt5 import QtCore, QtGui, QtWidgets

class TrayLauncher(QtWidgets.QSystemTrayIcon):
    def __init__(self, icon, parent=None):
        QtWidgets.QSystemTrayIcon.__init__(self, icon, parent)

        self.setToolTip("Schmod Launcher")
        self.main_menu = QtWidgets.QMenu(parent)

        # Vars
        self.unreal_recent_projects = []
        self.houdini_recent_projects = []
        self.blender_recent_projects = []

        self.unreal_project_menu = None
        self.launch_unreal_action = None
        self.houdini_project_menu = None
        self.launch_houdini_action = None
        self.blender_project_menu = None
        self.launch_blender_action = None
        self.launch_vscode_action = None
        self.launch_powershell_action = None
        self.launch_pico8_action = None
        self.close_launcher_action = None

        # UI
        self.initialize_class_variables()
        self.build_ui(parent)
        self.populate_ui()
        self.make_connections()

        # Add Context Menu
        self.setContextMenu(self.main_menu)
        self.activated.connect(self.onTrayIconActivated)

    def initialize_class_variables(self):
        self.unreal_recent_projects = unreal.application.getRecentlyOpenedFiles()
        self.houdini_recent_projects = houdini.application.getRecentlyOpenedFiles()
        self.blender_recent_projects = blender.application.getRecentlyOpenedFiles()

    def build_ui(self, parent):
        # Add Unreal Menu
        self.unreal_project_menu = QtWidgets.QMenu(parent)
        self.unreal_project_menu.setTitle('Unreal')
        self.launch_unreal_action = self.unreal_project_menu.addAction("Launch Unreal")
        self.unreal_project_menu.addSeparator()
        self.main_menu.addMenu(self.unreal_project_menu)

        self.setContextMenu(self.main_menu)
        self.activated.connect(self.onTrayIconActivated)

        # Add Houdini Menu
        self.houdini_project_menu = QtWidgets.QMenu(parent)
        self.houdini_project_menu.setTitle("Houdini")
        self.launch_houdini_action = self.houdini_project_menu.addAction("Launch Houdini")
        self.houdini_project_menu.addSeparator()
        self.main_menu.addMenu(self.houdini_project_menu)

        # Add Blender Menu
        self.blender_project_menu = QtWidgets.QMenu(parent)
        self.blender_project_menu.setTitle('Blender')
        self.launch_blender_action = self.blender_project_menu.addAction('Launch Blender')
        self.blender_project_menu.addSeparator()
        self.main_menu.addMenu(self.blender_project_menu)

        # Add Schmod Menu
        self.schmod_project_menu = QtWidgets.QMenu(parent)
        self.schmod_project_menu.setTitle('Schmod Tools')
        self.main_menu.addMenu(self.schmod_project_menu)

        self.launch_schmod_command_server_action = self.schmod_project_menu.addAction("Launch Schmod Command Server")

        ## Setup VS Code / Powershell / Pico 8
        self.main_menu.addSeparator()
        self.launch_vscode_action = self.main_menu.addAction("Launch VS Code")
        self.launch_powershell_action = self.main_menu.addAction("Launch Powershell")
        self.launch_pico8_action = self.main_menu.addAction("Launch Pico-8")
        
        ## Setup Close
        self.main_menu.addSeparator()
        self.close_launcher_action = self.main_menu.addAction("Exit")

    def populate_ui(self):
        # Populate Unreal Menu with Recent Projects
        for project in self.unreal_recent_projects:
            cur_action = self.unreal_project_menu.addAction(project)
            cur_action.triggered.connect(
                    lambda checked, 
                    item=cur_action: unreal.application.launchWithProject(item.text())
                    )
        
        # Populate Houdini with Recent Projects
        for project in self.houdini_recent_projects:
            cur_action = self.houdini_project_menu.addAction(project)
            cur_action.triggered.connect(
                    lambda checked, 
                    item=cur_action: houdini.application.launchWithProject(item.text())
                    )
        
        # Populate Blender with Recent Projects
        for project in self.blender_recent_projects:
            cur_action = self.blender_project_menu.addAction(project)
            cur_action.triggered.connect(
                    lambda checked, 
                    item=cur_action: blender.application.launchWithProject(item.text())
                    )
        
    def make_connections(self):
        self.launch_unreal_action.triggered.connect(lambda: unreal.application.launchWithProject(''))
        self.launch_houdini_action.triggered.connect(lambda: houdini.application.launchWithProject(''))
        self.launch_blender_action.triggered.connect(lambda: blender.application.launchWithProject(''))
        self.launch_schmod_command_server_action.triggered.connect(self.temp_launch_command_server)
        self.launch_vscode_action.triggered.connect(self.temp_launch_vs_code)
        self.launch_powershell_action.triggered.connect(self.temp_launch_powershell)
        self.launch_pico8_action.triggered.connect(self.temp_launch_pico_8)
        self.close_launcher_action.triggered.connect(self.quit_launcher)

    def onTrayIconActivated(self, reason):
        if reason == QtWidgets.QSystemTrayIcon.Trigger:
            self.contextMenu().popup(QtGui.QCursor.pos())

    def temp_launch_vs_code(self):
        ## TODO
        ps_script = os.getenv("POWERSHELL_SCRIPTS") + r"\LaunchVSCode.ps1"
        subprocess.Popen(["powershell.exe", ps_script])
    
    def temp_launch_powershell(self):
        ## TODO
        ps_script = os.getenv("POWERSHELL_SCRIPTS") + r"\LaunchSchmodEnvironment.ps1.lnk"
        subprocess.Popen(["powershell.exe", ps_script])

    def temp_launch_pico_8(self):
        ## TODO
        subprocess.Popen([os.getenv('PICO8_EXE')])

    def temp_launch_command_server(self):
        try:
            # TODO
            py_EXE = os.getenv('PYTHON_ROOT') + '\python.exe'
            py_cmd = 'd:/Dev/Tools/Python/schmod/schmod_command_server/command_server_ui.py'
            subprocess.Popen([py_EXE, py_cmd])
        except:
            print ('Test 434')

    def quit_launcher(self):
        sys.exit()

def Show():
    app = QtWidgets.QApplication(sys.argv)

    win = QtWidgets.QWidget()
    icon = QtGui.QIcon('D:\Dev\Tools\Python\schmod\schmod_launcher\icon.png')
    launcher = TrayLauncher(icon, win)
    launcher.show()

    sys.exit(app.exec_())

if __name__ == '__main__':
    Show()
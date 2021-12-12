import sys
from cx_Freeze import setup, Executable

setup(name = "Schmodula Tray Launcher",
      version = "0.01",
      description = "Launcher for Schmodular Pipeline",
      executables = [Executable("tray_launcher.py", base = "Win32GUI")])
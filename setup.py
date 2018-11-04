# -*- coding: utf-8 -*-

import sys
from cx_Freeze import setup, Executable

includefiles = ["style.qss"]
includes = []
excludes = ['Tkinter']
packages = []


base = None
if sys.platform == 'win32':
    base = 'Win32GUI'

executables = [
    Executable('main.py', base=base)
]

setup(name='SpringTerm',
      version='0.1',
      description='Spring Terminal client',
      author="TurBoss",
      options={'build_exe': {'includes': includes,
                             'excludes': excludes,
                             'packages': packages,
                             'include_files': includefiles}},
      executables=executables
)

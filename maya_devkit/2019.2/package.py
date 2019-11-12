name = "maya_devkit"
version = "2019.2"

description = \
"""
Autodesk Maya Devkit
"""

build_command = "python {root}/rezbuild.py {install}"
build_requires = ['python']

variants = [
    ['platform-windows']
]


def commands():
    global env
  
    # Note that the devkitBase folder is: {root}/devkitBase 
    env.MAYA_DEVKIT_LOCATION = "{root}/devkitBase"
    env.MAYA_DEVKIT_INC_DIR = "{root}/devkitBase/include"
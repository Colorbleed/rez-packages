# -*- coding: utf-8 -*-

name = 'alembic'

version = '1.7.12'

variants = [['platform-windows', 'arch==AMD64', "maya-2019"]]

build_command = "python {root}/rezbuild.py {install}"
build_requires = ['python',
                  'visualstudio-2017',
                  'cmake',
                  'openexr-2.2.0'
                  #'hdf5',
                  #'boost-1.55',
                  #'pyilmbase',
                  #'arnold'
                  ]

requires = [
    "openexr-2.2.0",
]

def commands():
    global env
    global request

    env.PATH.prepend("{root}/bin")
    env.LD_LIBRARY_PATH.prepend('{root}/lib/')
    env.PATH.prepend("{root}/lib")
    
    if "maya" in request:
        # Try and get it found before Maya's plug-in path to
        # hopefully force it in front of the built-in Alembic
        # plug-in.
        env.MAYA_PLUG_IN_PATH.prepend("{root}/maya/plug-ins")
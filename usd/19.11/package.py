# -*- coding: utf-8 -*-

name = 'usd'

version = '19.11'

requires = [
    'Jinja2',
    'PyOpenGL'
]

build_command = "python {root}/rezbuild.py {install}"
build_requires = ['python-2',
                  'cmake-3.2+',
                  'visualstudio-2017',
                  'nasm']

variants = [
    ['platform-windows', 'PySide'],
    ['platform-windows', 'PySide2']
]


def commands():
    global env
    
    env.PATH.append("{root}/bin")
    env.PYTHONPATH.append('{root}/lib/python')
    env.LD_LIBRARY_PATH.append('{root}/lib/')
    
    # Required additionally on Windows
    env.PATH.append('{root}/lib/')
    
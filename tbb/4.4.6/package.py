# -*- coding: utf-8 -*-

name = 'tbb'

version = '4.4.6'

variants = [['platform-windows', 'arch==AMD64']]

build_command = "python {root}/rezbuild.py {install}"
build_requires = ['python']

def commands():

    env.PATH.append("{root}/bin")
    env.PATH.append("{root}/lib")
    env.TBB_LIBRARIES = "{root}" 

# -*- coding: utf-8 -*-

name = 'arnold'

version = '5.4.0.2'

variants = [['platform-windows']]

build_command = "python {root}/rezbuild.py {install}"
build_requires = ['python']

def commands():

    env.PATH.append("{root}/bin")
    env.PATH.append("{root}/lib")
    env.PYTHONPATH.append("{root}/python")
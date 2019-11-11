# -*- coding: utf-8 -*-

name = 'googletest'

version = '1.10.0'

variants = [['platform-windows', 'arch==AMD64']]

build_command = "python {root}/rezbuild.py {install}"
build_requires = ['python',
                  'cmake-3.2+']

def commands():

    env.LD_LIBRARY_PATH.append("{root}/lib")
    env.GTEST_ROOT.set('{root}')


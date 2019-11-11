# -*- coding: utf-8 -*-

name = 'ilmbase'

version = '2.2.0'

variants = [['platform-windows', 'arch==AMD64']]

# This is important, otherwise the build scripts fail
# on == in the build folder names.
hashed_variants = True

build_command = "python {root}/rezbuild.py {install}"
build_requires = ['python',
                  'cmake-3.2+']

def commands():

    env.ILMBASE_ROOT = '{root}'
    env.LD_LIBRARY_PATH.append('{root}/lib/')
    env.PKG_CONFIG_PATH.append('{root}/lib/pkgconfig/')



# -*- coding: utf-8 -*-

name = 'openexr'

version = '2.2.0'

requires = [
            'ilmbase-2.2.0',
            'zlib'
           ]

# This is important, otherwise the build scripts fail
# on == in the build folder names.
hashed_variants = True

variants = [['platform-windows', 'arch==AMD64']]

build_command = "python {root}/rezbuild.py {install}"
build_requires = ['python',
                  'cmake-3.2+']

def commands():

    env.PATH.append("{root}/bin/")
    env.LD_LIBRARY_PATH.append("{root}/lib")
    env.PKG_CONFIG_PATH.append("{root}/lib/pkgconfig")
    env.OPENEXR_ROOT = "{root}"

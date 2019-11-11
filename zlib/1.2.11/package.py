# -*- coding: utf-8 -*-

name = 'zlib'

version = '1.2.11'

variants = [['platform-windows', 'arch==AMD64']]

build_command = "python {root}/rezbuild.py {install}"
build_requires = ['python',
                  'cmake-3.2+']

def commands():
    env.ZLIB_ROOT.set('{root}')
    env.PATH.append('{root}/bin')
    env.ZLIB_INCLUDE_DIR.append('{root}/include')
    env.ZLIB_LIBRARY.append('{root}/lib')
    env.PKG_CONFIG_PATH.append('{root}/share/pkgconfig')
    
    env.LD_LIBRARY_PATH.append("{root}/lib")


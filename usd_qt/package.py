# -*- coding: utf-8 -*-

name = 'usd_qt'

# This is a test version to compile the usd-qt git repository
# so that's why it's this odd placeholder version here.
version = '0.0.git'

variants = [['platform-windows', 'arch==AMD64']]

requires = [
    # todo: This actually requires boost too aside USD
    #       but since we have no Boost package yet. We steel
    #       the required library and includdes from USD.
    # Note: You need usd-qt dev branch to build against USD 19.11
    'usd-19.11',
    'tbb-4.4.6',
    'python-2.7',
]

build_command = "python {root}/rezbuild.py {install}"
private_build_requires = [
    'visualstudio-2017'
]

def commands():
    global env
    global request
    
    env.PYTHONPATH.prepend("{root}/lib/python")

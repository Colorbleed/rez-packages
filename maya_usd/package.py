# -*- coding: utf-8 -*-

name = 'maya_usd'

# This is a test version to compile the maya-usd git repository
# so that's why it's this odd placeholder version here.
version = '0.0.git'

variants = [['platform-windows', 'arch==AMD64']]

build_command = "python {root}/rezbuild.py {install}"
build_requires = ['python-2.7',
                  'visualstudio-2017',
                  'maya_devkit-2019.2']

requires = [
    "usd-19.11",
    "maya-2019",
    # todo: can we remove this hard requirement and have it
    #       be a variant so we support Python 3+?
    "python-2.7"
]

def commands():
    global env
    global request

    env.MAYA_MODULE_PATH.append("{root}")

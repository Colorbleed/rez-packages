# -*- coding: utf-8 -*-

name = 'arnold_usd'

# This is a test version to compile the arnold-usd git repository
# so that's why it's this odd placeholder version here.
version = '0.0.git'

variants = [['platform-windows', 'arch==AMD64']]

build_command = "python {root}/rezbuild.py {install}"
build_requires = ['python-2.7',
                  'visualstudio-2017']

requires = [
    "arnold-5.4.0.2",
    "usd-19.11",
    "tbb-4.4.6",
    # todo: can we remove this hard requirement and have it
    #       be a variant so we support Python 3+?
    "python-2.7",
    "jinja2"
]

def commands():
    global env
    global request

    env.PATH.prepend("{root}/bin")
    env.LD_LIBRARY_PATH.prepend('{root}/lib/')  # unix
    env.PATH.prepend("{root}/lib")              # windows
    
    env.ARNOLD_PLUGIN_PATH.append("{root}/plugin")
    env.PATH.append("{root}/procedural")
    
    # todo: is this needed for mtoa?
    if "maya" in request:
        env.MTOA_EXTENSIONS_PATH.append("{root}/plugin")

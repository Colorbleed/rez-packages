name = "mtoa"
version = "3.3.0.2"

description = \
"""
Maya to Arnold Renderer
"""

tools = [
    "kick",
    'oslc',
    'oslinfo',
    "maketx"
]


build_command = "python {root}/rezbuild.py {install}"
build_requires = ['python',
                  '7zip']

variants = [
    ['platform-windows', 'maya-2018'],
    ['platform-windows', 'maya-2019']
]


def commands():
    global env
    import os
  
    env.MTOA = root
    env.MAYA_RENDER_DESC_PATH.append(root)
    env.MTOA_EXTENSIONS_PATH.append(os.path.join(root, "extensions"))
    env.MTOA_EXTENSIONS.append(os.path.join(root, "extensions"))
    env.MAYA_MODULE_PATH.append(root)
    env.ARNOLD_PLUGIN_PATH.append(os.path.join(root, "shaders"))
    env.PATH.append(os.path.join(root, "bin"))
    
    # Additionally match what mtoa.mod file does by default
    env.MAYA_CUSTOM_TEMPLATE_PATH.append(os.path.join(root, "scripts/mtoa/ui/templates"))
    env.MAYA_SCRIPT_PATH.append(os.path.join(root, "scripts/mtoa/mel"))
    env.MAYA_RENDER_DESC_PATH.append(root)
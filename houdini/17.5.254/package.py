name = "houdini"
version = '17.5.254'
build_command = False
 
description = \
    """SideFX Houdini
    
    This is distributed as "reference package" and
    references a local installation of SideFX.
    
    """
homepage = 'https://www.sidefx.com/'
 
authors = ['Side Effects Software']
 
variants = [
    ['platform-windows']
]

def commands():
    global env
    
    houdini_version = str(env.REZ_HOUDINI_VERSION)
    houdini_root = "C:/Program Files/Side Effects Software/Houdini %s" % houdini_version
    
    env.PATH.append(houdini_root + "/bin")
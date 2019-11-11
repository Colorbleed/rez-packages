name = "vrayformaya"
build_command = False

version = '4.12.02'
 
description = \
    """
    ChaosGroup VRay Next for Maya (reference package)
    """
homepage = 'http://www.chaosgroup.com'
 
authors = ['ChaosGroup']
 
variants = [['platform-windows', 'maya-2018'],
            ['platform-windows', 'maya-2019']]

def commands():
    global env
    global request
    import platform
    import os
    
    maya_version = str(env.REZ_MAYA_MAJOR_VERSION)
    
    # MAYA_LOCATION is set up by maya package.py
    maya_vray  = os.path.join(str(env.MAYA_LOCATION), "vray")
    vray_root = "C:/Program Files/Chaos Group/V-Ray/Maya {} for x64".format(maya_version)
    
    env.MAYA_RENDER_DESC_PATH.append(os.path.join(maya_vray, "bin")) 
    env["VRAY_FOR_MAYA{}_MAIN".format(maya_version)] = maya_vray
    env["VRAY_FOR_MAYA{}_PLUGINS".format(maya_version)] = os.path.join(maya_vray, "vrayplugins")
    env["VRAY_OSL_PATH_MAYA{}".format(maya_version)] = os.path.join(vray_root, "opensl")
    env["VRAY_TOOLS_MAYA{}".format(maya_version)] = os.path.join(vray_root, "bin")
    
    env.VRAY_PLUGINS.set(os.path.join(maya_vray, "vrayplugins"))
    env.MAYA_PLUG_IN_PATH.append(os.path.join(maya_vray, "plug-ins"))
    env.MAYA_SCRIPT_PATH.append(os.path.join(maya_vray, "scripts"))
    env.PYTHONPATH.append(os.path.join(maya_vray, "scripts"))
    env.XBMLANGPATH.append(os.path.join(maya_vray, "icons"))
    
    env.PATH.append(os.path.join(maya_vray, "bin"))
    env.PATH.append(os.path.join(vray_root, "bin"))

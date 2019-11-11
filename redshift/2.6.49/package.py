name = "redshift"

version = '2.6.49'
 
description = \
    """
    Redshift3D Renderer
    """
homepage = 'https://www.redshift3d.com/'
 
authors = ['Redshift']
 
variants = [
    ['platform-windows', 'maya-2018'],
    ['platform-windows', 'maya-2019'],
    ['platform-windows', 'houdini-17.5.293'],
    ['platform-windows', 'houdini-17.5.327'],
    ['platform-windows', 'houdini-17.5.360'],
    ['platform-windows', 'katana-3.2v1']
]

requires = ["redshift_recipe-2.6.49"]


def commands():
    global env
    global request
    
    # See this page for details on Redshift's
    # required environment variables for custom locations
    # https://docs.redshift3d.com/display/RSDOCS/Custom+Install+Locations
    redshift_root = "C:/ProgramData/Redshift" 
    
    if "maya" in request:
        # Include Maya plug-in
        maya_version = str(env.REZ_MAYA_MAJOR_VERSION)
        
        env.REDSHIFT_PLUG_IN_PATH = redshift_root + "/Plugins/Maya/" + maya_version + "/nt-x86-64"
        env.REDSHIFT_SCRIPT_PATH = redshift_root + "/Plugins/Maya/Common/scripts"
        env.REDSHIFT_XBMLANGPATH = redshift_root + "/Plugins/Maya/Common/icons"
        env.REDSHIFT_RENDER_DESC_PATH = redshift_root + "/Plugins/Maya/Common/rendererDesc"
        env.REDSHIFT_CUSTOM_TEMPLATE_PATH = redshift_root + "/Plugins/Maya/Common/scripts/NETemplates"
        env.REDSHIFT_MAYAEXTENSIONSPATH = redshift_root + "/extensions"
        
        env.MAYA_PLUG_IN_PATH.append("{env.REDSHIFT_PLUG_IN_PATH}")
        env.MAYA_SCRIPT_PATH.append("{env.REDSHIFT_SCRIPT_PATH}")
        env.PYTHONPATH.append("{env.REDSHIFT_SCRIPT_PATH}")
        env.XBMLANGPATH.append("{env.REDSHIFT_XBMLANGPATH}")
        env.MAYA_RENDER_DESC_PATH.append("{env.REDSHIFT_RENDER_DESC_PATH}")
        env.MAYA_CUSTOM_TEMPLATE_PATH.append("{env.REDSHIFT_CUSTOM_TEMPLATE_PATH}")
        
    if "houdini" in request:
        # Include Houdini plug-in
        houdini_version = "{env.REZ_HOUDINI_VERSION}"
        env.HOUDINI_DSO_ERROR = "2"
        
        # It's important to prepend so that Houdini's regular installation
        # still has `&` at the end as that refers to Houdini's own locations.
        # This is required to not break Houdini in finding its native plug-ins
        env.HOUDINI_PATH.prepend(redshift_root + "/Plugins/Houdini/" + houdini_version)
        
    if "katana" in request:
        # Include Katana plug-in
        katana_version = "{env.REZ_KATANA_VERSION}"
        env.KATANA_RESOURCES.append(redshift_root + "/Plugins/Katana/" + katana_version)
        env.DEFAULT_RENDERER = "Redshift"
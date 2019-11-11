name = "yeti_maya"
version = "3.5.3"

build_command = "python {root}/rezbuild.py {install}"
build_requires = ['python']

variants = [
    #['platform-windows', 'maya-2018'],
    ['platform-windows', 'maya-2019']
]

def commands():
    global env
    global request
    import platform
    import os
    
    platform_name = platform.system().lower()
    
    env["YETI_ROOT"] = "{root}"
    env["MAYA_MODULE_PATH"].append("{root}")
    env["PATH"].append("{root}/bin")
    
    # V-Ray
    if "vrayformaya" in request:
        env["VRAY_PLUGINS"].append("{root}/bin")
        # todo(roy): And this is specific to specific maya version?
        env["VRAY_FOR_MAYA2018_PLUGINS"].append("{root}/bin")
    
    # Redshift
    if "redshift" in request:
        env["REDSHIFT_MAYAEXTENSIONSPATH"].append("{root}/plug-ins")
    
    # Arnold
    if "arnold" in request:
        env["MTOA_EXTENSIONS_PATH"].append("{root}/plug-ins")
        env["ARNOLD_PLUGIN_PATH"].append("{root}/bin")
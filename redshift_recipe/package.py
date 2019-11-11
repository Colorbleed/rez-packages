name = "redshift"

version = '2.6.49'
 
description = \
    """
    Redshift3D Deployment Recipe
    
    This is separated into its own 'recipe' package
    so that the common files can be distributed as
    a single platform package. As opposed to having
    to copy over *all* binary files each time per
    Houdini or Maya variant.
    
    """
homepage = 'https://www.redshift3d.com/'
 
authors = ['Redshift']


build_command = "python {root}/rezbuild.py {install}"
build_requires = ['python',
                  '7zip']
 
variants = [
    ['platform-windows']
]

def commands():
    global env
    
    # Note: This package sets only the base environment variables
    #       for the REDSHIFT_CORE_PACKAGE. It's up to the separated
    #       redshift package to set things up for DCC plug-ins.
    env.REDSHIFT_COREDATAPATH = root
    env.REDSHIFT_PROCEDURALSPATH = "{root}/Procedurals"
    env.PATH.append("{root}/bin")
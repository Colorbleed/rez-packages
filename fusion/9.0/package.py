name = "fusion"
version = "9"
build_command = False

description = \
"""
Blackmagic Design Fusion (reference package)
"""

tools = [
    "fusion",
    "fusionscript",
    "fusionserver"
]

variants = [
    ['platform-windows']
]

requires = ["global", "avalon"]


def commands():
    global env
    import os
    
    fusion_version = str(env.REZ_FUSION_MAJOR_VERSION)
    
    env["AVALON_CORE"] = os.path.join(str(env.REZ_AVALON_ROOT),
                                      "python",
                                      "avalon")
    
    # Fusion
    env["FUSION_VERSION"] = fusion_version
    env["FUSION_LOCATION"] = "C:/Program Files/Blackmagic Design/Fusion {env.FUSION_VERSION}"
    env.PATH.append("{env.FUSION_LOCATION}")
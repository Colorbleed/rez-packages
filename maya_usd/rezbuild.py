"""Rezbuild for Maya-USD: https://github.com/Autodesk/maya-usd"""
import os
import sys
import subprocess


def build(source_path, build_path, install_path, targets):
    
    # Dependencies
    maya_location = os.environ["MAYA_LOCATION"]
    maya_devkit = os.environ["REZ_MAYA_DEVKIT_ROOT"]
    usd_root = os.environ["REZ_USD_ROOT"]
    
    # Maya-USD source (e.g. git repository)
    source_root = os.path.join(source_path, "source", "maya-usd")
    if not os.path.exists(source_root):
        raise RuntimeError("Couldn't find 'maya-usd' git repository "
                           "source root at: %s"  % source_root)
    
    print("Using source root: %s" % source_root)
    
    if "install" not in (targets or []):
        return
    
    # Run build
    # The build scripts tries to remove the build folder if it already
    # exists. Because the REZ_BUILD_PATH is in use and thus can't be
    # deleted we force the build_root into a subfolder so the script
    # succeeds to 'remove' it if it exists.
    build_root = os.path.join(build_path, "maya-usd")
    cmd = ["python", "build.py",
           "--maya-location", maya_location,
           "--devkit-location", os.path.join(maya_devkit, "devkitBase"),
           "--pxrusd-location", usd_root,
           "--build-location", build_root,
           # Enable UFE V2 features (like AE templates) which only is available
           # with Maya 2020+
           #'--build-args=-DCMAKE_UFE_V2_FEATURES_AVAILABLE=True',
           "--install-location", install_path,
           os.path.join(build_root, "tmp")]
    result = subprocess.call(cmd, cwd=source_root)
    if result != 0:
        raise RuntimeError("Build failed.")
        
    # todo: Reconfigure the .mod file so that it doesn't hardcode USD
    #       path. We can just rely on Rez having configuring USD itself.


if __name__ == '__main__':
    build(source_path=os.environ['REZ_BUILD_SOURCE_PATH'],
          build_path=os.environ['REZ_BUILD_PATH'],
          install_path=os.environ['REZ_BUILD_INSTALL_PATH'],
          targets=sys.argv[1:])

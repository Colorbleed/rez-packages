"""Rezbuild for USD on Windows

Note: Currently 3rd Party dependencies are not Rezified
      but included in the package. This makes it bigger
      than it *has* to be and additionally makes building
      the package a lot heavier since it'll download all
      dependencies and build all of them using USD's own
      `build_scripts/build_usd.py` script.
      
"""
import os
import sys
import subprocess
try:
    # Python 3
    import urllib.request as urllib
except ImportError:
    # Python 2
    import urllib
import zipfile


def build(source_path, build_path, install_path, targets):

    cmake_generator = "Visual Studio 15 2017 Win64"
    version = os.environ["REZ_BUILD_PROJECT_VERSION"]
    
    filename = 'v{0}.zip'.format(version)
    archive = os.path.join(build_path, filename)
    url = "https://github.com/PixarAnimationStudios/USD/archive/" + filename
    print("Downloading file: %s" % url)
    urllib.urlretrieve(url, archive)
        
    # Unzip the source to the build folder
    print("Unzipping to: %s" % build_path)
    with zipfile.ZipFile(archive, 'r') as zip_ref:
        zip_ref.extractall(build_path)
    
    assert os.path.exists(install_path), "Install path must exist"
        
    if "install" not in (targets or []):
        return
        
    # Due to a bug in boost we can't compile boost through Rez without
    # this hack because the environment variables for ProgramFiles(x86) 
    # and ProgramFiles are uppercased. 
    # So we ensure the subprocess will have them set correctly.
    # See: https://github.com/boostorg/build/issues/230
    keys = ["ProgramFiles", "ProgramFiles(x86)"]
    env = dict(os.environ)
    for key in keys:
        if key.upper() in env:
            env[key] = env.pop(key.upper())

    # For simplicity let's just compile USD as one big blob
    # without Rezifying all its dependencies using the USD
    # build_usd.py script. This makes this USD package quite
    # a heavy one to build and install.
    # TODO: Build this using cmake without relying on USD's build script.
    build_script = os.path.join(build_path, 
                                "USD-{0}".format(version),
                                "build_scripts",
                                "build_usd.py")
    result = subprocess.call(["python", 
                              build_script,
                              # Installation directory
                              install_path,
                              "--generator", cmake_generator,
                              # Build args for boost
                              "--build-args",  "boost,--with-date_time --with-thread --with-system --with-filesystem",
                              # Enable ptex support
                              "--ptex",
                              # Build OpenImageIO Plugin
                              "--openimageio",
                              # Build OpenColorIO Plugin
                              "--opencolorio",
                              # Enable Alembic support
                              "--alembic",
                              # Enable older HDF5 support for Alembic
                              "--hdf5",
                              # Build MaterialX Plugin
                              "--materialx",
                              # Explicitly do not build DCC Plugins
                              "--no-maya",
                              "--no-katana",
                              "--no-houdini"], 
                             cwd=build_path,
                             env=env)
    if result != 0:
        raise RuntimeError("Failed to compile USD succesfully.")
        
if __name__ == '__main__':
    build(source_path=os.environ['REZ_BUILD_SOURCE_PATH'],
          build_path=os.environ['REZ_BUILD_PATH'],
          install_path=os.environ['REZ_BUILD_INSTALL_PATH'],
          targets=sys.argv[1:])
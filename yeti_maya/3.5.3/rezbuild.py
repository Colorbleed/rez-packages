"""Rezbuild for Yeti for Maya on Windows

Note: 
    This builds from Yeti archive zips in the yeti package folder.
    As such, to install version x.y.z make sure to download the
    related `Yeti-vx.y.z_Maya2019-windows.zip and place it in this
    yeti package folder. This rezbuild.py will then extract the
    contents to install path on `rez build --install` and make
    any necessary changes.

"""
import os
import sys
import subprocess
import tempfile
import shutil
import zipfile


def build(source_path, build_path, install_path, targets):

    version = os.environ["REZ_BUILD_PROJECT_VERSION"]
    maya_version = os.environ["REZ_MAYA_MAJOR_VERSION"]

    # Assume the file archive is currently saved in the
    # package's root as the download links for Yeti archives
    # are not publicly available, but only downloadable through
    # yeticentral.com
    filename = 'Yeti-v{0}_Maya{1}-windows.zip'.format(version,
                                                      maya_version)
    archive = os.path.join(source_path, filename)
    assert os.path.exists(archive), "Yeti archive not found: %s" % archive
    print("Detected Yeti archive: %s" % archive)

    if "install" not in (targets or []):
        return
        
    # Unzip the source to the build folder
    print("Unzipping to: %s" % install_path)
    with zipfile.ZipFile(archive, 'r') as zip_ref:
        zip_ref.extractall(install_path)    
        
    # By default the `pgYetiMaya.mod` files has a placeholder
    # value for 'path_to_yeti_root' so we will change that line
    # so it understands the files are directly relative to the package.
    module = os.path.join(install_path, "pgYetiMaya.mod")
    assert os.path.exists(module), "Yeti Module does not exist: %s" % module
    with open(module) as src, tempfile.NamedTemporaryFile(
            'w', dir=os.path.dirname(module), delete=False) as dst:

        # Read only first line and make sure it's the line as we expect it
        line = src.readline()  
        assert line.startswith("+ pgYetiMaya ")
        assert line.endswith(" path_to_yeti_root\n")
        
        # Remove ` path_to_yeti_root` and add ` .`
        line = line.rsplit(" ", 1)[0] + " ."
        print("Changing first line of pgYetiMaya.mod to: %s" % line)
        dst.write(line + '\n')
        
        # Copy the rest of the file
        shutil.copyfileobj(src, dst)

    os.unlink(module)           # Remove .mod file
    os.rename(dst.name, module) # Rename new .mod file
    
    # Remove the EULA.pdf from the Yeti module's root directory as
    # there is known Maya slowdown when `` plug-in is loaded that
    # occasionally triggers a reread of files in MAYA_MODULE_PATH.
    # As such we avoid having somewhat larger files in those root
    # directories, like e.g. a 90KB PDF. (Note that the slowdown
    # is usually noticable for larger files, e.g. 100s of MB)
    remove = ["EULA.pdf"]
    for fname in remove:
        path = os.path.join(install_path, fname)
        if os.path.exists(path):
            print("Removing file: %s" % path)
            os.unlink(path)    
    

if __name__ == '__main__':
    build(source_path=os.environ['REZ_BUILD_SOURCE_PATH'],
          build_path=os.environ['REZ_BUILD_PATH'],
          install_path=os.environ['REZ_BUILD_INSTALL_PATH'],
          targets=sys.argv[1:])
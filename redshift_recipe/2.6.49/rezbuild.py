"""Rezbuild for Redshift on Windows

Note: 
    This builds from Redshift from its .exe installer located inside
    this package folder.
    
    As such, to install version x.y.z make sure to download the
    related `redshift-vx.y.z_setup.exe and place it in this package folder. 
    This rezbuild.py will then extract the contents to install path 
    on `rez build --install` and make any necessary changes.

"""
import os
import sys
import subprocess
import tempfile
import shutil


def build(source_path, build_path, install_path, targets):

    version = os.environ["REZ_BUILD_PROJECT_VERSION"]

    # Assume the file archive is currently saved in the
    # package's root as the download links for MtoA archives
    # are not publicly available, but only downloadable through
    # the Autodesk website. They only provide .exe file so we
    # unzip the NSIS-2 type archive using 7zip.
    filename = 'redshift_v{0}_setup.exe'.format(version)
    archive = os.path.join(source_path, filename)
    assert os.path.exists(archive), "Archive not found: %s" % archive
    print("Detected archive: %s" % archive)

    if "install" not in (targets or []):
        return
        
    # Unzip the .exe to the install folder
    print("Extracting archive to: %s" % install_path)
    subprocess.call(["7z",
                     "x",
                     archive,
                     # Overwrite all existing files without prompt
                     "-aoa",
                     # Somehow this flag must be concatenated 
                     # as single string to function correctly
                     "-o%s" % install_path,
                     # Exclude all folders starting with $_
                     # and $PLUGINSDIR as they are part of the
                     # NSIS .exe installer and redundant output
                     # Also exclude `uninstall.exe`
                     "-x!$_*",
                     "-x!$PLUGINSDIR",
                     "-x!uninstall.exe",
                     # Apply 'yes' to any 7zip prompt
                     "-y"],
                     cwd=install_path)  
                     

if __name__ == '__main__':
    build(source_path=os.environ['REZ_BUILD_SOURCE_PATH'],
          build_path=os.environ['REZ_BUILD_PATH'],
          install_path=os.environ['REZ_BUILD_INSTALL_PATH'],
          targets=sys.argv[1:])
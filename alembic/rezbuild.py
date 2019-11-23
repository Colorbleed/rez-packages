"""Rezbuild for Alembic: https://github.com/alembic/alembic"""
import os
import sys
import subprocess
import urllib.request
import zipfile


def build(source_path, build_path, install_path, targets):

    cmake_generator = "Visual Studio 15 2017 Win64"
    cmake_target_platform = "v141"
    version = os.environ["REZ_BUILD_PROJECT_VERSION"]

    # Download the source
    filename = '{0}.zip'.format(version)
    zip_path = os.path.join(build_path, filename)
    url = "https://github.com/alembic/alembic/archive/" + filename
    print("Downloading file: %s" % url)
    urllib.request.urlretrieve(url, zip_path)
    
    # Unzip the source
    print("Unzipping to: %s" % build_path)
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(build_path)
        
        folder_name = next(info.filename for info in zip_ref.infolist() if info.is_dir())
    
    source_root = os.path.join(build_path, folder_name)
    print("Building source root: %s" % source_root)
    
    # todo: enable HDF5 support
    # todo: enable PyAlembic support
        
    # Run cmake
    cmdline = ["cmake", 
               "-G", cmake_generator, 
               "-T", cmake_target_platform, 
               "-DOUTPUT_PATH=" + build_path,
               # todo: double check whether these are actually needed
               "-DILMBASE_ROOT=" + os.environ["REZ_ILMBASE_ROOT"],
               "-DOPENEXR_ROOT=" + os.environ["REZ_OPENEXR_ROOT"],
               # Build Maya plug-in
               "-DUSE_MAYA=ON",
               "-DMAYA_ROOT=" + os.environ["MAYA_LOCATION"],
               # Build PyAlembic
               #"USE_PYALEMBIC=ON",
               "-DCMAKE_INSTALL_PREFIX=" + install_path,
               source_root]
    subprocess.call(cmdline, cwd=build_path)
    
    # Build binaries
    subprocess.call(["cmake", 
                     "--build", ".", 
                     "--config", "Release"], cwd=build_path)

    if "install" not in (targets or []):
        return
        
    # Trigger install file
    subprocess.call(["cmake",
                     "-P", "cmake_install.cmake",
                     build_path])


if __name__ == '__main__':
    build(source_path=os.environ['REZ_BUILD_SOURCE_PATH'],
          build_path=os.environ['REZ_BUILD_PATH'],
          install_path=os.environ['REZ_BUILD_INSTALL_PATH'],
          targets=sys.argv[1:])
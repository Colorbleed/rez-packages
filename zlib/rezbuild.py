"""Rezbuild for OpenEXR on Windows"""
import os
import sys
import subprocess
import urllib.request
import tarfile


def build(source_path, build_path, install_path, targets):

    cmake_generator = "Visual Studio 15 2017 Win64"
    cmake_target_platform = "v141"
    version = os.environ["REZ_BUILD_PROJECT_VERSION"]

    # Download the source
    filename = 'zlib-{0}.tar.gz'.format(version)
    archive = os.path.join(build_path, filename)
    url = "https://zlib.net/" + filename
    print("Downloading file: %s" % url)
    urllib.request.urlretrieve(url, archive)
    
    # Unzip the source
    print("Unzipping to: %s" % build_path)
    with tarfile.TarFile.open(archive, mode='r:gz') as tar:
        tar.extractall(build_path)
    
    folder_name = filename.rsplit(".tar.gz")[0]
    source_root = os.path.join(build_path, folder_name)
    print("Building source root: %s" % source_root)
    
    # Run cmake
    cmdline = ["cmake", 
               "-G", cmake_generator, 
               "-T", cmake_target_platform, 
               source_root, 
               "-DOUTPUT_PATH=" + build_path,
               "-DCMAKE_INSTALL_PREFIX=" + install_path]

    subprocess.call(cmdline, cwd=build_path)
    
    # Build binaries
    subprocess.call(["cmake", "--build", ".", "--config",
                     "Release"], cwd=build_path)

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
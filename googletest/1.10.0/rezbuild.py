"""Rezbuild for googletest: https://github.com/google/googletest"""
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
    filename = 'release-{0}.zip'.format(version)
    zip_path = os.path.join(build_path, filename)
    url = "https://github.com/google/googletest/archive/" + filename
    print("Downloading file: %s" % url)
    urllib.request.urlretrieve(url, zip_path)
    
    # Unzip the source
    print("Unzipping to: %s" % build_path)
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(build_path)
        
        folder_name = next(info.filename for info in zip_ref.infolist() if info.is_dir())
    
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
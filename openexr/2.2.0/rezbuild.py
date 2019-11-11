"""Rezbuild for OpenEXR on Windows"""
import os
import sys
import shutil
import subprocess
import urllib.request
import tarfile


def build(source_path, build_path, install_path, targets):

    cmake_generator = "Visual Studio 15 2017 Win64"
    cmake_target_platform = "v141"
    version = os.environ["REZ_BUILD_PROJECT_VERSION"]

    # Download the source
    filename = 'openexr-{0}.tar.gz'.format(version)
    archive = os.path.join(build_path, filename)
    url = "http://download.savannah.nongnu.org/releases/openexr/" + filename
    print("Downloading file: %s" % url)
    #urllib.request.urlretrieve(url, archive)
    
    # Unzip the source
    print("Unzipping to: %s" % build_path)
    with tarfile.TarFile.open(archive, mode='r:gz') as tar:
        tar.extractall(build_path)
    
    folder_name = filename.rsplit(".tar.gz")[0]
    source_root = os.path.join(build_path, folder_name)
    print("Building source root: %s" % source_root)

    # WORKAROUND -- 
    # Apparently there are some files in `ilmbase` that need to be copied into the OpenEXR package for it to compile
    # Also some packages assume ilmbase and openexr headers/libs live together (like usd, katana plugins)
    #print("Patching OpenEXR by including ilmbase/include/OpenEXR and ilmbase/lib files")
    #shutil.copytree(os.path.join(os.environ["REZ_ILMBASE_ROOT"], "include/OpenEXR"), os.path.join(source_root, "include/OpenEXR"))
    #shutil.copytree(os.path.join(os.environ["REZ_ILMBASE_ROOT"], "lib"), os.path.join(source_root, "lib"))
    
    # Run cmake
    cmdline = ["cmake", 
               "-G", cmake_generator, 
               "-T", cmake_target_platform, 
               #"-DOUTPUT_PATH=" + build_path,
               # HACK: This flag is required to be so explicitly passed along
               # TODO: Can we resolve this through an environment variable during build - or should this be here?
               "-DILMBASE_PACKAGE_PREFIX=" + os.environ["REZ_ILMBASE_ROOT"],
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
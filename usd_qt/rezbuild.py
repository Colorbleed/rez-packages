"""Rezbuild for usd-qt: https://github.com/LumaPictures/usd-qt"""

import os
import sys
import subprocess


def build(source_path, build_path, install_path, targets):

    cmake_generator = "Visual Studio 15 2017 Win64"
    cmake_target_platform = "v141"
    
    tbb_root = os.environ["REZ_TBB_ROOT"]
    # todo: rezify, don't steel from USD
    boost_lib = os.path.join(os.environ["REZ_USD_ROOT"], "lib")
    boost_include = os.path.join(os.environ["REZ_USD_ROOT"], "include", "boost-1_65_1")
        
    # usd-qt source (e.g. git repository)
    source_root = os.path.join(source_path, "source", "usd-qt")
    if not os.path.exists(source_root):
        raise RuntimeError("Couldn't find 'arnold-usd' git repository "
                           "source root at: %s"  % source_root)
    
    print("Building source root: %s" % source_root)
    
    # Run cmake
    cmdline = ["cmake", 
               "-G", cmake_generator, 
               "-T", cmake_target_platform, 
               #"-DOUTPUT_PATH=" + build_path,
               "-B", build_path,
               "-DBOOST_LIBRARYDIR=" + boost_lib,
               "-DBoost_INCLUDE_DIR=" + boost_include,
               "-DTBB_ROOT_DIR=" + tbb_root,
               
               "-DCMAKE_INSTALL_PREFIX=" + install_path,
               source_root]
    subprocess.call(cmdline, cwd=build_path)
    
    # Build binaries
    returncode = subprocess.call(["cmake", 
                                  "--build", ".", 
                                  "--config", "Release"], 
                                  cwd=build_path)
    if returncode != 0:
        raise RuntimeError("Failed to build.")

    if "install" not in (targets or []):
        return
        
    # Trigger install file
    returncode = subprocess.call(["cmake",
                                  "-P", "cmake_install.cmake",
                                  build_path])
    if returncode != 0:
        raise RuntimeError("Failed to install.")


if __name__ == '__main__':
    build(source_path=os.environ['REZ_BUILD_SOURCE_PATH'],
          build_path=os.environ['REZ_BUILD_PATH'],
          install_path=os.environ['REZ_BUILD_INSTALL_PATH'],
          targets=sys.argv[1:])

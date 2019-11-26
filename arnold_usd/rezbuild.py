"""Rezbuild for Arnold-USD: https://github.com/Autodesk/arnold-usd"""
import os
import sys
import subprocess


def build(source_path, build_path, install_path, targets):

    cmake_generator = "Visual Studio 15 2017 Win64"
    cmake_target_platform = "v141"
    version = os.environ["REZ_BUILD_PROJECT_VERSION"]
    arnold_root = os.environ["REZ_ARNOLD_ROOT"]
    usd_root = os.environ["REZ_USD_ROOT"]
    tbb_root = os.environ["REZ_TBB_ROOT"]
    
    # For now assume Python was installed with rez scoopz which
    # installs the binaries into an `app` folder inside the root.
    python_root = os.path.join(os.environ["REZ_PYTHON_ROOT"], "app")
    
    # Arnold-USD source (e.g. git repository)
    source_root = os.path.join(source_path, "source", "arnold-usd")
    if not os.path.exists(source_root):
        raise RuntimeError("Couldn't find 'arnold-usd' git repository "
                           "source root at: %s"  % source_root)
    
    print("Building source root: %s" % source_root)
    
    # Set build parameters
    args = [
        ("ARNOLD_PATH", arnold_root),
        ("USD_PATH", usd_root),
        # Set the build mode for USD that it generates when running 
        # default build script, which is 'shared_libs'
        ("USD_BUILD_MODE", r"shared_libs"),
        # Set the BOOST_INCLUDE prefix for USD built on Windows using
        # Visual Studio 2017 or greater, which builds boost 1.65.1
        ("BOOST_INCLUDE", usd_root + "/include/boost-1_65_1"),
        # Building USD on Windows using Pixar's build script appends
        # a suffix to all Boost generated files, so we need to make
        # sure that Arnold-USD finds it.
        ("BOOST_LIB_NAME", "boost_%s-vc141-mt-1_65_1.lib"),
        ("PYTHON_INCLUDE", os.path.join(python_root, "include")),
        ("PYTHON_LIB", os.path.join(python_root, "libs")),
        ("PYTHON_LIB_NAME", r"python27"),
        ("TBB_INCLUDE", os.path.join(tbb_root, "include")),
        ("TBB_LIB", os.path.join(tbb_root, "lib")),
        ("BUILD_SCHEMAS", "True"),
        # todo: Fix building the docs. It fails on:
        # AttributeError: 'SConsEnvironment' object has no attribute 'Doxygen':
        #   File "D:\dev\usd\arnold-usd\SConstruct", line 392:
        #     DOCS = env.Doxygen(source='docs/Doxyfile', target=docs_output)
        ("BUILD_DOCS", "False"),
        ("DISABLE_CXX11_ABI", "True"),
        ("MSVC_VERSION", "14.1"),
        # Install location
        ("PREFIX", install_path)
        
    ]
    
    # todo: handle paths with spaces?
    cmd_build_args = ["%s=%s" % (key, value) for key, value in args]
    
    if "install" not in (targets or []):
        return
    
    # Run arnold-usd/abuild
    cmd = [os.path.join(source_root, "abuild.bat")]
    cmd.extend(cmd_build_args)
    result = subprocess.call(cmd, cwd=source_root)
    if result != 0:
        raise RuntimeError("Build failed.")


if __name__ == '__main__':
    build(source_path=os.environ['REZ_BUILD_SOURCE_PATH'],
          build_path=os.environ['REZ_BUILD_PATH'],
          install_path=os.environ['REZ_BUILD_INSTALL_PATH'],
          targets=sys.argv[1:])

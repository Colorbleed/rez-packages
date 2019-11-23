"""Rezbuild for tbb: https://github.com/01org/tbb"""
import os
import glob
import sys
import shutil
import subprocess
import urllib.request
import zipfile

def copy_files(src, dest):
    files = glob.glob(src)
    if not files:
        raise RuntimeError("File(s) to copy not found: %s" % src)
    
    # Ensure destination folder is created
    if not os.path.exists(dest):
        os.makedirs(dest)
    
    for src_file in files:
    
        # Explicitly copy to file destination
        dest_file = os.path.join(dest, os.path.basename(src_file))
        print("Copying %s -> %s" % (src_file, dest_file))
        shutil.copyfile(src_file, dest_file)
        
def copy_directory(src, dest):
    if os.path.isdir(dest):
        shutil.rmtree(dest)    

    print("Copying %s -> %s" % (src, dest))
    shutil.copytree(src, dest)


def build(source_path, build_path, install_path, targets):

    version = os.environ["REZ_BUILD_PROJECT_VERSION"]

    # For simplicity like USD's build_script let's just collect
    # the precompiled binaries for Windows.
    # Note: This downloads a hardcoded version of tbb!
    url = "https://github.com/01org/tbb/releases/download/2017_U5/tbb2017_20170226oss_win.zip"
    filename = os.path.basename(url)
    zip_path = os.path.join(build_path, filename)
    print("Downloading file: %s" % url)
    urllib.request.urlretrieve(url, zip_path)
    
    # Unzip the compiled tbb
    print("Unzipping to: %s" % build_path)
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(build_path)
        folder_name = next(info.filename for info in zip_ref.infolist() if info.is_dir())
    
    source_root = os.path.join(build_path, folder_name)
    print("Building source root: %s" % source_root)
                     
    if "install" not in (targets or []):
        return
        
    # Install the files, like usd build script:
    # https://github.com/PixarAnimationStudios/USD/blob/4b1162957b2ad219e1635c81de8343be490e41fc/build_scripts/build_usd.py#L639
    copy_files(source_root + "/bin/intel64/vc14/*.*", install_path + "/bin")
    copy_files(source_root + "/lib/intel64/vc14/*.*", install_path + "/lib")
    copy_directory(source_root + "include/serial", install_path + "/include/serial")
    copy_directory(source_root + "include/tbb", install_path + "/include/tbb")


if __name__ == '__main__':
    build(source_path=os.environ['REZ_BUILD_SOURCE_PATH'],
          build_path=os.environ['REZ_BUILD_PATH'],
          install_path=os.environ['REZ_BUILD_INSTALL_PATH'],
          targets=sys.argv[1:])
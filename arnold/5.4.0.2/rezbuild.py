"""Rezbuild for Arnold: https://www.arnoldrenderer.com/arnold/download/"""
import os
import sys
import zipfile


def build(source_path, build_path, install_path, targets):

    version = os.environ["REZ_BUILD_PROJECT_VERSION"]
    archive = os.path.join(source_path, "Arnold-%s-windows.zip" % version)
    
    assert os.path.exists(archive), "Archive not found: %s" % archive
    print("Found archive: %s" % archive)

    if "install" not in (targets or []):
        return
    
    # Unzip the Arnold SDK
    print("Unzipping to: %s" % install_path)
    with zipfile.ZipFile(archive, 'r') as zip_ref:
        zip_ref.extractall(install_path)


if __name__ == '__main__':
    build(source_path=os.environ['REZ_BUILD_SOURCE_PATH'],
          build_path=os.environ['REZ_BUILD_PATH'],
          install_path=os.environ['REZ_BUILD_INSTALL_PATH'],
          targets=sys.argv[1:])
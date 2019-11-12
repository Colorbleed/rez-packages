"""Rezbuild for Maya Devkit

This will download the relevant devkit and deploy it on install.
Make sure the Maya version you'll need has a URL listed.
They can be found here: https://www.autodesk.com/developer-network/platform-technologies/maya

"""
import os
import sys
import subprocess
try:
    # Python 3
    import urllib.request as urllib
except ImportError:
    # Python 2
    import urllib
import zipfile

URLS = {
    "2019.2": "https://autodesk-adn-transfer.s3-us-west-2.amazonaws.com/ADN+Extranet/M%26E/Maya/devkit+2019/Autodesk_Maya_2019_2_Update_DEVKIT_Windows.zip",
    "2019.1": "https://s3-us-west-2.amazonaws.com/autodesk-adn-transfer/ADN+Extranet/M%26E/Maya/devkit+2019/Autodesk_Maya_2019_1_Update_DEVKIT_Windows.zip",
    "2019": "https://s3-us-west-2.amazonaws.com/autodesk-adn-transfer/ADN+Extranet/M%26E/Maya/devkit+2019/Autodesk_Maya_2019_DEVKIT_Windows.zip",
    "2018.6": "https://s3-us-west-2.amazonaws.com/autodesk-adn-transfer/ADN+Extranet/M%26E/Maya/devkit+2018/Autodesk_Maya_2018_6_Update_DEVKIT_Windows.zip"
}


def build(source_path, build_path, install_path, targets):

    version = os.environ["REZ_BUILD_PROJECT_VERSION"]
    
    # Download the devkit
    url = URLS[version]
    filename = os.path.basename(url)
    archive = os.path.join(build_path, filename)
    print("Downloading file: %s" % url)
    urllib.urlretrieve(url, archive)

    if "install" not in (targets or []):
        return
        
    # Unzip the devkit to the install folder
    print("Unzipping to: %s" % install_path)
    with zipfile.ZipFile(archive, 'r') as zip_ref:
        zip_ref.extractall(install_path)    


if __name__ == '__main__':
    build(source_path=os.environ['REZ_BUILD_SOURCE_PATH'],
          build_path=os.environ['REZ_BUILD_PATH'],
          install_path=os.environ['REZ_BUILD_INSTALL_PATH'],
          targets=sys.argv[1:])
from PyMicrosoftSQL.helper import get_system_details
import subprocess
import sys
import os

current_dir = os.path.dirname(os.path.realpath(__file__))

def get_mac_platform_architecture():
    # Get platform architecture
    # Will return 'x86_64' or 'arm64'
    platform = sys.platform
    if platform == 'darwin':
        # Get the architecture of the machine
        arch = subprocess.run(['uname', '-m'], stdout=subprocess.PIPE).stdout.decode('utf-8').strip()
        return arch
    return None

def configure_dylibs(reverse=False):
    # Get platform and configure paths
    arch = get_mac_platform_architecture()
    libmsodbcsql_path = os.path.join(current_dir, 'mac_dylibs', arch, 'lib', 'libmsodbcsql.18.dylib')
    libodbcinst_path = os.path.join(current_dir, 'mac_dylibs', arch, 'lib', 'libodbcinst.2.dylib')
    libltdl_path = os.path.join(current_dir, 'mac_dylibs', arch, 'lib', 'libltdl.7.dylib')

    # Get the existing library paths which are linked to the dylibs
    otool_list = subprocess.run(['otool', '-L', libmsodbcsql_path], stdout=subprocess.PIPE)
    libraries = otool_list.stdout.decode('utf-8').split('\n')
    # in the otool list of libmsodbcsql_path, get the library path for libodbcinst
    for lib in libraries:
        if 'libodbcinst' in lib:
            old_libodbcinst_path = lib.split()[0].strip()
            break
    # in the otool list of libodbcinst_path, get the library path for libltdl
    otool_list = subprocess.run(['otool', '-L', libodbcinst_path], stdout=subprocess.PIPE)
    libraries = otool_list.stdout.decode('utf-8').split('\n')
    for lib in libraries:
        if 'libltdl' in lib:
            old_libltdl_path = lib.split()[0].strip()
            break

    # Configure the library paths
    subprocess.run(['install_name_tool', '-change', old_libodbcinst_path, libodbcinst_path, libmsodbcsql_path], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
    subprocess.run(['install_name_tool', '-change', old_libltdl_path, libltdl_path, libodbcinst_path], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
    
    # Force codesign the dylibs
    subprocess.run(['codesign', '-s', '-', '-f', libmsodbcsql_path], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
    subprocess.run(['codesign', '-s', '-', '-f', libodbcinst_path], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

system_details = get_system_details()
if system_details['Operating System'] == 'Darwin':
    # Configure the dependent libraries to look for the dylibs in the current directory and force codesign them
    configure_dylibs()

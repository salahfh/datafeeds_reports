from pathlib import Path
import os
import subprocess
from time import sleep

# Requirement is to have python installed. 

REPO_URL = 'git+https://github.com/salahfh/datafeeds_reports'
PIP_INI_CONFIG  = \
'''
[global]
trusted-host = pypi.python.org
               pypi.org
               files.pythonhosted.org
               raw.githubusercontent.com
               github.com
'''
BAT_FILE_CONTENT = \
'''
@reports run %*
@pause
'''


def create_pip_ini():
    '''
    Create pip.ini to fix the self-signed cerficates issue due environment.
    '''
    folder_location = Path(os.getenv('APPDATA')) / 'pip'
    pip_ini = folder_location / 'pip.ini'
    if not pip_ini.exists():
        with open(pip_ini, 'w') as f:
            f.write(PIP_INI_CONFIG)
    return True


def install_package():
    subprocess.run(["pip", "install", "-U", REPO_URL])


def create_desktop_shortcut():
    '''
    Create a .bat file to run reports.
    '''
    username = os.getlogin()
    file_location = Path(fr"C:\Users\{username}\OneDrive - Enterprise 365\Desktop") / 'Run Reports.bat'
    with open(file_location, 'w') as f:
        f.write(BAT_FILE_CONTENT)


if __name__ == '__main__':
    create_pip_ini()
    install_package()
    create_desktop_shortcut()
    print('\nSetup finished.')
    sleep(3)


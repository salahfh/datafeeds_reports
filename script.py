from pathlib import Path
import os
import subprocess

# Requirement is to have python installed. 

REPO_URL = 'git+https://github.com/salahfh/datafeeds_reports'
PIP_INI_CONFIG  = '''
[global]
trusted-host = pypi.python.org
               pypi.org
               files.pythonhosted.org
               raw.githubusercontent.com
               github.com
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


if __name__ == '__main__':
    create_pip_ini()
    install_package()
    input('Setup finished. press any key to continue ...')



# Launch pip to install the package
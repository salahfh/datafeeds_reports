from pathlib import Path
import os
import subprocess


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


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


def ensure_pip_is_installed() -> int:
    status = subprocess.run(['py', '-m', 'ensurepip', '--upgrade'])
    return status.returncode


def create_pip_ini() -> int:
    '''
    Create pip.ini to fix the self-signed cerficates issue due environment setup.
    '''
    folder_location = Path(os.getenv('APPDATA')) / 'pip'
    pip_ini = folder_location / 'pip.ini'
    if not pip_ini.exists():
        with open(pip_ini, 'w') as f:
            f.write(PIP_INI_CONFIG)
    return 0


def install_packages() -> int:
    status = subprocess.run(["pip", "install", "-U", REPO_URL])
    return status.returncode


def create_desktop_shortcut() -> int:
    '''
    Create a .bat file to run reports.
    '''
    username = os.getlogin()
    file_location = Path(fr"C:\Users\{username}\OneDrive - Enterprise 365\Desktop") / 'Run Reports.bat'
    with open(file_location, 'w') as f:
        f.write(BAT_FILE_CONTENT)
    return 0


def create_folder_structure() -> int:
    status = subprocess.run(["reports", "run"])
    return status.returncode


def allow_bat_script_to_run_for_current_user() -> int:
    subprocess.Popen(["powershell.exe",  "Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUse"])
    return 0


if __name__ == '__main__':
    for index, step in enumerate([
        ensure_pip_is_installed,
        create_pip_ini,
        install_packages,
        create_desktop_shortcut,
        allow_bat_script_to_run_for_current_user,
        create_folder_structure,
            ]):
        print(f'{bcolors.OKCYAN}{index+1}. {step.__name__.replace('_', ' ').title()} ...{bcolors.ENDC}')
        status_code = step()
        if status_code != 0:
            print(f'\n{bcolors.FAIL}Setup step failed.{bcolors.ENDC}')
    if status_code == 0:
        print(f'\n{bcolors.OKGREEN}Setup finished.{bcolors.ENDC}')
    input('Press any key to continue ...')

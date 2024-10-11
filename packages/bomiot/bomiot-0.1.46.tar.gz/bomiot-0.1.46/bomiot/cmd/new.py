from os.path import join, exists
from os import makedirs, getcwd
import subprocess
import sys
import shutil
from pathlib import Path
import toml


def new(folder):
    """
    init workspace
    :param folder:
    :return:
    """
    if len(sys.argv) < 3:
        print('Please enter your project name')
    else:
        current_path = Path(__file__).resolve()
        file_path = join(current_path.parent, 'file')

        project_path = join(getcwd(), sys.argv[2])
        exists(project_path) or makedirs(project_path)
        shutil.copy2(join(file_path, 'config.ini'), project_path)
        shutil.copy2(join(file_path, 'LICENSE'), project_path)
        shutil.copy2(join(file_path, 'README.md'), project_path)

        with open(join(file_path, 'pyproject.toml'), 'r', encoding='utf-8') as project:
            project_pip = toml.load(project)
        del project_pip['tool']['poetry']['scripts']
        project_pip['tool']['poetry']['name'] = sys.argv[2]
        project_pip['tool']['poetry']['version'] = '0.0.1'
        with open(join(project_path, 'pyproject.toml'), 'w', encoding='utf-8') as file:
            toml.dump(project_pip, file)

        log_path = join(getcwd(), 'logs')
        exists(log_path) or makedirs(log_path)

        print('Initialized workspace %s' % folder)

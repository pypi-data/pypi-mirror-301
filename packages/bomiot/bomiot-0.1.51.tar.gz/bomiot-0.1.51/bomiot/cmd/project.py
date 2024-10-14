from os.path import join, exists
from os import makedirs, getcwd
import sys
import shutil
from pathlib import Path
import toml
from configparser import ConfigParser


def project(folder):
    """
    project workspace
    :param folder:
    :return:
    """
    if len(sys.argv) < 3:
        print('Please enter your project name')
    else:
        project_path = join(getcwd(), sys.argv[2])
        if exists(project_path):
            print('Project directory already exists')
        else:
            makedirs(project_path)
            current_path = Path(__file__).resolve()
            file_path = join(current_path.parent, 'file')

            shutil.copy2(join(file_path, 'project_config.ini'), project_path)
            shutil.copy2(join(file_path, 'LICENSE'), project_path)
            shutil.copy2(join(file_path, 'README.md'), project_path)

            if exists(join(getcwd(), 'setup.ini')) is False:
                shutil.copy2(join(file_path, 'setup.ini'), join(getcwd()))
                config = ConfigParser()
                config.read(join(getcwd(), 'setup.ini'))
                config.set('site', 'name', sys.argv[2])
                config.set('db_name', 'name', sys.argv[2])
                with open(join(getcwd(), 'setup.ini'), 'w') as setupfile:
                    config.write(setupfile)

            with open(join(file_path, 'pyproject.toml'), 'r', encoding='utf-8') as project:
                project_pip = toml.load(project)
            del project_pip['tool']['poetry']['scripts']
            project_pip['tool']['poetry']['name'] = sys.argv[2]
            project_pip['tool']['poetry']['version'] = '0.0.1'
            with open(join(project_path, 'pyproject.toml'), 'w', encoding='utf-8') as file:
                toml.dump(project_pip, file)

            log_path = join(getcwd(), 'logs')
            exists(log_path) or makedirs(log_path)

            media_path = join(getcwd(), 'media')
            exists(media_path) or makedirs(media_path)

            print('Initialized workspace %s' % sys.argv[2])

from os.path import join, exists
from os import makedirs, getcwd
import shutil
from pathlib import Path
from .create import create_file
from configparser import ConfigParser

def deploy(folder):
    """
    deploy project
    :param folder:
    :return:
    """
    current_path = Path(__file__).resolve()
    file_path = join(current_path.parent, 'file')

    create_file()
    if exists(join(getcwd(), 'deploy/uwsgi.ini')) is False:
        shutil.copy2(join(file_path, 'uwsgi.ini'), join(getcwd(), 'deploy'))
        config = ConfigParser()
        config.read(join(getcwd(), 'deploy/uwsgi.ini'))
        config.set('uwsgi', 'chdir', join(current_path.parent.parent, 'server'))
        config.set('uwsgi', 'wsgi-file', join(current_path.parent.parent, 'server/wsgi.py'))
        config.set('uwsgi', 'logto', join(getcwd(), 'logs'))
        with open(join(getcwd(), 'deploy/uwsgi.ini'), 'w') as deploy_file:
            config.write(deploy_file)

    print('Deploy project workspace success')

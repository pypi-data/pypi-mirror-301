from os.path import join, exists
from os import makedirs, getcwd
import shutil
from pathlib import Path
from .create import create_file


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


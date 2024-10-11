from os.path import join, exists, abspath
from os import makedirs, getcwd
import subprocess
import sys
import shutil

def new(folder):
    """
    init workspace
    :param folder:
    :return:
    """
    if len(sys.argv) < 3:
        print('Please enter your project name')
    else:
        current_path = abspath(__file__)
        file_path = join(current_path, 'file')
        uwsgi_path = join(file_path, 'uwsgi.ini')

        project_path = join(getcwd(), sys.argv[2])
        exists(project_path) or makedirs(project_path)
        shutil.copy2(uwsgi_path, project_path)

        log_path = join(getcwd(), 'logs')
        exists(log_path) or makedirs(log_path)

    print('Initialized workspace %s' % folder)

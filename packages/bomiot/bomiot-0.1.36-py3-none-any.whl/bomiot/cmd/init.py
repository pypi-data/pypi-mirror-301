from os.path import join, exists
from os import makedirs, getcwd
import subprocess
import sys

def init(folder):
    """
    init workspace
    :param folder:
    :return:
    """
    print(1)
    print(len(sys.argv[3]))
    log_path = join(getcwd(), 'logs')
    exists(log_path) or makedirs(log_path)

    print('Initialized workspace %s' % folder)

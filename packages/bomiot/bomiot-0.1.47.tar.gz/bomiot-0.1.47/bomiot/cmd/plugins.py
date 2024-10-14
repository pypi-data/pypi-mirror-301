from os.path import join, exists
from os import makedirs, getcwd
import sys
import shutil
from pathlib import Path
import toml


def plugins(folder):
    """
    plugins workspace
    :param folder:
    :return:
    """
    if len(sys.argv) < 3:
        print('Please enter your plugins name')
    else:
        plugins_path = join(getcwd(), sys.argv[2])
        if exists(plugins_path):
            print('Plugins directory already exists')
        else:
            makedirs(plugins_path)
            current_path = Path(__file__).resolve()
            file_path = join(current_path.parent, 'file')

            shutil.copy2(join(file_path, 'plugins_config.ini'), plugins_path)
            shutil.copy2(join(file_path, 'LICENSE'), plugins_path)
            shutil.copy2(join(file_path, 'README.md'), plugins_path)
            shutil.copy2(join(file_path, 'README.md'), join(getcwd()))

            with open(join(file_path, 'pyplugins.toml'), 'r', encoding='utf-8') as plugin:
                plugins_pip = toml.load(plugin)
            del plugins_pip['tool']['poetry']['scripts']
            plugins_pip['tool']['poetry']['name'] = sys.argv[2]
            plugins_pip['tool']['poetry']['version'] = '0.0.1'
            with open(join(plugins_path, 'pyplugins.toml'), 'w', encoding='utf-8') as file:
                toml.dump(plugins_pip, file)

            log_path = join(getcwd(), 'logs')
            exists(log_path) or makedirs(log_path)

            media_path = join(getcwd(), 'media')
            exists(media_path) or makedirs(media_path)

            print('Initialized workspace %s' % sys.argv[2])

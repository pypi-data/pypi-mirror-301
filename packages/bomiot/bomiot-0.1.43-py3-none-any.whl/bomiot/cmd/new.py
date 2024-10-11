from os.path import join, exists
from os import makedirs, getcwd
import subprocess
import sys
import shutil
from pathlib import Path
import toml

# 读取TOML文件
# with open('example.toml', 'r', encoding='utf-8') as file:
#     data = toml.load(file)

# 删除键
# del data['key_to_remove']  # 将'key_to_remove'替换成你想要删除的键的名称

# 如果要删除嵌套键，可以使用如下方式：
# del data['parent_key']['child_key']

# 保存更改到TOML文件
# with open('example.toml', 'w', encoding='utf-8') as file:
#     toml.dump(data, file)

def new(folder):
    """
    init workspace
    :param folder:
    :return:
    """
    if len(sys.argv) < 3:
        print('Please enter your project name')
    else:
        current_path = Path(__file__).resolve().parent
        file_path = join(current_path, 'file')
        uwsgi_path = join(file_path, 'uwsgi.ini')

        project_path = join(getcwd(), sys.argv[2])
        exists(project_path) or makedirs(project_path)
        shutil.copy2(uwsgi_path, project_path)

        with open(join(file_path, 'pyproject.toml'), 'r', encoding='utf-8') as project:
            data = toml.load(project)
        print(data)
        log_path = join(getcwd(), 'logs')
        exists(log_path) or makedirs(log_path)

    print('Initialized workspace %s' % folder)

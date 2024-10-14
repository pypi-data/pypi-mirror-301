import os
import sys
from ..compilation import compile


def get_init_loader(module_name):
    return \
f'''import sys
import shutil
import os

PWD = os.path.abspath(os.path.dirname(__file__))


def get_python_version():
    return str(sys.version_info.major) + '-' + str(sys.version_info.minor)


def flood_here(source_folder):
    for root, dirs, files in os.walk(source_folder):
        for file in files:
            source_file = os.path.join(root, file)

            relative_path = os.path.relpath(root, source_folder)
            destination_folder = os.path.join(PWD, relative_path)
            destination_file_path = os.path.join(destination_folder, file)

            if destination_file_path.endswith('.py'):
                destination_file_path += 'c'

            os.makedirs(destination_folder, exist_ok=True)
            shutil.copy(source_file, destination_file_path)


flood_here(f'{{PWD}}/_CB/{module_name}{{get_python_version()}}')

from . import second_init

for thing in dir(second_init):
    globals()[thing] = getattr(second_init, thing)
'''


def get_python_version():
    return str(sys.version_info.major) + '-' + str(sys.version_info.minor)


def multiversion_obfuscate_package(path: str, output_path=None, syspath: str = None, scaffoldy: bool = True, global_variables=None):
    if syspath:
        sys.path.insert(1, syspath)

    assert os.path.exists(path), Exception('Folder does not exist.')

    folder_name = os.path.basename(path)

    if not output_path:
        output_path = f'c{folder_name}'

    compile(folder_name, f"{output_path}/_CB/{folder_name}{get_python_version()}", rename_init='second_init.py', scaffoldy=scaffoldy, global_variables=global_variables)

    with open(f'{output_path}/__init__.py', 'w') as f:
        f.write(get_init_loader(folder_name))

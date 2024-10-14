import os
import sys
from ..compilation import compile


def obfuscate_package(path: str, output_path=None, syspath: str = None, scaffoldy: bool = True, global_variables=None):
    if syspath:
        sys.path.insert(1, syspath)

    assert os.path.exists(path), Exception('Folder does not exist.')

    folder_name = os.path.basename(path)

    if not output_path:
        output_path = f'c{folder_name}'

    compile(folder_name, f"{output_path}", scaffoldy=scaffoldy, global_variables=global_variables)

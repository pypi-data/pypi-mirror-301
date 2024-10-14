import os
import py_compile
import sys
import shutil
import tempfile
from ..scaffoldy import CodeProcessor


def scaffold_file(file_path, global_variables):
    destination_dir = os.path.dirname(file_path)
    destination_path = os.path.join(destination_dir, os.path.basename(file_path))
    os.makedirs(destination_dir, exist_ok=True)

    with open(file_path, 'r') as f:
        content = f.read()

    with open(destination_path, 'w') as f:
        f.write(CodeProcessor.process_code(content, global_variables))

    return destination_path, file_path, content


def compile_file(path: str, output_path: str, scaffoldy=True, global_variables=None):
    if global_variables is None:
        global_variables = {}

    if scaffoldy:
        path, old_content = scaffold_file(path, global_variables)

    if os.path.isdir(output_path) and not os.path.isfile(output_path):
        filename = os.path.basename(path)
        output_path = os.path.join(output_path, filename)

    py_compile.compile(path, cfile=pyc_path, optimize=0)
    print(f"Compiled file: {path} to {pyc_path}")


def extension(file_path):
    return os.path.splitext(file_path)[1][1:]


def scaffold_copy(filepath, output_path, global_variables, scaffold_files):
    shutil.copy(filepath, output_path)

    if extension(filepath) in scaffold_files:
        print(f'Processing file because its extension is in scaffold_files: {filepath}')
        with open(output_path, 'r') as f:
            code = f.read()

        with open(output_path, 'w') as f:
            f.write(CodeProcessor.process_code(code, global_variables))


def compile_directory(path: str, output_dir: str, rename_init: str = '__init__.py', scaffoldy=True, scaffold_files=None, global_variables=None):
    if scaffold_files is None:
        scaffold_files = ['py', 'css', 'js', 'xml', 'html']

    os.makedirs(output_dir, exist_ok=True)

    if global_variables is None:
        global_variables = {}

    for root, dirs, files in os.walk(path):
        for file in files:
            file_path = os.path.join(root, file)

            if scaffoldy and extension(file_path) in scaffold_files:
                file_path, old_path, old_content = scaffold_file(file_path, global_variables)

            rel_path = os.path.relpath(file_path, path)
            output_file = os.path.join(output_dir, rel_path)

            os.makedirs(os.path.dirname(output_file), exist_ok=True)

            if file.endswith('.py'):
                if file == '__init__.py':
                    output_file = output_file.replace('__init__.py', 'second_init.py')

                py_compile.compile(file_path, cfile=output_file, optimize=0)
                print(f"Compiled file: {file_path} to {output_file}")
            else:
                scaffold_copy(file_path, output_file, global_variables, scaffold_files)
                print(f"Copied file: {file_path} to {output_file}")

            if scaffoldy:
                with open(old_path, 'w') as f:
                    f.write(old_content)


def compile(path: str,
            output_dir: str = 'compiled_files',  # Directory name to store compiled package
            output_file: str = 'compiled_file.py',  # File name to store compiled python file
            rename_init: str = '__init__.py',
            syspath: str = None,
            scaffoldy: bool = True,
            global_variables: dict = None):

    if global_variables is None:
        global_variables = {}

    if syspath:
        sys.path.insert(1, syspath)

    if os.path.isfile(path):
        compile_file(path, output_dir, scaffoldy=scaffoldy, global_variables=global_variables)
    elif os.path.isdir(path):
        compile_directory(path, output_dir, rename_init=rename_init, scaffoldy=scaffoldy, global_variables=global_variables)
    else:
        raise Exception(f"The path {path} is neither a file nor a directory or does not exist.")

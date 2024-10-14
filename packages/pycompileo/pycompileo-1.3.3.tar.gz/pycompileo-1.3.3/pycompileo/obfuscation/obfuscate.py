import os
from .obfuscate_package import obfuscate_package
from .obfuscate_module import obfuscate_module


def obfuscate(path: str, output_path=None, syspath: str = None, scaffoldy: bool = True, global_variables=None):
    if os.path.isfile(path):
        obfuscate_module(path, output_path, syspath, scaffoldy=scaffoldy, global_variables=global_variables)
    elif os.path.isdir(path):
        obfuscate_package(path, output_path, syspath, scaffoldy=scaffoldy, global_variables=global_variables)
    else:
        raise Exception(f"The path {path} is neither a file nor a directory or does not exist..")

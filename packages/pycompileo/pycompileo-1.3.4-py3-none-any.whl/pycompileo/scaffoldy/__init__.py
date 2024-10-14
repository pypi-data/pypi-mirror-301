import re
import os
import shutil


class CodeProcessor:
    DEFINE_PATTERN = re.compile(r"^\s*#DEFINE\s+(\w+)\s*=\s*(.+)")
    IF_PATTERN = re.compile(r"^\s*#IF\s+(.+)")
    ENDIF_PATTERN = re.compile(r"^\s*#ENDIF")

    @staticmethod
    def evaluate_condition(condition, variables):
        try:
            return eval(condition, {}, variables)
        except NameError as e:
            print(f"Error: {e}")
            return False

    @classmethod
    def process_code(cls, code, global_variables=None, file_extension: str = ''):
        if global_variables is None:
            global_variables = {}

        variables = global_variables
        execute = True
        processed_lines = []

        for line in code.splitlines():
            if define_match := cls.DEFINE_PATTERN.match(line):
                var_name = define_match.group(1).strip()
                var_value = eval(define_match.group(2).strip(), {}, variables)
                variables[var_name] = var_value

            elif if_match := cls.IF_PATTERN.match(line):
                condition = if_match.group(1).strip()
                execute = cls.evaluate_condition(condition, variables)
            elif cls.ENDIF_PATTERN.match(line):
                execute = True
            elif file_extension == 'xml' and variables['ODOO_VERSION'] == 18:
                processed_lines.append(line.replace('<tree', '<list').replace('</tree>', '</list>'))
            elif execute:
                processed_lines.append(line)

        return '\n'.join(processed_lines)


def build(global_variables, allowed_extensions, src_directory='src', output_directory='build/odoo{ODOO_VERSION}'):
    assert global_variables is not None, ValueError(
        'Please provide all the global variables using the parameter "global_variables"')

    output_directory = output_directory.format(**global_variables)
    os.makedirs(output_directory, exist_ok=True)

    for dirpath, _, filenames in os.walk(src_directory):
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)

            # Determine the relative path for the output file
            relative_path = os.path.relpath(dirpath, src_directory)
            output_dir = os.path.join(output_directory, relative_path)
            os.makedirs(output_dir, exist_ok=True)

            if filename.split('.')[-1] in allowed_extensions:
                with open(file_path, 'r') as file:
                    try:
                        code = file.read()
                    except Exception as e:
                        print(f'Error reading file: {file_path}! Reason: {e}')
                        continue

                processed_code = CodeProcessor.process_code(code, global_variables, filename.split('.')[-1])

                output_file_path = os.path.join(output_dir, filename)
                with open(output_file_path, 'w') as output_file:
                    output_file.write(processed_code)
            else:
                # Copy unrecognized files to the output directory
                shutil.copy2(file_path, output_dir)


if __name__ == '__main__':
    build({'ODOO_VERSION': 18}, ['py', 'css', 'xml'], 'src/', 'build/')

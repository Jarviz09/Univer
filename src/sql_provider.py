import os

from string import Template


class SQLProvider:
    """
    Makes dict with key: name of file; value: SQL request
    """
    def __init__(self, file_path):

        self._scripts = {}

        for file in os.listdir(file_path):
            if file.endswith('.sql'):
                self._scripts[file] = Template(open(f'{file_path}/{file}', 'r').read())

    def get(self, file_name, **kwargs):
        return self._scripts[file_name].substitute(**kwargs)

import os
import yaml
from typing import Union


class ConfigLoader:
    @staticmethod
    def load_env_var_from_file(variable_name: str, file_path: str):
        with open(file_path, 'r') as f:
            os.environ[variable_name] = f.read()

    @staticmethod
    def load_yaml_file(file_path: Union[str, bytes, os.PathLike]):
        try:
            with open(file_path, 'r') as stream:
                return yaml.safe_load(stream)
        except Exception as e:
            # TODO add error handling
            pass

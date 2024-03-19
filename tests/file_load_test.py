import os

from fun_project.config_model import ConfigModel
import yaml
import csv

cwd = os.getcwd()
if 'tests' not in cwd:
    cwd = f'{cwd}/tests'


def test_load_yaml_file_to_config() -> None:
    loaded_yaml = yaml.load(open(f'{cwd}/test_files/success_config.yaml', 'r'), Loader=yaml.FullLoader)
    cm = ConfigModel(**loaded_yaml)
    assert cm is not None


def test_load_csv_file() -> None:
    loaded_csv = csv.reader(open(f'{cwd}/test_files/test_csv.csv', 'r'))
    assert loaded_csv is not None

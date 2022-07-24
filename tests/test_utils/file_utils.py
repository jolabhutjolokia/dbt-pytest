import json
from typing import Dict
import os

dirname = os.path.dirname(__file__)


def load_template(object_name: str) -> Dict[str, str]:
    file_name = os.path.join(dirname, f'../data_templates/{object_name}.json')
    return read_json_from_file(file_name)


def read_json_from_file(file_path: str) -> Dict:
    return json.load(file_path)

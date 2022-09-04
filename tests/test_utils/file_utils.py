import json
from typing import Dict
import os

dirname = os.path.dirname(__file__)


def load_template(object_name: str) -> Dict[str, str]:
    file_name = os.path.join(dirname, 'data_templates', f'{object_name}.json')
    return read_json_from_file(file_name)


def read_json_from_file(file_path: str) -> Dict:
    print(f'reading file {file_path}')
    with open(file_path, 'rb') as f:
        return json.load(f)

import os
from typing import Dict

import chevron

dirname = os.path.dirname(__file__)


def load_template(object_name: str, tokens: Dict[str, str]) -> str:
    file_name = os.path.join(dirname, 'data_templates', f'{object_name}.json')
    with open(file_name, 'r') as f:
        return chevron.render(f, tokens)

import json
from typing import List, Dict

from tests.test_utils.file_utils import load_template


def _fill_tokens_in_template(template: Dict, tokens: Dict[str, str]) -> Dict[str, str]:
    json_str = json.dumps(template)
    for prop in tokens.keys():
        json_str = json_str.replace(f'{{{prop}}}', tokens[prop])
    return json.loads(json_str)


def _apply_overrides(template: Dict, overrides: Dict[str, str]) -> Dict[str, str]:
    template_copy = template.copy()
    for prop in overrides.keys():
        template_copy[prop] = overrides[prop]
    return template_copy


def _apply_relationships(template: Dict, relationships: Dict[str, str], tokens: Dict[str, str]) -> Dict[str, str]:
    template_copy = template.copy()
    for obj_to_join_to in relationships.keys():
        fk_prop = relationships[obj_to_join_to]
        template_copy[fk_prop] = f"{tokens['EXEC_ID']}{obj_to_join_to}"
    return template_copy


class ScenarioBuilder:

    def __init__(self, object_names: List[str]):
        self._object_names = object_names
        self._relationships: Dict[str, Dict[str, str]] = {}
        self._overrides: Dict[str, Dict[str, str]] = {}

    def add_relationship(self, object_from: str, fk: str, object_to) -> "ScenarioBuilder":
        if object_from in self._relationships.keys():
            self._relationships[object_from][object_to] = fk
        else:
            self._relationships[object_from] = {object_to: fk}
        return self

    def add_overrides(self, obj: str, overrides: Dict[str, str]) -> "ScenarioBuilder":
        self._overrides[obj] = overrides
        return self

    def build(self, tokens: Dict[str, str]) -> Dict[str, Dict[str, str]]:
        build_data: Dict[str, Dict[str, str]] = {}
        for object_name in self._object_names:
            data = load_template(object_name)
            data = _apply_overrides(data, self._overrides[object_name])
            data = _fill_tokens_in_template(data, tokens)
            build_data[object_name] = _apply_relationships(data, self._relationships[object_name], tokens)
        return build_data

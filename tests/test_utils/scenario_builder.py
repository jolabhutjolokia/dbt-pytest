import json
from typing import List, Dict

from tests.test_utils.file_utils import load_template


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

    def _apply_overrides(self, json_data: Dict[str, str], object_name: str) -> Dict[str, str]:
        if object_name not in self._overrides.keys():
            return json_data
        overrides = self._overrides[object_name]
        return {**json_data, **overrides}

    def _apply_relationships(self, data: Dict, object_name: str, tokens: Dict[str, str]) -> Dict[str, str]:
        if object_name not in self._relationships.keys():
            return data
        data_copy = data.copy()
        relationships = self._relationships[object_name]
        for obj_to_join_to in relationships.keys():
            fk_prop = relationships[obj_to_join_to]
            fk = f"{tokens['EXEC_ID']}{obj_to_join_to}"
            data_copy[fk_prop] = fk
        return data_copy

    def build(self, tokens: Dict[str, str]) -> Dict[str, Dict[str, str]]:
        build_data: Dict[str, Dict[str, str]] = {}
        for object_name in self._object_names:
            json_str_template = load_template(object_name, tokens)
            json_data = json.loads(json_str_template)
            json_data = self._apply_overrides(json_data, object_name)
            build_data[object_name] = self._apply_relationships(json_data, object_name, tokens)
        return build_data

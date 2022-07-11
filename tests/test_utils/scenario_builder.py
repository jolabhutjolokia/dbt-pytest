from typing import List, Dict


class ScenarioBuilder:

    def __init__(self, objects: List[str]):
        self._objects = objects

    def add_relationship(self, object_from: str, fk: str, object_to) -> "ScenarioBuilder":
        return self

    def add_overrides(self, object: str, overrides: Dict[str, str]) -> "ScenarioBuilder":
        return self

    def build(self, token: Dict[str, str]) -> Dict[str, Dict[str, str]]:
        return {}
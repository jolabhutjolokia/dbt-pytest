from typing import Dict, Optional

from scenario_builder import ScenarioBuilder


class ScenarioData:

    def __init__(self, config: ScenarioBuilder, tokens: Dict[str, str]):
        self._object_values: Optional[Dict[str, Dict[str, str]]] = None
        self._tokens = tokens
        self._config = config

    def generate(self) -> Dict[str, Dict[str, str]]:
        if self._object_values is not None:
            return self._object_values
        self._object_values = self._config.build(self._tokens)
        return self._object_values

    def value_for(self, entity: str, prop: str):
        return self._object_values[entity][prop]

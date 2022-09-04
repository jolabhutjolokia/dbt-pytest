import json
from typing import Dict, List

from tests.test_utils.scenario_builder import ScenarioBuilder


class ExternalTableData:

    def __init__(self, object_name: str, data: Dict[str, str], date_partition: str) -> None:
        self._object_name = object_name
        self._data = data
        self._date_partition = date_partition

    def object_name(self):
        return self._object_name

    def get_value(self, prop: str) -> str:
        return self._data[prop]

    def insert_sql(self):
        json_str = json.dumps(self._data)
        name = self._object_name.lower()
        return f"Insert into test_ext.ext_{name}(date_partition, value) values(date_partition, ('{json_str}')::json)"


class ScenarioData:

    def __init__(self, config: ScenarioBuilder, tokens: Dict[str, str]):
        self._external_table_data: List[ExternalTableData] = []
        self._tokens = tokens
        self._config = config

    def generate(self) -> list[ExternalTableData]:
        if len(self._external_table_data) == 0:
            self._generate_data()
        return self._external_table_data

    def _generate_data(self):
        built_data = self._config.build(self._tokens)
        for key in built_data.keys():
            table_data = ExternalTableData(key, built_data[key], self._tokens['DATE_PARTITION'])
            self._external_table_data.append(table_data)

    def value_for(self, entity: str, prop: str):
        if len(self._external_table_data) == 0:
            self._generate_data()
        matching_data = list(filter(lambda x: x.object_name() == entity, self._external_table_data))
        if len(matching_data) == 0:
            raise AttributeError(f'No data for {entity} object')
        return matching_data[0].get_value(prop)

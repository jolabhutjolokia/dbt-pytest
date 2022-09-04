import os
from functools import reduce
from typing import Dict, List

import pendulum
import pytest

from tests.test_utils.process_utils import execute_command
from tests.test_utils.db_wrapper import DbWrapper
from tests.test_utils.scenario_data import ScenarioData, ExternalTableData


@pytest.fixture(scope="session")
def db_conn() -> DbWrapper:
    return DbWrapper()


@pytest.fixture(scope="session")
def test_time() -> pendulum.DateTime:
    return pendulum.now('UTC')


@pytest.fixture(scope="session")
def default_args(test_time: pendulum.DateTime) -> Dict[str, str]:
    return {
        'SYS_MOD_STAMP': test_time.isoformat(),
        'DEFAULT_DATE': test_time.format('YYYY-MM-DD'),
        'DEFAULT_INT': 100,
        'DATE_PARTITION': test_time.isoformat()
    }


@pytest.fixture(scope="session")
def dbt_env_vars(test_time: pendulum.DateTime) -> Dict[str, str]:
    return {
        'SYS_MOD_STAMP': test_time.isoformat(),
        'DEFAULT_DATE': test_time.format('YYYY-MM-DD'),
        'DEFAULT_INT': 100
    }


@pytest.fixture(scope="session")
def scenario_data(default_args: Dict[str, str],
                  dbt_env_vars: Dict[str, str],
                  request) -> List[ScenarioData]:
    seen = {None}
    session = request.node
    all_scenario_data = []
    for item in session.items:
        cls = item.getparent(pytest.Class)
        if cls not in seen:
            if hasattr(cls.obj, "get_scenario_data"):
                all_scenario_data = all_scenario_data + cls.obj.get_scenario_data(default_args, dbt_env_vars)
            seen.add(cls)
    return all_scenario_data


@pytest.fixture(scope="session", autouse=True)
def setup_data_and_run_dbt(db_conn: DbWrapper,
                           scenario_data: List[ScenarioData]) -> None:
    all_external_data: List[ExternalTableData] = reduce(lambda acc, x: acc + x.generate(), scenario_data, [])
    object_names = reduce(lambda acc, x: acc.union({x.object_name()}), all_external_data, set())

    for object_name in object_names:
        db_conn.execute_sql('CREATE SCHEMA IF NOT EXISTS test_ext')
        lowercase_name = str(object_name).lower()
        db_conn.execute_sql(
            f'CREATE TABLE IF NOT EXISTS test_ext.ext_{lowercase_name}(date_partition TIMESTAMP, value JSON)')

    for data_for_tables in all_external_data:
        db_conn.execute_sql(data_for_tables.insert_sql())

    cwd = os.path.join(os.path.dirname(__file__), '..', 'dbt')

    execute_command('dbt run', {'IS_TEST_MODE': 'true'}, cwd=cwd)

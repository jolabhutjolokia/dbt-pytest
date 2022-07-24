from typing import Dict, List

import pendulum
import pytest

from tests.test_utils.db_wrapper import DbWrapper
from tests.test_utils.scenario_data import ScenarioData


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
        'DEFAULT_INT': 100
    }


@pytest.fixture(scope="session")
def dbt_env_vars(test_time: pendulum.DateTime) -> Dict[str, str]:
    return {
        'SYS_MOD_STAMP': test_time.isoformat(),
        'DEFAULT_DATE': test_time.format('YYYY-MM-DD'),
        'DEFAULT_INT': 100
    }


@pytest.fixture(scope="session")
def scenario_data(request) -> List[ScenarioData]:
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
                           default_args: Dict[str, str],
                           dbt_env_vars: Dict[str, str],
                           scenario_data: List[ScenarioData]):
    data = map(lambda x: x.generate(), scenario_data)

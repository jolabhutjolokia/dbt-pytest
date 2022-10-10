from typing import Dict, List
from uuid import uuid4

from pandas import DataFrame

from tests.test_utils.db_wrapper import DbWrapper
from tests.test_utils.scenario_builder import ScenarioBuilder
from tests.test_utils.scenario_data import ScenarioData


def _get_all_account_details(contact_id: str, db_conn: DbWrapper) -> DataFrame:
    return db_conn.get_data_frame(f"Select * from AccountDetails WHERE AccountId='{contact_id}';")


def _contact_with_account() -> ScenarioBuilder:
    return ScenarioBuilder(['Contact', 'Account']) \
        .add_relationship('Account', 'ContactId', 'Contact') \
        .add_overrides('Contact', {'Mobile': '+614444444444'})


class TestWhenContactHasAnAccount:
    _account_with_contact = None

    @classmethod
    def get_scenario_data(cls,
                          default_args: Dict[str, str],
                          dbt_vars: Dict[str, str]) -> List[ScenarioData]:
        cls._default_args = default_args
        cls._dbt_vars = dbt_vars
        cls._account_with_contact = ScenarioData(_contact_with_account(), {'EXEC_ID': str(uuid4()), **default_args})
        return [cls._account_with_contact]

    def test_account_details_should_be_mapped_correctly(self, db_conn: DbWrapper):
        expected_account_id = self._account_with_contact.value_for('Account', 'Id')

        actual = _get_all_account_details(expected_account_id, db_conn)

        assert len(actual.index) == 1
        assert actual['mobile'].iloc[0] == self._account_with_contact.value_for('Contact', 'Mobile')
        assert actual['contact_id'].iloc[0] == self._account_with_contact.value_for('Contact', 'Id')
        assert actual['account_id'].iloc[0] == self._account_with_contact.value_for('Account', 'Id')
        assert actual['amount_due'].iloc[0] == int(self._account_with_contact.value_for('Account', 'AmountDue'))

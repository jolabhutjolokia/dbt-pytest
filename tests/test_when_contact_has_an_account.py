from typing import Dict, List

from tests.test_utils.scenario_builder import ScenarioBuilder
from tests.test_utils.scenario_data import ScenarioData
from uuid import uuid4
from snowflake.connector.connection import SnowflakeConnection
from pandas import DataFrame


def _get_all_account_details(contact_id: str, connection: SnowflakeConnection) -> DataFrame:
    with connection.cursor() as cursor:
        cursor.execute(f"Select * from AccountDetails WHERE AccountId='{contact_id}';")
        return cursor.fetch_pandas_all()


def _contact_with_account() -> ScenarioBuilder:
    return ScenarioBuilder(['Contact', 'Account']) \
        .add_relationship('Account', 'ContactId', 'Contact') \
        .add_overrides('Contact', {'Mobile': '+614444444444'})


class TestWhenContactHasAnAccount:
    _account_with_contact = None

    @classmethod
    def get_integration_test_data(cls,
                                  default_args: Dict[str, str],
                                  dbt_vars: Dict[str, str]) -> List[ScenarioData]:
        cls._default_args = default_args
        cls._dbt_vars = dbt_vars
        token_values = dict({'EXEC_ID': str(uuid4()), **default_args})
        cls._account_with_contact = ScenarioData(_contact_with_account(), token_values)
        return [cls._account_with_contact]

    def test_account_details_should_be_mapped_correctly(self, snowflake_connection: SnowflakeConnection):
        expected_account_id = self._account_with_contact.value_for('Account', 'Id')

        actual = _get_all_account_details(expected_account_id, snowflake_connection)

        assert len(actual.index) == 1
        assert actual['Mobile'].iloc[0] == self._account_with_contact.value_for('Contact', 'Mobile')
        assert actual['ContactId'].iloc[0] == self._account_with_contact.value_for('Contact', 'Id')
        assert actual['AccountId'].iloc[0] == self._account_with_contact.value_for('Account', 'Id')
        assert actual['AmountDue'].iloc[0] == int(self._account_with_contact.value_for('Account', 'AmountDue'))

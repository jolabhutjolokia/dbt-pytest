import pytest


@pytest.fixture(scope="session", autouse=True)
def setup_data_and_run_dbt(request):
    seen = {None}
    session = request.node
    all_data = []

    # create required dependencies for tests
    default_args = {}
    dbt_vars = {}

    # collect all the metadata for data to be created
    for item in session.items:
        cls = item.getparent(pytest.Class)
        if cls not in seen:
            if hasattr(cls.obj, "get_integration_test_data"):
                # provide the params to all tests and collect the data to setup
                all_data = all_data + cls.obj.get_integration_test_data(default_args, dbt_vars)
            seen.add(cls)

    # create external tables using snowflake connector
    # use the metadata from the tests to put data in the test external tables
    # execute dbt with the env vars in dbt_vars

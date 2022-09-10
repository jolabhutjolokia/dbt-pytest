import pandas
import sqlalchemy


class DbWrapper:
    _sql_engine = None
    _conn = None

    def __init__(self, host='localhost', user='postgres', password='postgres', database='postgres', port=5432) -> None:
        self._host = host
        self._user = user
        self._password = password
        self._database = database
        self._port = port
        connection_str = f"postgresql://{self._user}:{self._password}@{self._host}:{self._port}/{self._database}"
        self._sql_engine = sqlalchemy.create_engine(connection_str)

    def __enter__(self) -> 'DbWrapper':
        self._conn = self._sql_engine.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._conn.close()

    def get_data_frame(self, sql: str) -> pandas.DataFrame:
        return pandas.read_sql_query(sql, self._sql_engine)

    def execute_sql(self, sql: str) -> None:
        text_sql = sqlalchemy.sql.text(sql)
        if self._conn is None:
            self.__enter__()
        self._conn.execute(text_sql)

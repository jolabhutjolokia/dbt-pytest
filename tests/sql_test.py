from sqlalchemy import text, create_engine

connection_str = f"postgresql://postgres:postgres@localhost:5432/postgres"
engine = create_engine(connection_str)
with engine.connect() as conn:
    conn.execute(text('CREATE SCHEMA IF NOT EXISTS test_ext'))
    conn.execute(text('CREATE TABLE IF NOT EXISTS test_ext.ext_contact(date_partition TIMESTAMP, value JSON)'))

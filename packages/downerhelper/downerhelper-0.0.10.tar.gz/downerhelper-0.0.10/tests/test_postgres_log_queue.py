import pytest
from downerhelper.logs import PostgresLogQueue
from downerhelper.secrets import get_secret_value, get_config_dict
import os
from uuid import uuid4
import psycopg2 as pg

def test_class_valid_queue():
    db_config = get_config_dict('db-config-1', os.getenv('KEYVAULT_URL'))
    logger_name = str(uuid4())
    job_id = str(uuid4())
    table = 'pytest_logs_queue'

    queue = PostgresLogQueue(logger_name, job_id, table, db_config)

    messages = [str(uuid4()) for _ in range(4)]
    for message in messages:
        queue.add('INFO', message)

    queue.save()

    try:
        conn = pg.connect(**db_config)
        cur = conn.cursor()
        cur.execute(f"""select name, job_id 
        from {table}
        where job_id = '{job_id}';""")
        rows = cur.fetchall()
    except:
        assert False

    assert len(rows) >= len(messages)
    for row in rows:
        assert row[0] == logger_name
        assert row[1] == job_id

def test_invalid_queue():
    db_config_str = get_secret_value('db-config-1', os.getenv('KEYVAULT_URL'))
    db_config_split = db_config_str.split(',')
    keys = ['dbname', 'user', 'password', 'host']
    db_config = {k: v for k, v in zip(keys, db_config_split)}

    with pytest.raises(Exception):
        PostgresLogQueue(None, 'a', 'a', db_config)

    with pytest.raises(Exception):
        PostgresLogQueue('a', None, 'a', db_config)

    with pytest.raises(Exception):
        PostgresLogQueue('a', 'a', None, db_config)

    with pytest.raises(Exception):
        PostgresLogQueue('a', 'a', 'a', {})
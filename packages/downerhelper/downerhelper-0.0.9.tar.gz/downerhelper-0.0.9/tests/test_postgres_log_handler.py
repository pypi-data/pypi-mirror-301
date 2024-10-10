import pytest
from downerhelper.logs import PostgresLogHandler
from downerhelper.secrets import get_secret_value
import os
from uuid import uuid4
import psycopg2 as pg

def test_class_valid():
    db_config_str = get_secret_value('db-config-1', os.getenv('KEYVAULT_URL'))
    db_config_split = db_config_str.split(',')
    keys = ['dbname', 'user', 'password', 'host']
    db_config = {k: v for k, v in zip(keys, db_config_split)}

    logger_name = str(uuid4())
    job_id = str(uuid4())
    table = 'pytest_logs'

    logger = PostgresLogHandler(logger_name, job_id, table, db_config)

    messages = [str(uuid4()) for _ in range(4)]
    for message in messages:
        logger.info(message)
    
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

def test_invalid():
    db_config_str = get_secret_value('db-config-1', os.getenv('KEYVAULT_URL'))
    db_config_split = db_config_str.split(',')
    keys = ['dbname', 'user', 'password', 'host']
    db_config = {k: v for k, v in zip(keys, db_config_split)}

    logger = PostgresLogHandler(None, 'a', 'a', db_config)
    assert logger == None

    logger = PostgresLogHandler('a', None, 'a', db_config)
    assert logger == None

    logger = PostgresLogHandler('a', 'a', None, db_config)
    assert logger == None

    logger = PostgresLogHandler('a', 'a', 'a', {})
    assert logger == None
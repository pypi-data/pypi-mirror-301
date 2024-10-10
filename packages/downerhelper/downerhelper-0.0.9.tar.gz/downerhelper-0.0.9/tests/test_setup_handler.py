import pytest
from downerhelper.logs import setup_handler, get_config_dict
from downerhelper.secrets import get_secret_value
import os
from uuid import uuid4
import psycopg2 as pg

def test_get_config_dict():
    secret_name = 'db-config-test'
    db_config = get_config_dict(secret_name, os.getenv('KEYVAULT_URL'))
    assert db_config == {
        'dbname': 'value0',
        'user': 'value1',
        'password': 'VALue2',
        'host': 'value3'
    }

    with pytest.raises(Exception):
        get_config_dict('invalid', os.getenv('KEYVAULT_URL'))

def test_setup_handler():
    secret_name = 'db-config-1'
    table = os.getenv('LOG_TABLE')
    logger_name = str(uuid4())
    logger, job_id = setup_handler(secret_name, os.getenv('KEYVAULT_URL'), logger_name, table)
    assert logger != None
    assert isinstance(job_id, str)

    messages = [str(uuid4()) for _ in range(4)]
    for message in messages:
        logger.info(message)
    
    db_config_str = get_secret_value(secret_name, os.getenv('KEYVAULT_URL'))
    db_config_split = db_config_str.split(',')
    keys = ['dbname', 'user', 'password', 'host']
    db_config = {k: v for k, v in zip(keys, db_config_split)}

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

    set_job_id = str(uuid4())
    logger, job_id = setup_handler(secret_name, os.getenv('KEYVAULT_URL'), logger_name, table, job_id=set_job_id)
    assert logger != None
    assert job_id == set_job_id
    
def test_setup_handler_invalid():
    table = os.getenv('LOG_TABLE')
    logger_name = str(uuid4())
    logger, job_id = setup_handler('invalid', os.getenv('KEYVAULT_URL'), logger_name, table)
    assert logger == job_id == None
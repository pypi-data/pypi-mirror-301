from . import PostgresLogHandler
from ..secrets import get_secret_value
import logging 
from uuid import uuid4

def setup_handler(secret_name, keyvault_url, logger_name, table, job_id=None):
    try:
        db_config = get_config_dict(secret_name, keyvault_url)
        if not job_id:
            job_id = str(uuid4())
            logging.warning(f"Job ID: {job_id}")
        logger = PostgresLogHandler(logger_name, job_id, table, db_config)
        return logger, job_id
    except Exception as e:
        logging.error(f"Error setting up handler: {e}")
        return None, None
    
def get_config_dict(secret_name, keyvault_url):
    db_config_str = get_secret_value(secret_name, keyvault_url)
    db_config_split = db_config_str.split(',')
    keys = ['dbname', 'user', 'password', 'host']
    return {k: v for k, v in zip(keys, db_config_split)}

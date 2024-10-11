from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential
import logging

def get_secret_value(secret_name, vault_url, credential=DefaultAzureCredential(), logger=None):
    try:
        if not logger:
            logger = logging.getLogger(__name__)
        client = SecretClient(vault_url=vault_url, credential=credential)
        secret = client.get_secret(secret_name)
        return secret.value
    except Exception as e:
        logger.error(f"Error getting secret {secret_name}: {e}")
    return None

def get_config_dict(secret_name, keyvault_url):
    db_config_str = get_secret_value(secret_name, keyvault_url)
    db_config_split = db_config_str.split(',')
    keys = ['dbname', 'user', 'password', 'host']
    return {k: v for k, v in zip(keys, db_config_split)}
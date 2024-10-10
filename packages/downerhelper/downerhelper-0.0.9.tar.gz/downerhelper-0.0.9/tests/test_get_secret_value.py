import pytest
from downerhelper.secrets import get_secret_value
import os 
import logging 

def test_valid_secret():
    value = get_secret_value('test-secret', os.getenv('KEYVAULT_URL'))
    assert value == 'dfaec67d-cf0a-44e8-b5df-6e8346092450'

def test_valid_secret_logging():
    value = get_secret_value('test-secret', os.getenv('KEYVAULT_URL'), logger=logging.getLogger('test'))
    assert value == 'dfaec67d-cf0a-44e8-b5df-6e8346092450'

def test_invalid_secret():
    value = get_secret_value('invalid', os.getenv('KEYVAULT_URL'))
    assert value == None

def test_invalid_keyvault():
    value = get_secret_value('test-secret', 'https://invalid.vault.azure.net')
    assert value == None


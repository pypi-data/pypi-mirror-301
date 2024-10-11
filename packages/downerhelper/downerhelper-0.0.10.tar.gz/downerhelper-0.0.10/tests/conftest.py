import pytest
from dotenv import load_dotenv

@pytest.fixture(scope="session", autouse=True)
def setup_session():
    load_dotenv()
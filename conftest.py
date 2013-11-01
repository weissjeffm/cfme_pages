import pytest
import pages.login
pytest_plugins = "plugin.randomness",\
        "plugin.navigation",\
        "plugin.pytest_selenium"

@pytest.fixture
def login_admin():
    pass

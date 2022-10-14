from fastapi.testclient import TestClient
import pytest

from application.fastapi.app import create_app
# from application.flask.app import create_app
from manage import read_json_configuration


# @pytest.fixture
# def app():
#     app = create_app("testing")

#     return app

@pytest.fixture
def client():
    return TestClient(create_app())



@pytest.fixture(scope="session")
def app_configuration():
    return read_json_configuration("testing")


def pytest_addoption(parser):
    parser.addoption(
        "--integration", action="store_true", help="run integration tests"
    )


def pytest_runtest_setup(item):
    if "integration" in item.keywords and not item.config.getvalue(
        "integration"
    ):
        pytest.skip("need --integration option to run")

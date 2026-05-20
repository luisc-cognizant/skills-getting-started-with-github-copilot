import copy

import pytest

from src import app as app_module
from fastapi.testclient import TestClient


@pytest.fixture(scope="module")
def client():
    return TestClient(app_module.app)


@pytest.fixture(autouse=True)
def reset_activities():
    original_activities = copy.deepcopy(app_module.activities)
    yield
    app_module.activities = copy.deepcopy(original_activities)

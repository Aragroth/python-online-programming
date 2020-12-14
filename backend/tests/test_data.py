import pytest
from fastapi.testclient import TestClient

from api import app
from tests.storage_mock import StorageMock
from tests.utils import tasks_public_description


@pytest.fixture
async def api_server():
    return TestClient(app)


def test_get_tasks_description(api_server: TestClient):
    token = StorageMock.admin_token
    response = api_server.get(
        "/tasks", headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200 and response.json() == {"response": tasks_public_description}

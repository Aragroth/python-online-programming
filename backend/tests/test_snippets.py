import json

import pytest
from fastapi.testclient import TestClient

from api import app
from tests.storage_mock import StorageMock


@pytest.fixture
async def api_server():
    return TestClient(app)


def test_get_snippet_task_exists(api_server: TestClient):
    token = StorageMock.admin_token
    task_uuid = StorageMock.task_uuid

    response = api_server.get(
        f"/snippets/{task_uuid}", headers={"Authorization": f"Bearer {token}"},
    )
    assert (
            response.status_code == 200 and
            response.json() == {"code_snippet": StorageMock.code_snippet}
    )


def test_get_snippet_task_do_not_exists(api_server: TestClient):
    token = StorageMock.admin_token
    task_uuid = "SomeTaskThatDoesNotExists"

    response = api_server.get(
        f"/snippets/{task_uuid}", headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 404 and "code_snippet" not in response.json()


def test_save_snippet_task_exists(api_server: TestClient):
    token = StorageMock.admin_token
    task_uuid = StorageMock.task_uuid

    response = api_server.post(
        f"/snippets/{task_uuid}", headers={"Authorization": f"Bearer {token}"},
        data=json.dumps({"code": "print('hello world!')"})
    )

    assert response.status_code == 200 and response.json() == {"response": "ok"}


def test_save_snippet_task_do_not_exists(api_server: TestClient):
    token = StorageMock.admin_token
    task_uuid = "SomeTaskThatDoesNotExists"

    response = api_server.get(
        f"/snippets/{task_uuid}", headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 404 and "code_snippet" not in response.json()

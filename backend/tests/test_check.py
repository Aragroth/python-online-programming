import json

import pytest
from fastapi.testclient import TestClient

from api import app
from tests.storage_mock import StorageMock


@pytest.fixture
async def api_server():
    return TestClient(app)


def test_check_right_sample(api_server: TestClient):
    token = StorageMock.admin_token
    task_uuid = StorageMock.task_uuid

    response = api_server.post(
        f"/check/test/{task_uuid}/sample", headers={"Authorization": f"Bearer {token}"},
        data=json.dumps({"code": StorageMock.right_code})
    )

    assert (
            response.status_code == 200 and
            response.json() == {
                "results": [
                    {
                        "output": "hello world\n",
                        "exit_code": 0,
                        "correct": True
                    },
                    {
                        "output": "Всем привет!\n",
                        "exit_code": 0,
                        "correct": True
                    }
                ],
                "total_tests": 2,
                "right_tests": 2
            }
    )


def test_check_half_right_sample(api_server: TestClient):
    token = StorageMock.admin_token
    task_uuid = StorageMock.task_uuid

    response = api_server.post(
        f"/check/test/{task_uuid}/all", headers={"Authorization": f"Bearer {token}"},
        data=json.dumps({"code": StorageMock.half_right_code})
    )
    print(response.json())
    assert (
            response.status_code == 200 and
            response.json() == {
                "total_tests": 3,
                "right_tests": 1
            }
    )

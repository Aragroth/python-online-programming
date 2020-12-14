import pytest
from fastapi.testclient import TestClient

from api import app
from tests.storage_mock import StorageMock
from tests.utils import auth_headers


@pytest.fixture
async def api_server():
    return TestClient(app)


def test_login_user_valid(api_server: TestClient):
    username, password = StorageMock.admin_username, StorageMock.admin_password
    response = api_server.post(
        "/login", headers=auth_headers,
        data=f"grant_type=password&username={username}&password={password}"
    )
    assert response.status_code == 200 and response.json()["access_token"] == "32e7325cb3a447e1825951cea4fda017"


def test_login_user_username_invalid(api_server: TestClient):
    username, password = "SomeStrangeUsername", StorageMock.admin_password
    response = api_server.post(
        "/login", headers=auth_headers,
        data=f"grant_type=password&username={username}&password={password}"
    )
    assert response.status_code != 200 and "token" not in response.json()


def test_login_user_password_invalid(api_server: TestClient):
    username, password = StorageMock.admin_username, "SomeStrangePassword"
    response = api_server.post(
        "/login", headers=auth_headers,
        data=f"grant_type=password&username={username}&password={password}"
    )
    assert response.status_code != 200 and "token" not in response.json()


def test_login_user_all_invalid(api_server: TestClient):
    username, password = "SomeStrangeUsername", "SomeStrangePassword"
    response = api_server.post(
        "/login", headers=auth_headers,
        data=f"grant_type=password&username={username}&password={password}"
    )
    assert response.status_code != 200 and "token" not in response.json()


def test_logout_user_valid_token(api_server: TestClient):
    token = StorageMock.admin_token
    response = api_server.get(
        "/logout", headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200 and response.json()["response"] == "ok"


def test_logout_user_invalid_token(api_server: TestClient):
    token = "SomeNoExistingToken"
    response = api_server.get(
        "/logout", headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 401 and "detail" in response.json()

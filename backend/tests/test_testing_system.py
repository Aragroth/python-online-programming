import os

import pytest

from testing_system.testing import RunnerTests
from tests.storage_mock import StorageMock


def create_runner(code):
    return RunnerTests(StorageMock.admin_username, code, StorageMock.task_uuid)


def test_folders_create_first_time():
    runner = create_runner(StorageMock.right_code)
    process_directory = runner.process_directory
    user_directory = (os.path.join(runner.RESULTS_FOLDER, StorageMock.admin_username))

    assert os.path.exists(user_directory)
    assert os.path.exists(process_directory)
    assert os.path.exists(os.path.join(process_directory, 'examples'))
    assert os.path.exists(os.path.join(process_directory, 'secrets'))


def test_save_code_to_file():
    runner = create_runner(StorageMock.right_code)
    runner.save_code()

    filepath = os.path.join(runner.process_directory, "main.py")
    with open(filepath) as f:
        data = ''.join(f.readlines())

    assert data == StorageMock.right_code


@pytest.mark.asyncio
async def test_check_sample_total_right():
    runner = create_runner(StorageMock.right_code)
    await runner.check_sample()

    assert runner.count_score_validate() == (2, 2)


@pytest.mark.asyncio
async def test_check_sample_half_right():
    runner = create_runner(StorageMock.half_right_code)
    await runner.check_sample()

    assert runner.count_score_validate() == (2, 1)


@pytest.mark.asyncio
async def test_check_secret_total_right():
    runner = create_runner(StorageMock.right_code)
    await runner.check_secret()

#     token = StorageMock.admin_token
#     task_uuid = StorageMock.task_uuid

#     response = api_server.get(
#         f"/snippets/{task_uuid}", headers={"Authorization": f"Bearer {token}"},
#     )
#     assert (
#         response.status_code == 200 and
#         response.json() == {"code_snippet": StorageMock.code_snippet}
#     )


# class TestRunner:
#     RESULTS_FOLDER = 'data'

#     def __init__(self, username, code, test_uuid, image_name='testing'):

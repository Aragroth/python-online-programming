from crud.abstract_db import AbstractDB
from schemas.models import User
from tests.utils import tasks_public_description


class StorageMock(AbstractDB):
    user_id = "1f279b0e-4035-4603-b933-552199846d2b"
    admin_username = "admin"
    admin_password = "12345"
    admin_token = "32e7325cb3a447e1825951cea4fda017"

    task_uuid = "81292eb1-1f24-4723-8f2f-feef58537f42"
    code_snippet = "a = 5\nprint('1')"

    right_code = "print(input())"
    half_right_code = "print('hello world')"
    wrong_code = "print(1)"

    async def get_user(self, username) -> User:
        if username != self.admin_username:
            return None

        return User(
            user_id=self.user_id,
            username=self.admin_username,
            hashed_password=self.hash_password(self.admin_password)
        )

    async def create_session(self, username):
        if username == "admin":
            return self.admin_token

    async def verify_session(self, token):
        if token != self.admin_token:
            return None

        return {"username": self.admin_username}

    async def delete_user_sessions(self, user):
        if user.username != "admin":
            raise ValueError

    async def get_tasks(self):
        return tasks_public_description

    async def test_exists(self, task_uuid):
        return True if task_uuid == self.task_uuid else False

    async def get_snippet(self, username, task_uuid):
        if task_uuid != self.task_uuid or username != self.admin_username:
            raise ValueError

        return self.code_snippet

    async def save_snippet(self, username, test_id, code):
        if test_id != self.task_uuid or username != self.admin_username:
            raise ValueError

    async def log_query(self, test_uuid, process_uuid, username):
        if username != self.admin_username or test_uuid != self.task_uuid:
            raise ValueError

    async def get_example_tests(self, task_uuid):
        if task_uuid != self.task_uuid:
            raise ValueError

        return [
            {'input': 'hello world', 'output': 'hello world\n', 'is_answer_empty': False},
            {'input': 'Всем привет!', 'output': 'Всем привет!\n', 'is_answer_empty': False}
        ]

    async def get_secret_tests(self, task_uuid):
        if task_uuid != self.task_uuid:
            raise ValueError

        return [
            {'input': 'спрятано', 'output': 'спрятано\n', 'is_answer_empty': False}
        ]

    async def total_running_containers(self):
        return 0

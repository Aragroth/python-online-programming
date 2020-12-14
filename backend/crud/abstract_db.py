import abc
import hashlib
import uuid

import motor.motor_asyncio

from schemas.models import Test


class AbstractDB(abc.ABC):
    def __init__(self, url=None):
        client = motor.motor_asyncio.AsyncIOMotorClient(url)
        self.client = client

        self.db_users = client.users
        self.db_tests = client.TestSystem

    def files_conn(self):
        pass

    async def create_task(self, task: Test):
        pass

    async def get_example_tests(self, task_uuid):
        pass

    async def get_secret_tests(self, task_uuid):
        pass

    async def get_user(self, username):
        pass

    async def test_exists(self, test_uuid):
        pass

    async def create_session(self, username):
        pass

    async def delete_user_sessions(self, session):
        pass

    async def verify_session(self, token):
        pass

    async def get_tasks(self):
        pass

    async def add_to_completed(self, username, task_uuid):
        pass

    async def get_test_description(self, task_uuid):
        pass

    async def get_quiz(self, task_uuid):
        pass

    async def get_quiz_answers(self, task_uuid):
        pass

    async def already_passed(self, username, task_uuid):
        pass

    async def log_query(self, test_uuid, process_uuid, username):
        pass

    async def tests_finished(self, username, process_uuid):
        pass

    async def delete_logs(self, username):
        await self.db_tests.queries.delete_many({"username": username})

    async def user_running_containers(self, username):
        pass

    async def total_running_containers(self):
        pass

    async def save_snippet(self, username, test_id, code):
        pass

    async def get_snippet(self, username, test_id):
        pass

    @staticmethod
    def create_token():
        return uuid.uuid4().hex

    @staticmethod
    def hash_password(password: str):
        hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()
        return hashed_password

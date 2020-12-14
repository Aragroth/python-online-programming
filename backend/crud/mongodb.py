from datetime import datetime, timedelta

import motor.motor_asyncio
from loguru import logger

from crud.utils import all_tasks_query
from schemas.models import Test
from schemas.models import User
from crud.abstract_db import AbstractDB


class MongoDB(AbstractDB):
    """
    Реализация хранилища данных просредством MongoDB
    """
    def __init__(self, url=None):
        client = motor.motor_asyncio.AsyncIOMotorClient(url)
        self.client = client

        self.db_users = client.users
        self.db_tests = client.TestSystem

    def files_conn(self):
        return self.client.files

    async def create_task(self, task: Test):
        await self.db_tests.tasks.insert_one({
            "task_uuid": task.task_uuid,
            "title": task.title,
            "examples": task.sample,
            "photo": task.photo,
            "description": task.description
        })

        await self.db_tests.tasksList.insert_one({
            "task_uuid": task.task_uuid,
            "name": task.name,
            "group": task.group,
            "type": task.type
        })

    async def get_example_tests(self, task_uuid):
        logger.debug(task_uuid)

        return (await self.db_tests.tests.find_one(
            {"_id": task_uuid},
            {"examples": 1, "_id": 0}
        ))["examples"]

    async def get_secret_tests(self, task_uuid):
        return (await self.db_tests.tests.find_one(
            {"_id": task_uuid},
            {"real_tests": 1, "_id": 0}
        ))["real_tests"]

    async def get_user(self, username) -> User:
        """
        Возвращает данные пользователя по никнейму, если пользователя
        с таким никнеймом не существует, то возращается None
        """
        if not (user_dict := await self.db_users.profiles.find_one({"username": username})):
            return None

        return User(
            user_id=user_dict['_id'],
            username=user_dict['username'],
            hashed_password=user_dict['password']
        )

    async def test_exists(self, test_uuid):
        test = await self.db_tests.tests.find_one({"_id": test_uuid})
        return False if test is None else True

    async def create_session(self, username):
        token = self.create_token()
        await self.db_users.sessions.insert_one({"username": username, "token": token})

        return token

    async def delete_user_session(self, user: User):
        print(user.username)
        await self.db_users.sessions.delete_many({"username": user.username})

    async def verify_session(self, token):
        session = await self.db_users.sessions.find_one({"token": token})
        return session

    async def get_tasks(self):
        """
        Группируем данные по названию секции, внутри лежат все задания
        данные отсортированы по названиям. TODO также добавить викторины
        """
        cursor = self.db_tests.tests.aggregate(all_tasks_query)
        data = [task async for task in cursor]

        # заменяем object_id всех фотографий на строку, чтобы
        # fast_api мог отправить его обратно пользователю
        for section in range(len(data)):
            for task in range(len(data[section]['tasks'])):
                try:
                    data[section]['tasks'][task]['photo'] = str(
                        data[section]['tasks'][task]['photo'])
                except KeyError:
                    pass

        return data

    async def add_to_completed(self, username, task_uuid):
        await self.db_users.profiles.update_one(
            {"username": username},
            {
                "$push": {
                    "passed_tests": task_uuid
                }
            }
        )

    async def get_test_description(self, task_uuid):
        value = await self.db_tests.tasks.find_one(
            {"task_uuid": task_uuid},
            {"_id": 0, "description": 1, "photo": 1, "examples": 1, "title": 1}
        )
        return value

    async def get_quiz(self, task_uuid):
        value = await self.db_tests.tasks.find_one(
            {"task_uuid": task_uuid},
            {"_id": 0, "questions.correct": 0, "task_uuid": 0}
        )
        return value

    async def get_quiz_answers(self, task_uuid):
        value = await self.db_tests.tasks.find_one(
            {"task_uuid": task_uuid},
            {"_id": 0, "questions.id": 1, "questions.correct": 1}
        )
        return value["questions"]

    async def already_passed(self, username, task_uuid):
        value = await self.db_users.profiles.find_one({'username': username})
        return task_uuid in value['passed_tests'] if 'passed_tests' in value else False

    async def log_query(self, test_uuid, process_uuid, username):
        user = await self.get_user(username)

        await self.db_tests.queries.insert_one(
            {
                "_id": process_uuid,
                "task": test_uuid,
                "timestamp": datetime.now(),
                "status": "accepted",
                "username": str(user.user_id),
                "passed_all": None,
                "percent_passed": None,
                "sample_test": None,
            }
        )

    async def tests_finished(self, username, process_uuid):
        user = await self.get_user(username)

        await self.db_tests.queries.update_one(
            {"username": user.user_id, "_id": process_uuid},
            {"$set": {"status": "finished"}}
        )

    async def delete_logs(self, username):
        await self.db_tests.queries.delete_many({"username": username})

    async def user_running_containers(self, username):
        """
        Возвращает список контейнеров пользователя, которые были запущены последний 25
        секунд и не закончили выполнение. (Контейнеры старше 25 секунд считаютя забагованными)
        """
        user = await self.get_user(username)

        return await self.db_tests.queries.count_documents(
            {
                "username": user.user_id,
                "timestamp": {"$gte": datetime.now() - timedelta(seconds=25)},
                "status": {"$ne": "finished"}
            },
        )

    async def total_running_containers(self):
        """
        Возвращает список контейнеров, которые были запущены последний 25 секунд и
        не закончили выполнение. (Контейнеры старше 25 секунд считаютя забагованными)
        """
        return await self.db_tests.queries.count_documents(
            {
                "timestamp": {"$gte": datetime.now() - timedelta(seconds=25)},
                "status": {"$ne": "finished"}
            },
        )

    async def save_snippet(self, username, test_id, code):
        # TODO check if test_id exists

        await self.db_users.profiles.update_one(
            {"username": username},
            {"$pull": {"snippets": {"test_id": test_id}}}
        )
        await self.db_users.profiles.update_one(
            {"username": username},
            {
                "$push": {"snippets": {
                    "test_id": test_id,
                    "code": code.code
                }}
            }
        )

    async def get_snippet(self, username, test_id):
        cursor = self.db_users.profiles.aggregate([
            {
                "$match": {
                    "username": username,
                }
            },
            {
                "$project": {
                    "snippet": {
                        "$filter": {
                            "input": "$snippets",
                            "as": "snippets",
                            "cond": {
                                "$eq": [
                                    "$$snippets.test_id",
                                    test_id
                                ]
                            }
                        }
                    },
                    "_id": 0
                }
            }
        ])
        snippet = [task async for task in cursor][0]["snippet"]
        if snippet:
            return snippet[0]['code']
        return ""

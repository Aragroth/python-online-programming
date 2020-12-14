from schemas.models import Test
from schemas.models import User
from crud.utils import cache_timeout


# TODO по мимо кэширующих декораторов, добавить декораторы ошибок доступа к базе данных
class Database:
    def __init__(self, storage_model):
        self.storage = storage_model

    def files_conn(self):
        # TODO сделать из этого отдельный метод, который по айди файла возвращает,
        # тем самым скрывая то, как хранилище сохраняет файлики
        return self.storage.files_conn()

    async def create_task(self, task: Test):
        await self.storage.create_task(task)

    async def get_example_tests(self, task_uuid):
        """Получить описание теста по его айди"""
        return await self.storage.get_example_tests(task_uuid)

    async def get_secret_tests(self, task_uuid):
        return await self.storage.get_secret_tests(task_uuid)

    async def get_by_username(self, username: str) -> User:
        """Возвращает пользователя по его никнейму"""
        return await self.storage.get_user(username)

    async def test_exists(self, test_uuid):
        """Проверяет, существует ли тест с заданными айди"""
        return await self.storage.test_exists(test_uuid)

    async def login_user(self, username):
        """Создаёт сессию пользователя в тестриующей системе"""
        return await self.storage.create_session(username)

    async def logout_user(self, user: User):
        """Удаляет сессию пользователя из системы"""
        await self.storage.delete_user_sessions(user)

    async def get_by_token(self, token) -> User:
        """Возвращает пользователя по его токену, иначе None"""
        session = (await self.storage.verify_session(token))
        if session is None:
            return

        return await self.storage.get_user(session['username'])

    @cache_timeout(timeout=15)
    async def get_tasks(self):
        """
        Группируем данные по названию секции, внутри лежат все задания
        данные отсортированы по названиям. TODO также добавить викторины
        """
        return await self.storage.get_tasks()

    async def add_to_completed(self, username, task_uuid):
        """Добавить тест в список пройденных пользователем"""
        await self.storage.add_to_completed(username, task_uuid)

    async def get_test_description(self, task_uuid):
        """Возвращает описание конкретного задания с кодом"""
        return await self.storage.get_test_description(task_uuid)

    async def get_quiz(self, task_uuid):
        # TODO разобраться, что делает этот метод
        await self.storage.get_quiz(task_uuid)

    async def get_quiz_answers(self, task_uuid):
        # TODO проверить работу этого метода на новой схеме базе данных
        return await self.get_quiz_answers(task_uuid)

    async def already_passed(self, username, task_uuid):
        """Проверяет, не прошёл ли пользователь уже это задание"""
        return await self.storage.already_passed(username, task_uuid)

    async def log_query(self, test_uuid, process_uuid, username):
        """Логирует вызов тестов для теста от какого-то пользователя"""
        await self.storage.log_query(test_uuid, process_uuid, username)

    async def tests_finished(self, username, process_uuid):
        """Помечает запуск тест в системе логирования, как пройдённый"""
        await self.storage.tests_finished(username, process_uuid)

    async def delete_logs(self, username):
        """Удаляет все логи пользователя из системы тестирования"""
        await self.storage.delete_logs(username)

    async def has_user_running_containers(self, username):
        """Проверяет, есть ли у пользователя уже запущенные контейнеры тестов"""
        return await self.storage.user_running_containers(username)

    async def total_running_containers(self):
        """Возвращает общее количество запущенных в системе контейнеров"""
        return await self.storage.total_running_containers()

    async def save_snippet(self, username, test_id, code):
        """Сохраняет сниппет с кодом"""
        # TODO проверять, что test_id существует
        await self.storage.save_snippet(username, test_id, code)

    async def get_snippet(self, username, test_id):
        """Получить сниппеты кода"""
        return await self.storage.get_snippet(username, test_id)

"""Используется для тестирования программ пользователя"""
import asyncio
import os
import subprocess
import time
import uuid
from asyncio.subprocess import DEVNULL, PIPE
from typing import List

from core.config import database
from schemas.models import TestResult


# pylint: disable=R0902
class RunnerTests:
    """
    Сохраняет переданный код, выполняет необходимые тесты, запуская программы в докер
    контёйнерах (по заранее собранному образу). Далее считывает результаты из файлов и выводит
    количество пройдённых тестов (и если надо, то данные которые были выведены программой)
    """
    RESULTS_FOLDER = 'data'

    def __init__(self, username, code, test_uuid, image_name='testing'):
        self.username = username
        self.process_uuid = self.create_uuid()
        self.test_uuid = test_uuid
        self.image_name = image_name
        self.code = code

        self.process_uuid = self.create_uuid()
        self.process_directory = self.create_task_folders(
            username=self.username,
            process_uuid=self.process_uuid
        )
        self.main_file = self.save_code()

        self.results: List[TestResult] = []

    def save_code(self):
        """Сохраняет исходный код программы в файл main процесса"""
        filepath = os.path.join(self.process_directory, "main.py")
        with open(filepath, 'w') as file:
            file.writelines(self.code)

        return filepath

    def count_score_validate(self):
        """Подсчитывает количество пройденных тестов"""
        total_tests = right_tests = 0
        for elem in self.results:
            if elem.output == elem.right:
                elem.correct = True
                right_tests += 1
            else:
                elem.correct = False
            if len(elem.output) > 300:
                elem.output = elem.output[:300] + "\n<output was truncated>"
            total_tests += 1

        return total_tests, right_tests

    def create_task_folders(self, username, process_uuid):
        """Создаёт именную папку пользователя для загрузки его main.py файлов"""

        user_directory = os.path.join(self.RESULTS_FOLDER, username)
        if not os.path.exists(user_directory):
            os.makedirs(user_directory)

        process_directory = os.path.join(user_directory, process_uuid)
        if not os.path.exists(process_directory):
            os.makedirs(process_directory)

        os.makedirs(os.path.join(process_directory, 'examples'))
        os.makedirs(os.path.join(process_directory, 'secrets'))

        return process_directory

    async def check_secret(self):
        """Проверяет код на 'скрытых' от пользователя тестах"""
        # TODO delete duplication with check_sample
        # no need to log query, because before secret tests run samples tests and queries it
        secrets = await database.get_secret_tests(self.test_uuid)
        coroutines = []

        right_answers = []
        for num, test in enumerate(secrets):
            input_file = self.create_input_file("secrets", num, test['input'])
            output_file = self.create_output_file("secrets", num)

            right_answers.append(test['output'])
            coroutines.append(self.run_test(input_file, output_file))

        data = await asyncio.gather(*coroutines)
        for num, data in enumerate(data):
            test_exit_code = data
            test_output = self.read_output_file("secrets", num)
            self.results.append(
                TestResult(
                    exit_code=test_exit_code,
                    output=''.join(test_output),
                    right=right_answers[num]
                )
            )

    async def check_sample(self):
        """Проверяет код на 'открытых' тестах, указанных в описании в заданию"""
        await database.log_query(self.test_uuid, self.process_uuid, self.username)

        examples = await database.get_example_tests(self.test_uuid)
        coroutines = []

        right_answers = []
        for num, test in enumerate(examples):
            input_file = self.create_input_file("examples", num, test['input'])
            output_file = self.create_output_file("examples", num)

            right_answers.append(test['output'])
            coroutines.append(self.run_test(input_file, output_file))

        data = await asyncio.gather(*coroutines)
        for num, data in enumerate(data):
            test_exit_code = data
            test_output = self.read_output_file("examples", num)
            self.results.append(
                TestResult(
                    exit_code=test_exit_code,
                    output=''.join(test_output),
                    right=right_answers[num]
                )
            )

    async def finished_tests(self):
        """Обновляет состояние тестов в базе данных, когда они были все выполнены"""
        await database.tests_finished(self.username, self.process_uuid)

    def read_output_file(self, folder, num):
        """Считывает данные из файла, который прошёл тесты"""
        file_folder = os.path.join(self.process_directory, folder)
        filepath = os.path.join(file_folder, str(num) + '.out')
        with open(filepath) as file:
            return file.readlines()

    def create_input_file(self, folder, num, data):
        """Создаёт файл с текстом вывода выполненного задания"""
        file_folder = os.path.join(self.process_directory, folder)
        filepath = os.path.join(file_folder, str(num) + '.in')
        with open(filepath, 'w') as file:
            file.writelines(data)

        return filepath

    def create_output_file(self, folder, num):
        """ФакТически не создаёт файл для вывода, просто даёт путь для него"""
        file_folder = os.path.join(self.process_directory, folder)
        return os.path.join(file_folder, str(num) + '.out')

    @staticmethod
    async def execute_command(command_body, stdout):
        """Шорткат для асинхронного выполнения какой-то команды в консоли"""
        return await asyncio.create_subprocess_shell(command_body, stdout=stdout)

    async def run_test(self, input_file, output_file):
        """Выполняет переданный файлик пользователя и сохраняет выходные данные"""
        container_uuid = self.create_uuid()

        proc = await self.execute_command(
            f"docker create --network none --name {container_uuid} -m 100m {self.image_name}",
            DEVNULL
        )
        await proc.wait()

        proc = await self.execute_command(
            f"docker cp ./{self.main_file} {container_uuid}:/testing/main.py", DEVNULL)
        await proc.wait()

        proc = await self.execute_command(
            f"docker cp ./{input_file} {container_uuid}:/testing/input", DEVNULL)
        await proc.wait()

        proc = await self.execute_command(
            f"docker start {container_uuid}", DEVNULL)
        await proc.wait()

        start = time.time()

        while await self.is_running(container_uuid) and time.time() - start < 2:
            await asyncio.sleep(0.2)

        proc = await self.execute_command(
            f"docker cp {container_uuid}:/testing/stdout ./{output_file}", DEVNULL)
        await proc.wait()

        proc = await self.execute_command(
            f"docker inspect {container_uuid} --format={{{{.State.ExitCode}}}}", PIPE)
        exit_code = await proc.stdout.read()

        # делаем это в отдельном потоке, чтобы не заставлять пользовотеля ждать
        subprocess.Popen(
            f"docker stop {container_uuid}; docker rm {container_uuid}",
            shell=True,
            stdout=subprocess.DEVNULL
        )

        return int(exit_code.decode("utf-8").strip())

    @staticmethod
    async def is_running(container_name):
        """Проверят, работает ли всё ещё контейнер с тестами"""
        proc = await asyncio.create_subprocess_shell(
            f"docker inspect {container_name} --format={{{{.State.Running}}}}",
            stdout=asyncio.subprocess.PIPE)
        value = await proc.stdout.read()

        return value.decode("utf-8").strip() == "true"

    @staticmethod
    def create_uuid():
        """Создаёт уникальные идентификаторы для процессов"""
        return uuid.uuid4().hex

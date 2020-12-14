"""
Проверяет все виды заданий (с автотестами/викторины), которые есть в системе
"""
from typing import Dict

from fastapi import APIRouter, Depends, BackgroundTasks

from endpoints.utils import validate_quiz, can_perform_request, finished_tests
from core.config import database, settings
from core.security import get_user_by_token
from schemas.models import CodeSnippet, Quiz, User
from testing_system.testing import RunnerTests

router = APIRouter()


@router.post("/test/{test_uuid}/sample", dependencies=[Depends(can_perform_request)])
async def check_sample_test(test_uuid: str, code: CodeSnippet, background_tasks: BackgroundTasks,
                            user: User = Depends(get_user_by_token)):
    """
    Проверяет присланный код только на 'открытых' тестах, которые расположены в описание задания.
    Возвращает вызодные коды, правильность выведенного результата, а также сам выведенный результат
    """
    await database.save_snippet(user.username, test_uuid, code)

    runner = RunnerTests(user.username, code.code, test_uuid)
    background_tasks.add_task(finished_tests, runner)

    await runner.check_sample()
    total_tests, right_tests = runner.count_score_validate()

    return {
        "results": [
            {
                "output": data.output,
                "exit_code": data.exit_code,
                "correct": data.correct
            } for data in runner.results
        ],
        "total_tests": total_tests,
        "right_tests": right_tests
    }


@router.post("/test/{test_uuid}/all", dependencies=[Depends(can_perform_request)])
async def check_all_tests(test_uuid: str, code: CodeSnippet, background_tasks: BackgroundTasks,
                          user: User = Depends(get_user_by_token)):
    """
    Проверяет присланный код и на 'открытых' тестах, которые расположены в описание задания, и на
    'скрытых' тестах, которые не доступны для просмотра. Возвращает только общее количество тестов
    и количество пройденных
    """
    await database.save_snippet(user.username, test_uuid, code)

    runner = RunnerTests(user.username, code.code, test_uuid)
    background_tasks.add_task(finished_tests, runner)
    await runner.check_sample()
    await runner.check_secret()

    total_tests, right_tests = runner.count_score_validate()

    if total_tests == right_tests:
        await database.add_to_completed(user.username, test_uuid)

    data = runner.results[0]
    if len(data.output) > 300:
        data.output = data.output[:300] + "\n<output was truncated>"

    return {
        "total_tests": total_tests,
        "right_tests": right_tests
    }


# pylint: disable=W0511
if not settings.QUIZZES_DISABLED:  # pragma: no cover
    @router.post("/quiz/{task_uuid}")
    async def check_quiz(task_uuid, quiz: Quiz, session: Dict = Depends(get_user_by_token)):
        """Проверяет правильность выполнения викторины"""
        # TODO check if type of test_id is quiz, not sample.text
        # TODO mongo.log_query(test_id, process_uuid, username)
        # TODO check if allowed to repeat
        # TODO update percents

        if await validate_quiz(quiz, task_uuid):
            await database.add_to_completed(session['username'], task_uuid)
            return {"response": "correct"}

        return {"response": "incorrect"}

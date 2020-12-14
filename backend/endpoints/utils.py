"""
Вспомогательные функции для API сервера
"""
from fastapi import Depends, HTTPException, status

from core.config import database, settings
from core.security import get_user_by_token
from schemas.models import User

QUIZZES_DISABLED = True


async def test_exists(test_uuid: str):
    """Проверяет, существет ли задание с заданным айди"""
    if not await database.test_exists(test_uuid):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No such test exists",
        )


async def finished_tests(runner):
    """Проверяет, завершил ли 'исполнитель' тестов выполнени"""
    await runner.finished_tests()


async def validate_quiz(answers, task_uuid):
    """Проверяет, опросник"""
    real_answers = await database.get_quiz_answers(task_uuid)
    return real_answers == answers.answers


async def can_perform_request(test_uuid: str, user: User = Depends(get_user_by_token)):
    """
    Проверяет, существует ли тест, прошёл ли пользователь его уже, выполняются ли у
    пользователя тесты других заданий, а также не превышает ли количество проверяемых заданий
    максимально возможное количество (меняется через файл настроек)
    """
    if not await database.test_exists(test_uuid):
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="Такого задания не существует",
        )

    if await database.already_passed(user.username, test_uuid):
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="Вы уже выполнили данное задание на 100%",
        )

    if await database.has_user_running_containers(user.username):
        raise HTTPException(
            status_code=status.HTTP_202_ACCEPTED,
            detail="Какой-то из ваших тестов уже выполняется",
        )

    if await database.total_running_containers() >= settings.MAX_TESTS_AT_SAME_TIME:
        raise HTTPException(
            status_code=status.HTTP_202_ACCEPTED,
            detail="Просим подождать, система переполнена запросами",
        )

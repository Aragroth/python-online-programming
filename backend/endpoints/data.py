"""
Возвращает содержание заданий и опросников
"""
from fastapi import APIRouter, Depends

from core.config import database, settings
from core.security import get_user_by_token
from schemas.models import SimpleResponse

router = APIRouter()


@router.get("/tasks", dependencies=[Depends(get_user_by_token)], response_model=SimpleResponse)
async def get_tasks_tree():
    """Возвращает дерево всех заданий в системе"""
    return {"response": await database.get_tasks()}


# pylint: disable=W0511
if not settings.QUIZZES_DISABLED:  # pragma: no cover

    @router.get("/quizzes/{task_uuid}", dependencies=[Depends(get_user_by_token)],
                response_model=SimpleResponse)
    async def get_quiz(task_uuid):
        """Возвращает список вопросов/ответов для опросника"""
        # TODO check if type of test_id is quiz, not sample.test
        return {"response": await database.get_quiz(task_uuid)}

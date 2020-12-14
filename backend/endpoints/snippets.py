"""
Обрабатывает код, который пользователь вводит в бразузерном редакторе кода
"""
from fastapi import APIRouter, Depends

from core.config import database
from core.security import get_user_by_token
from endpoints.utils import test_exists
from schemas.models import CodeSnippet, User

router = APIRouter()


@router.get("/{test_uuid}", dependencies=[Depends(test_exists)])
async def get_snippet(test_uuid: str, user=Depends(get_user_by_token)):
    """Возвращает последний сохранённый код пользователя в каком-то задании"""
    snippet = await database.get_snippet(user.username, test_uuid)
    return {"code_snippet": snippet}


@router.post("/{test_uuid}", dependencies=[Depends(test_exists)])
async def save_snippet(test_uuid: str, code: CodeSnippet, user: User = Depends(get_user_by_token)):
    """Сохранет код пользователя по айди задания. Есть лимит на размер сохраняемого кода"""
    await database.save_snippet(user.username, test_uuid, code)
    return {"response": "ok"}

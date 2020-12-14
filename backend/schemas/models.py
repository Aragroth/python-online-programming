"""
Содержит PyDantic модели, необходимые для FastAPI и вообще для
соблюдения контрактов между частами и классами системы
"""

from typing import Dict, List, Any
from uuid import UUID

from pydantic import BaseModel, constr


class Quiz(BaseModel):
    """Часть задания с вопросами"""
    answers: List[Dict[str, int]]


class CodeSnippet(BaseModel):
    """Хранит пользовательский, одновременно валидируя его на максимальную длину"""
    code: constr(max_length=5000)


class Item(BaseModel):
    """Хранит что-то... костыльное"""
    code: str


class Test(BaseModel):
    """Хранит информацию об одном задании, возвращаемом пользователю"""
    task_uuid: UUID = None
    name: str = None
    group: str = None
    type: str = None

    title: str = None
    description: str = None
    photo: str = None
    sample: List[Dict] = []


class TestResult(BaseModel):
    """Хранит результат проверки кода автотестами"""
    exit_code: int
    output: str
    right: str
    correct: bool = None


class User(BaseModel):
    """Данные о пользователе"""
    user_id: UUID
    username: str
    hashed_password: str


class SingleResultMetadata(BaseModel):
    """Хранит данные о выполненных секретных тестах в FastAPI"""
    output: str
    exit_code: int
    correct: int


class SampleTestResults(BaseModel):
    """Хранит данные о выполненных открытых тестах в FastAPI"""
    results: List[SingleResultMetadata]
    total_tests: int
    right_tests: int


class SimpleResponse(BaseModel):
    """Возвращает что-то. Нужен для создания автодокументации"""
    response: Any

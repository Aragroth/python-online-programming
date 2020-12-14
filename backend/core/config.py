"""
Содержит объект настроек и объект базы данных (которая заменяется mock-версией,
если в настроках проекта был указан параметр DEBUG=1)
"""

import os
import re
from typing import List, Dict

from pydantic import AnyHttpUrl, BaseSettings, validator

from crud.database import Database
from crud.mongodb import MongoDB


# pylint: disable=C0103,E0213,R0903,R0201
class Settings(BaseSettings):
    """
    Хранит основные настройки конфигурации проекта. Считываются из файла .env, но могут быть
    перезаписаны, если переопределить их переменных среды из которой идёт запуск.
    """
    IS_ADMIN_PANEL: bool = False
    BASE_DOMAIN: str = "testing.example.com"
    API_PREFIX: str = "/api"
    ADMIN_PANEL_PREFIX: str = "/admin"

    MAX_TESTS_AT_SAME_TIME: int = 15
    SECRET_KEY = '<add key here in format>'

    QUIZZES_DISABLED: bool = True
    DEBUG: bool = False

    # Передать массив url через запятую для cors origin
    DEVELOPMENT_CORS_ORIGINS: List[AnyHttpUrl] = []
    MONGODB_DATABASE_URI: str
    MONGODB_ADMIN: List[Dict] = None

    @validator("MONGODB_DATABASE_URI", pre=True, allow_reuse=True)
    def validate_mongo_uri(cls, v: str) -> str:
        """При считывании ссылки на MongoDB проверяет, передана ли она в формате mongodb URI"""
        if v.startswith("mongodb://"):
            return v
        raise ValueError("Invalid format")

    class Config:
        """
        Делаем настройки чувствительными к регистру букв,
        указываем дефолтный файл считывания настроек в utf-8
        """
        case_sensitive = True
        env_file = 'core/.env'
        env_file_encoding = 'utf-8'


settings = Settings()
settings.MONGODB_ADMIN = [
    {
        "ALIAS": db_name,
        "username": re.findall(r'://(.+?):', settings.MONGODB_DATABASE_URI)[0],
        "authentication_source": "admin",
        'host': "mongo",
        "password": re.findall(r'/\w+?:(.+?)@', settings.MONGODB_DATABASE_URI)[0],
        'port': 27017,
        'db': db_name,
        'connect': True,
    } for db_name in ['users', 'TestSystem', 'files']
]

# Создаёт образ для тестирующего кода при запуске контейнера, если запускаем не админ панель
if not settings.IS_ADMIN_PANEL:
    os.system("docker build -t testing - < testing_system/Dockerfile.testing")

# Если в параметрах виртуального окружения было установлено DEBUG = true, то
# вместо реальной базы данных будет использоваться mock-версия, основанная на словарях
if settings.DEBUG:
    from tests.storage_mock import StorageMock

    storage = StorageMock()
    print("Using mocks")
else:
    print(settings.MONGODB_DATABASE_URI)
    storage = MongoDB(settings.MONGODB_DATABASE_URI)

database = Database(storage)

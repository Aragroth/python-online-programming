"""Основные функции используемые для валидации пользователей и хэширования паролей"""
import hashlib

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from loguru import logger

from core.config import database

logger.add("log/password.log")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


async def get_user_by_token(token: str = Depends(oauth2_scheme)):
    """
    Возвращает пользователя, если такой токен существует,
    иначе возникает ошибка авторизации
    """
    if not (user := await database.get_by_token(token)):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No such session exist",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


def hash_password(password: str):
    """Хэширует переданный пароль"""
    hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()
    return hashed_password


def check_password(real_hashed_password, password):
    """Проверяет, совпадает ли прееданный пароль с хэшированной версией"""
    hashed_password = hash_password(password)
    return real_hashed_password == hashed_password
